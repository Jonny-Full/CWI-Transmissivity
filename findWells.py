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
    with arcpy.da.SearchCursor(allwells, ['SHAPE', 'AQUIFER'], f"RELATEID = '{ID}'") as cursor: 
        
        for row in cursor:
            targetWell.append(row) #redefine targetwell
        targetWell = targetWell[0]
    well_data = []
    with arcpy.da.SearchCursor(allwells, ["SHAPE", "AQUIFER", "RELATEID"], f"AQUIFER = '{targetWell[1]}'") as cursor:
        for row in cursor:
            well_data.append(row)

    xy = np.array([[well[0][0], well[0][1]] for well in well_data])

    tree = spatial.cKDTree(xy)

    selectedWellindex = tree.query_ball_point(targetWell[0], RADIUS)
    selectedWells = []
    for i in selectedWellindex:
        selectedWells.append(well_data[i])
    return selectedWells
            


   
    



    
    
    
    
    
    
    
    