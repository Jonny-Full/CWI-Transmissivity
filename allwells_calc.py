# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the screen length
and casing radius from the CWI data.

Notes:
This function requires Data Location and Verify to run properly.
Author: Jonny Full
Version: 6/16/2020

"""
import arcpy
from DataLocation import allwells

def allwells_data(relate_id):
    length = []
    radius = []
    with arcpy.da.SearchCursor(allwells, ["CASE_DEPTH", "DEPTH_DRLL", "CASE_DIAM"],\
                               f"RELATEID in {tuple(relate_id)}") as cursor:
        for row in cursor:
            #Determines Screen Length
            if row[0] is not None and row[0] > 0 and row[1] is not None and row[1] > 0:
                screen = row[1] - row[0]
                length.append(screen)
            elif row[1] is None or row[1] <= 0:
                screen = row[0]
                length.append(screen)
            else:
                screen = 0
                length.append(screen)
            #Finds Casing Radius
            if row[2] is not None and row[2] > 0:
                radius_well = row[2]/24
                radius.append(radius_well)
            else:
                radius_well = 0
                radius.append(radius_well)
    return length, radius
