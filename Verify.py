# -*- coding: utf-8 -*-
"""
This file verifies that the Well ID is valid in CWI.
----------------------------------------------------
This file requires DataLocation to run

----------------------------------------------------

Author: Jonny Full
Version: 5/22/2020
"""
import arcpy
from DataLocation import CWIPL, CWIST
import sys

def Verify():
    ID = "0000593596"
    #ID = input("Please input a RELATEID number: ")
    with arcpy.da.SearchCursor(CWIPL , ["RELATEID"], f"RELATEID = '{ID}'") as cursor:
        for row in cursor:   
            break
        else:
           print("RELATEID not found.")
           sys.exit()  #Terminates the function
            
    with arcpy.da.SearchCursor(CWIST , ["RELATEID"], f"RELATEID = '{ID}'") as cursor:
        for row in cursor:   
            break
        else:
            print("RELATEID not found.")
            sys.exit()  #Terminates the function
    return ID
