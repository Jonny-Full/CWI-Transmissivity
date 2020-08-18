"""
This file is called Play.

It is purely for experimentation

"""
import arcpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
arcpy.env.workspace=r"C:\Users\JonnyA\Desktop\Research\Test\water_well_information.gdb"
allwells = "allwells"
CWIPL = "C5PL"
CWIST = "C5ST"

#DO NOT DELETE THIS CODE!!!!!!!
"""
if "calculate_data" in WORKSPACE == False:
    arcpy.CreateFeatureclass_management(WORKSPACE, "calculate_data", 'POINT')
data_table = WORKSPACE + r'\calculate_data'
arcpy.AddField_management(data_table, 'UTME', 'DOUBLE') 
arcpy.AddField_management(data_table, 'UTMN', 'DOUBLE')
arcpy.AddField_management(data_table, 'T_MIN', 'DOUBLE')
arcpy.AddField_management(data_table, 'T_NORM', 'DOUBLE')
arcpy.AddField_management(data_table, 'T_MAX', 'DOUBLE')
arcpy.AddField_management(data_table, 'K_MIN', 'DOUBLE')
arcpy.AddField_management(data_table, 'K_NORM', 'DOUBLE')
arcpy.AddField_management(data_table, 'K_MAX', 'DOUBLE')
arcpy.AddField_management(data_table, 'WELLID', 'LONG')
edit_points = arcpy.InsertCursor(data_table, '*')
count = 1
#Try json or csv. Maybe pandas? Look at what GIS likes for data tables.
for row in range(len(well_id)): #data is not being appended. Issue with Object ID I think
    ID = well_id[row]
    UTME = utm_e[row]
    UTMN = utm_n[row]
    location = arcpy.Point(UTME, UTMN)
    T_min = t_min[row]
    T_med = t_med[row]
    T_max = t_max[row]
    K_min = k_min[row]
    K_med = k_med[row]
    K_max = k_max[row]
    data = [count, location, T_min, T_med, T_max, K_min, K_med, K_max, ID]
    edit_points.insertRow(data)
    count = count + 1
"""