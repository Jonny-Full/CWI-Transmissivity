"""
This is a helper function for Transmissivity that retrieves the stroativity 
of aquifers from Justin Blum's pump test spreadsheet.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020
"""

import arcpy
from DataLocation import loc1
#from findWells import selectedWells
import xlrd


def Store():

    inputExcel = loc1
    sheetName = "data"
    memoryTable = "in_memory" + "\\" + "memoryTable"

    #Make sure the memory is empty
    arcpy.Delete_management(memoryTable)

    arcpy.ExcelToTable_conversion(inputExcel, memoryTable,sheetName )


    d = {}
    fieldIndices = {}

    fields = arcpy.ListFields(memoryTable)
    for i,field in enumerate(fields):
        d[field.name]=[]
        fieldIndices[i] = field.name
        print(field.name)

    with arcpy.da.SearchCursor(memoryTable, ['Relateid', 'testS']) as cursor:
        for row in cursor:
            for i in range(len(row)):
                if row[1] != 0 and row[1] != None:
                    d[fieldIndices[i]].append(row[i])
                    


    print(d) #come back to





Store()
  
"""


def StoreNThick():
     strID = str(148173)
     S = []
     b = []
     
     #ID = Verify.strID #WILL NEED TO CHANGE THIS WHEN YOU BRING BACK THE input
     with arcpy.da.SearchCursor(allwells , ["COUNTY_C", "WELLID"], "WELLID = " + selectedWells) as cursor:
         for row in cursor:
             if cursor[0] == "01" and cursor[0] != None:
                 
             elif cursor[0] == "02" and cursor[0] != None:
                 
             elif cursor[0] == "03" and cursor[0] != None:
                
             elif cursor[0] == "04" and cursor[0] != None:

             elif cursor[0] == "05" and cursor[0] != None:
        
             elif cursor[0] == "06" and cursor[0] != None:

             elif cursor[0] == "07" and cursor[0] != None:

             elif cursor[0] == "08" and cursor[0] != None:
                 
             elif cursor[0] == "09" and cursor[0] != None:
                 
             elif cursor[0] == "10" and cursor[0] != None:
                 
             elif cursor[0] == "11" and cursor[0] != None:
                 
             elif cursor[0] == "12" and cursor[0] != None:
                 
             elif cursor[0] == "13" and cursor[0] != None:
                 
             elif cursor[0] == "14" and cursor[0] != None:
                 
             elif cursor[0] == "15" and cursor[0] != None:
                 
             elif cursor[0] == "16" and cursor[0] != None:
                 
             elif cursor[0] == "17" and cursor[0] != None:
                 
             elif cursor[0] == "18" and cursor[0] != None:
                 
             elif cursor[0] == "19" and cursor[0] != None:
                 
             elif cursor[0] == "20" and cursor[0] != None:
                 
             elif cursor[0] == "21" and cursor[0] != None:
                 
             elif cursor[0] == "22" and cursor[0] != None:
                 
             elif cursor[0] == "23" and cursor[0] != None:
                 
             elif cursor[0] == "24" and cursor[0] != None:
                 
             elif cursor[0] == "25" and cursor[0] != None:
                 
             elif cursor[0] == "26" and cursor[0] != None:
                 
             elif cursor[0] == "27" and cursor[0] != None:
                 
             elif cursor[0] == "28" and cursor[0] != None:
                 
             elif cursor[0] == "29" and cursor[0] != None:

             elif cursor[0] == "30" and cursor[0] != None:
                 
             elif cursor[0] == "31" and cursor[0] != None:
                 
             elif cursor[0] == "32" and cursor[0] != None:
                 
             elif cursor[0] == "33" and cursor[0] != None:
                 
             elif cursor[0] == "34" and cursor[0] != None:
                 
             elif cursor[0] == "35" and cursor[0] != None:
                 
             elif cursor[0] == "36" and cursor[0] != None:
                 
             elif cursor[0] == "37" and cursor[0] != None:
                 
             elif cursor[0] == "38" and cursor[0] != None:
                 
             elif cursor[0] == "39" and cursor[0] != None:
                 
             elif cursor[0] == "40" and cursor[0] != None:
                 
             elif cursor[0] == "41" and cursor[0] != None:
                 
             elif cursor[0] == "42" and cursor[0] != None:
                 
             elif cursor[0] == "43" and cursor[0] != None:
                 
             elif cursor[0] == "44" and cursor[0] != None:
                 
             elif cursor[0] == "45" and cursor[0] != None:
                 
             elif cursor[0] == "46" and cursor[0] != None:
                 
             elif cursor[0] == "47" and cursor[0] != None:
                 
             elif cursor[0] == "48" and cursor[0] != None:
                 
             elif cursor[0] == "49" and cursor[0] != None:
                 
             elif cursor[0] == "50" and cursor[0] != None:
                 
             elif cursor[0] == "51" and cursor[0] != None:
                 
             elif cursor[0] == "52" and cursor[0] != None:
                 
             elif cursor[0] == "53" and cursor[0] != None:
                 
             elif cursor[0] == "54" and cursor[0] != None:
                 
             elif cursor[0] == "55" and cursor[0] != None:
                 
             elif cursor[0] == "56" and cursor[0] != None:
                 
             elif cursor[0] == "57" and cursor[0] != None:
                 
             elif cursor[0] == "58" and cursor[0] != None:
                 
             elif cursor[0] == "59" and cursor[0] != None:
                 
             elif cursor[0] == "60" and cursor[0] != None:
                 
             elif cursor[0] == "61" and cursor[0] != None:
                 
             elif cursor[0] == "62" and cursor[0] != None:
                 
             elif cursor[0] == "63" and cursor[0] != None:
                 
             elif cursor[0] == "64" and cursor[0] != None:
                 
             elif cursor[0] == "65" and cursor[0] != None:
                 
             elif cursor[0] == "66" and cursor[0] != None:
                 
             elif cursor[0] == "67" and cursor[0] != None:
                 
             elif cursor[0] == "68" and cursor[0] != None:
                 
             elif cursor[0] == "69" and cursor[0] != None:
                 
             elif cursor[0] == "70" and cursor[0] != None:
                 
             elif cursor[0] == "71" and cursor[0] != None:
                 
             elif cursor[0] == "72" and cursor[0] != None:
                 
             elif cursor[0] == "73" and cursor[0] != None:
                 
             elif cursor[0] == "74" and cursor[0] != None:
                 
             elif cursor[0] == "75" and cursor[0] != None:
                 
             elif cursor[0] == "76" and cursor[0] != None:
                 
             elif cursor[0] == "77" and cursor[0] != None:
                 
             elif cursor[0] == "78" and cursor[0] != None:
                 
             elif cursor[0] == "79" and cursor[0] != None:
                 
             elif cursor[0] == "80" and cursor[0] != None:
                 
             elif cursor[0] == "81" and cursor[0] != None:
                 
             elif cursor[0] == "82" and cursor[0] != None:
                 
             elif cursor[0] == "83" and cursor[0] != None:
                 
             elif cursor[0] == "84" and cursor[0] != None:
                 
             elif cursor[0] == "85" and cursor[0] != None:
                 
             elif cursor[0] == "86" and cursor[0] != None:
                 
             elif cursor[0] == "87" and cursor[0] != None:
                 
             elif cursor[0] == "89" and cursor[0] != None:
                 
             elif cursor[0] == "91" and cursor[0] != None:
                 
             else:
                 print("Aquifer could not be identified.")
"""