
"""
Function Buffer:
    This function does the following:
        1. Requests a well ID from the user
        2. Locates in Well in CWI
        3. Draws a buffer layer for analysis
        4. Selects all wells in this radus
@author: Jonny Full
Created on Mon May 18 10:06:07 2020

"""
from DataLocation import allwells, CWIPL, CWIST
import arcpy
import sys
import time


def Model():  # Model
  
    start_time = time.time()
    
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
    


    ID = 593596 #Just using for simplicity
    ID = str(593596)
    #ID = input("Please provide a Well ID number: ")
    #IDint = int(ID)
    with arcpy.da.SearchCursor(CWIPL, ["WELLID"], "WELLID = " + ID) as cursor:
        for row in cursor:   
            break
        else:
           print("Well ID not found.")
           sys.exit()  #Terminates the function
            
    with arcpy.da.SearchCursor(CWIST, ["WELLID"], "WELLID = " + ID) as cursor:
        for row in cursor:   
            break
        else:
            print("Well ID not found.")
            sys.exit()  #Terminates the function
    
    
    # Process: Join Field (Join Field) 
    allwells_2_ = arcpy.AddJoin_management(allwells, "RELATEID", CWIPL, "RELATEID", "KEEP_COMMON")[0]
    print("Well 2 done")
    # Process: Join Field (2) (Join Field) 
    allwells_3_ = arcpy.AddJoin_management(allwells_2_, "RELATEID",CWIST, "RELATEID", "KEEP_COMMON")[0]
    print("Well 3 Done")
    
    # Process: Select Layer By Attribute (Select Layer By Attribute) 
    
    allwells_4_, Count = arcpy.SelectLayerByAttribute_management(allwells_3_, "NEW_SELECTION", "C5ST.WELLID = " + ID, "")
    print(Count)
    
    # Process: Select Layer By Location (Select Layer By Location) 
    allwells_5_, Output_Layer_Names, Count_2_ = arcpy.SelectLayerByLocation_management([allwells_4_], "WITHIN_A_DISTANCE", "", "5 Miles", "NEW_SELECTION", "NOT_INVERT")
    
    
    print(Count_2_)
    print("--- %s seconds ---" % (time.time() - start_time))
    
if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\JonnyA\Documents\ArcGIS\Projects\CWI_Current\CWI_Current.gdb", workspace=r"C:\Users\JonnyA\Documents\ArcGIS\Projects\CWI_Current\CWI_Current.gdb"):
        Model()
        

    
           
