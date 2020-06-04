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

5/22/2020
"""
import numpy as np
import math
from scipy.optimize import fsolve
from Pump import Pump
from DrawDown import DrawDown
from getTime import Time
from CasingRadius import Radius
from ScreenLength import Screen



def Calc(RID):
   #This code assumes imperial units only 
    Q = 100    #gpm
    s = 5     #ft  
    t = 1     #day  
    L = 100   #ft  
    r = 0.25  #ft  not required for calculations but needed for rw
    b = 100   #ft  
    rw = 0.25 #ft
    Co = 0
    sw = Co * Q**2 
    Tguess = 1
    sp = 0
    S = 0.001 #storativity = S temporary constant 

        
    Q = []
    Q = Pump(RID)
    print("Q Done")    
    s = []
    s = DrawDown(RID)
    print("s Done")    
    L = []
    L = Screen(RID)
    print("L Done")
    rw = []
    rw = Radius(RID)
    print("rw done")
    t = []
    t = Time(RID)
    print("t done")
    
    for i in range(len(Q)):
        
        Lb = L[i]/100  
        G =  2.948 - (7.363*(Lb)) + (11.447*((Lb)**2)) - (4.675*((Lb)**3))
        
        sp = ((1-Lb)/Lb)*(math.log(b[i]/rw[i])-G)
        
    #change to a while loop
        Transmissivity = (Q[i]/(4*math.pi*(s[i]-sw)))*(math.log(2.25*Tguess*t[i]/((rw[i]**2) * S)) + 2*sp[i])

    print(Transmissivity)   
    
    return(Q/(4*math.pi*(s-sw)))*(math.log(2.25*Tguess*t/((rw**2) * S)) + 2*sp)
    
#x = fsolve(T, 0)
 


