"""Verifies that the user input is valid in the CWI data.

This file asks the user to input a Well ID. The ID is then checked in the CWI
attribute tables to ensure that the Well ID exists. The user is then prompted
to input a radial distance. This distance is a boundary condition for the 
sample size.

Author: Jonny Full
Version: 6/24/2020
"""
import arcpy
from data_location import CWIPL, allwells
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
    with arcpy.da.SearchCursor(CWIPL , ["WELLID"], f"WELLID = {target_well}") as cursor:
        for row in cursor:   
            break
        else:
           print("Well ID not found.")
           sys.exit()  #Terminates the function
            
    with arcpy.da.SearchCursor(allwells , ["WELLID"], f"WELLID = {target_well}") as cursor:
        for row in cursor:   
            break
        else:
            print("Well ID not found.")
            sys.exit()  #Terminates the function
    rad = input('Please input the radius from the target well (in meters): ')
    error_bounds = int(input('Please enter the error bounds for your calculations(ft): '))
    return target_well, rad, error_bounds
