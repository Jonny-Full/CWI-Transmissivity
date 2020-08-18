# -*- coding: utf-8 -*-
"""
runme.py is a variation of analyze_wells.py. runme.py does not require
the user to input a Well ID or radial distance (radius). Hence, this program
can be used for troubleshooting.

Author: Jonny Full
Version: 7/24/2020
"""
from Transmissivity import transmissivity_calculations, conductivity_calculations
from data_retrieve import find_wells, data_organization, pump_log,\
aquifer_thickness, storativity_calculations
from plots import *

"""
Analyze Wells should be used for GIS based work/tests.
Use runme.py for work in Spyder.
"""

def runme():
    target_coords = []
    target_well = '457883' #My family's well
    radius = 1000 #This makes the program run quickly but alter as you wish (meters)
    error_bounds = 5
    candidate_wells = find_wells(target_well, radius, error_bounds)
    
    """The loop below finds the target well's UTM coordinates. This allows the
    target well to have a unique aesthetic on the scatterplots (red square).
    """
    for row in candidate_wells: 
        if int(target_well) == row[5]:
            utm_e = row[0]
            utm_n = row[1]
            well_id = row[5]
            data = [utm_e, utm_n, well_id]
            target_coords.append(data)
            
    pump_log_results = pump_log(candidate_wells, error_bounds)
    thickness_data = aquifer_thickness(candidate_wells, error_bounds)
    thickness_storativity_data = storativity_calculations(candidate_wells, thickness_data)
    confirmed_wells = data_organization(candidate_wells, pump_log_results, thickness_storativity_data)
    transmissivity_calculated = transmissivity_calculations(confirmed_wells)
    conductivity_calculated = conductivity_calculations(confirmed_wells, transmissivity_calculated)
    """
    plot_histogram_transmissivity(transmissivity_calculated)
    plot_spacial_transmissivity(target_well, radius, confirmed_wells, transmissivity_calculated, target_coords)
    plot_spacial_conductivity(target_well, radius, confirmed_wells, conductivity_calculated, target_coords)
    """
if __name__ == '__main__':
    runme()