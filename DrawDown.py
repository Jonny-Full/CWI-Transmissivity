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
import Verify
from DataLocation import CWIPL

def DrawDown():
     strID = str(593596)
     s = []
     #ID = Verify.strID #WILL NEED TO CHANGE THIS WHEN YOU BRING BACK THE input
     with arcpy.da.SearchCursor(CWIPL , ["START_MEAS","PUMP_MEAS" ,"WELLID"], "WELLID = " + strID) as cursor:
         for row in cursor:
             if cursor[0] > 0:
                 if cursor[1] != None and cursor[1] > 0:
                     s = cursor[1] - cursor[0]
                 else:
                     s = cursor[0]
             else:
                 s = cursor[1]
     return s
               
