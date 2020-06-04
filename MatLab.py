
"""
This function is just for playing with matplotlib


Author: Jonny Full
Version: 6/1/2020
"""
import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0.0, 2.0, 0.01)
s = 20*t - 10
plt.plot(t,s)

plt.title("Transmissivity")
