
"""
function analyzeWells:
    This function calculates Transmissivity and performs statistical analysis
    of a series of water wells.
-------------------------------------------------------------------------------
Notes:
    -This file requires Data Location, findWells, Transmissivity, and Verify to execute

@author: Jonny Full
Version: 6/10/2020
-------------------------------------------------------------------------------
"""
import time
from Verify import Verify
from findWells import findWells
from Transmissivity import calc
start_time = time.time()
RADIUS = 500 #meters
ID = Verify()
selected_wells = findWells(ID, RADIUS)
relate_id = [i[2] for i in selected_wells]

TSIV = calc(relate_id)
print(time.time() - start_time)
