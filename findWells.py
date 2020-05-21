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
import sys
import time
from DataLocation import allwells, CWIPL, CWIST

def Trees():
    start_time = time.time()
    
    ID = 593596 #Just using for simplicity
    ID = str(593596)
    #ID = input("Please provide a Well ID number: ")
    #IDint = int(ID)
    with arcpy.da.SearchCursor(CWIPL , ["WELLID"], "WELLID = " + ID) as cursor:
        for row in cursor:   
            break
        else:
           print("Well ID not found.")
           sys.exit()  #Terminates the function
            
    with arcpy.da.SearchCursor(CWIST , ["WELLID"], "WELLID = " + ID) as cursor:
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
    
    with arcpy.da.SearchCursor(allwells_3_, ["C5ST.WELLID"], "WELLID = " + ID) as cursor:
        for rows in cursor:
            well_data.append(rows)

    return well_data



Trees()
            