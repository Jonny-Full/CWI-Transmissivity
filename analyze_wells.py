""" This is a driver function that calculates Transmissivity for an area
of wells in the state of Minnesota.

This function calculates Transmissivity and Hydraulic Conductivity at every well
in our system. Interval arithmetic is performed in conjunction with these
calculations to represent the uncertainties in the specific capacity data.
The program will prompt the user to input a WellID number and radial distance 
(in meters) to act as a boundary condition for the query. Transmissivity is 
being calculated with the Bradbury & Rothschild Method.

Notes
-----
    This file requires data_location, data_retrieve, Transmissivity,
    aquifer_values, Thickness, Transmissivity, and Verify to execute. See these
    files for clarification on their respective functions.

    The file paths in data_location must be changed to properly reference the
    data tables used by this function on the user's computer.

Author: Jonny Full
Version: 8/18/2020
-------------------------------------------------------------------------------
"""
import arcpy
import numpy as np
import pandas as pd
from Verify import Verify
from data_location import CWI_DATA
from Transmissivity import transmissivity_calculations, conductivity_calculations
from data_retrieve import find_wells, data_organization, pump_log,\
aquifer_thickness, storativity_calculations
from data_to_csv import calculated_data_to_csv
from plots import plot_histogram_transmissivity, plot_spacial_transmissivity,\
plot_spacial_conductivity, plot_spacial_thickness

"""
Analyze Wells should be used for GIS based work/tests.
Use runme.py for work in Spyder.
"""

target_well = arcpy.GetParameter(0)
radius = arcpy.GetParameter(1) #meters
error_bounds = arcpy.GetParameter(2) #feet
feature_class_name = arcpy.GetParameterAsText(3)
WORKSPACE = arcpy.GetParameterAsText(4)
target_coords = []
#target_well, rad, error_bounds = Verify()
#radius = int(rad) #remove once a full GIS program
#feature_class_name = 'Testing'
candidate_wells = find_wells(target_well, radius, error_bounds)

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
my_df, raw_csv_name = calculated_data_to_csv(transmissivity_calculated, conductivity_calculated,\
                           confirmed_wells, feature_class_name)

if feature_class_name is not None:
    # Delete the shape file if it already exists.
    shapefile = WORKSPACE + f"\{feature_class_name}"
    if arcpy.Exists(shapefile):
        arcpy.Delete_management(shapefile)
else:
    shapefile = WORKSPACE + r"\calculated_well_data" #currently broken
    if arcpy.Exists(shapefile):
        arcpy.Delete_management(shapefile)
print(shapefile)
arcpy.management.XYTableToPoint(raw_csv_name, shapefile, 'UTME', 'UTMN',\
                                coordinate_system = arcpy.SpatialReference(26915)) # NAD 83 UTM zone 15N (EPSG:26915).
"""
#plot_histogram_transmissivity(transmissivity_calculated)
#plot_spacial_transmissivity(target_well, radius, confirmed_wells,\
#                            transmissivity_calculated, target_coords)
#plot_spacial_conductivity(target_well, radius, confirmed_wells,\
#                          conductivity_calculated, target_coords)
#plot_spacial_thickness(target_well, radius, confirmed_wells, target_coords)
"""









    