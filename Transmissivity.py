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
Version: 7/30/2020
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
    S_min = [i[2][1] for i in confirmed_wells] #storativity = S temporary constant
    S_max = [i[2][2] for i in confirmed_wells]
    Q_min = [i[1][0] for i in confirmed_wells]
    Q = [i[1][1] for i in confirmed_wells]
    Q_max = [i[1][2] for i in confirmed_wells]
    t = [i[1][3] for i in confirmed_wells]
    s_min = [i[1][4] for i in confirmed_wells]
    s = [i[1][5] for i in confirmed_wells]
    s_max = [i[1][6] for i in confirmed_wells]
    L = [i[0][3] for i in confirmed_wells]
    rw = [i[0][4] for i in confirmed_wells]
    b = [i[2][0] for i in confirmed_wells]
    for i in range(len(Q_min)):
        #sw = [Co * (Q[i]**2)]
        T_max = 1.0
        T = 1.0
        T_min = 1.0
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
        while (T_min - LastValue) >= 0.001:
            LastValue = T_min
            T_min = (Q_min[i]/(4*math.pi*(s_max[i])))*\
            (math.log((2.25*T_min* t[i])/((rw[i]**2) * S_max[i])) + (2*sp))
        
        LastValue = 0
        while (T - LastValue) >= 0.001:
            LastValue = T
            T = (Q[i]/(4*math.pi*(s[i])))*\
            (math.log((2.25*T* t[i])/((rw[i]**2) * S_max[i])) + (2*sp))
        
        LastValue = 0 
        while (T_max - LastValue) >= 0.001:
            LastValue = T_max
            T_max = (Q_max[i]/(4*math.pi*(s_min[i])))*\
            (math.log((2.25*T_max* t[i])/((rw[i]**2) * S_min[i])) + (2*sp))
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
    b = [i[2][0] for i in confirmed_wells]
    T_min = [i[0] for i in transmissivity_calculated]
    T_guess = [i[0] for i in transmissivity_calculated]
    T_max = [i[2] for i in transmissivity_calculated]
#    well_identify = [i[2] for i in transmissivity_calculated]
    hydro_cond = []
    for i in range(len(transmissivity_calculated)):
#        well_id = well_identify[i]
        K_min = T_min[i] / b[i]
        K_guess = T_guess[i] / b[i]
        K_max = T_max[i] / b[i]
        K_values = [K_min, K_guess, K_max]
        hydro_cond.append(K_values)
    return hydro_cond

#if __name__ == '__main__':
#    transmissivity_calculations(confirmed_wells)
#    conductivity_calculations(confirmed_wells, transmissivity_calculated)