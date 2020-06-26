""" Retrieves Storativity values from previous pump tests.

This is a helper function for Transmissivity that retrieves the stroativity
of aquifers from Justin Blum's pump test spreadsheet. This spreadsheet is then
read and dumped into a .JSON file. This function only needs to be executed once
for the values to be organized. SUBJECT TO CHANGE

Notes:
    This function requires Data Location and Verify to run properly.

Author: Jonny Full
Version: 6/26/2020
"""
import json
import arcpy
from data_location import loc, allwells
#from findWells import selectedWells
def store_sheet(loc):
    """Retrieves pump test data from a spreadsheet and converts it to a json
       file for future use.
    
    This function reads Justin Blum's pump test spreadsheet. The Relate ID and
    any Storativity values that are greater than zero and not null are then
    recorded. These are then dumped into a .json file for future use.
    
    Parameters
    ----------
    loc: Excel Spreadsheet
    This spreadsheet has data from every pumping test performed in Minnesota from
    the last 57 years.
    
    Notes
    -----
    This function only needs to be executed once for the .json file to be created.
    The spreadsheet is not currently being updated so the data set will not change.
    """
    input_excel = loc
    sheet_name = "data"
    memory_table = "in_memory" + "\\" + "memoryTable"
    #Makes sure memory_table is empty
    arcpy.Delete_management(memory_table)
    arcpy.ExcelToTable_conversion(input_excel, memory_table, sheet_name)
    storativity = {}
    field_indices = {}
    fields = ['Relate_ID', 'Storativity']
    for i, field in enumerate(fields):
        storativity[field] = []
        field_indices[i] = field
    with arcpy.da.SearchCursor(memory_table, ['Relateid', 'testS']) as cursor:
        for row in cursor:
            for i in range(len(row)):
                if row[1] != 0 and row[1] is not None:
                    storativity[field_indices[i]].append(row[i])
    store_data = json.dumps(storativity)
    outfile = open('storativity_data.json', 'w')
    outfile.write(store_data)
    return storativity


def store_atmpt():
    #May remove just was experimenting
    input_excel = loc
    sheet_name = "data"
    memory_table = "in_memory" + "\\" + "memoryTable"
    #Make sure the memory is empty
    arcpy.Delete_management(memory_table)
    arcpy.ExcelToTable_conversion(input_excel, memory_table, sheet_name)
    table_join = arcpy.AddJoin_management(allwells, "RELATEID", memory_table, "Relateid")
    fieldlist = arcpy.ListFields(table_join)
    print(fieldlist)