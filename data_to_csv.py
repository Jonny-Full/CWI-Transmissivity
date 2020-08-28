# -*- coding: utf-8 -*-
"""
This module was created to hold any code that transforms our data into csv files.
This module has two functions:
    
calculated_data_to_csv: This function take the data from transmissivity
    calculated and conductivity_calculated and converts the data into a csv file
    so the user can easily interact with the data. This file will also be used
    to create a feature class.

Author: Jonny Full
Version: 8/28/2020
"""
import arcpy
import numpy as np
import pandas as pd

def calculated_data_to_csv(transmissivity_calculated, conductivity_calculated,\
                           confirmed_wells, feature_class_name):
    utm_e = [i[0][0] for i  in confirmed_wells]
    utm_n = [i[0][1] for i in confirmed_wells]
    np.set_printoptions(suppress=True) #removes scientific notation
    location = np.array([utm_e, utm_n])
    location = location.transpose()
    transmissivity_calculated = np.array(transmissivity_calculated)
    conductivity_calculated = np.array(conductivity_calculated)
    joined_data = np.concatenate((location, transmissivity_calculated, conductivity_calculated), axis = 1)
    my_df = pd.DataFrame(joined_data)
    header_list = ['UTME', 'UTMN', 'T_min', 'T_raw', 'T_max', 'K_min', 'K_raw', 'K_max', 'Well ID']
    raw_csv_name = f"{feature_class_name}.csv"
    my_df.to_csv(raw_csv_name, index = False, header = header_list)
    return raw_csv_name