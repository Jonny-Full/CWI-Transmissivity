# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves data from the 
C5PL table and allwells table.

Notes:
    This function requires Data Location and Verify to run properly.
Author: Jonny Full
Version: 6/19/2020
"""

#COMPLETED
import arcpy
from DataLocation import allwells, CWIPL


def pump_log(candidate_wells):
    pump_results = []
    requested_values = ["FLOW_RATE", "DURATION", "START_MEAS", "PUMP_MEAS", "RELATEID"]
    where_clause = (
        "(RELATEID is not NULL) AND "
        "(FLOW_RATE is not NULL) AND "
        "(DURATION is not NULL) AND "
        "(START_MEAS is not NULL) AND "
        "(PUMP_MEAS is not NULL) AND "
         f"RELATEID in {tuple([i[5] for i in candidate_wells])}"
         )
    with arcpy.da.SearchCursor(CWIPL, requested_values, where_clause) as cursor:
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
        pump_results.sort(key = lambda x: x[3]) #sorts list by Relate ID number
    return pump_results

