import numpy as np

# Constants of the problem
G = 9.81 # [m/s^2] gravity constant
R = 287.05 # [J/(kg*K)] gas constant
MTOW = 28300 # [kg] maximum take-off weight
ALT_CRUISE = 7600 # [m] altitude at cruise
V_CRUISE = 110 # [m/s] speed at cruise
V_TAKEOFF = 60 # [m/s] speed at take-off
V_TAKEOFF_4000 = 75 # [m/s] speed at take-off at 4000 m
RHO_0 = 1.225 # [kg/m^3] density at sea level
RHO_11000 = 0.3639 # [kg/m^3] density at 11 km
T0 = 288.15 # [K] temperature at sea level
T_11000 = 216.65 # [K] temperature at 11 km
LAMBDA = -0.0065 # [K/m] temperature gradient
MU_0 = 1.789e-5 # [kg/(m*s)] dynamic viscosity at sea level
MU_4000 = 1.659e-5 # [kg/(m*s)] dynamic viscosity at 4000 m
MU_7600 = 1.365e-5 # [kg/(m*s)] dynamic viscosity at 5460 m
MU_CRUISE = MU_7600 # [kg/(m*s)] dynamic viscosity at cruise
WS = 32 - 2.8 # [m] wingspan
AREA = 69.41 # [m^2] wing area
TR = 0.8 # taper ratio

# Find the root and tip chord lengths
root_chord = 2*AREA/(WS*(1+TR)) # meters
tip_chord = TR*root_chord # meters

# Calculate the density at a certain altitude over 11 km
def density(altitude):
    if(altitude < 11e+3 and altitude >= 0):
        return RHO_0*((T0+LAMBDA*altitude)/T0)**(-G/(R*LAMBDA)-1)
    elif(altitude >= 11e+3):
        return RHO_11000*np.exp(-(G*(altitude-11e+3))/(R*T_11000))
    else:
        print('The altitude is invalid.')
        return 0

# Calculate the temperature at a certain altitude
def temperature(altitude):
    if(altitude < 11e+3 and altitude >= 0):
        return T0+LAMBDA*altitude
    elif(altitude >= 11e+3):
        return T_11000
    else:
        print('The altitude is invalid.')
        return 0

# Calculate the SCL at certain density and speed
def scl(density, speed):
    return 2*MTOW*G/(density*speed**2)

# Find the reynolds number for every situation
def reynolds(density, speed, chord, mu):
    return density*speed*chord/mu

# Display the chords
print('Root chord:', f"{root_chord:.4f}")
print('Tip chord:', f"{tip_chord:.4f}", '\n')

# Display the results for SCL
print('SCL at cruise:', f"{scl(density(ALT_CRUISE), V_CRUISE):.4f}")
print('SCL at takeoff:', f"{scl(RHO_0, V_TAKEOFF):.4f}")
print('SCL at takeoff (airport at 4000 m):', f"{scl(density(4000), V_TAKEOFF):.4f}", '\n')

# Display the results for Reynolds number
print('Reynolds number at cruise, root:', f"{reynolds(density(ALT_CRUISE), V_CRUISE, root_chord, MU_CRUISE):.2e}")
print('Reynolds number at cruise, tip:', f"{reynolds(density(ALT_CRUISE), V_CRUISE, tip_chord, MU_CRUISE):.2e}")
print('Reynolds number at takeoff, root:', f"{reynolds(RHO_0, V_TAKEOFF, root_chord, MU_0):.2e}")
print('Reynolds number at takeoff, tip:', f"{reynolds(RHO_0, V_TAKEOFF, tip_chord, MU_0):.2e}")
print('Reynolds number at takeoff (airport at 4000 m), root:', f"{reynolds(density(4000), V_TAKEOFF_4000, root_chord, MU_4000):.2e}")
print('Reynolds number at takeoff (airport at 4000 m), tip:', f"{reynolds(density(4000), V_TAKEOFF_4000, tip_chord, MU_4000):.2e}")