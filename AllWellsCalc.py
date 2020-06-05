# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the screen length 
and casing radius from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020

"""
import arcpy
import numpy as np
from DataLocation import allwells
import time


def ALLWELLS_DATA(RID):
     start_time = time.time()
     LENGTH = []
     RADIUS = []
     for row in RID:
         with arcpy.da.SearchCursor(allwells, ["CASE_DEPTH","DEPTH_DRLL", "CASE_DIAM"], f"RELATEID = '{row}'") as cursor:
             for row in cursor:
                 
                 #Determines Screen Length
                 if cursor[0] != None and cursor[0] > 0:
                     if cursor[1] != None and cursor[1] > 0:
                         L = cursor[1] - cursor[0]
                         LENGTH.append(L)
                        
                     else:
                         L = cursor[0]
                         LENGTH.append(L)        
                 else:
                     L = 0
                     LENGTH.append(L)
                     
                 #Finds Casing Radius    
                 if cursor[2] != None and cursor[2] > 0:
                     RW = cursor[2]/24
                     RADIUS.append(RW)
                 else:
                     RW = 0
                     RADIUS.append(RW)  
                     
     print(time.time() - start_time)         
     return LENGTH, RADIUS



