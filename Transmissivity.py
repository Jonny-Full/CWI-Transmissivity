"""Calculates Transmissivity and Hydralic Conductivity of every well in the
   confirmed_wells table. The method used to calculate the Transmissivity
   is the Bradbury & Rothschild Method.

Functions
---------

    transmissivity_calculations: Calculates the Transmissivity for each entry 
    in confirmed_wells

    conductivity_calculations: Calculates the Hydralic Conductivity from 
    transmissivity_calculated

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
Version: 7/30/2020
-------------------------------------------------------------------------------
"""
import math
from scipy.special import lambertw

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
    S_min = [i[2][3] for i in confirmed_wells] #storativity = S temporary constant
    S_max = [i[2][4] for i in confirmed_wells]
    Q_min = [i[1][0] for i in confirmed_wells]
    Q = [i[1][1] for i in confirmed_wells]
    Q_max = [i[1][2] for i in confirmed_wells]
    t = [i[1][3] for i in confirmed_wells]
    s_min = [i[1][4] for i in confirmed_wells]
    s = [i[1][5] for i in confirmed_wells]
    s_max = [i[1][6] for i in confirmed_wells]
    L = [i[0][3] for i in confirmed_wells]
    rw = [i[0][4] for i in confirmed_wells]
    b = [i[2][1] for i in confirmed_wells]
    for i in range(len(Q_min)):
      
        
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
        
        data = (-16*math.pi/9)*(1/math.exp(2*sp))*(s_min[i]*(rw[i]**2)*S_min[i]\
                /(Q_min[i]*t[i]))
        W_min = lambertw(data,-1)
        T_max = -(Q_min[i]/(4*math.pi*(s_min[i])))*W_min
        

        data = (-16*math.pi/9)*(1/math.exp(2*sp))*(s[i]*(rw[i]**2)*\
                S_max[i]/(Q[i]*t[i]))
        W_raw = lambertw(data,-1)
        T = -(Q[i]/(4*math.pi*(s[i])))*W_raw
            
        data = (-16*math.pi/9)*(1/math.exp(2*sp))*(s_max[i]*(rw[i]**2)*\
                S_max[i]/(Q_max[i]*t[i]))
        W_max = lambertw(data,-1)
        T_min = -(Q_max[i]/(4*math.pi*(s_max[i])))*W_max
        
        T_range = [T_min, T, T_max]
        transmissivity_calculated.append(T_range)
    return transmissivity_calculated #break into two lists?


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
    b_min = [i[2][0] for i in confirmed_wells]
    b = [i[2][1] for i in confirmed_wells]
    b_max = [i[2][2] for i in confirmed_wells]
    T_min = [i[0] for i in transmissivity_calculated]
    T = [i[1] for i in transmissivity_calculated]
    T_max = [i[2] for i in transmissivity_calculated]
    well_id = [i[0][5] for i in confirmed_wells]
    hydro_cond = []
    for i in range(len(transmissivity_calculated)):
        well_id_data = well_id[i]
        K_min = T_min[i] / b_max[i]
        K_guess = T[i] / b[i]
        K_max = T_max[i] / b_min[i]
        K_values = [K_min, K_guess, K_max, well_id_data]
        hydro_cond.append(K_values)
    return hydro_cond
