import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymavlink import mavutil
from pathlib import Path

# pymavlink data pipeline establishment

bin_folder = Path(r"C:\Users\GA\Desktop\New folder")



# feeding inputs from the test files into the parameters here

altitude_m = 
current_motor = 



# Constants and coefficients related to power loss
R_copper = 0.10025 # ohms
k_h = 0.000305 # hysteresis loss coefficient
k_e = 1e-6        # eddy current loss coefficient
k_b = 5.852344e-02 # Bearing friction losses
prop_coeff = 7.185656e-01 # propeller efficiency coefficient
radius = 0.3048 # m
A_lost = 0.0081 # m^2, thrust blockage and effective area removed for each motor
prop_wash_area = np.pi * radius**2 - A_lost

current = 10 # A, at 50% throttle
radpersec = RPM * 2 * np.pi / 60 # rad/s        

R = 287.058 # Specific Gas constant
L  = 0.0065 # temperature lapse rate
g = 9.81 # m/s^2
# Wind load calculation parameters
rho_0 = 1.1551 # kg/m^3
exponent = (g/(R*L) - 1 )
T_0 = 303.15 # K
rho = rho_0 * ((1 - (L * altitude_m) / T_0) ** exponent) # kg/m^3



# Power loss calculations
P_motor_loss = R_copper * current**2 + k_h * RPM + k_e * RPM**2 + k_b * radpersec

# Power consumed 
P_total = 460 # watts at 50% throttle

T_total = ((P_total - P_motor_loss) * prop_coeff * np.  sqrt(2*rho*prop_wash_area)) ** (2/3)
Weight = T_total / 9.81

print(Weight)



