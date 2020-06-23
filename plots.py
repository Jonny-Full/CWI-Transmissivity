
"""
This function is just for playing with matplotlib


Author: Jonny Full
Version: 6/16/2020
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_T(TSIV):
    plt.hist(np.log(TSIV), bins=50)
    plt.title('Transmissivity Distribution')
    plt.xlabel('ln(T)')
    plt.ylabel('Number of entries')
     
def spacial_T(confirmed_wells, TSIV):
    #This does not work due to indexing
    x = [i[0][0] for i in confirmed_wells]
    y = [i[0][1] for i in confirmed_wells]
    plt.grid(True)
    plt.scatter(x, y, 12, TSIV)
    plt.colorbar()
    plt.axis('equal')