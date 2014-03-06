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

class Source:
    def __init__(self,strength,x,y):
        self.strength = strength
        self.x,self.y = x,y
    #get the velocity field
    def velocity(self,X,Y):
        self.u = self.strength/(2*pi)*(X-self.x)/((X-self.x)**2+(Y-self.y)**2)
        self.v = self.strength/(2*pi)*(Y-self.y)/((X-self.x)**2+(Y-self.y)**2)
    
    #get the stream function
    def streamFunction(self,X,Y):
        self.psi = self.strength/(2*pi)*np.arctan2((Y-self.y),(X-self.x))

# definition of my sources
Nsource = 11
strength = 5.0
strengthSource = strength/Nsource
xSource=0.0
ySource=np.linspace(-1.0,1.0,Nsource)

#creation of the source line
source = np.empty(Nsource,dtype=object)
for i in range(Nsource):
    source[i] = Source(strengthSource,xSource,ySource[i])
    source[i].velocity(X,Y)

#superposition
u = uFreestream.copy()
v = vFreestream.copy()

for s in source:
    u=np.add(u,s.u)
    v=np.add(v,s.v)
    
 #plotting
size = 8
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.grid(True)
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,density=3,linewidth=1,arrowsize=1,arrowstyle='->')
plt.scatter(xSource*np.ones(Nsource,dtype=float),ySource,c='r',s=80,marker='o')
cont = plt.contourf(X,Y,np.sqrt(u**2+v**2),levels=np.linspace(0.0,0.1,10))
cbar = plt.colorbar(cont)
cbar.set_label('U',fontsize=16);
    