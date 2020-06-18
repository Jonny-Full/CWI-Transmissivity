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
    with arcpy.da.SearchCursor(allwells, ["UTME", "UTMN", "AQUIFER", "RELATEID"], f"AQUIFER = '{targetWell[0][2]}'") as cursor:
        for row in cursor:
            well_data.append(row)

    xy = np.array([[well[0], well[1]] for well in well_data])

    tree = spatial.cKDTree(xy)
    
    candidate_Well_index = tree.query_ball_point(data, RADIUS)
    candidateWells = []
    for i in candidate_Well_index:
        candidateWells.append(well_data[i])
    return candidateWells
            


   
    



    
    
    
    
    
    
    
    