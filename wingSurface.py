import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# General parameters
AIRFOIL = 'fx60100sm'
WS = 32 - 2.8 # wingspan (meters)
AREA = 69.41 # wing's surface (square meters)
TR = 0.8 # taper ratio
SWEEP = 3.0 # sweep angle (degrees)
ETIP = 2.0 # torsion at the tip (degrees)
AOI = 12.46 # angle of incidence (degrees)

# Displaying parameters
REAL_SCALE = False # True: the plot will be in real scale, False: the plot will be adjusted in scale

# Function to represent the chord length (input in meters)
def chord_length(y):
    return root_chord - (root_chord - tip_chord)*np.abs(y)/(WS/2)

# Function to rotate a vector by an angle (input in degrees)
def rotate_vector(vector, angle):
    angle = np.deg2rad(angle)
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]).dot(vector)

# Find the root and tip chord lengths
root_chord = 2*AREA/(WS*(1+TR)) # meters
tip_chord = TR*root_chord # meters

print('Root chord:', f"{root_chord:.4f}", 'm')
print('Tip chord:', f"{tip_chord:.4f}", 'm')

# Colormap features
cmap = 'inferno' # colormap: 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Blues', 'Reds'
cmap_inv = cmap + '_r'

# Get the coordinates in extrados and intrados
airfoil_path = 'Airfoils\\' + AIRFOIL + '.txt'
data = pd.read_csv(airfoil_path, sep=r'\s+', skiprows=0, names=['x', 'z'])

# Convert the data
x = data['x'].values
z = data['z'].values

# Check if the number of points is even or odd
if len(x) % 2 == 0:
    l = 0
else:
    l = 1

# Set values for the extrados
x_extrados = x[:(len(x)//2) + l]
x_extrados = x_extrados[::-1]
z_extrados = z[:(len(z)//2) + l]
z_extrados = z_extrados[::-1]

# Set values for the intradoss
x_intrados = x[(len(x)//2):]
x_intrados = x_intrados[::-1]
z_intrados = z[(len(z)//2):]
z_intrados = z_intrados[::-1]

# Build the mesh
span = np.linspace(-WS/2, WS/2, 101)
chord_points_extr = z_extrados.shape[0]
chord_points_intr = z_intrados.shape[0]
mesh_extrados = np.zeros((chord_points_extr, len(span)), dtype=np.float64)
mesh_intrados = np.zeros((chord_points_intr, len(span)), dtype=np.float64)

# Establish heights for both intrados and extrados
extrados_height = np.zeros((chord_points_extr, len(span)))
intrados_height = np.zeros((chord_points_intr, len(span)))

# Set the torsion for every point in the span
torsion1 = np.linspace(0, ETIP, 51)
torsion2 = np.linspace(ETIP, 0, 51)
torsion = np.concatenate((torsion2, torsion1))
torsion = np.delete(torsion, int(len(torsion)/2))

# Add the angle of incidence to have the total angle of each section
torsion = torsion + AOI

# Create the vectors for every point
vectors_extr = np.column_stack((x_extrados-1/4, z_extrados))
vectors_intr = np.column_stack((x_intrados-1/4, z_intrados))

# Iterate over all spans to find the mesh and the heights
for i in range(0, len(span)):
    rotated_extr = np.zeros((len(vectors_extr),2))
    rotated_intr = np.zeros((len(vectors_intr),2))
    x_extr = np.zeros(chord_points_extr)
    x_intr = np.zeros(chord_points_intr)
    z_extr = np.zeros(chord_points_extr)
    z_intr = np.zeros(chord_points_intr)

    # Iterate over all points in the chord
    for j in range(0, len(vectors_extr)):
        rotated_extr[j] = rotate_vector(vectors_extr[j]*chord_length(np.abs(span[i])), -torsion[i])
        rotated_intr[j] = rotate_vector(vectors_intr[j]*chord_length(np.abs(span[i])), -torsion[i])
        x_extr[j] = rotated_extr[j][0]
        x_intr[j] = rotated_intr[j][0]
        z_extr[j] = rotated_extr[j][1]
        z_intr[j] = rotated_intr[j][1]

    # Generate the mesh and the heights
    mesh_extrados[:, i] = x_extr + np.tan(np.deg2rad(SWEEP))*np.abs(span[i]) + chord_length(np.abs(0))/4 - chord_length(np.abs(span[i]))/4
    mesh_intrados[:, i] = x_intr + np.tan(np.deg2rad(SWEEP))*np.abs(span[i]) + chord_length(np.abs(0))/4 - chord_length(np.abs(span[i]))/4
    extrados_height[:, i] = z_extr
    intrados_height[:, i] = z_intr

# Set 2D matrices for the surface plot
XEX = mesh_extrados
XIN = mesh_intrados
YEX = np.tile(span, (chord_points_extr, 1))
YIN = np.tile(span, (chord_points_intr, 1))
ZEX = extrados_height
ZIN = intrados_height

# Create the wing surface
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(XEX, YEX, ZEX, cmap=cmap)
ax.plot_surface(XIN, YIN, ZIN, cmap=cmap_inv)

# Set the labels
ax.set_title('Wing Surface', fontsize=18, fontweight='bold', color='red')
ax.set_xlabel('X Axis', fontsize=12, fontweight='bold', color='blue')
ax.set_ylabel('Y Axis', fontsize=12, fontweight='bold', color='blue')
ax.set_zlabel('Z Axis', fontsize=12, fontweight='bold', color='blue')

# Change the numbers of the axes with less values
ax.locator_params(axis='x', nbins=5)
ax.locator_params(axis='y', nbins=5)
ax.locator_params(axis='z', nbins=5)

# Set the aspect of the plot
if(REAL_SCALE):
    ax.set_aspect('equal')
    plt.axis('off')
else:
    ax.set_xlim(-3, 6)
    ax.set_ylim(-WS/2, WS/2)
    ax.set_zlim(-2, 2)

plt.show()