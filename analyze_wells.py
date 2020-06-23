
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
from Transmissivity import calc, Conduct
from data_retrieve import data_organization, pump_log
from plots import plot_T, spacial_T

ID, rad = Verify()
RADIUS = int(rad) #meters
candidate_wells = findWells(ID, RADIUS)
pump_log_results = pump_log(candidate_wells)
confirmed_wells = data_organization(candidate_wells, pump_log_results)
TSIV = calc(confirmed_wells)
TSIV.pop(0)
HYDCONDUCT = Conduct(TSIV)
#plot_T(TSIV)
spacial_T(confirmed_wells, TSIV)
