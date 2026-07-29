from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv(r"C:\Users\Tejo\Downloads\GPS_OF_merged - OF_GPS_merged.csv")


reference_time = df['TimeUS'].iloc[0]

df['Time_sec'] = (df['TimeUS'] - reference_time )/1000000.0

df = df.dropna(subset=['TimeUS', 'Speed_GPS', 'Speed_OF']) 
df = df[np.isfinite(df['TimeUS']) & np.isfinite(df['Speed_GPS']) & np.isfinite(df['Speed_OF'])]  



x_data = df['Time_sec'].values
y_data = df['Speed_GPS'].values
y_data_2 = df['Speed_OF'].values

def model(x, m, c):
    return m*x + c

popt, _ = curve_fit(model, x_data, y_data)
popt2, _ = curve_fit(model, x_data, y_data_2 )



plt.scatter(x_data, y_data, label = 'Speed Detected by GPS')
plt.scatter(x_data, y_data_2, label = 'Speed Detected by OF')
plt.plot(x_data, model(x_data, *popt), 'r-', label='Fit')
plt.plot(x_data,model(x_data, *popt2), 'black' ,  label = 'fit')

res_1 = stats.linregress(x_data, y_data)
print(f"Speed Detected by GPS Slope: {res_1.slope}, Intercept: {res_1.intercept}")

res_2 = stats.linregress(x_data, y_data_2)
print(f"Speed Detected by OF Slope: {res_2.slope}, Intercept: {res_2.intercept}")

plt.legend()
plt.show()
