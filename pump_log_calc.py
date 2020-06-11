# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the pump rate
from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
Author: Jonny Full
Version: 6/10/2020
"""

#COMPLETED
import arcpy
from DataLocation import CWIPL


def pump_log(relate_id):
    flow = []
    time = []
    draw = []
    with arcpy.da.SearchCursor(CWIPL, ["FLOW_RATE", "DURATION", "START_MEAS", "PUMP_MEAS"], f"RELATEID in {tuple(relate_id)}") as cursor:
        for row in cursor:
            if row[0] is not None and row[0] > 0:
                rate = row[0]
                rate = rate*192.5 #convert from gal/min to ft^3/day
                flow.append(rate)
            elif row[0] is not None and row[0] <= 0 :
                rate = 0
                flow.append(rate)
            else:
                rate = 0
                flow.append(rate)
            #Calculates pump duration in days
            if row[1] is not None and row[1] > 0:
                dur = row[1]/24
                time.append(dur)
            elif row[1] is not None and row[1] <= 0:
                dur = 0
                time.append(dur)
            else:
                dur = 0
                time.append(dur)
            #Calculates Drawdown
            if row[2] is not None and row[2] > 0:
                if row[3] is not None and row[3] > 0:
                    down = row[3] - row[2]
                    draw.append(down)
                else:
                    down = row[2]
                    draw.append(down)
            else:
                down = row[3]
                draw.append(down)
    return flow, time, draw
