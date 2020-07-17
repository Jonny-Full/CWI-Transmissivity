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
    plt.legend(loc = 'upper right')

    
def plot_spacial_transmissivity(target_well, radius, confirmed_wells, transmissivity_calculated):
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
    T = [i for i in transmissivity_calculated]
    bounds = np.percentile(transmissivity_calculated, np.arange(0, 100, 10)) #calculates deciles
    for row in T:
        value = 0
        if row < bounds[1]:
            value = 1
        elif row < bounds[2]:
            value = 2
        elif row < bounds[3]:
            value = 3
        elif row < bounds[4]:
            value = 4
        elif row < bounds[5]:
            value = 5
        elif row < bounds[6]:
            value = 6
        elif row < bounds[7]:
            value = 7
        elif row < bounds[8]:
            value = 8
        elif row < bounds[9]:
            value = 9
        else:
            value = 10
        distribute_t.append(value)
    sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)
    sns.scatterplot(x, y, hue = distribute_t, palette = "Set2") #Set2 allows for the gradient
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
        "(FLOW_RATE < 100) AND "
        "(DURATION is not NULL) AND "
        "(DURATION > 0) AND"
        "(DURATION < 12)"
         )
    with arcpy.da.SearchCursor(CWIPL, ['FLOW_RATE', 'DURATION'] , where_clause) as cursor:
        for row in cursor:
           stuff = [row[0], row[1]]
           VALUES.append(stuff)
           
        DUR_DATA = [i[1] for i in VALUES]
        PUMP_DATA = [i[0] for i in VALUES]
        plt.figure(1)
        plt.hist(DUR_DATA, bins = 100)
        plt.title('# of Durations')
        plt.xlabel('DURATION')
        plt.ylabel('Number of Entries')
        plt.xticks(np.arange(0, 13, step = 1))
        plt.yticks(np.arange(0, 130000, step = 10000))
       
        
        
        plt.figure(2)
        plt.hist(PUMP_DATA, bins = 100)
        plt.title('# of Pump Rates')
        plt.xlabel('Pump Rate')
        plt.ylabel('Number of Entries')
        plt.xticks(np.arange(0, 110, step = 10))
        plt.yticks(np.arange(0, 60000, step = 5000))
        plt.minorticks_on()
       
        
        with PdfPages('DATA.pdf') as pdf:        
            fig, ax = plt.subplots(1,1)
            ax.set_axisbelow(True)
            plt.figure(3)
            plt.scatter(PUMP_DATA, DUR_DATA)
            plt.minorticks_on()
            plt.xlim([0,100])
            plt.ylim([0,12])
            plt.xlabel('Pumping Rates [GPM]', fontsize = 12)
            plt.ylabel('Duration of Test [hours]', fontsize = 12)
            ax.xaxis.set_major_locator(MultipleLocator(20))
            ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.xaxis.set_minor_locator(MultipleLocator(10))
            ax.yaxis.set_major_locator(MultipleLocator(1))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
            ax.yaxis.set_minor_locator(MultipleLocator(0.5))
            plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray', zorder = 0)
            plt.grid(which='major', linestyle='-', linewidth='0.5', color='black', zorder = 0)
            pdf.savefig()
        
         
         
         