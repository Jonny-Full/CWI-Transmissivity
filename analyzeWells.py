
"""
function analyzeWells:
    This function calculates Transmissivity and performs statistical analysis
    of a series of water wells.
    
    

@author: Jonny Full
Created on Mon May 18 09:02:19 2020
-------------------------------------------------------------------------------
"""

import arcpy
import math
from scipy.optimize import fsolve
from Transmissivity import T
from Buffer import Model

Model()

T()
