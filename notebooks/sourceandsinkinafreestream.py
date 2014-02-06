import numpy as np
import matplotlib.pyplot as plt
from math import *

#create mesh as done in source and sink
N=200                           # number of points in each direction
xStart,xEnd = -4.0, 4.0         # x-direction boundaries
yStart,yEnd = -2.0,2.0          # y-direction boundaries
x=np.linspace(xStart,xEnd,N)    # x 1D - array
y=np.linspace(yStart,yEnd,N)    # y 1D - array
X,Y = np.meshgrid(x,y)          # generation of the mesh grid

# If you want to determine the size of X and Y you type in np.shape(X) 
# or np.shape(Y) to get the size of the array

#source in a uniform stream

Uinf = 1.0                      # freestream speed
alphaInDegrees = 0.0            # angle of attack (in degrees)
alpha = alphaInDegrees*pi/180

#computing the velocity components on the mesh grid
uFreestream = Uinf*cos(alpha)*np.ones((N,N),dtype=float)
vFreestream = Uinf*sin(alpha)*np.ones((N,N),dtype=float)

#computing the stream-function on the meshgrid
psiFreestream = + Uinf*cos(alpha)*Y - Uinf*sin(alpha)*X

''' the below simply defines the function we plan to use in the future
we do not have all of the parameters we plan to use to execute this function
ie ys and xs and strength are not defined yet'''

# function to compute the velocity field of a source/ sink
def getVelocity(strength,xs,ys,X,Y):
    u=(strength/(2*pi))*(X-xs)/((X-xs)**2+(Y-ys)**2)
    v=(strength/(2*pi))*(Y-ys)/((X-xs)**2+(Y-ys)**2)
    return u,v

#function to compute the stream-function of a source/ sink
def getStreamFunction(strength,xs,ys,X,Y):
    psi=strength/(2*pi)*np.arctan2((Y-ys),(X-xs))
    return psi

''' this concludes the defining of functions to use. time to include the necessary
input for the above two functions. This defines the functions in this notebook only'''
'''now to use functions defined above'''

strengthSource = 5.0            #strength of the source
xSource,ySource = -1.0,0.0      #location of the source

#computing the velocity components
uSource,vSource = getVelocity(strengthSource,xSource,ySource,X,Y)

#computing the stream-function
psiSource= getStreamFunction(strengthSource,xSource,ySource,X,Y)