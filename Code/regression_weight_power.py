import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. The Extracted Data (3090 Propeller)
thrust_kg = np.array([1.3, 1.9, 2.7, 3.7, 4.7, 5.9, 7.2, 8.8, 10.5, 12.2, 14.1, 16.1, 18.4])
power_watts = np.array([95, 162, 260, 394, 576, 811, 1107, 1474, 1917, 2447, 3071, 3800, 4641])

# 2. Model 1: 2nd-Degree Polynomial (ESP32 Flight Code)
# P = a*W^2 + b*W + c
poly_coeffs = np.polyfit(thrust_kg, power_watts, 2)
poly_func = np.poly1d(poly_coeffs)
power_pred_poly = poly_func(thrust_kg)

# 3. Model 2: Theoretical Physics (Actuator Disk Theory)
# P = k * W^1.5
def physics_model(w, k):
    return k * np.power(w, 1.5)

popt, _ = curve_fit(physics_model, thrust_kg, power_watts)
k_coeff = popt[0]
power_pred_physics = physics_model(thrust_kg, k_coeff)

# 4. Accuracy Measurement Function (R² and RMSE)
def calc_accuracy(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    r_squared = 1 - (ss_res / ss_tot)
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    return r_squared, rmse

r2_poly, rmse_poly = calc_accuracy(power_watts, power_pred_poly)
r2_phys, rmse_phys = calc_accuracy(power_watts, power_pred_physics)

# 5. Console Output (The Coefficients and Accuracy)
print("--- MODEL 1: 2ND-DEGREE POLYNOMIAL (ESP32) ---")
print(f"Equation: P = {poly_coeffs[0]:.4f}W² + {poly_coeffs[1]:.4f}W + {poly_coeffs[2]:.4f}")
print(f"R-Squared:  {r2_poly:.6f}")
print(f"RMSE:       {rmse_poly:.2f} Watts\n")

print("--- MODEL 2: THEORETICAL PHYSICS (W^1.5) ---")
print(f"Equation: P = {k_coeff:.4f} * W^1.5")
print(f"R-Squared:  {r2_phys:.6f}")
print(f"RMSE:       {rmse_phys:.2f} Watts\n")

# 6. Plotting the Curves
x_smooth = np.linspace(min(thrust_kg), max(thrust_kg), 100)

plt.figure(figsize=(10, 6))
plt.scatter(thrust_kg, power_watts, color='black', label='Thrust Rig Test Data', zorder=5)

plt.plot(x_smooth, poly_func(x_smooth), color='red', linestyle='-', linewidth=2, 
         label='Polynomial Fit (2nd Degree)')
plt.plot(x_smooth, physics_model(x_smooth, k_coeff), color='blue', linestyle='--', linewidth=2, 
         label='Physics Fit (W^1.5)')

plt.title('Propeller Thrust vs. Power Draw')
plt.xlabel('Thrust (kg)')
plt.ylabel('Power (Watts)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()