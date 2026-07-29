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

popt, _ = curve_fit(model, x_data, y_data)
popt2, _ = curve_fit(model, x_data, y_data_2 )



plt.scatter(x_data, y_data, label = 'Altitude')
plt.scatter(x_data, y_data_2, label = 'Power in KW')
plt.plot(x_data, model(x_data, *popt), 'r-', label='Fit')
plt.plot(x_data,model(x_data, *popt2), 'black' ,  label = 'fit')

res_1 = stats.linregress(x_data, y_data)
print(f"Altitude Slope: {res_1.slope}, Intercept: {res_1.intercept}")

res_2 = stats.linregress(x_data, y_data_2)
print(f"Power Slope: {res_2.slope}, Intercept: {res_2.intercept}")

plt.legend()
plt.show()
