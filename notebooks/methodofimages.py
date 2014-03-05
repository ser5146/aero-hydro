import numpy as np
import matplotlib.pyplot as plt
from math import *
from IPython.core.display import clear_output

N=50                                 # Number of points in each direction
xStart,xEnd = -2.0,2.0               # x-direction boundaries
yStart,yEnd = -1.0,1.0               # y-direction boundaries
x=np.linspace(xStart,xEnd,N)         # x 1D-array
y=np.linspace(yStart,yEnd,N)         # y 1D-array
X,Y= np.meshgrid(x,y)                # generation of the mesh grid

#Define a 'Class' called Source- use 3 attributes
'''strength: strength of the source
x: the location of the source on the x axis
y: the location of the source on the y axis'''

class Source:
    def __init__(self,strength,x,y):
        self.strength = strength
        self.x,self.y = x,y
    # get the velocity field
    def velocity(self,X,Y):
        self.u = self.strength/(2*pi)*(X-self.x)/((X-self.x)**2+(Y-self.y)**2)
        self.v = self.strength/(2*pi)*(Y-self.y)/((X-self.x)**2+(Y-self.y)**2)
    # get the stream-function
    def streamFunction(self,X,Y):
        self.psi = self.strength/(2*pi)*np.arctan2((Y-self.y),(X-self.x))

        ''' we define an object  called source as an 'instantiation'
        of the class Source, defining the strength and the location
        of the singularity'''
strengthSource=1.0
xSource,ySource = 0.0,0.5
source = Source(strengthSource,xSource,ySource)
source.velocity(X,Y)
source.streamFunction(X,Y)
sourceImage = Source(strengthSource,xSource,-ySource)
sourceImage.velocity(X,Y)
sourceImage.streamFunction(X,Y)


# Superimposition of the source and its image
u = source.u + sourceImage.u
v = source.v + sourceImage.v
psi = source.psi + sourceImage.psi

# Plotting
size = 10
plt.figure(num=0,figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,\
               density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
plt.scatter(source.x,source.y,c='r',s=80,marker='o')
plt.scatter(sourceImage.x,sourceImage.y,c='r',s=80,marker='D')
plt.axhline(0.0,color='k',linestyle='--',linewidth=4);