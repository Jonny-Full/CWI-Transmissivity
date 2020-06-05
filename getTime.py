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

def Time():

    if cursor[1] != None and cursor[1] > 0:
        t = cursor[1]/24
        TIME.append(t)
    elif cursor[1] != None and cursor[1] <= 0 :
        t = 0
        TIME.append(row)   
    else:
        t = 0
        TIME.append(t)   
          
    return TIME
    

