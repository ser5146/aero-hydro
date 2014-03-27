# objective of this notebook is to implement a source-vortex panel code
# to calculate the pressure coefficient on the surface

import numpy as np
from scipy import integrate
from math import *
import matplotlib.pyplot as plt

# read of the geometry from a data file

coords = np.loadtxt(fname='../data/naca0012.dat')
xp,yp = coords[:,0],coords[:,1]

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
plt.plot(xp,yp,'k-',linewidth=2);

# class panel containing the information about one panel
class Panel:
    def __init__(self,xa,ya,xb,yb):
        self.xa,self.ya = xa,ya                 # 1st end-point
        self.xb,self.yb = ya,yb                 # 2nd end-point
        self.xc,self.yc-(xa+xb)/2,(ya+yb)/2     # control point