import numpy as np
import scipy as sp
from scipy.integrate import odeint 
import matplotlib.pyplot as plt

#### Set-up Parameters #####

V = 25          # Volume of water in the storage tank
rho = 1000      # Density of water
M = V*rho       # Mass of water in the storage tank
CP = 4.2        # Specific heat capacity of water
D = 5           # Vessel inner diameter

CSA = 0.25*sp.pi*D**2   # Cross-sectional area of the vessel

m = 3.3           # Recirculation rate around the recirc / heater loop
Tout = 85       # Outlet temperature setpoint of the heat exchanger

U = 0.002                   # Overall heat transfer coefficient for heat losses to environment
WSA = sp.pi*D*(V/CSA)       # Wetted surface area of the vessel
Tamb = 15                   # Ambient temperature

Tf = 80         # Target final temperature

T0 = 65         # Initial tank temperature


alpha = m*CP*Tout + U*WSA*(Tamb)      # Simplifies maths.

beta = m*CP + U*WSA                   # Simplifies maths.


### Differential Equation Function ###

def model(y, t):
    
    dydt = (alpha - beta*y) / (M*CP)
    return dydt


# Set initial condition

y0 = T0


# Generate time vector

t= np.linspace(0,15*3600)

thours = t/3600

# Solve ODE

y = odeint(model, y0, t)


# Finds where the target end temperature was reached.

index = (np.abs(Tf - y)).argmin()

time_reached = round(t[index]/3600, 2)

print(f"Time to reach {Tf} degrees C is {time_reached} hours.")


# Plot results

plt.plot(thours,y)
plt.xlabel('Time After Start of Heating [hours]')
plt.ylabel('Bulk Tank Temperature [deg C]')
plt.show()