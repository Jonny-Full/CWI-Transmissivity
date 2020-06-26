# -*- coding: utf-8 -*-
"""
The functions below retrieve data from the allwells and C5PL table and organize
them into one table for analysis.

Functions
---------
        findWells

Notes:
    This function requires Data Location and Verify to run properly.
Author: Jonny Full
Version: 6/25/2020
"""

import arcpy
import numpy as np
from scipy import spatial
from data_location import allwells, CWIPL

def find_wells(target_well, RADIUS):
    """ Use the target well input by the user to find all wells within a given 
    distance of the target well.
    
    Retrieves data on all wells that exist within the distance 'RADIUS' and
    draw water from the same 'AQUIFER' as the target well. This function
    does not include any wells that do not have any of the following parameters.
    
    Parameters
    ----------
    target_well: string
        The RELATEID of the well input by the user in Verify.
        Example : '0000123456'
        
    RADIUS: int (meters)
        RADIUS represents a boundry condition for the scope of analysis. 
        Any wells used in future calculations fall within this distance of the
        target well. 
        Example: 10000 (meters)
        
    Returns
    -------
    candidate_wells: list
        candidate_wells is a list that contains the UTM easting and northing (int),
        Aquifer code (str), screen length (float), casing radius (float), 
        and Relate ID (str). All entries in this list are located within the 
        RADIUS of the targetwell and draw water from the same aquifer as 
        the target well. This list is sorted by ascending Relate ID number.

    """
    initial_well = []
    with arcpy.da.SearchCursor(allwells, ['UTME', 'UTMN', 'AQUIFER'],\
                               f"RELATEID = '{target_well}'") as cursor: 
        for row in cursor:
            initial_well.append(row) 
    data = [initial_well[0][0], initial_well[0][1]] #records UTM coordinates
    well_data = []
    field_names = [
        "UTME",
        "UTMN", 
        "AQUIFER",
        "CASE_DEPTH", 
        "DEPTH_DRLL",
        "CASE_DIAM", 
        "RELATEID"
        ]

    where_clause = (
        "(RELATEID is not NULL) AND "
        "(AQUIFER is not NULL) AND "
        "(UTME is not NULL) AND "
        "(UTMN is not NULL) AND "
        "(CASE_DEPTH is not NULL) AND "
        "(CASE_DEPTH > 0) AND "
        "(DEPTH_DRLL is not NULL) AND "
        "(DEPTH_DRLL > 0) AND "
        "(CASE_DIAM is not NULL) AND "
        "(CASE_DIAM > 0) AND "
         f"AQUIFER = '{initial_well[0][2]}'"
        )
    with arcpy.da.SearchCursor(allwells, field_names , where_clause) as cursor:
        for row in cursor:
            utm_east = row[0]
            utm_north = row[1]
            aquifer = row[2]
            relationid = row[6]
            if row[3] is not None and row[4] is not None and row[5] is not None:
                if row[3] > 0 and row[4] > 0:    
                    screen = row[4] - row[3]
                elif row[4] is None or row[4] <= 0:
                    screen = row[3]
                else:
                    screen = 0
                #Finds Casing Radius
                if row[5] is not None and row[5] > 0:
                    radius_well = row[5]/24
                else:
                    radius_well = 0
            values = [utm_east, utm_north, aquifer, screen, radius_well, relationid]
            well_data.append(values)
    xy = np.array([[well[0], well[1]] for well in well_data])
    tree = spatial.cKDTree(xy)
    candidate_Well_index = tree.query_ball_point(data, RADIUS) #finds wells inside the boundary condition
    candidateWells = []
    for i in candidate_Well_index:
        candidateWells.append(well_data[i])
    candidateWells.sort(key = lambda x: x[5]) #sorts by ascending RELATEID number   
    return candidateWells

def pump_log(candidate_wells):
    
    pump_log_wells = []
    requested_values = [
            "FLOW_RATE",
            "DURATION", 
            "START_MEAS", 
            "PUMP_MEAS", 
            "RELATEID"
            ]
    
    where_clause = (
        "(RELATEID is not NULL) AND "
        "(FLOW_RATE is not NULL) AND "
        "(FLOW_RATE > 0) AND "
        "(DURATION is not NULL) AND "
        "(DURATION > 0) AND"
        "(START_MEAS is not NULL) AND "
        "(START_MEAS > 0) AND "
        "(PUMP_MEAS is not NULL) AND "
        "(PUMP_MEAS > 0) AND "
         f"RELATEID in {tuple([i[5] for i in candidate_wells])}"
         )
    
    with arcpy.da.SearchCursor(CWIPL, requested_values, where_clause) as cursor:
        for row in cursor:
            relateid = row[4]
            if row[0] > 0:
                rate = row[0]
                rate = rate*192.5 #convert from gal/min to ft^3/day
            elif row[0] <= 0 :
                rate = 0
            else:
                rate = 0
            #Calculates pump duration in days
            if row[1] > 0:
                dur = row[1]/24
            elif row[1] <= 0:
                dur = 0
            else:
                dur = 0
            #Calculates Drawdown
            if row[2] > 0:
                if row[3] > 0:
                    down = row[3] - row[2]
                else:
                    down = row[2]
            else:
                down = row[3]
            value = [rate, dur, down, relateid]   
            pump_log_wells.append(value)
        pump_log_wells.sort(key = lambda x: x[3]) #sorts list by Relate ID number
    return pump_log_wells

def data_organization(candidate_wells, pump_log_results):
    confirmed_wells = []
    for item in pump_log_results:
        for row in candidate_wells:    
            if row[5] == item[3]:
                value = [row, item]
        confirmed_wells.append(value)
    return confirmed_wells

