""" This is a driver function that calculates Transmissivity for an area
of wells in the state of Minnesota.

This function calculates Transmissivity and performs statistical analysis
of a series of water wells. The program will prompt the user to input a WellID
number and radial distance (in meters) to act as a boundary condition for the
query. Transmissivity is being calculated with the Bradbury & Rothschild Method.


Notes
-----
    This file requires data_location, data_retrieve, Transmissivity,
    aquifer_values, Thickness, Transmissivity, and Verify to execute. See these
    files for clarification on their respective functions.

    The file paths in data_location must be changed to properly reference the
    data tables used by this function on the user's computer.

Author: Jonny Full
Version: 7/13/2020
-------------------------------------------------------------------------------
"""
#COMPLETE
from Verify import Verify
from Transmissivity import transmissivity_calculations, conductivity_calculations
from data_retrieve import find_wells, data_organization, pump_log,\
aquifer_thickness, storativity_calculations
from plots import plot_histogram_transmissivity, plot_spacial_transmissivity

target_well, rad = Verify()
radius = int(rad) #meters
candidate_wells = find_wells(target_well, radius)
pump_log_results = pump_log(candidate_wells)
thickness_data = aquifer_thickness(candidate_wells)
thickness_storativity_data = storativity_calculations(candidate_wells, thickness_data)
confirmed_wells = data_organization(candidate_wells, pump_log_results, thickness_storativity_data)
transmissivity_calculated = transmissivity_calculations(confirmed_wells)
HYDCONDUCT = conductivity_calculations(confirmed_wells, transmissivity_calculated)
plot_histogram_transmissivity(transmissivity_calculated)
plot_spacial_transmissivity(target_well, radius, confirmed_wells, transmissivity_calculated)
