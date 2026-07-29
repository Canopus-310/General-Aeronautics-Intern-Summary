import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
RPM = 3184 # RPM at 50% throttle
radpersec = RPM * 2 * np.pi / 60 # rad/s


# Wind load calculation parameters
C_d = 1.26 # updated based on calculations of drag area and dividing by total area.
rho = 1.225 # kg/m^3
A_front = 0.096 # m^2
A_side = 0.145 # m^2
horizontal_wind_angle = 0 # degrees
A_projected = A_front * np.cos(np.radians(horizontal_wind_angle)) + A_side * np.sin(np.radians(horizontal_wind_angle))
v_wind = 10 # m/s, just an example value, can be replaced with actual wind speed data


# Power loss calculations
P_motor_loss = R_copper * current**2 + k_h * RPM + k_e * RPM**2 + k_b * radpersec
D_wind = 0.5 * rho * A_projected * v_wind**2 * C_d
P_wind = (D_wind ** 1.5) / np.sqrt(2 * rho * prop_wash_area)

# Power consumed 
P_total = 460 # watts at 50% throttle

T_total = ((P_total - P_motor_loss) * prop_coeff * np.  sqrt(2*rho*prop_wash_area)) ** (2/3)
Weight = np.sqrt(T_total**2 - D_wind**2) / 9.81

print(Weight)
print(P_wind)
