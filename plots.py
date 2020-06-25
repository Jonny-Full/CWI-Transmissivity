
"""
This function is just for playing with matplotlib


Author: Jonny Full
Version: 6/16/2020
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_T(transmissivity_calculated):
    plt.hist(np.log(TSIV), bins=50)
    plt.title('Transmissivity Distribution')
    plt.xlabel('ln(T)')
    plt.ylabel('Number of entries')


def spacial_T(confirmed_wells, transmissivity_calculated):
    plt.clf()
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    plt.grid(True)
    plt.scatter(x, y, 16, transmissivity_calculated)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Transmissivity', rotation=270)
    plt.xlabel("UTM Easting")
    plt.ylabel("UTM Northing")
    plt.axis('equal')
