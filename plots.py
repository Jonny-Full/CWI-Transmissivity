"""Creates plots of data using matplotlib

This is a file of helper functions that plots the data calculated from
Transmissivity.py as a histogram and scatter plot.

Functions
---------
plot_histogram_transmissivity:
    Creates a histogram of the natural logorithem of the calculated Transmissivities.
    
plot_spacial_transmissicity:
    Creates a scatter plot where each point is plotted at its UTM coordinates.
    Each point is colored baised on which decile its Transmissivity lies in.

Author: Jonny Full
Version: 6/26/2020
"""
import arcpy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from data_location import allwells, CWIPL, THICKNESS
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from matplotlib.backends.backend_pdf import PdfPages


def plot_histogram_transmissivity(transmissivity_calculated):
    """Plots the natural log of the transmissivity values
    
    Parameters
    ----------
    transmissivity_calculated: list
    A list of Transmissivities that were calculated from confirmed_wells. 
    The units are ft^2/day.
    
    Notes
    -----
    This function produces a histogram of the natural logoritem of the Transmissivity
    values. The histogram has 50 bars to represent a clear distribution.
    
    """
    plt.clf()
    plt.figure(1)
    plt.hist(np.log(transmissivity_calculated), bins=50, label = ['T_Min', 'T_Max'])
    plt.title('Transmissivity Distribution')
    plt.xlabel('ln(T)')
    plt.ylabel('Number of entries')
    plt.legend(['T_Min', 'T_Max'], loc = 'upper right')

    
def plot_spacial_transmissivity(target_well, radius, confirmed_wells, transmissivity_calculated, target_coords):
    """Plots the confirmed_wells geographical location and shows the 
    Transmissivity for each well.
    
    Parameters
    ----------
    ----------
    target_well: string
        The RELATEID of the well input by the user in Verify.
        Example : '0000123456'
        
    RADIUS: int (meters)
        RADIUS represents a boundry condition for the scope of analysis. 
        Any wells used in future calculations fall within this distance of the
        target well. 
        Example: 10000 (meters)
        
    confirmed_wells: list[[list1][list2]]
        This is a list of all pertinant information required to plot the wells
        spacially and calculate Transmissivity.
    
        list1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float), 
                     Casing Radius (ft), Relate ID (str)
        
        list 2 = list[Pump Rate (float), Duration (float), Drawdown (float), 
                     Relate ID (str)]
    
    transmissivity_calculated: list
        A list of Transmissivities that were calculated from confirmed_wells. 
        The units are ft^2/day.
    
    target_coords:list
        Contains the UTM coordinates of the original well input by the user.
        This data will be used to create a unique data point on the scatterplot
        to represent the location of the target well.
        
    Notes
    -----
    This function returnes a scatter plot. The axis will use the UTM Easting (x)
    and UTM Northing (y) on its axis. The plotted points will be color coded
    depending on the decile that their respective transmissivity fall into.
    """
    
    plt.figure(2)
    distribute_t = []
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    T = [i[0] for i in transmissivity_calculated]
    T_ln = []

    for row in T:
        data = np.log(row)
        T_ln.append(data)

    bounds = np.percentile(transmissivity_calculated, np.arange(0, 110, 10)) #calculates deciles
    #May not be necessary
    for row in T:
        #Ask Barnes so I understand the logic entirely
        decile = next(indx for indx, trans in enumerate(bounds) if trans > row)
        distribute_t.append(decile)
    plt.scatter(x, y, c = T_ln, s = 30, cmap='Blues', vmin = min(T_ln), vmax = max(T_ln))
    cbar = plt.colorbar()
    cbar.set_label('Natural Logaritum of Transmissivity', rotation = 270)
    sns.scatterplot([target_coords[0][0]], [target_coords[0][1]], color='red', marker = 's', edgecolor = 'k', s = 50, label = 'Target Well')
    plt.title(f"Transmissivity for Wells within {radius} meters of Well ID {target_well}")
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')
    plt.grid(True)
    
def plot_spacial_conductivity(target_well, radius, confirmed_wells, conductivity_calculated, target_coords):
    """Plots the confirmed_wells geographical location and shows the 
    Transmissivity for each well.
    
    Parameters
    ----------
    ----------
    target_well: string
        The RELATEID of the well input by the user in Verify.
        Example : '0000123456'
        
    RADIUS: int (meters)
        RADIUS represents a boundry condition for the scope of analysis. 
        Any wells used in future calculations fall within this distance of the
        target well. 
        Example: 10000 (meters)
        
    confirmed_wells: list[[list1][list2]]
        This is a list of all pertinant information required to plot the wells
        spacially and calculate Transmissivity.
    
        list1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float), 
                     Casing Radius (ft), Relate ID (str)
        
        list 2 = list[Pump Rate (float), Duration (float), Drawdown (float), 
                     Relate ID (str)]
    
    conductivity_calculated: list
        A list of hydralic conductivities that were calculated from confirmed_wells. 
        The units are ft/day.
    
    target_coords:list
        Contains the UTM coordinates of the original well input by the user.
        This data will be used to create a unique data point on the scatterplot
        to represent the location of the target well.
        
    Notes
    -----
    This function returnes a scatter plot. The axis will use the UTM Easting (x)
    and UTM Northing (y) on its axis. The plotted points will be color coded
    depending on the decile that their respective transmissivity fall into.
    """
    
    plt.figure(3)
    distribute_K = []
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    K = [i[0] for i in conductivity_calculated]
    K_ln = []

    for row in K:
        data = np.log(row)
        K_ln.append(data)
        
    bounds = np.percentile(conductivity_calculated, np.arange(0, 110, 10)) #calculates deciles
    for row in K:
        decile = next(indx for indx, trans in enumerate(bounds) if trans > row)
        distribute_K.append(decile)
    plt.scatter(x, y, c = K_ln, s = 30, cmap='Reds', vmin = min(K_ln), vmax = max(K_ln))
    cbar = plt.colorbar()
    cbar.set_label('Natural Logaritum of Transmissivity', rotation = 270)
    sns.scatterplot([target_coords[0][0]], [target_coords[0][1]], color='blue', marker = 's', edgecolor = 'k', s = 50, label = 'Target Well')
    plt.title(f"Transmissivity for Wells within {radius} meters of Well ID {target_well}")
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')
    plt.grid(True)
    
    
def Pump_Durations_Plots():
    """ Temporary file
    
    This file shows how common roundoff errors occur in the CWI data base
    """
    plt.clf()
    VALUES = []
    where_clause = (
        "(FLOW_RATE is not NULL) AND "
        "(FLOW_RATE > 0) AND "
        "(FLOW_RATE <= 100) AND "
        "(DURATION is not NULL) AND "
        "(DURATION > 0) AND"
        "(DURATION <= 12) AND"
        "(START_MEAS is not NULL) AND "
        "(START_MEAS > 0) AND "
        "(PUMP_MEAS is not NULL) AND "
        "(PUMP_MEAS > 0)"
         )
    with arcpy.da.SearchCursor(CWIPL, ['FLOW_RATE', 'DURATION', 'START_MEAS', 'PUMP_MEAS'], where_clause) as cursor:
        for row in cursor:
            down = row[3] - row[2]
            stuff = [row[0], row[1], down]
            VALUES.append(stuff)
        DUR_DATA = [i[1] for i in VALUES]
        PUMP_DATA = [i[0] for i in VALUES]
        Drawdown_data = [i[2] for i in VALUES]
        plt.figure(1)
        plt.hist(DUR_DATA, bins = 48, label = 'Duration')
        plt.xlim([0, 12])
        plt.ylim([0, 125000])
        plt.minorticks_on()
        plt.xticks(fontsize = 24)
        plt.yticks(fontsize = 24)
        plt.xlabel('Duration [hours]', fontsize = 30)
        plt.ylabel('Number of entries', fontsize = 30)
        plt.grid(True)
       
        plt.figure(2)
        plt.hist(PUMP_DATA, bins = 100, label = 'Pump Rata Data')
        plt.minorticks_on()
        plt.xlim([0, 100])
        plt.ylim([0, 60000])
        plt.xticks(fontsize = 24)
        plt.yticks(fontsize = 24)
        plt.xlabel('Pump Rate [GPM]', fontsize = 30)
        plt.ylabel('Number of entries', fontsize = 30)
        plt.grid(True)
        
        plt.figure(3)
        plt.hist(Drawdown_data, bins = 500, label = 'Pump Rata Data')
        plt.minorticks_on()
        plt.xlim([0, 500])
        plt.ylim([0, 100000])
        plt.xticks(fontsize = 24)
        plt.yticks(fontsize = 24)
        plt.xlabel('Drawdown [ft]', fontsize = 30)
        plt.ylabel('Number of entries', fontsize = 30)
        plt.grid(True)
        
        fig, ax = plt.subplots(1,1)
        plt.figure(4)
        plt.scatter(PUMP_DATA, DUR_DATA)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.minorticks_on()
        plt.xlim([0,100])
        plt.ylim([0,12])
        plt.xlabel('Pumping Rates [GPM]', fontsize = 16)
        plt.ylabel('Duration of Test [hours]', fontsize = 16)
        ax.xaxis.set_major_locator(MultipleLocator(20))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(10))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.axis.set_major_formatter(FormatStrFormatter('%d'))
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray', zorder = 0)
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='black', zorder = 0)
        ax.set_axisbelow(True)

        
         
         
         