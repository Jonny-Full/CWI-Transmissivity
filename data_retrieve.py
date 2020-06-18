# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves data from the 
C5PL table and allwells table.

Notes:
    This function requires Data Location and Verify to run properly.
Author: Jonny Full
Version: 6/18/2020
"""

#COMPLETED
import arcpy
from DataLocation import allwells, CWIPL


def pump_log(candidate_wells):
    pump_results = []
    with arcpy.da.SearchCursor(CWIPL, ["FLOW_RATE", "DURATION", "START_MEAS", "PUMP_MEAS", "RELATEID"],\
                               f"RELATEID in {tuple([i[3] for i in candidate_wells])}") as cursor:
        for row in cursor:
            relateid = row[4]
            if row[0] is not None and row[0] > 0:
                rate = row[0]
                rate = rate*192.5 #convert from gal/min to ft^3/day
            elif row[0] is not None and row[0] <= 0 :
                rate = 0
            else:
                rate = 0
            #Calculates pump duration in days
            if row[1] is not None and row[1] > 0:
                dur = row[1]/24
            elif row[1] is not None and row[1] <= 0:
                dur = 0
            else:
                dur = 0
            #Calculates Drawdown
            if row[2] is not None and row[2] > 0:
                if row[3] is not None and row[3] > 0:
                    down = row[3] - row[2]
                else:
                    down = row[2]
            else:
                down = row[3]
            value = rate, dur, down, relateid    
            pump_results.append(value)
    return pump_results

def allwells_data(pump_log_results):
    confirmed_wells = []
    with arcpy.da.SearchCursor(allwells, ["CASE_DEPTH", "DEPTH_DRLL", "CASE_DIAM", "UTME", "UTMN", "RELATEID"],\
                               f"RELATEID in {tuple([j[3] for j in pump_log_results])}") as cursor:
        for row in cursor:
            utm_east = row[3]
            utm_north = row[4]
            relationid = row[5]
            #Determines Screen Length
            if row[0] is not None and row[0] > 0 and row[1] is not None and row[1] > 0:
                screen = row[1] - row[0]
            elif row[1] is None or row[1] <= 0:
                screen = row[0]
            else:
                screen = 0
            #Finds Casing Radius
            if row[2] is not None and row[2] > 0:
                radius_well = row[2]/24
            else:
                radius_well = 0
            data = (screen, radius_well, utm_east, utm_north, relationid)
            confirmed_wells.append(data)
    return confirmed_wells
