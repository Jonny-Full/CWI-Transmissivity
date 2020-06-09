"""
Transmissivity T(x):

This function calculates the Transmissivity for a specific well. This function
uses the Bradbury & Rothschild method for calculations.

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

6/8/2020
"""
import math
from scipy.optimize import fsolve
from PumpLogCalc import PumpLog
from AllWellsCalc import ALLWELLS_DATA




def Calc(RID):
    Q = [] #gpm
    s = [] #ft
    L = [] #day
    rw = [] #ft
    t = [] #ft
    VALUE = [] #ft^2/day
    b = 100   #ft  
    Co = 0
    #sw = Co * Q**2 
    T = 1
    sp = 0
    S = 0.001 #storativity = S temporary constant     

    Q = [] #gpm
    s = [] #ft
    L = [] #day
    rw = [] #ft
    t = [] #ft
    VALUE = []
    
    Q, t, s = PumpLog(RID)

    
    L, rw = ALLWELLS_DATA(RID)
    
    for i in range(len(Q)):
        T = 1.0
        LastValue = 0
        #Lb = [L[i]/b]  
        #G =  [2.948 - (7.363*(Lb)) + (11.447*((Lb)**2)) - (4.675*((Lb)**3))]
        #sp = ((1-Lb)/Lb)*(math.log(b[i]/rw[i])-G)
        while (T - LastValue) >= 0.001:
            LastValue = T
            if Q[i] > 0 and t[i] > 0 and L[i] > 0 and rw[i] > 0 and s[i] > 0:
                
                T = (Q[i] /(4*math.pi*(s[i])))*(math.log(2.25*T* t[i] /((rw[i] **2) * S))) + (2*sp)
            else:
                T = 0
                
        VALUE.append(T)

    return VALUE
    
#x = fsolve(T, 0)
#VALUE = Calc(RID)
#print(Calc(RID))   








