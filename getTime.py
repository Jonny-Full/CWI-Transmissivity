# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the time
from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020
"""

#Needs code for Locate by Distance but will come back
import arcpy
from DataLocation import CWIPL
import time

def Time(RID):

     TIME = []
     for row in RID:
         with arcpy.da.SearchCursor(CWIPL , ["DURATION"], f"RELATEID = '{row}'") as cursor:
             for row in cursor:
                 if cursor[0] != None and cursor[0] > 0:
                     t = cursor[0]/24
                     TIME.append(t)
                 elif cursor[0] != None and cursor[0] <= 0 :
                     t = 0
                     TIME.append(row)   
                 else:
                     t = 0
                     TIME.append(t)   
          
     return TIME
    

