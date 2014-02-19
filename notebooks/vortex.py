import numpy as np
import matplotlib.pyplot as plt
from math import *
N=50                                    #Number of points in each direction
xStart,xEnd = -2.0,2.0                  #x-direction boundaries
yStart,yEnd = -1.0,1.0                  # y-direction boundaries
x=np.linspace(xStart,xEnd,N)            #x 1D-array
y=np.linspace(yStart,yEnd,N)            # y 1D-array
X,Y=np.meshgrid(x,y)                    # generation of the mesh grid

gamma=5.0                               # strength of the vortex
xVortex,yVortex=0.0,0.0                 # Location of the vortex

# create function to compute the velocity components of a vortex
def getVelocityVortex(strength,xv,yv,X,Y):
    u = + strength/(2*pi)*(Y-yv)/((X-xv)**2+(Y-yv)**2)
    v = - strength/(2*pi)*(X-xv)/((X-xv)**2+(Y-yv)**2)
    return u,v
    
 # define function to compute the stream-function of a vortex
def getStreamFunctionVortex(strength,xv,yv,X,Y):
    psi = strength/(4*pi)*np.log((X-xv)**2+(Y-yv)**2)
    return psi   
    
#compute the velocity componets on the mesh grid
uVortex,vVortex=getVelocityVortex(gamma,xVortex,yVortex,X,Y)

# compute the stream function on the meshgrid
psiVortex=getStreamFunctionVortex(gamma,xVortex,yVortex,X,Y)

# plot time!
#ps. don't forget to say plt.show() or else nothing will hapen

size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,uVortex,vVortex,\
               density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
plt.scatter(xVortex,yVortex,c='r',s=80,marker='o');

#lets add a sink to our votex.. 

strengthSink=-1.0                           #strength of the sink
xSink,ySink = 0.0,0.0                       #location of the sink

#define a function to compute the velocity components of a sink
def getVelocitySink(strength,xs,ys,X,Y):
    u = strength/(2*pi)*(X-xs)/((X-xs)**2+(Y-ys)**2)
    v = strength/(2*pi)*(Y-ys)/((X-xs)**2+(Y-ys)**2)
    return u,v

# define a function to compute the stream function of a sink
def getStreamFunctionSink(strength,xs,ys,X,Y):
    psi = strength/(2*pi)*np.arctan2((Y-ys),(X-xs))
    return psi
    
# compute the velocity components on the mesh grid
uSink,vSink=getVelocitySink(strengthSink,xSink,ySink,X,Y)

# compute the stream function on the mesh grid
psiSink=getStreamFunctionSink(strengthSink,xSink,ySink,X,Y)

#to visualize the streamlines inducted by a vortex-sink pair, we apply superposition

#superimposition of the sink and the vortex
u=uVortex+uSink
v=vVortex+vSink
psi=psiVortex+psiSink

#plotting
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,\
               density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
plt.scatter(xVortex,yVortex,c='r',s=80,marker='o');