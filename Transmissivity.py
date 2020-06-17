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
Author: Jonny Full
Version: 6/11/2020
-------------------------------------------------------------------------------
"""
"""
This function should be broken down into smaller helper function, this will
make things simpiler.

6/17/2020
"""
import math
from pump_log_calc import pump_log
from allwells_calc import allwells_data

def calc(relate_id):
    Q = [float()] #gpm
    s = [float()] #ft
    L = [float()] #day
    rw = [float()] #ft
    t = [float()] #ft
    VALUE = [float()] #ft^2/day
    b = 100   #ft  
    Co = 0
    T = 1
    S = 0.001 #storativity = S temporary constant

    Q, t, s = pump_log(relate_id)
    L, rw = allwells_data(relate_id)
    for i in range(len(Q)):
        sw = [Co * (Q[i]**2)]
        T = 1.0
        LastValue = 0
        Lb = L[i]/b  
        G = 2.948 - (7.363*(Lb)) + (11.447*((Lb)**2)) - (4.675*((Lb)**3))
        if L[i] > 0 and rw[i] > 0:
            sp = ((1-Lb)/Lb)*(math.log(b/rw[i])-G)
        else:
            sp = 0
        while (T - LastValue) >= 0.001:
            LastValue = T
            if Q[i] is not None and t[i] is not None and L[i] is not None and rw[i] is not None and s[i] is not None:
                if Q[i] > 0 and t[i] > 0 and L[i] > 0 and rw[i] > 0 and s[i] > 0:
                    T = (Q[i] /(4*math.pi*(s[i])))*(math.log(2.25*T* t[i] /((rw[i] **2) * S)) + (2*sp))
                else:
                    T = 0
            else:
                T = 0
        VALUE.append(T)
        VALUE = [t for t in VALUE if t > 0] #removes T = 0 values redesign later
    return VALUE



"""
Conduct(TSIV)
This function transilates the Transmissivity values from Calc into 
Hydralic conductivity values.

This function requires analyze_wells.TSIV to run.
-------------------------------------------------------------------------------
Author: Jonny Full
Version:6/12/2020
"""
def Conduct(TSIV):
    b = 100
    hydro_cond = []
    for i in range(len(TSIV)):
        K=TSIV[i]/b
        hydro_cond.append(K)
    return hydro_cond
