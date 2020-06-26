
"""
This function is just for playing with matplotlib


Author: Jonny Full
Version: 6/16/2020
"""
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


def plot_spacial_transmissivity(confirmed_wells, transmissivity_calculated):
    """Plots the confirmed_wells geographical location and shows the 
    Transmissivity for each well.
    
    Parameters
    ----------
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
    #NEED TO FIGURE OUT DECILE COLORBAR
    plt.clf()
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    plt.grid(True)
    plt.scatter(x, y, 16, transmissivity_calculated)
    bounds = np.percentile(transmissivity_calculated, np.arange(0, 100, 10)) #calculates deciles
        
    cbar = plt.colorbar()
    
    cbar.ax.set_ylabel('Transmissivity', rotation=270)
    
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')
