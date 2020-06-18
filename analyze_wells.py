
"""
function analyzeWells:
    This function calculates Transmissivity and performs statistical analysis
    of a series of water wells. Transmissivity is being calculated with the 
    Bradbury & Rothschild Method.
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
#from Transmissivity import calc, Conduct
from data_retrieve import pump_log, allwells_data
from plots import plot_T

ID, rad = Verify()
RADIUS = int(rad) #meters
candidate_wells = findWells(ID, RADIUS)
pump_log_results = pump_log(candidate_wells)
confirmed_wells= allwells_data(pump_log_results)
#relate_id = [i[2] for i in selected_wells]
"""
TSIV = calc(selected_wells)
HYDCONDUCT = Conduct(TSIV)
plot_T(TSIV)
"""