# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the screen length
from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020

"""
#Needs code for Locate by Distance but will come back
import arcpy
import Verify
from DataLocation import allwells



def Screen():
     strID = str(593596)
     L = []
     #ID = Verify.strID #WILL NEED TO CHANGE THIS WHEN YOU BRING BACK THE input
     with arcpy.da.SearchCursor(allwells , ["CASE_DEPTH","DEPTH_DRLL", "WELLID"], "WELLID = " + strID) as cursor:
         for row in cursor:
             if cursor[0] > 0 and cursor[0] != None:
                 if cursor[1] > 0 and cursor[1] != None:
                     L = cursor[1] - cursor[0]
                 else:
                     L = cursor[0]
             else:
                 L = 0
                 print("Screen Length is Zero")
                 
     return L
    




