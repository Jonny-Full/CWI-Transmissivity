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
import numpy as np
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
    fields = ['Well_ID', 'Storativity']
    for i, field in enumerate(fields):
        storativity[field] = []
        field_indices[i] = field
    with arcpy.da.SearchCursor(memory_table, ['WellID', 'testS']) as cursor:
        for row in cursor:
            for i in range(len(row)):
                if row[1] != 0 and row[1] is not None:
                    storativity[field_indices[i]].append(row[i])
    store_data = json.dumps(storativity)
    outfile = open('storativity_data.json', 'w')
    outfile.write(store_data)
    return storativity

def storetivity_data_check(loc):
    input_excel = loc
    sheet_name = "data"
    memory_table = "in_memory" + "\\" + "memoryTable"
    #Makes sure memory_table is empty
    arcpy.Delete_management(memory_table)
    arcpy.ExcelToTable_conversion(input_excel, memory_table, sheet_name)
    STORE = []
    with arcpy.da.SearchCursor(memory_table, ['testS', 'WellID']) as cursor:
        for row in cursor:
            if row[0] != 0 and row[0] is not None:
                STORE.append(row)
    return STORE

def opie(STORE):
    USEFUL = []
    with arcpy.da.SearchCursor(allwells, ['UTME', 'UTMN', 'AQUIFER', 'WELLID'], f"WELLID in {tuple([i[1] for i in STORE])}") as cursor:
        for row in cursor:
            USEFUL.append(row)
    return USEFUL

def storativity_calculations(candidate_wells, thickness_data):
    data_holder = []
    #uses maximum specific storage values from literature
    if candidate_wells[0][2] == "CJDN" or "CTCG" or "OSTP" or "QUUU" or "CTCW":
        Ss_max = 6.2*10**-5
    elif candidate_wells[0][2] == "QBAA" or "QWTA" or "CWOC":
        Ss_max = 3.1*10**-5
    elif candidate_wells[0][2] == "OPDC":
        Ss_max = 2.1*10**-5
    elif candidate_wells[0][2] == "CSLT":
        Ss_max = 3.9*10**-4
    elif candidate_wells[0][2] == "PEVT":
        Ss_max = 7.8*10**-4
    else:
        Ss_max = 1 #come back to approximation
    #for minimum specific storage values from literature
    if candidate_wells[0][2] == "CJDN" or "CTCG" or "OSTP" or "QUUU" or "CTCW":
        Ss_min = 3.9*10**-5
    elif candidate_wells[0][2] == "QBAA" or "QWTA" or "CWOC":
        Ss_min = 1.5*10**-5
    elif candidate_wells[0][2] == "OPDC":
        Ss_min = 1*10**-6
    elif candidate_wells[0][2] == "CSLT":
        Ss_min = 2.8*10**-4
    elif candidate_wells[0][2] == "PEVT":
        Ss_min = 3.9*10**-4
    else:
        Ss_min = 1 #come back to approximation
    for row in thickness_data:
        well_id = row[1]
        b = row[0]
        S_max = Ss_max * b
        S_min = Ss_min * b
        data = [b, S_min, S_max, well_id]
        data_holder.append(data)
        thickness_storativity_data = np.array(data_holder)
    thickness_storativity_data = thickness_storativity_data.tolist()
    return thickness_storativity_data