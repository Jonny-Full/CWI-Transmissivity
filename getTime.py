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
import Verify
from DataLocation import CWIPL

def Time():
     strID = str(593596)
     T = []
     #ID = Verify.strID #WILL NEED TO CHANGE THIS WHEN YOU BRING BACK THE input
     with arcpy.da.SearchCursor(CWIPL , ["DURATION", "WELLID"], "WELLID = " + strID) as cursor:
         for row in cursor:
             if cursor[0] != None and cursor[0] > 0:
                 T = cursor[0]/24 
                 print(T)
             elif cursor[0] != None and cursor[0] <= 0 :
                 T = 0
                 print("Time is Zero")
             else:
                 T = 0
                 print("Time Rate is Null")
                 
     return T
    

