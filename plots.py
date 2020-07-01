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
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



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
    plt.hist(np.log(transmissivity_calculated), bins=50)
    plt.title('Transmissivity Distribution')
    plt.xlabel('ln(T)')
    plt.ylabel('Number of entries')

    
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
    plt.clf()
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
    sns.scatterplot(x, y, hue = distribute_t, palette = "Set2")
    plt.title(f"Transmissivity for Wells within {radius} meters of Well ID {target_well}")
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')
    plt.grid(True)