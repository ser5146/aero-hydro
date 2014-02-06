#Lesson 1 Source and Sink
import numpy as np
import matplotlib.pyplot as plt
from math import *

N=50                            #Number of points in each direction
xStart,xEnd = -2.0,2.0          # x-direction boundaries (float not integer)
yStart,yEnd = -1.0,1.0          # y-direction boundaries
x=np.linspace(xStart,xEnd,N)    # x 1D-array(reminder:we imported numpy as np)
y=np.linspace(yStart,yEnd,N)    # y 1D-array
print 'x= ',x
print 'y= ',y
X,Y=np.meshgrid(x,y)             #generation of the mesh grid

#plotting the mesh using matplotlib (imported as plt)
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.scatter(X,Y,s=10,c='#CD2305',marker='o',linewidth=0.1)
#s is the size of the points, c is the color
# you could pick a color by saying c='b' or c='g' etc.
#plt.show()                      # this is how you show the plot you created

strengthSource = 5.0            # source strength
xSource, ySource = -1.0, 0.0    # location of the source

uSource=np.empty((N,N),dtype=float)      #Creation of a 2D-array for u
vSource=np.empty((N,N),dtype=float)      #Creation of a 2D-array for v

uSource = (strengthSource/(2*pi))*(X[:,:]-xSource)/((X[:,:]-xSource)**2+(Y[:,:]-ySource)**2)



#computing the velocity components at ever point on the mesh grid
for i in range(N):
    for j in range(N):
        uSource[i,j] = strengthSource/(2*pi)\
            *(X[i,j]-xSource)/((X[i,j]-xSource)**2+(Y[i,j]-ySource)**2)
        vSource[i,j] = strengthSource/(2*pi)\
            *(Y[i,j]-ySource)/((X[i,j]-xSource)**2+(Y[i,j]-ySource)**2)
            # ** is power (^) and \ wraps the line

strengthSink=-5.0                      #Strength of the sink
xSink,ySink=1.0,0.0                     #location of the sink
uSink=np.empty((N,N),dtype=float)       #creation of a 2D-array for u
vSink=np.empty((N,N),dtype=float)       #creation of a 2D-array for v

# computing the velocity components at every point on the mesh grid
for i in range (N):
    for j in range (N):
        uSink[i,j]=strengthSink/(2*pi)\
            *(X[i,j]-xSink)/((X[i,j]-xSink)**2+(Y[i,j]-ySink)**2)
        vSink[i,j]=strengthSink/(2*pi)\
            *(Y[i,j]-ySink)/((X[i,j]-xSink)**2+(Y[i,j]-ySink)**2)
            
Umag=uSource[:,:]*uSource[:,:]+vSource[:,:]*vSource[:,:]

#plotting the streamlines
size=10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,uSource,vSource,density=2.0,linewidth=1,color=np.log(Umag),cmap=plt.cm.jet,arrowsize=2,arrowstyle='->')
plt.scatter(xSource,ySource,c='r',s=80, marker='o')


uPair=np.empty_like(uSource)
vPair=np.empty_like(vSource)

uPair = uSource + uSink
vPair = vSource + vSink

size=10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,uPair,vPair,density=2.0,linewidth=1,arrowsize=2,arrowstyle='->')
plt.scatter([xSource,xSink],[ySource,ySink],c='r',s=80,marker='o')
plt.show()

# challenge task? Need to plot potential lines 
