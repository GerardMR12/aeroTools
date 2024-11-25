import pandas as pd
import matplotlib.pyplot as plt

# Parameters
AIRFOIL1 = 'naca4412'
AIRFOIL2 = 'naca63215'
AIRFOIL3 = 'naca63415'
AIRFOIL4 = 'naca63615'
AIRFOIL5 = 'naca4412'
AIRFOIL6 = 'naca63615'

# Read the data from each of the files
airfoil_path = 'Airfoils\\' + AIRFOIL1 + '.txt'
data1 = pd.read_csv(airfoil_path, sep=r'\s+', skiprows=0, names=['x', 'z'])

airfoil_path = 'Airfoils\\' + AIRFOIL2 + '.txt'
data2 = pd.read_csv(airfoil_path, sep=r'\s+', skiprows=0, names=['x', 'z'])
data2['z'] = data2['z'] - 0.2

airfoil_path = 'Airfoils\\' + AIRFOIL3 + '.txt'
data3 = pd.read_csv(airfoil_path, sep=r'\s+', skiprows=0, names=['x', 'z'])
data3['z'] = data3['z'] - 0.4

airfoil_path = 'Airfoils\\' + AIRFOIL4 + '.txt'
data4 = pd.read_csv(airfoil_path, sep=r'\s+', skiprows=0, names=['x', 'z'])
data4['z'] = data4['z'] - 0.6

# Plot the airfoil
plt.figure(figsize=(10, 6))
plt.plot(data1['x'], data1['z'], label=AIRFOIL1)
plt.plot(data2['x'], data2['z'], label=AIRFOIL2)
plt.plot(data3['x'], data3['z'], label=AIRFOIL3)
plt.plot(data4['x'], data4['z'], label=AIRFOIL4)
plt.title('Several airfoils', fontsize=30, fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=14)
plt.xlabel('Coordinate X', fontsize=20)
plt.ylabel('Coordinate Z', fontsize=20)
plt.axis('equal')
plt.legend()
plt.grid(True)

# Read the data from each of the files
airfoil_path = 'Airfoils\\' + AIRFOIL5 + '.txt'
data5 = pd.read_csv(airfoil_path, sep=r'\s+', skiprows=0, names=['x', 'z'])

airfoil_path = 'Airfoils\\' + AIRFOIL6 + '.txt'
data6 = pd.read_csv(airfoil_path, sep=r'\s+', skiprows=0, names=['x', 'z'])

# Plot the airfoil
plt.figure(figsize=(10, 6))
plt.plot(data5['x'], data5['z'], label=AIRFOIL5, color='red')
plt.plot(data6['x'], data6['z'], label=AIRFOIL6, color='blue')
plt.title('Width comparison', fontsize=30, fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=14)
plt.xlabel('Coordinate X', fontsize=20)
plt.ylabel('Coordinate Z', fontsize=20)
plt.axis('equal')
plt.legend()
plt.grid(True)
plt.show()