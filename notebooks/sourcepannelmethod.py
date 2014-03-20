#import libraries
import numpy as np
from scipy import integrate
from math import *
import matplotlib.pyplot as plt

#function to read coordinates and store them into two 1D arrays
def readGeometry():
    inFile = open('naca0012.dat','r')
    #inFile = open('../resources/cylinder.dat','r')
    x,y = [],[]
    for line in inFile:
        data = line.split()
        x.append(float(data[0]))
        y.append(float(data[1]))
    x,y = np.array(x),np.array(y)
    inFile.close()
    return x,y
    
xp,yp = readGeometry()         # read of the geometry from a data file

# plotting the geometry
valX,valY = 0.1,0.2
xmin,xmax = min(xp),max(xp)
ymin,ymax = min(yp),max(yp)
xStart,xEnd = xmin-valX*(xmax-xmin),xmax+valX*(xmax-xmin)
yStart,yEnd = ymin-valY*(ymax-ymin),ymax+valY*(ymax-ymin)
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.grid(True)
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.plot(xp,yp,'k-',linewidth=2)

