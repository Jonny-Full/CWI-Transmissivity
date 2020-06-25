""" This is a driver function that calculates Transmissivity for a selected
well in the state of Minnesota.

This function calculates Transmissivity and performs statistical analysis
of a series of water wells. Transmissivity is being calculated with the 
Bradbury & Rothschild Method.


Notes
-----
    This file requires Data Location, findWells, Transmissivity, and Verify to execute

Author: Jonny Full
Version: 6/24/2020
-------------------------------------------------------------------------------
"""
#COMPLETE
from Verify import Verify
from Transmissivity import calc, Conduct
from data_retrieve import find_wells, data_organization, pump_log
from plots import plot_T, spacial_T

target_well, rad = Verify()
RADIUS = int(rad) #meters
candidate_wells = find_wells(target_well, RADIUS)
pump_log_results = pump_log(candidate_wells)
confirmed_wells = data_organization(candidate_wells, pump_log_results)
transmissivity_calculated = calc(confirmed_wells)
transmissivity_calculated.pop(0)
HYDCONDUCT = Conduct(transmissivity_calculated)
#plot_T(TSIV)
spacial_T(confirmed_wells, transmissivity_calculated)
