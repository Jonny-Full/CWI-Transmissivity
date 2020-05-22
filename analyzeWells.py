
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


from Transmissivity import T
from findWells import Model
from Verify import Verify

#Verifies the Well ID input
Verify()

Model()

T()
