"""
This function is called Play.

It is purely for experimentation

"""

import arcpy
import math
import sys
arcpy.env.workspace=r"C:\Users\JonnyA\Desktop\Research\CWI_gdb_updated\water_well_information.gdb"

allwells = "allwells"
C5PL = "C5PL"
C5ST = "C5ST"

def Play():
    ID = input("Please enter Well ID: ")
    ID = int(ID)
    with arcpy.da.SearchCursor("C5ST", ["WELLID"], "WELLID = " + str(ID)) as cursor:
                
        for row in cursor:
            print("Well ID is valid")
            break
        else:
            print("Well ID not found.")
            sys.exit()  #Terminates the function
        

def Elastic():
    #discussion best apporach with Barnes

  
             