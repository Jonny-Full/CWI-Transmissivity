"""
A function to calculate and determine the number of wells in CWI that 
match a given set of parameters.

-------------
PreRequisites:
    DataLocation.py is required for execution.
    
-------------
Author: Jonny Full

Version: 6/16/2020
"""

import arcpy
import numpy as np
from DataLocation import allwells
from scipy import spatial



def findWells(ID, RADIUS):
      
    targetWell = []        
    with arcpy.da.SearchCursor(allwells, ['UTME', 'UTMN', 'AQUIFER'], f"RELATEID = '{ID}'") as cursor: 
        for row in cursor:
            targetWell.append(row) #redefine targetwell
    data = [targetWell[0][0], targetWell[0][1]]
    well_data = []
    with arcpy.da.SearchCursor(allwells, ["UTME", "UTMN", "AQUIFER","CASE_DEPTH", "DEPTH_DRLL", "CASE_DIAM", "RELATEID"], f"AQUIFER = '{targetWell[0][2]}'") as cursor:
        for row in cursor:
            utm_east = row[0]
            utm_north = row[1]
            aquifer = row[2]
            relationid = row[6]            
            if row[3] is not None and row[3] > 0 and row[4] is not None and row[4] > 0:
                screen = row[4] - row[3]
            elif row[4] is None or row[4] <= 0:
                screen = row[3]
            else:
                screen = 0
            #Finds Casing Radius
            if row[5] is not None and row[5] > 0:
                radius_well = row[5]/24
            else:
                radius_well = 0
            values = (utm_east, utm_north, aquifer, screen, radius_well, relationid)
            well_data.append(values)
    xy = np.array([[well[0], well[1]] for well in well_data])

    tree = spatial.cKDTree(xy)
    
    candidate_Well_index = tree.query_ball_point(data, RADIUS)
    candidateWells = []
    for i in candidate_Well_index:
        candidateWells.append(well_data[i])
    return candidateWells
            
