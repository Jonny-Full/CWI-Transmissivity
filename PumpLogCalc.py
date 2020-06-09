# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the pump rate
from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 6/8/2020
"""

#COMPLETED
import arcpy
from DataLocation import CWIPL
import time

def PumpLog(RID):
    start = time.time()
    FLOW = []
    TIME = []
    DRAW = []
    for item in RID:
         with arcpy.da.SearchCursor(CWIPL , ["FLOW_RATE", "DURATION","START_MEAS","PUMP_MEAS"],\
                                   f"RELATEID = '{item}'") as cursor:

             for row in cursor:
                 if cursor[0] > 0 and cursor[0] != None:
                    Q = cursor[0]
                    Q = Q*192.5 #convert from gal/min to ft^3/day
                    FLOW.append(Q)
                
                 elif cursor[0] <= 0 and cursor[0] != None:
                    Q = 0
                    FLOW.append(Q)
                
                 else:
                    Q = 0
                    FLOW.append(Q)
            
            #Calculates pump duration in days
                 if cursor[1] != None and cursor[1] > 0:
                     t = cursor[1]/24
                     TIME.append(t)
                 elif cursor[1] != None and cursor[1] <= 0 :
                     t = 0
                     TIME.append(t)   
                 else:
                     t = 0
                     TIME.append(t)
                 
                 #Calculates Drawdown
                 if cursor[2] != None and cursor[2] > 0:
                     
                    if cursor[3] != None and cursor[3] > 0:
                         s = cursor[3] - cursor[2]
                         DRAW.append(s)
                    else:
                         s = cursor[2]
                         DRAW.append(s)
                 else: 
                     s = cursor[3]
                     DRAW.append(s)

    return FLOW, TIME, DRAW


