# -*- coding: utf-8 -*-
"""
This module was created to hold any code that transforms our data into csv files.
This module has two functions:

Functions
-----------
    
calculated_data_to_csv: This function take the data from transmissivity
    calculated and conductivity_calculated and converts the data into a csv file
    so the user can easily interact with the data. This file will also be used
    to create a feature class.

calculated_data_statistics_csv: This function takes the .csv file created in
    calculated_data_to_csv and performes statistical analysis. This function
    then creates another .csv file for the user to interact with at their
    convienience.
    
Author: Jonny Full
Version: 9/31/2020
"""
import numpy as np
import pandas as pd



def calculated_data_to_csv(transmissivity_calculated, conductivity_calculated,
                           confirmed_wells, feature_class_name):
    """Converts the transmissivity, hydraulic conductivity, and well location
    data into a csv file.
    
    Parameters:
    -----------
    transmissivity_calculated: list[float]
        transmissivity_calculated represents the calculated Transmissivity for
        each row in confirmed_wells.
        
    conductivity_calculated: list[float]
        conductivity_calculated represents the calculated hydraulic conductivity
        for each row intransmissivity_calculated.
        
    confirmed_wells: list[[list1][list2]]
        This is a list of all pertinant information required to plot the wells
        spacially and calculate Transmissivity.

        list1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float),
                     Casing Radius (ft), Relate ID (str)]

        list 2 = list[Pump Rate (float), Duration (float), Drawdown (float),
                      Relate ID (str)]
        
    feature_class_name = string
        This is the name of the csv file. This is input by the user in GIS.
        
    Returns:
    --------
    my_df: pandas dataframe
        A dataframe containing the location, transmissivities, and
        hydraulic conductivities for every well in our neighborhood.
        
    raw_csv_name: string
        The name of the csv file created.
        
    Notes:
    --------
    This .csv file is dropped into the ArcGIS project in which they are running
    this script through.
    
    """
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

def calculated_data_statistics_csv(my_df, feature_class_name):
    """Uses the data in my_df to create another csv file with
    statistical analysis. Each column will have the following items calculated,
    Count, Mean, Standard Deviation, Minimum, 25% Percentile, Median,
    75% Percentile, Maximum, Logrithmic Mean, Logrithmic Standard Deviation.
    
    Parameters:
    -----------
    my_df: pandas dataframe
        A dataframe containing the location, transmissivities, and
        hydraulic conductivities for every well in our neighborhood.
            
    feature_class_name = string
        This is the name of the csv file. This is input by the user in GIS.
    
    Notes:
    ------
    This .csv file is dropped into the ArcGIS project in which they are running
    this script through.
    
    This .csv file also has the same primary name as the file created in 
    calculated_data_to_csv. However, this file has _statistics attached to its
    file name.
    """
    #remove Well ID and UTMs from dataframe
    updated_df = my_df.drop([0, 1, 8], axis = 1)
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
                  4:'25th Percentile',
                  5:'Median',
                  6:'75th Percentile',
                  7:'Maximum',
                  8:'Logrithmic Mean',
                  9:'Logrithmic Standard Deviation'}
    log_mean = np.log10(updated_df.mean())
    log_std = np.log10(updated_df.std())
    useful_values = updated_df.describe()
    useful_values = useful_values.append(log_mean, ignore_index = True)
    useful_values = useful_values.append(log_std, ignore_index = True)
    useful_values = useful_values.rename(index = index_list) #gives the index unique names
    useful_values.to_csv(raw_csv_name_stats, header = header_list)
        