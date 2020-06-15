"""
This is a helper function for Transmissivity that retrieves the stroativity 
of aquifers from Justin Blum's pump test spreadsheet. This spreadsheet is then
read and dumped into a .JSON file. This function only needs to be executed once
for the values to be organized.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 6/15/2020
"""

import arcpy
import json
from DataLocation import loc
#from findWells import selectedWells
def Store():

    inputExcel = loc
    sheetName = "data"
    memoryTable = "in_memory" + "\\" + "memoryTable"

    #Make sure the memory is empty
    arcpy.Delete_management(memoryTable)

    arcpy.ExcelToTable_conversion(inputExcel, memoryTable, sheetName )


    Storativity = {}
    fieldIndices = {}
    
    fields = ['RelateID', 'testS']
    for i,field in enumerate(fields):
        Storativity[field]=[]
        fieldIndices[i] = field
    
    with arcpy.da.SearchCursor(memoryTable, ['Relateid', 'testS']) as cursor:
        for row in cursor:
            for i in range(len(row)):
                if row[1] != 0 and row[1] != None:
                    Storativity[fieldIndices[i]].append(row[i])
    return Storativity


def create_json(Storativity):
    store_data = json.dumps(Storativity)
    outfile = open('storativity_data.json', 'w+')
    outfile.write(store_data)


Store()
create_json(Storativity)   