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
import Verify
from DataLocation import allwells

def Radius():
     strID = str(593596)
     rw = []
     #ID = Verify.strID #WILL NEED TO CHANGE THIS WHEN YOU BRING BACK THE input
     with arcpy.da.SearchCursor(allwells , ["CASE_DIAM", "WELLID"], "WELLID = " + strID) as cursor:
         for row in cursor:
             if cursor[0] > 0 and cursor[0] != None:
                 rw = cursor[0]/24
             else:
                 rw = 0
                 print("Casing Radius is Zero")
                 
     return rw
    

