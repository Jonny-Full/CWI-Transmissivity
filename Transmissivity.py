"""Calculates Transmissivity and Hydralic Conductivity of every well in the 
   confirmed_wells table. The method used to calculate the Transmissivity
   is the Bradbury & Rothschild Method.

Functions
---------

    calc: Calculates the Transmissivity for each entry in confirmed_wells
    
    Conduct: Calculates the Hydralic Conductivity from transmissivity_calculated
    
Notes
-----
    This function uses imperial units. The relationship of variables and their
    units are shown below:
    Q = Pump Rate (ft/day)
    s = Drawdown (ft)
    t = Duration of Test (days)
    L = Screen Length (ft)
    r = Well Radius (ft)
    b = Aquifer Thickness (ft)
    rw = Radius of Influence (ft)
    Co = Step-Drawdown Test
    T = Transmissivity (ft^2/day)
    K = Hydralic Conductivity (ft/day)

Assumptions
-----------
    Radius of Influence = Well Radius
    The aquifer is infidently long
    Constant Pump Rate
    Homogonous Nonleaky Aquifer
    
Citations
---------
    Bradbury, K. R. & Rothschild, E. R.
    A COMPUTERIZED TECHNIQUE FOR ESTIMATING THE HYDRAULIC CONDUCTIVITY OF 
    AQUIFERS FROM SPECIFIC CAPACITY DATA, 
    Groundwater, 1985, 23, 240-246 

Author: Jonny Full
Version: 6/24/2020
-------------------------------------------------------------------------------
"""
import math

def transmissivity_calculations(confirmed_wells):
    """Computes the Transmissivity for every well in confirmed_wells
    
    Parameters
    ----------
        confirmed_wells: list[[list1][list2]]
            This is a list of all pertinant information required to plot the wells
            spacially and calculate Transmissivity.
    
            list1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float), 
                         Casing Radius (ft), Relate ID (str)]
    
            list 2 = list[Pump Rate (float), Duration (float), Drawdown (float), 
                          Relate ID (str)]
    Returns
    -------
        transmissivity_calculated: list[float]
        transmissivity_calculated represents the calculated Transmissivity for 
        each row in confirmed_wells.
    """
    transmissivity_calculated = [] #ft^2/day  
    Co = 0
    T = 1
    S = [i[2][1] for i in confirmed_wells] #storativity = S temporary constant
    Q = [i[1][0] for i in confirmed_wells]
    t = [i[1][1] for i in confirmed_wells]
    s = [i[1][2] for i in confirmed_wells]
    L = [i[0][3] for i in confirmed_wells]
    rw = [i[0][4] for i in confirmed_wells]
    b = [i[2][0] for i in confirmed_wells]
    
    for i in range(len(Q)):
        #sw = [Co * (Q[i]**2)]
        T = 1.0
        LastValue = 0
        if L[i] > 0 and rw[i] > 0:
             Lb = L[i]/b[i]
             """
             There are errors in the CWI_hydro table data. This data may
             describes an aquifer setting where the well penetrates through
             multiple aquifers. If this is the case, we will assume that the
             well only penetrates the entire aquifer based on the data
             available. This can be seen with the logic below.
             """
             if Lb > 1:
                Lb = 1
             G = 2.948 - (7.363*(Lb)) + (11.447*((Lb)**2)) - (4.675*((Lb)**3))
             sp = ((1-Lb)/Lb)*(math.log(b[i]/rw[i])-G)
        else:
            sp = 0
        while (T - LastValue) >= 0.001:
            LastValue = T
            if Q[i] is not None and t[i] is not None and L[i] is not None and rw[i] is not None and s[i] is not None:
                if Q[i] > 0 and t[i] > 0 and L[i] > 0 and rw[i] > 0 and s[i] > 0:
                    T = (Q[i]/(4*math.pi*(s[i])))*(math.log((2.25*T* t[i])/((rw[i]**2) * S[i])) + (2*sp))
        transmissivity_calculated.append(T)
    return transmissivity_calculated


def conductivity_calculations(confirmed_wells, transmissivity_calculated):
    """Converts the Transmissivity values to Hydralic Conductivity
    
    Parameters
    ----------
    transmissivity_calculated: list[float]
    transmissivity_calculated represents the calculated Transmissivity for each
    row in confirmed_wells.
    
    
    Returns
    -------
    hydro_cond: list[float]
    hydro_cond represents the calculated hydralic conductivity for each row in
    transmissivity_calculated.
    
    Notes
    -----
    Hydralic Conductivity can be calculated with the following equation:
        K = T/b
    """
    b = [i[2][0] for i in confirmed_wells]
    hydro_cond = []
    for i in range(len(transmissivity_calculated)):
        K=transmissivity_calculated[i]/b[i]
        hydro_cond.append(K)
    return hydro_cond
