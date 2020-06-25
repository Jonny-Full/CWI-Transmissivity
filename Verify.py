# -*- coding: utf-8 -*-
"""
This file verifies that the Well ID is valid in CWI.
----------------------------------------------------
This file requires DataLocation to run

----------------------------------------------------

Author: Jonny Full
Version: 6/24/2020
"""
import arcpy
from DataLocation import CWIPL, CWIST
import sys

def Verify():
    """ Requests the user to input a WellID number and sample area.
    
    This function asks the user to provide a valid WellID number and converts
    it to a Relate ID number. The function then verifies that the Relate ID
    data exists in the CWI data set. The user then inputs a length to determine
    the size of the area in which wells can be selected.
    
    Parameters
    ----------
    This function does not take any parameters.
    
    Returns
    -------
    target_well: str
    The Relate ID of the well input by the user.
    
    rad: int (meters)
    The maximum radiall distance from the target_well that can be considered for
    analysis. This value is in meters.
    
    """
    target_well = input("Please input a WellID number: ") #This is easier/ more simple for the user
    target_well = "0000" + target_well
    with arcpy.da.SearchCursor(CWIPL , ["RELATEID"], f"RELATEID = '{target_well}'") as cursor:
        for row in cursor:   
            break
        else:
           print("RELATEID not found.")
           sys.exit()  #Terminates the function
            
    with arcpy.da.SearchCursor(CWIST , ["RELATEID"], f"RELATEID = '{target_well}'") as cursor:
        for row in cursor:   
            break
        else:
            print("RELATEID not found.")
            sys.exit()  #Terminates the function
    rad = input('Please input the radius from the target well (in meters): ')
    return target_well, rad
