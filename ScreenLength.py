# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the screen length
from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020

"""
import arcpy
import numpy as np
from DataLocation import allwells
import time


def Screen(RID):
     start_time = time.time()
     LENGTH = []
     for row in RID:
         with arcpy.da.SearchCursor(allwells, ["CASE_DEPTH","DEPTH_DRLL"], f"RELATEID = '{row}'") as cursor:
             for row in cursor:
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
                     
     print(time.time() - start_time)         
     return LENGTH




