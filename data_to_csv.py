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
#from analyze_wells import transmissivity_calculated, conductivity_calculated,\
#confirmed_wells, feature_class_name


def calculated_data_to_csv(transmissivity_calculated, conductivity_calculated,
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
    return my_df, raw_csv_name

def calculated_data_statistics_csv(my_df):
    updated_df = my_df.drop([0, 1, 8], axis = 1) #removes Well ID and UTMs from dataframe
    raw_csv_name_stats = f"{feature_class_name}_statistics.csv"
    header_list = ["T_min", 
                   "T_raw", 
                   "T_max", 
                   "K_min", 
                   "K_raw", 
                   "K_max"]
    index_list = {0:'Count', 
                  1:'Mean', 
                  2:'Standard Deviation', 
                  3:'Minimum',
                  4:'25%', 
                  5:'Median', 
                  6:'75%', 
                  7:'Maximum', 
                  8:'Logrithmic Mean',
                  9:'Logrithmic Standard Deviation'}
    log_mean = np.log10(updated_df.mean())
    log_std = np.log10(updated_df.std())
    useful_values = updated_df.describe()
    useful_values = useful_values.append(log_mean, ignore_index = True)
    useful_values = useful_values.append(log_std, ignore_index = True)
    useful_values = useful_values.rename(index = index_list)
    useful_values.to_csv(raw_csv_name_stats, header = header_list)
    
    return useful_values
    
#if __name__ == '__main__':
#    my_df, raw_csv_name = calculated_data_to_csv(transmissivity_calculated, 
#                                                 conductivity_calculated, 
#                                                 confirmed_wells, 
#                                                 feature_class_name)
#                           
#    useful_values = calculated_data_statistics_csv(my_df)
#    