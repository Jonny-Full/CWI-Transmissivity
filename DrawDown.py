# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the drawdown
from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020
"""

import arcpy
from DataLocation import CWIPL

def DrawDown(RID):
     DRAW = []
     for row in RID:
         with arcpy.da.SearchCursor(CWIPL , ["START_MEAS","PUMP_MEAS"], f"RELATEID = '{row}'") as cursor:
             for row in cursor:
                 if cursor[0] != None and cursor[0] > 0:
                     if cursor[1] != None and cursor[1] > 0:
                         s = cursor[1] - cursor[0]
                         DRAW.append(s)
                     else:
                         s = cursor[0]
                         DRAW.append(s)
                 else: 
                     s = cursor[1]
                     DRAW.append(s)
     return DRAW

