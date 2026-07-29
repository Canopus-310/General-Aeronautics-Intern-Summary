from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv(r"C:\Users\GA\Downloads\30 March Final - aligned_30_March.csv")


reference_time = df['TimeUS'].iloc[0]

df['Time_sec'] = (df['TimeUS'] - reference_time )/1000000.0

df = df.dropna(subset=['TimeUS', 'SAlt_m', 'Power in KW']) 
df = df[np.isfinite(df['TimeUS']) & np.isfinite(df['SAlt_m']) & np.isfinite(df['Power in KW'])]  



x_data = df['Time_sec'].values
y_data = df['SAlt_m'].values
y_data_2 = df['Power in KW'].values

def model(x, m, c):
    return m*x + c


coeffs = np.polyfit(x_data, y_data, 2)
p_function = np.poly1d(coeffs)

popt2, _ = curve_fit(model, x_data, y_data_2 )

x_fit = np.linspace(x_data.min(), x_data.max(), 4330)
y_fit = p_function(x_fit)


plt.scatter(x_data, y_data_2, label='Power in KW', color='blue')
plt.scatter(x_data, y_data, label='Altitude', color='orange')
plt.plot(x_fit, y_fit, label = 'Altitude')
plt.plot(x_data,model(x_data, *popt2), 'black' ,  label = 'fit')

print(f"Altitude Equation: {coeffs[0]}x² + {coeffs[1]}x + {coeffs[2]}")

res_2 = stats.linregress(x_data, y_data_2)
print(f"Power Slope: {res_2.slope}, Intercept: {res_2.intercept}")

plt.legend()
plt.show()
