"""Creates plots of data using matplotlib

This is a file of helper functions that plots the data calculated from
Transmissivity.py as a histogram and scatter plot.

Functions
---------
plot_histogram_transmissivity:
    Creates a histogram of the calculated Transmissivities (log 10 scale).
    
plot_spacial_transmissivity:
    Creates a scatterplot where each well is plotted at its UTM coordinates.
    Each point is colored baised on a log10 color ramp where the points 
    become darker as transmissivity increases.
    
plot_spacial_conductivity:
    Creates a scatterplot where each well is plotted at its UTM 
    coordinates. Each point is colored baised on a log10 color ramp where the 
    points become darker as hydraulic conductivity increases.
    
plot_spacial_thickness:
    Creates a scatter plot where each point is plotted at its UTM coordinates.
    Each point is colored baised on a color ramp where the points become darker
    as aquifer thickness increases.
    
Pump_Durations_Plots:
    This is a temporary file that has been used to create a series of plots
    that show rounding bias in the CWI data base. These plots have been added
    to my technical writeup.
    
Author: Jonny Full
Version: 8/6/2020
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import arcpy
from data_location import CWIPL
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)
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
    T_min = [i[0] for i in transmissivity_calculated]
    T_guess = [i[1] for i in transmissivity_calculated]
    T_max = [i[2] for i in transmissivity_calculated]
    plt.close('all')
    fig, axs = plt.subplots(3, sharex = True, sharey = True)
    #logbins creates an evenly distributed log 10 array for our histograms
    logbins = np.logspace(np.log10(min(T_min)),np.log10(max(T_min)),100)
    axs[0].hist(T_min, bins = logbins, label = ['T_Min'], color = 'red',\
       edgecolor = 'k', zorder = 3)    
    logbins = np.logspace(np.log10(min(T_guess)),np.log10(max(T_guess)), 100)
    axs[1].hist(T_guess, bins=logbins, label = ['Recorded Data'],\
       color = 'blue', edgecolor = 'k', zorder = 3)    
    logbins = np.logspace(np.log10(min(T_max)),np.log10(max(T_max)), 100)
    axs[2].hist(T_max, bins= logbins, label = ['T_max'], color = 'green',\
       edgecolor = 'k', zorder = 3)
    axs[2].set_xlabel('Log 10 of Transmissivity', fontsize = 24)
    axs[1].set_ylabel('Count', fontsize = 24)
    plt.xscale('log')
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    axs[0].grid(True, zorder = 0)
    axs[1].grid(True, zorder = 0)
    axs[2].grid(True, zorder = 0)
    
def plot_spacial_transmissivity(target_well, radius, confirmed_wells, transmissivity_calculated, target_coords):
    """Plots the confirmed_wells geographical location and shows the 
    Transmissivity for each well.
    
    Parameters
    ----------
    target_well: string
        The RELATEID of the well input by the user in Verify.
        Example : '0000123456'
        
    RADIUS: int (meters)
        RADIUS represents a boundry condition for the scope of analysis. 
        Any wells used in future calculations fall within this distance of the
        target well. 
        Example: 10000 (meters)
        
    confirmed_wells: list[[list1][list2][list3]]
        This is a list of all pertinant information required to plot the wells
        spacially and calculate Transmissivity.
    
        list1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float), 
                     Casing Radius (ft), Relate ID (str)
        
        list 2 = list[Pump Rate (float), Duration (float), Drawdown (float), 
                     Relate ID (str)]
        
        list 3 = list[aquifer thickness (float),
                      miniumum storage coefficent (float), maximum storage
                      coefficent (float), and Well ID (int)]
    
    transmissivity_calculated: list
        A list of Transmissivities that were calculated from confirmed_wells. 
        The units are ft^2/day.
    
    target_coords:list
        Contains the UTM coordinates of the original well input by the user.
        This data will be used to create a unique data point on the scatterplot
        to represent the location of the target well.
        
    Notes
    -----
    This function returns a scatterplot. The axis will use the UTM Easting (x)
    and UTM Northing (y) on its axis. The plotted points will be color coded
    where each well will become darker as Transmissivity increases. The color
    ramp used is on a log10 scale. The target well is represented by a red
    square on the plot.
    """
    plt.figure(3)
    distribute_t = []
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    T = [i[0] for i in transmissivity_calculated]
    bounds = np.percentile(transmissivity_calculated, np.arange(0, 110, 10)) #calculates deciles
    #May not be necessary
    for row in T:
        for decile, trans in enumerate(bounds):
            if trans > row:
                 break
        distribute_t.append(decile)
    plt.grid(True, zorder = 0)
    plt.scatter(x, y, c = T, s = 30, cmap='Blues',\
                norm = LogNorm(vmin= min(T), vmax=max(T)), zorder = 3)
    cbar = plt.colorbar()
    cbar.set_label('log10() of Transmissivity', rotation = 270, labelpad = 15)
    plt.scatter([target_coords[0][0]], [target_coords[0][1]], color='red',\
                    marker = 's', edgecolor = 'k', s = 50,\
                    label = 'Target Well', zorder = 3)
    plt.title(f"Transmissivity for Wells within {radius} meters of Well ID {target_well}")
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')

def plot_spacial_conductivity(target_well, radius, confirmed_wells,\
                              conductivity_calculated, target_coords):
    """Plots the confirmed_wells geographical location and shows the 
    Hydraulic Conductivity for each well.
    
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
        
    confirmed_wells: list[[list1][list2][list3]]
        This is a list of all pertinant information required to plot the wells
        spacially and calculate Transmissivity/Hydraulic Conductivity.
    
        list1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float), 
                     Casing Radius (ft), Relate ID (str)
        
        list 2 = list[Pump Rate (float), Duration (float), Drawdown (float), 
                     Relate ID (str)]
        
        list 3 = list[aquifer thickness (float),
                      miniumum storage coefficent (float), maximum storage
                      coefficent (float), and Well ID (int)]
    
    conductivity_calculated: list
        A list of hydralic conductivities that were calculated from confirmed_wells. 
        The units are ft/day.
    
    target_coords:list
        Contains the UTM coordinates of the original well input by the user.
        This data will be used to create a unique data point on the scatterplot
        to represent the location of the target well.
        
    Notes
    -----
    This function returns a scatterplot. The axis will use the UTM Easting (x)
    and UTM Northing (y) on its axis. The plotted points are color coded so that
    they will get darker as the hydralic conductivity increases. The colorbar
    being used in based on a log10 scale. The target well input by the user
    is represented by a blue diamond on the plot.
    """
    
    plt.figure(4)
    distribute_K = []
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    K = [i[0] for i in conductivity_calculated]
    bounds = np.percentile(conductivity_calculated, np.arange(0, 110, 10)) #calculates deciles
    for row in K:
        for decile, trans in enumerate(bounds):
            if trans > row:
                break
        distribute_K.append(decile)
    plt.grid(True, zorder = 0)
    plt.scatter(x, y, c = K, s = 30, cmap='Purples',\
                norm = LogNorm(vmin= min(K), vmax=max(K)), zorder = 3)
    cbar = plt.colorbar()
    cbar.set_label('log10() of Hydraulic Conductivity', rotation = 270, labelpad = 15)
    plt.scatter([target_coords[0][0]], [target_coords[0][1]],\
                    color='red', marker = 's', edgecolor = 'k',\
                    s = 50, label = 'Target Well', zorder = 3)
    plt.title(f"Hydraulic Conductivity for Wells within {radius} meters of Well ID {target_well}")
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')
    
def plot_spacial_thickness(target_well, radius, confirmed_wells, target_coords):
    """Plots the confirmed_wells geographical location and shows the 
    Aquifer Thickness for each well.
    
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
        
    confirmed_wells: list[[list1][list2][list3]]
        This is a list of all pertinant information required to plot the wells
        spacially and calculate Transmissivity.
    
        list 1 = list[UTME (int), UTMN (int), AQUIFER (str), Screen Length (float), 
                     Casing Radius (ft), Relate ID (str)
        
        list 2 = list[Pump Rate (float), Duration (float), Drawdown (float), 
                     Relate ID (str)]
        
        list 3 = list[aquifer thickness (float),
                      miniumum storage coefficent (float), maximum storage
                      coefficent (float), and Well ID (int)]
    
    target_coords:list
        Contains the UTM coordinates of the original well input by the user.
        This data will be used to create a unique data point on the scatterplot
        to represent the location of the target well.
        
    Notes
    -----
    This function returns a scatterplot. The axis will use the UTM Easting (x)
    and UTM Northing (y) on its axis. The plotted points will be color coded
    based on the colorbar that is displayed. The color of the points will get
    darker as aquifer's thickness increases. The location of the target well
    can be identified by the purple X on the plot.
    """
    plt.figure(5)
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    thickness = [i[2][0] for i in confirmed_wells]
    plt.grid(True, zorder = 0)
    plt.scatter(x, y, c = thickness, s = 30, cmap='Greens',zorder = 3)
    cbar = plt.colorbar()
    cbar.set_label('Thickness (ft)', rotation = 270, labelpad = 15)
    plt.scatter([target_coords[0][0]], [target_coords[0][1]],\
                    color='red', marker = 's', edgecolor = 'k',\
                    s = 100, label = 'Target Well', zorder = 3)
    plt.title(f"Aquifer Thickness for wells within {radius} meters of Well ID {target_well}")
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')
    
def Pump_Durations_Plots():
    """ Temporary file
    
    This file shows how common roundoff errors occur in the CWI database
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
    with arcpy.da.SearchCursor(CWIPL, ['FLOW_RATE', 'DURATION', 'START_MEAS',\
                                       'PUMP_MEAS'], where_clause) as cursor:
        for row in cursor:
            down = row[3] - row[2]
            if down > 0 and down < 100 and row[3] <=200:
                stuff = [row[0], row[1], row[3], down]
                VALUES.append(stuff)
        DUR_DATA = [i[1] for i in VALUES]
        PUMP_DATA = [i[0] for i in VALUES]
        Water_Level = [i[2] for i in VALUES]
        Drawdown_data = [i[3] for i in VALUES]
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
        plt.hist(Water_Level, bins = 200, label = 'Static Level Data', edgecolor = 'k')
        plt.minorticks_on()
        plt.xticks(fontsize = 24)
        plt.yticks(fontsize = 24)
        plt.xlabel('Static Water Level [ft]', fontsize = 30)
        plt.ylabel('Number of entries', fontsize = 30)
        plt.grid(True)
        
        plt.figure(4)
        plt.hist(Drawdown_data, bins = 100, label = 'Drawdown Data', color = 'g' , edgecolor = 'k')
        plt.minorticks_on()
#        plt.xlim([0, 100])
#        plt.ylim([0, 100000])
        plt.xticks(fontsize = 24)
        plt.yticks(fontsize = 24)
        plt.xlabel('Drawdown [ft]', fontsize = 30)
        plt.ylabel('Number of entries', fontsize = 30)
        plt.grid(True)
        
        fig, ax = plt.subplots(1,1)
        plt.figure(5)
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray',\
                 zorder = 0)
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='black',\
                 zorder = 0)
        plt.scatter(PUMP_DATA, DUR_DATA, zorder = 3)
        plt.xticks(fontsize = 24)
        plt.yticks(fontsize = 24)
        plt.minorticks_on()
        plt.xlim([0,101])
        plt.ylim([0,12.25])
        plt.xlabel('Pumping Rates [GPM]', fontsize = 30)
        plt.ylabel('Duration of Test [hours]', fontsize = 30)
        ax.xaxis.set_major_locator(MultipleLocator(20))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(10))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        #ax.axis.set_major_formatter(FormatStrFormatter('%d'))
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))
        ax.set_axisbelow(True)

if __name__ == '__main__':
# execute only if run as a script (comment out unnecessary functions)      
    plot_histogram_transmissivity(transmissivity_calculated)
#    plot_spacial_transmissivity(target_well, radius, confirmed_wells,\
#                                transmissivity_calculated, target_coords)
#    plot_spacial_conductivity(target_well, radius, confirmed_wells,\
#                              conductivity_calculated, target_coords) 
#    plot_spacial_thickness(target_well, radius, confirmed_wells, target_coords)
#    Pump_Durations_Plots()