import pandas as pd
import matplotlib.pyplot as plt

# Parameters
AIRFOIL = 'hq158'

# Read the data from the file
airfoil_path = 'Airfoils\\' + AIRFOIL + '.txt'
data = pd.read_csv(airfoil_path, sep='\s+', skiprows=0, names=['x', 'z'])

# Print the first few rows of the data
print(data.head())

# Plot the airfoil
plt.figure(figsize=(10, 6))
plt.plot(data['x'], data['z'])
plt.title(AIRFOIL, fontsize=18, fontweight='bold')
plt.xlabel('Coordinate X')
plt.ylabel('Coordinate Z')
plt.axis('equal')
plt.grid(True)
plt.show()