# -*- coding: utf-8 -*-
"""The functions below retrieve data from the allwells and C5PL table and organize
them into one table for analysis.

Functions
---------
find_wells: Retrieves data regarding well location and well construction.
This function only selects wells within an input radial distance from the
target_well and draws water from the same aquifer as the target_well.

pump_log: Uses the wells retrieved from find_wells to select specific capacity
data from the CWI Pump Log table.

aquifer_thickness: Uses data from find_wells to select aquifer thickness data
from the CWI_Hydro table

storativity_calculations: Uses aquifer thickness and code to determine material
properties and determine the storage coefficent for every well observed.

data_organization: Combines the data retrieved from find_wells and pump_log.
This creates one large table where each entry is related by Relate ID.

Citations
---------
Batu
Aquifer Hydraulics: A Comprehensive Guide to Hydrogeologic Data Analysis
John Wiley & Sons, 1998, PG. 61

Author: Jonny Full
Version: 7/13/2020
"""
import numpy as np
from scipy import spatial
import arcpy
from data_location import allwells, CWIPL, THICKNESS

def find_wells(target_well, radius, error_bounds):
    """ Use the target well input by the user to find all wells within a given
    distance of the target well.

    Retrieves data on all wells that exist within the distance 'radius' and
    draw water from the same 'AQUIFER' as the target well. This function
    does not include any wells that do not have any of the following parameters.

    Parameters
    ----------
    target_well: int
        The WELLID of the well input by the user in Verify.
        Example : 123456

    radius: int (meters)
        RADIUS represents a boundry condition for the scope of analysis.
        Any wells used in future calculations fall within this distance of the
        target well.
        Example: 10000 (meters)
        
    error_bounds: int
        error_bounds represents the limit on the bounds used for the
        uncertainty surrounding the recorded values in the CWI database.

    Returns
    -------
    candidate_wells: list
        candidate_wells is a list that contains the UTM easting and northing (int),
        Aquifer code (str), screen length (float), casing radius (float),
        and Well ID (str). All entries in this list are located within the
        RADIUS of the targetwell and draw water from the same aquifer as
        the target well. This list is sorted by ascending Well ID number.

    Notes
    -----    
    The casing diameter value (inches) is converted to a radius and from inches
    to feet.

    """
    initial_well = []
    with arcpy.da.SearchCursor(allwells, ['UTME', 'UTMN', 'AQUIFER'],\
                               f"WELLID = {target_well}") as cursor:
        for row in cursor:
            initial_well.append(row)
    data = [initial_well[0][0], initial_well[0][1]] #records UTM coordinates
    well_data = []
    field_names = [
        "UTME",
        "UTMN",
        "AQUIFER",
        "CASE_DEPTH",
        "DEPTH_DRLL",
        "CASE_DIAM",
        "WELLID"
        ]

    where_clause = (
        "(WELLID is not NULL) AND "
        "(AQUIFER is not NULL) AND "
        "(UTME is not NULL) AND "
        "(UTMN is not NULL) AND "
        "(CASE_DEPTH is not NULL) AND "
        "(CASE_DEPTH > 0) AND "
        "(DEPTH_DRLL is not NULL) AND "
        "(DEPTH_DRLL > 0) AND "
        "(CASE_DIAM is not NULL) AND "
        "(CASE_DIAM > 0) AND "
        f"AQUIFER = '{initial_well[0][2]}'"
        )
    with arcpy.da.SearchCursor(allwells, field_names, where_clause) as cursor:
        for row in cursor:
            utm_east = row[0]
            utm_north = row[1]
            aquifer = row[2]
            well_id = row[6]
            #Calculates Screen Length
            screen_len = row[4] - row[3]
            #Calculates casing radius
            radius_well = row[5]/24 #converts well diameter(inches) to well radius in feet
            if screen_len < 0: #filters out negative values
                continue
            values = [utm_east, utm_north, aquifer, screen_len,\
                      radius_well, well_id]
            well_data.append(values)
    xy = np.array([[well[0], well[1]] for well in well_data])
    tree = spatial.cKDTree(xy)
    #finds wells inside the boundary condition
    candidate_well_index = tree.query_ball_point(data, radius)
    candidate_wells = []
    for i in candidate_well_index:
        candidate_wells.append(well_data[i])
    candidate_wells.sort(key=lambda x: x[5])#sorts by ascending WELLID number
    return candidate_wells

def pump_log(candidate_wells, error_bounds):

    """Uses candidate_wells to retrieve data from the CWI Pump Log attribute
       table.

    Retrieves specific capcity test data from the CWI Pump Log table. In order
    for a well to be considered, it must have the same Relate ID as one or
    more entries in candidate wells. This function retrieves data regarding
    pump rate, duration of the specific capacity test, Static Water Level, and
    Pumping Water Level (after the pumping has stopped). These are then recorded
    in a list for analysis.

    Parameters
    ----------
    candidate_wells: list
        candidate_wells is a list that contains the UTM easting and northing (int),
        Aquifer code (str), screen length (float), casing radius (float),
        and Relate ID (str). All entries in this list are located within the
        RADIUS of the targetwell and draw water from the same aquifer as
        the target well. This list is sorted by ascending Well ID number.
        
    error_bounds: int
        error_bounds represents the limit on the bounds used for the
        uncertainty surrounding the recorded values in the CWI database.

    Returns
    -------
    pump_log_wells: list
        pump_log_wells is a list that contains the Pump Rate (float),
        Duration (float), Drawdown (float), and Relate ID (str). All entries
        in this list must also exist in candidate_wells and all of their
        respective field must be greater than zero and not null. This list is
        sorted by ascending Well ID number.

    Notes
    -----

    The pump rate data is converted from gallons per minute [gpm] to cubic feet
    per day [ft^3/day].

    The test duration is converted from hours to days.

    """
    pump_log_wells = []
    requested_values = [
        "FLOW_RATE",
        "DURATION", 
        "START_MEAS", 
        "PUMP_MEAS", 
        "WELLID"
        ]

    where_clause = (
        "(WELLID is not NULL) AND "
        "(FLOW_RATE is not NULL) AND "
        "(FLOW_RATE > 0) AND "
        "(DURATION is not NULL) AND "
        "(DURATION > 0) AND"
        "(START_MEAS is not NULL) AND "
        "(START_MEAS > 0) AND "
        "(PUMP_MEAS is not NULL) AND "
        "(PUMP_MEAS > 0) AND "
        f"WELLID in {tuple([i[5] for i in candidate_wells])}"
        )

    with arcpy.da.SearchCursor(CWIPL, requested_values, where_clause) as cursor:
        for row in cursor:
            wellid = row[4]
            #Calculates pump rate
            pump_rate_min = row[0] - error_bounds
            pump_rate_max = row[0] + error_bounds
            rate_min = pump_rate_min*192.5 #converts from gal/min to ft^3/day
            rate = row[0]*192.5 #original data
            rate_max = pump_rate_max*192.5
            #Calculates pump duration in days
            dur = row[1]/24
            #Calculates Drawdown
            static_wl_min = row[2] - error_bounds
            static_wl_max = row[2] + error_bounds
            pump_wl_min = row[3] - error_bounds
            pump_wl_max = row[3] + error_bounds
            down_min = pump_wl_min - static_wl_max
            down = row[3] - row[2]
            down_max = pump_wl_max - static_wl_min
            if down_min <= 0: #filters out entries where drawdown less\ equals 0
                continue
            value = [rate_min, rate, rate_max, dur, down_min, down, down_max, wellid]
            pump_log_wells.append(value)
        pump_log_wells.sort(key=lambda x: x[7])#sorts list by Relate ID number
    return pump_log_wells


def aquifer_thickness(candidate_wells, error_bounds):
    """Uses the Well ID from candidate_wells to retrieve data about aquifer
    thickness.

    This function retrieves data regarding aquifer thickness from the CWI_HYDRO
    (THICKNESS) attribute table supplied by Rich Soule from the Minnesota
    Department of Health. The data in this table is queried using the Well ID
    values from candidate_wells. This data will then be returned to analyize_wells
    and then appended to the confirmed_wells table for analysis.

    Parameters
    ----------
    candidate_wells: list
        candidate_wells is a list that contains the UTM easting and northing (int),
        Aquifer code (str), screen length (float), casing radius (float),
        and Relate ID (str). All entries in this list are located within the
        RADIUS of the targetwell and draw water from the same aquifer as
        the target well. This list is sorted by ascending Well ID number.
        
    error_bounds: int
        error_bounds represents the limit on the bounds used for the
        uncertainty surrounding the recorded values in the CWI database.

    Returns
    -------
    thickness_aquired: list
        A list of Well ID and aquifer thickness values (float).
    """
    thickness_aquired = []
    requested_values = [
        "AQ_THICK",
        "WELLID"
        ]
    where_clause = (
        "(WELLID is not NULL) AND "
        "(AQ_THICK is not NULL) AND "
        "(AQ_THICK > 0) AND "
        f"WELLID in {tuple([i[5] for i in candidate_wells])}"
        )
    with arcpy.da.SearchCursor(THICKNESS, requested_values, where_clause) as cursor:
        for row in cursor:
            thickness_min = row[0] - error_bounds
            thickness_values = row[0]
            thickness_max = row[0] + error_bounds
            wellid = row[1]
            if thickness_min <= 0 or thickness_values <= 0:
                thickness_min = 1
                thickness_values = 1
            info = [thickness_min, thickness_values, thickness_max, wellid]
            thickness_aquired.append(info)
    return thickness_aquired

def storativity_calculations(candidate_wells, thickness_data):
    """This function uses the aquifer thickness data to calculate the storage
    coefficient for each well.

    This function uses the data retrieved from aquifer_thickness to determine
    the storage coeffient of each individual well. These calculations are based
    on the following equation:

    S = Ss * b

    where S [-] is the storage coefficent, Ss [ft^-1] is the specific storage,
    and b [ft] is the aquifer thickness. Ss values are a material based
    property and have been approximated (Batu pg.61). This function uses a range
    of values to determine a range of storage values for each observed well.

    Parameters
    ----------
    candidate_wells: list
        candidate_wells is a list that contains the UTM easting and northing (int),
        Aquifer code (str), screen length (float), casing radius (float),
        and Relate ID (str). All entries in this list are located within the
        RADIUS of the targetwell and draw water from the same aquifer as
        the target well. This list is sorted by ascending Well ID number.

    thickness_aquired: list
        A list of Well ID (long) and aquifer thickness values (float).

    Returns
    -------
    thickness_storativity_data: list
        thickness_storativity_data is a list that contains the aquifer thickness
        (float), miniumum storage coefficent (float), maximum storage
        coefficent (float), and Well ID (int). This list is sorted by acsending
        Well ID.

    """
    #Will approximate for more aquifer codes over time
    thickness_storativity_data = []
    dense_sands = ('CJ**', 'CT**', 'OS**', 'CW**', 'CM**', 'CE**', 'MTPL', \
                   'KR**', 'PMFL', 'PMHF', 'PMHN')
    sand_gravel = ('QB**', 'QU**', 'QW**')
    fissured_rock = ('OP**', 'PA**', 'PC**', 'PE**')
    
    if candidate_wells[0][2] in dense_sands:
        Ss_max = 6.2*10**-5 #dense sands
        Ss_min = 3.9*10**-5
    elif candidate_wells[0][2] in sand_gravel:
        Ss_max = 3.1*10**-5 #dense sands and gravels
        Ss_min = 1.5*10**-5
    elif candidate_wells[0][2] in fissured_rock:
        Ss_max = 2.1*10**-5 #fizzured rock
        Ss_min = 1*10**-6
    else:
        Ss_max = 6.2*10**-5 #dense sands
        Ss_min = 3.9*10**-5

    for row in thickness_data:
        well_id = row[3]
        b_min = row[0]
        b = row[1]
        b_max = row[2]
        S_max = Ss_max * b
        S_min = Ss_min * b
        data = [b_min, b, b_max, S_min, S_max, well_id]
        thickness_storativity_data.append(data)
        thickness_storativity_data.sort(key=lambda x: x[5]) #sorts list by Well ID number
    return thickness_storativity_data


def data_organization(candidate_wells, pump_log_results, thickness_storativity_data):
    """This function organizes the candidate_wells and the pump_log_results
    lists into one large data set.

    This function creates one large data set that relates the candidate_wells
    and pump_log_results lists into one large list that is connected by
    Relate ID. This function filters out entries that do not exist only one
    of the two tables. The function also includes entries that have multiple
    entries in either table.

    Parameters
    ----------
    candidate_wells: list
        candidate_wells is a list that contains the UTM easting and northing (int),
        Aquifer code (str), screen length (float), casing radius (float),
        and Relate ID (str). All entries in this list are located within the
        RADIUS of the targetwell and draw water from the same aquifer as
        the target well. This list is sorted by ascending Relate ID number.

    pump_log_results: list
        pump_log_wells is a list that contains the Pump Rate (float),
        Duration (float), Drawdown (float), and Relate ID (str). All entries
        in this list must also exist in candidate_wells and all of their
        respective field must be greater than zero and not null. This list is
        sorted by ascending Relate ID number.

    thickness_storativity_data: list
        thickness_storativity_data is a list that contains the aquifer thickness
        (float), miniumum storage coefficent (float), maximum storage
        coefficent (float), and Well ID (int). This list is sorted by acsending
        Well ID.

    Results
    -------
    confirmed_wells: list[list1, list2, list3]
        This is a list of all pertinant information required to plot the wells
        spacially and calculate transmissivity / hydraulic conductivity.

        list1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float),
                     Casing Radius (ft), Well ID (int)]

        list 2 = list[Pump Rate (float), Duration (float), Drawdown (float),
                      Well ID (int)]

        list 3 = list[aquifer thickness (float),
                      miniumum storage coefficent (float), maximum storage
                      coefficent (float), and Well ID (int)]
    """
    confirmed_wells = []
    for item in pump_log_results: #there are duplicate well IDs in this table
        for row in candidate_wells: # there are duplicate well IDs in this table
            if row[5] != item[7]:
                continue
            for data in thickness_storativity_data: #there are no duplicate well IDs
                if row[5] == item[7] == data[5]:
                    value = [row, item, data]
                    confirmed_wells.append(value)
    return confirmed_wells

#    # execute only if run as a script
#    find_wells(target_well, radius, error_bounds)
#    pump_log(candidate_wells, error_bounds)
#  aquifer_thickness(candidate_wells, error_bounds)
#    storativity_calculations(candidate_wells, thickness_data)
#    data_organization(candidate_wells, pump_log_results, thickness_storativity_data)