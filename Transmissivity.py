"""
Transmissivity T(x):

This function calculates the Transmissivity for a specific well.

INPUTS:
    Q = pump rate (gal/min)
    s = drawdown  (ft)
    t = time (days)
    L = Screen Length (ft)
    r = Well Radius   (in)
    b = Aquifer Thickness (ft)
    rw = radius of influence (ft)
    Co = Step-Drawdown Test
    
OUTPUTS:
    
    Transmissivity (ft^2/day)
    
    
ASSUMPTIONS:
    Radius of Influence = Well Radius
    Aquifer is infidently long
    Constant Pump Rate
    Homogonous Nonleaky Aquifer
    
@author: Jonny Full
Created on Mon May 18 09:01:15 2020
-------------------------------------------------------------------------------
"""
"""
This function should be broken down into smaller helper function, this will
make things simpiler.

5/22/2020
"""

import math
from scipy.optimize import fsolve
#from Buffer import Count_2
#from Buffer import allwells_3_

def T(x):
   #This code assumes imperial units only 
    Q = 100    #gpm
    s = 5     #ft  
    t = 1     #day  
    L = 100   #ft  
    r = 0.25  #ft  not required for calculations but needed for rw
    b = 100   #ft  
    rw = 0.25 #ft
    Co = 0
    #WW = 62.4 #Lb/ft^3 weight of water
    #ADD EFFECTIVE RADIUS CALCULATION

    """
    Q = input("Insert Pump Rate (gal/min): ")
    Q = float(Q)
    s = input("Enter drawdown (ft):")
    s = float(s)
    t = input("Enter Pumping Duration (days): ")
    t = float(t)
    L = input("Enter screen length (ft): ")
    L = float(L)
    r = input ("Enter wellbore radius (in): ")
    r = float(r)
    
    b = input("Aquifer Thickness (ft): ")
    b = float(b)
    rw = input("Effective Radius (ft): ") #Use the radius of the casing
    rw = float(rw)
    Co = input("Enter step-test value: ")
    Co = float(Co)
    """
    
    Q = Q*192.5
    
   # Sy = WW/E
    
    #S= Sy*b #Use Rich's code to determine storativity
    
    S = 0.001 #storativity = S temporary constant
    
     
    Lb = L/b
      
    G =  2.948 - (7.363*(Lb)) + (11.447*((Lb)**2)) - (4.675*((Lb)**3))
    sp = 0
    sp = ((1-Lb)/Lb)*(math.log(b/rw)-G)
    
    sw = Co * Q**2 
    T = 1
    
    T = (Q/(4*math.pi*(s-sw)))*(math.log(2.25*T*t/((rw**2) * S)) + 2*sp)

       
    return(Q/(4*math.pi*(s-sw)))*(math.log(2.25*T*t/((rw**2) * S)) + 2*sp)
x = fsolve(T, 0.001)
T(x)
    
print(T(x))

