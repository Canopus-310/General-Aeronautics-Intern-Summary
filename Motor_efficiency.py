from scipy.optimize import curve_fit
import numpy as np 
import matplotlib.pyplot as plt



def power_decay(x, a, b, c):
    """
    a: Amplitude / initial scale
    b: Decay rate constant
    c: Y-axis offset / asymptote
    """
    return a * (x ** -b) + c


current_A = np.array([
    4.6, 5.5, 6.4, 7.4, 8.7, 9.9, 11.2, 12.5, 14.1, 15.6, 
    17.3, 19.1, 20.7, 22.6, 24.9, 26.6, 28.8, 31.0, 32.7, 
    35.1, 37.6, 43.6, 51.8
])

efficiency_gW = np.array([
    11.3, 10.6, 10.3, 9.7, 9.2, 8.9, 8.4, 8.3, 8.0, 7.6, 
    7.4, 7.2, 7.0, 6.7, 6.5, 6.3, 6.2, 6.0, 5.9, 5.7, 
    5.6, 5.3, 4.9
])

guess_c = np.min(efficiency_gW)                    # Asymptote roughly equals minimum Y
guess_a = np.max(efficiency_gW) - guess_c          # Amplitude roughly equals total Y span
guess_b = 1.0                               # Default standard decay rate
initial_guesses = [guess_a, guess_b, guess_c]

popt, pcov = curve_fit(power_decay, current_A, efficiency_gW, p0=initial_guesses)
opt_a, opt_b, opt_c = popt
# 5. Calculate R-squared (R²) Value
residuals = efficiency_gW - power_decay(current_A, *popt)
ss_res = np.sum(residuals**2)                        # Sum of squares of residuals
ss_tot = np.sum((efficiency_gW - np.mean(efficiency_gW))**2)       # Total sum of squares
r_squared = 1 - (ss_res / ss_tot)

print("--- Discovered Parameters ---")
print(f"Amplitude (a): {opt_a:.4f}")        
print(f"Decay Rate (b): {opt_b:.4f}")
print(f"Y-Offset   (c): {opt_c:.4f}")
print(f"R² Score     : {r_squared:.4f}")

x_dense = np.linspace(min(current_A), 90 , 1000)
y_fit = power_decay(x_dense, *popt)

plt.scatter(current_A, efficiency_gW, label = "Actual Data")
plt.plot(x_dense, y_fit, color='blue', label=f'Curve Fit: $y = {opt_a:.2f}x^{{-{opt_b:.2f}}} + {opt_c:.2f}$' )
plt.axvline(x=max(current_A) , color = 'red' , linestyle = '--' , label = 'Extrapolation at the right side of the line')
plt.ylabel('Efficiency in grams/Watt')
plt.xlabel('Current in Amperes')
plt.grid(True)
plt.legend()
plt.show()