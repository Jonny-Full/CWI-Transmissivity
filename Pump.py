# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the pump rate
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

def Pump():
     strID = str(593596)
     Q = []
     #ID = Verify.strID #WILL NEED TO CHANGE THIS WHEN YOU BRING BACK THE input
     with arcpy.da.SearchCursor(CWIPL , ["FLOW_RATE", "WELLID"], "WELLID = " + strID) as cursor:
         for row in cursor:
             if cursor[0] > 0 and cursor[0] != None:
                 Q = cursor[0]
                 print(Q)
             elif cursor[0] <= 0 and cursor[0] != None:
                 Q = 0
                 print("Flow Rate is Zero")
             else:
                 Q = 0
                 print("Flow Rate is Null")
                 
     return Q
    

