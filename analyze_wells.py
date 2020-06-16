
"""
function analyzeWells:
    This function calculates Transmissivity and performs statistical analysis
    of a series of water wells.
-------------------------------------------------------------------------------
Notes:
    -This file requires Data Location, findWells, Transmissivity, and Verify to execute

@author: Jonny Full
Version: 6/16/2020
-------------------------------------------------------------------------------
"""
#COMPLETE
from Verify import Verify
from findWells import findWells
from Transmissivity import calc, Conduct
from plots import plot_T

ID, rad = Verify()
RADIUS = int(rad) #meters
selected_wells = findWells(ID, RADIUS)
location = [i[0] for i in selected_wells]
aqui_id = [i[1] for i in selected_wells] #incorperate into Storativity/ Thickness calculations
relate_id = [i[2] for i in selected_wells]
TSIV = calc(relate_id)
HYDCONDUCT = Conduct(TSIV)
plot_T(TSIV)
