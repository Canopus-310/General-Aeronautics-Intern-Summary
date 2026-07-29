import matplotlib.pyplot as plt
import numpy as np

# Data extracted from Hobbywing X6 Plus (24x8.0 Prop) Datasheet at 46V
rpm = np.array([2455, 2605, 2754, 2900, 3047, 3184, 3325, 3456, 3589, 
                3716, 3841, 3959, 4080, 4194, 4307, 4415, 4519, 4627, 
                4723, 4821, 4912, 5142, 5442])

thrust_g = np.array([2416, 2732, 3058, 3377, 3746, 4106, 4419, 4822, 5209, 
                     5476, 5947, 6370, 6709, 7086, 7501, 7779, 8238, 8654, 
                     9016, 9294, 9782, 10731, 11822])

# Convert thrust to Newtons for standard physics calculations (1g = 0.00980665 N)
thrust_n = thrust_g * 0.00980665

# Fit a 2nd-degree polynomial (quadratic) to the data: T = C_T * w^2 + C_T0 * w + C
# Note: polyfit returns coefficients [a, b, c] for ax^2 + bx + c
coefficients = np.polyfit(rpm, thrust_n, 2)
C_T = coefficients[0]
C_T0 = coefficients[1]
constant = coefficients[2]

print(f"Quadratic Coefficients:")
print(f"C_T (omega^2): {C_T:.8f}")
print(f"C_T0 (omega): {C_T0:.8f}")
print(f"Constant offset: {constant:.8f}")

# Generate a smooth curve for the plot using the calculated coefficients
rpm_trend = np.linspace(min(rpm), max(rpm), 100)
thrust_trend = (C_T * rpm_trend**2) + (C_T0 * rpm_trend) + constant

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(rpm, thrust_n, color='blue', label='Hobbywing Datasheet Data', zorder=5)
plt.plot(rpm_trend, thrust_trend, color='red', linestyle='--', label='Quadratic Fit ($T = C_T \omega^2 + C_{T0} \omega$)')

# Formatting
plt.title('Hobbywing X6 Plus: Motor RPM vs Thrust', fontsize=14)
plt.xlabel('Motor Speed (RPM)', fontsize=12)
plt.ylabel('Thrust (Newtons)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()