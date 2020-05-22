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
    ID = 593596 #Just using for simplicity
    strID = str(593596)
    #ID = input("Please provide a Well ID number: ")
    with arcpy.da.SearchCursor(CWIPL , ["WELLID"], "WELLID = " + strID) as cursor:
        for row in cursor:   
            break
        else:
           print("Well ID not found.")
           sys.exit()  #Terminates the function
            
    with arcpy.da.SearchCursor(CWIST , ["WELLID"], "WELLID = " + strID) as cursor:
        for row in cursor:   
            break
        else:
            print("Well ID not found.")
            sys.exit()  #Terminates the function
        print("Done")
