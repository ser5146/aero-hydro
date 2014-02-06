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
alphaInDegrees = 0.0          # angle of attack (in degrees)
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

#superposition of the source on the freestream
u=uFreestream + uSource
v=vFreestream + vSource
psi = psiFreestream + psiSource

#plotting
size=10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.grid(True)
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,density=2.0,linewidth=1,color='b',arrowsize=1,arrowstyle = '->')
plt.scatter(xSource,ySource,c='#CD2305',s=80,marker='o')

#computing the stagnation point
xStagnation= xSource - strengthSource/(2*pi*Uinf)*cos(alpha)
yStagnation = ySource - strengthSource/(2*pi*Uinf)*sin(alpha)

#adding the stagnation point to the figure
plt.scatter(xStagnation,yStagnation,c='g',s=80,marker = 'o')

#adding the dividing line to the figure
if (alpha==0.0):
    plt.contour(X,Y,psi,\
        levels=[-strengthSource/2,+strengthSource/2],\
        colors ='#CD2305',linewidth=2,linestyles='solid')

''' if you youse contourf instead of contour it fills the contour level as defined by levels
it fills in the source portion of the level'''


'''we can use the functions getStreamfunction and getVelocity (defined above) 
to code for adding the sink without much coding'''

# source-sink pair in a uniform flow
strengthSink=-5.0               #strength of the sink
xSink,ySink=1.0,0.0             #location of the sink

# computing the velocity field on the mesh grid
uSink,vSink=getVelocity(strengthSink,xSink,ySink,X,Y)

# computing the stream-function on the grid mesh
psiSink=getStreamFunction(strengthSink,xSink,ySink,X,Y)

# superposition of a source and a sink on the freestream
u = uFreestream + uSource + uSink
v = vFreestream + vSource + vSink
psi = psiFreestream + psiSource + psiSink

# plotting source plus sink in a freestream
size=10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
plt.scatter([xSource,xSink],[ySource,ySink],c='#CD2305',s=80,marker='o')
if(alpha ==0.0):
    plt.contour(X,Y,psi,levels=[0.0],colors='#CD2305',linewidth=2,linestyles='solid')

# computing the pressure coefficient
Cp=1.0-(u**2+v**2)/Uinf**2

# plotting
size=10
plt.figure(figsize=(1.1*size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
contf = plt.contourf(X,Y,Cp,levels=np.linspace(-2.0,1.0,100),extend='both')
cbar = plt.colorbar(contf)
cbar.set_label(r'$C_p$',fontsize=16)
cbar.set_ticks([-2.0,-1.0,0.0,1.0])
plt.scatter([xSource,xSink],[ySource,ySink],c='#CD2305',s=80,marker='o')
plt.contour(X,Y,psi,\
    levels=[0.0],\
    colors='#CD2305',linewidths=2,linestyles='solid')
    
plt.show()
