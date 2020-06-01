"""
A function to calculate and determine the number of wells in CWI that 
match a given set of parameters.

-------------
PreRequisites:
    DataLocation.py is required for execution.
    
-------------
Author: Jonny Full

Version: 5/29/2020
"""

import arcpy
import numpy as np
from DataLocation import allwells
from scipy import spatial
import time
#from Verify import strID

def findWells(strID, radius):
    start_time = time.time()
            
    targetWell = []        
    with arcpy.da.SearchCursor(allwells, ['SHAPE', 'AQUIFER'], f"RELATEID = '{strID}'") as cursor: 
        
        for row in cursor:
            targetWell.append(row) #redefine targetwell
        targetWell = targetWell[0]
    print(f'Search 1 Complete {time.time() - start_time}')        
    #with arcpy.da.SearchCursor(allwells_2_, ["allwells.SHAPE", "allwells.AQUIFER", "C5PL.WELLID"], f"allwells.AQUIFER = '{AQ}'") as cursor:   
    well_data = []
    with arcpy.da.SearchCursor(allwells, ["SHAPE", "AQUIFER", "RELATEID"], f"AQUIFER = '{targetWell[1]}'") as cursor:         
        for row in cursor:
            well_data.append(row)

    print(f'Search 2 Complete {time.time() - start_time} {len(well_data)}')    
    xy = np.array([[well[0][0], well[0][1]] for well in well_data])
    
    tree = spatial.cKDTree(xy)
    
    selectedWellindex = tree.query_ball_point(targetWell[0], radius) #I am stumped ask Barnes 
    selectedWells = []
    for i in selectedWellindex:
        selectedWells.append(well_data[i])
    
    print(f'Total Time {time.time() - start_time} {len(selectedWells)}')    
    return selectedWells
            



   
    
#selectedWells = findWells(strID, radius)

#Remove Aquifer()

def Aquifer():
    with arcpy.da.SearchCursor(allwells_3_, ["allwells.SHAPE", "AQUIFER", "C5PL.WELLID"], "WELLID = " + strID) as cursor:
    
        for row in cursor:
            if row[1] == AQ:
                well_data.append(row)
    
    
    
    
    
    
    
    