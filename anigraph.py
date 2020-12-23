import csv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

with open('india_covid.csv', 'r') as inFile:
    fileReader = csv.reader(inFile)
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)



def animate(i):
    x = ['29-01-2020']
    y = [0]
    x.append()
    y.append()
    ax1.clear()
    plt.plot(x, y, color="blue")


ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()