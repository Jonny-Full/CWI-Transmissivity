# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the casing radius
from the CWI data. The casing radius is being used as an assumption for 
radius of influence.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020
"""

#Needs code for Locate by Distance but will come back
import arcpy
from DataLocation import allwells

def Radius(RID):
    RADIUS= []
    for row in RID:
         with arcpy.da.SearchCursor(allwells , ["CASE_DIAM"], f"RELATEID = '{row}'") as cursor:
             for row in cursor:
                 if cursor[0] != None and cursor[0] > 0:
                     RW = cursor[0]/24
                     RADIUS.append(RW)
                 else:
                     RW = 0
                     RADIUS.append(RW)        
    return RADIUS
    

