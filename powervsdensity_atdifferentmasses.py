import numpy as np
import matplotlib.pyplot as plt
import scipy

m_values = np.arange(0,11,2)
rho = np.linspace(0.9, 1.225, 1000)
radius = 0.3048 # metres
A = np.pi * (radius**2) 


for m in m_values:
    power_consumption = ((9.81 ** 1.5) * (18.8/6.0 + m/6.0)** 1.5) / np.sqrt(2 * rho * A)

    plt.plot(rho, power_consumption, label=f'{m} kg')

plt.plot(rho, power_consumption)
plt.xlabel('Density (kg/m^3)')
plt.ylabel('Power Consumption per motor (Watts)')
plt.title('Power Consumption vs Density at different payload masses')
plt.grid(True)
plt.legend()
plt.show()
