"""
A function to calculate and determine the number of wells in CWI that 
match a given set of parameters.

-------------
PreRequisites:
    DataLocation.py is required for execution.
    
-------------
Author: Jonny Full

Version: 5/20/2020
"""

import arcpy
import numpy as np
import sys
import time
from DataLocation import allwells, CWIPL, CWIST
from scipy import spatial
#from Verify import strID

def findWells():
    strID = str(593596) #remove        
    with arcpy.da.SearchCursor(CWIST , ["WELLID"], "WELLID = " + strID) as cursor:
        for row in cursor:   
            break
        else:
            print("Well ID not found.")
            sys.exit()  #Terminates the function
            
    # Process: Join Field (Join Field) 
    allwells_2_ = arcpy.AddJoin_management(allwells, "RELATEID", CWIPL, "RELATEID", "KEEP_COMMON")[0]
    print("Well 2 done")
    
    # Process: Join Field (2) (Join Field) 
    allwells_3_ = arcpy.AddJoin_management(allwells_2_, "RELATEID",CWIST, "RELATEID", "KEEP_COMMON")[0]
    print("Well 3 Done")

    well_data = []
    
    well_data = arcpy.da.SearchCursor(allwells_3_, ["allwells.SHAPE","C5ST.WELLID"], "WELLID = " + strID)
    
    
    
    xy = np.array([[well[0][0], well[0][1]] for well in well_data])
    tree = spatial.cKDTree(xy[:, 0:1])
    #xtarget, ytarget =  arcpy.da.SearchCursor(allwells_3_, ["UTME", "UTMN", "C5ST.WELLID"], "WELLID = " + ID)
    
    
    query = tree.query_ball_point(xy, 5)
    print(query)











