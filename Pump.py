# -*- coding: utf-8 -*-
"""
This is a helper function for Transmissivity that retrieves the pump rate
from the CWI data.

Notes:
    This function requires Data Location and Verify to run properly.
    
Author: Jonny Full
Version: 5/26/2020
"""

#COMPLETED
import arcpy
from DataLocation import CWIPL
def Pump(RID):
    
    FLOW = []
    for row in RID:
        with arcpy.da.SearchCursor(CWIPL , ["FLOW_RATE"], f"RELATEID = '{row}'") as cursor:
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
    return FLOW
    

