
"""
function analyzeWells:
    This function calculates Transmissivity and performs statistical analysis
    of a series of water wells.
    
-------------------------------------------------------------------------------
Notes:
    -This file requires Data Location, findWells, Transmissivity, and Verify to execute
    
    

@author: Jonny Full
Version: 5/22/2020
-------------------------------------------------------------------------------
"""

from Verify import Verify
from findWells import findWells
import numpy as np
from Transmissivity import Calc
import time

start_time = time.time()
RADIUS = 1000 #meters
ID = Verify()
selectedWells = findWells(ID, RADIUS)
RID = [i[2] for i in selectedWells]

TSIV = Calc(RID)
print(time.time() - start_time)
