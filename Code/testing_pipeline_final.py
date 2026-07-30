import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymavlink import mavutil
from pathlib import Path

# establish pipeline for the files in the 

testing_folder = Path(r"C:\Users\GA\Desktop\Test_folder")
output_folder = testing_folder / "aligned_csv"

if output_folder.exists():
    shutil.rmtree(output_folder)
output_folder.mkdir(exist_ok=True)

TOL = 60_000  # us -- GPS needs this much slack; BAT/RCOU/CTUN are tighter but this is safe for all, this is the time window for aligning the messages of gps, ctun, bat and rcou messages for each bin file into one bin file. 60 milisecond is the current value
drone_without_payload_weight = 18.5 # kg, weight of the drone without any payload
WINDOW = '2.5s'          #
# start looping over each bin files inside the folder

for bin_file in sorted(testing_folder.glob("*.bin")):

    # start defining and establishing the mavlink connection for each bin file
    log = mavutil.mavlink_connection(str(bin_file)) # opens the bin file and prepares it for message-by-message reading

    # needed parameters for weight estimation calculations from the bin file and log all of these paramaters with their time US values in a list of dictionaries for each bin file
    


    GPS_rows = [] # contains altitude above sea level data
    CTUN_rows = [] # contains SAlt data which would be needed to find the power consumed by the drone computer at 0 height
    RCOU_rows = [] # contains C1 TO C6 MOTOR PWM values
    BAT_rows = [] # contains current and voltage values for the BATery

    while True:
        msg = log.recv_match(type=["GPS", "RCOU", "BAT", "CTUN"]) # fetches the next message that is either GPS, RCOU or BAT type — returns None when log is exhausted
        if msg is None:
            break   
        d = msg.to_dict() # converts that single message into a flat dictionary of its fields e.g. {"TimeUS": 123, "Spd": 1.2 ...}
        if msg.get_type() == "GPS":
            GPS_rows.append(d)
        elif msg.get_type() == "RCOU":
            RCOU_rows.append(d)
        elif msg.get_type() == "BAT":
            BAT_rows.append(d)
        elif msg.get_type() == "CTUN":
            CTUN_rows.append(d)

    if not (GPS_rows and CTUN_rows and RCOU_rows and BAT_rows):
        print(f"Skipping {bin_file.stem}: missing a message type")
        continue

    gps  = pd.DataFrame(GPS_rows) # feeding into pandas dataframe for easier manipulation and analysis
    ctun = pd.DataFrame(CTUN_rows) 
    rcou = pd.DataFrame(RCOU_rows)
    bat  = pd.DataFrame(BAT_rows)

    rcou['PWM_avg'] = rcou[['C1','C2','C3','C4','C5','C6']].mean(axis=1) # the median of the 6 motor PWM values is taken to get a single value for the PWM for each bin file

    gps_s  = gps[['TimeUS','Alt']].rename(columns={'Alt':'GPS_Alt'}).sort_values('TimeUS') # picking out the needed columns and renaming the Alt column to GPS_Alt for clarity and sorting by TimeUS
    bat_s  = bat[['TimeUS','Volt','Curr']].sort_values('TimeUS')      # Curr, not CurrTot
    ctun_s = ctun[['TimeUS','SAlt']].sort_values('TimeUS')
    rcou_s = rcou[['TimeUS','PWM_avg']].sort_values('TimeUS')

    merged = pd.merge_asof(ctun_s, rcou_s, on='TimeUS', direction='nearest', tolerance=TOL)
    merged = pd.merge_asof(merged, bat_s,  on='TimeUS', direction='nearest', tolerance=TOL)
    merged = pd.merge_asof(merged, gps_s,  on='TimeUS', direction='nearest', tolerance=TOL)

    merged['Power_total'] = merged['Volt'] * merged['Curr']   # total power readings

    n_before = len(merged)
    merged = merged.dropna()   # drops only the handful of edge rows at real arm-segment gaps
   #print(f"{bin_file.stem}: {n_before} rows -> {len(merged)} after dropping {n_before-len(merged)} gap-edge rows")

    out_path = output_folder / f"{bin_file.stem}_aligned.csv"
    merged.to_csv(out_path, index=False)


    # taking the median of the parameters to get a single value for each parameter for each bin file and implementing the logical algorithm for taking the values

    # subtract the current when SAlt is 0 from the current when SAlt is greater than 0 to get the current consumed by the drone computer at 0 height
    current_at_0_height = merged.loc[merged['SAlt'] < 0.05, 'Curr'].median()

    # find genuine stable hover: above ground-effect height AND steady over the trailing 2.5s
    merged['dt'] = pd.to_timedelta(merged['TimeUS'], unit='us')
    m = merged.set_index('dt').sort_index()

    m['SAlt_roll_std']   = m['SAlt'].rolling(WINDOW).std()
    # calculate 75th percentile of the rolling std to find a threshold for stable hover
    STD_THRESHOLD = m['SAlt_roll_std'].quantile(0.75)
    m['SAlt_roll_count'] = m['SAlt'].rolling(WINDOW).count()

    stable_hover = m[
        (m['SAlt'] > 1.5) &
        (m['SAlt_roll_std'] < STD_THRESHOLD) &
        (m['SAlt_roll_count'] >= 20)
    ]

    current_motor = (stable_hover['Curr'].median() - current_at_0_height) / 6.0 # subtracting the current at 0 height from the current at stable hover to get the current consumed by the motors
    altitude_above_sea_level = stable_hover['GPS_Alt'].median() # median of the GPS altitude above sea level for stable hover
    current_pwm = stable_hover['PWM_avg'].median() # median of the PWM values for stable hover
    P_total = stable_hover['Power_total'].median() / 6.0 # median of the total power consumed for stable hover per motor

    # motor and prop loss related parameters 
    R_copper = 0.10025 # ohms
    k_h = 0.000305 # hysteresis loss coefficient
    k_e = 1e-6        # eddy current loss coefficient
    k_b = 5.852344e-02 # Bearing friction losses
    prop_coeff = 7.185656e-01 # propeller efficiency coefficient

    # thrust blockage and effective area removed for each motor
    radius = 0.3048 # m
    A_lost = 0.0081 # m^2, thrust blockage and effective area removed for each motor
    prop_wash_area = np.pi * radius**2 - A_lost

    # density calculation parameters
    R = 287.058 # Specific Gas constant assuming 0% humidity
    L  = 0.0065 # temperature lapse rate
    g = 9.81 # m/s^2
    rho_0 = 1.1551 # kg/m^3
    exponent = (g/(R*L) - 1 )
    T_0 = 303.15 # K
    rho = rho_0 * ((1 - (L * altitude_above_sea_level) / T_0) ** exponent) # kg/m^3

    # RPM calculation 

    throttle_pct = np.array([40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,90,100])
    rpm_table    = np.array([2455,2605,2754,2900,3047,3184,3325,3456,3589,3716,3841,3959,4080,4194,4307,4415,4519,4627,4723,4821,4912,5142,5442])

    min_pwm = 1050 
    max_pwm = 1950
    throttle_pct_cmd = (current_pwm - min_pwm) / (max_pwm - min_pwm) * 100
    RPM = np.interp(throttle_pct_cmd, throttle_pct, rpm_table)
    radpersec = RPM * 2 * np.pi / 60 # rad/s

    # power loss calculations 
    P_motor_loss = R_copper * current_motor**2 + k_h * RPM + k_e * RPM**2 + k_b * radpersec

    if P_total - P_motor_loss <= 0:
       print(f"Skipping {bin_file.stem}: power balance went negative — check hover window")
       continue
    # Weight estimation calculations
    T_total = ((P_total - P_motor_loss) * prop_coeff * np.  sqrt(2*rho*prop_wash_area)) ** (2/3)
    Weight = T_total / 9.81
    Total_weight = Weight * 6.0 # 6 motors on drone
    Weight_Payload = Total_weight - drone_without_payload_weight # subtracting weight of the drone itself to get the payload weight

    print(f"Estimated Weight of Payload for {bin_file.stem} is: {Weight_Payload:.4f} kg")
    print(f"The estimated Motor Power loss for {bin_file.stem} is: {P_motor_loss:.4f} W")
    print(f"The estimated Total Power consumed per motor during stable hover for {bin_file.stem} is: {P_total:.4f} W")
    print()
