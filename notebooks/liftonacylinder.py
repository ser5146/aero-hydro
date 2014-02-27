import numpy as np
import matplotlib.pyplot as plt
from math import *

N=50                            #Number of points in each direction
xStart, xEnd = -2.0,2.0         #x-direction boundaries
yStart, yEnd = -1.0,1.0         #y-direction boundaries
x=np.linspace(xStart,xEnd,N)    #x 1D-array
y=np.linspace(yStart,yEnd,N)    #y 1D array
X,Y = np.meshgrid(x,y)      #generate the mesh grid

kappa = 1.0                    # strength of doublet
xDoublet,yDoublet = 0.0,0.0    # location of doublet

Uinf = 1.0        # freestream speed
#Function Definitions for the doublet

# function to compute the velocity components of a doublet
def getVelocityDoublet(strength,xd,yd,X,Y):
    u = - strength/(2*pi)*((X-xd)**2-(Y-yd)**2)/((X-xd)**2+(Y-yd)**2)**2
    v = - strength/(2*pi)*2*(X-xd)*(Y-yd)/((X-xd)**2+(Y-yd)**2)**2
    return u,v

# function to compute the stream-function of a doublet
def getStreamFunctionDoublet(strength,xd,yd,X,Y):
    psi = - strength/(2*pi)*(Y-yd)/((X-xd)**2+(Y-yd)**2)
    return psi

# computing the velocity components on the mesh grid
uDoublet,vDoublet = getVelocityDoublet(kappa,xDoublet,yDoublet,X,Y)

# computing the stream-function on the mesh grid
psiDoublet = getStreamFunctionDoublet(kappa,xDoublet,yDoublet,X,Y)

# freestream velocity components
uFreestream = Uinf*np.ones((N,N),dtype=float)
vFreestream = np.zeros((N,N),dtype=float)

# stream-function
psiFreestream = Uinf*Y

# superimposition of the doublet on the freestream flow
u = uFreestream + uDoublet
v = vFreestream + vDoublet
psi = psiFreestream + psiDoublet

# plotting
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,\
               density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
plt.scatter(xDoublet,yDoublet,c='r',s=80,marker='o')

#plot time!
# cylinder radius
R = sqrt(kappa/(2*pi*Uinf))
circle = plt.Circle((0,0),radius=R,color='r',alpha=0.5)
plt.gca().add_patch(circle)

# stagnation points
xStagn1,yStagn1 = +sqrt(kappa/(2*pi*Uinf)),0
xStagn2,yStagn2 = -sqrt(kappa/(2*pi*Uinf)),0
plt.scatter([xStagn1,xStagn2],[yStagn1,yStagn2],c='g',s=80,marker='o');

#End of pure cylinder flow.. lets ad vortex located at the orgin with strength Gamma.

gamma = 4.0                  # strength of vortex
xVortex,yVortex = 0.0,0.0    # location of vortex

# function to compute the velocity components of a vortex
def getVelocityVortex(strength,xv,yv,X,Y):
    u = + strength/(2*pi)*(Y-yv)/((X-xv)**2+(Y-yv)**2)
    v = - strength/(2*pi)*(X-xv)/((X-xv)**2+(Y-yv)**2)
    return u,v

# function to compute the stream-function of the vortex
def getStreamFunctionVortex(strength,xv,yv,X,Y):
    psi = strength/(4*pi)*np.log((X-xv)**2+(Y-yv)**2)
    return psi
    
    # computing the velocity components on the mesh grid
uVortex,vVortex = getVelocityVortex(gamma,xVortex,yVortex,X,Y)

# computing the stream-function on the mesh grid
psiVortex = getStreamFunctionVortex(gamma,xVortex,yVortex,X,Y)

#add up all the pices using superposition
# superimposition of the doublet and the vortex on the freestream flow
u = uFreestream + uDoublet +uVortex
v = vFreestream + vDoublet +vVortex
psi = psiFreestream + psiDoublet +psiVortex

# cylinder radius
R = sqrt(kappa/(2*pi*Uinf))

# stagnation points
xStagn1,yStagn1 = +sqrt(R**2-(gamma/(4*pi*Uinf))**2),-gamma/(4*pi*Uinf)
xStagn2,yStagn2 = -sqrt(R**2-(gamma/(4*pi*Uinf))**2),-gamma/(4*pi*Uinf)

# plotting
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,\
               density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
circle = plt.Circle((0,0),radius=R,color='r',alpha=0.5)
plt.gca().add_patch(circle)
plt.scatter(xVortex,yVortex,c='r',s=80,marker='o')
plt.scatter([xStagn1,xStagn2],[yStagn1,yStagn2],c='g',s=80,marker='o');