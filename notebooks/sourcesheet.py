import numpy as np
import matplotlib.pyplot as plt
from math import *
N = 100                         #Number of Points in each direction
xStart,xEnd = -1.0,1.0          #x-direction boundaries
yStart,yEnd = -1.5,1.5          #y-direction boundaries
x = np.linspace(xStart,xEnd,N)  #1D x array
y = np.linspace(yStart,yEnd,N)  #1D y-array
X,Y = np.meshgrid(x,y)          #generate mesh grid

Uinf =1.0                       #uniform flow parallel to horizontal axis

uFreestream = Uinf*np.ones((N,N),dtype=float)
vFreestream = np.zeros((N,N),dtype=float)
