import numpy as np
import matplotlib.pyplot as plt
from math import *

'''
from IPython.display import Image
Image(filename='../resources/doubletSketch1.png')
from IPython.display import Image
Image(filename='../resources/doubletSketch2.png')
'''

N = 50                            # Number of points in each direction
xStart,xEnd = -2.0,2.0            # x-direction boundaries
yStart,yEnd = -1.0,1.0            # y-direction boundaries
x = np.linspace(xStart,xEnd,N)    # x 1D-array
y = np.linspace(yStart,yEnd,N)    # y 1D-array
X,Y = np.meshgrid(x,y)            # generation of the mesh grid

#consider a doublet of strength k=1.0 located at the origin

kappa=1.0                        # strength of the doublet
xDoublet, yDoublet = 0.0,0      # loction of the doublet

'''define a functionn to calculate the stream function and velocity 
components this function could be re-used if we choose to insert 
and additional doublet into our domain'''

#function to compute the velocity components of a doublet
def getVelocityofDoublet(strength,xd,yd,X,Y):
    u= -strength/(2*pi)*((X-xd)**2-(Y-yd)**2)/((X-xd)**2+(Y-yd)**2)**2
    v= -strength/(2*pi)*2*(X-xd)*(Y-yd)/((X-xd)**2+(Y-yd)**2)**2
    return u,v

def getStreamFunctionofDoublet(strength,xd,yd,X,Y):
    psi=-strength/(2*pi)*(Y-yd)/((X-xd)**2+(Y-yd)**2)
    return psi

#computing the velocity components on the mesh grid
uDoublet,vDoublet=getVelocityofDoublet(kappa,xDoublet,yDoublet,X,Y)

#computing the stream-function on the mesh grid
psiDoublet=getStreamFunctionofDoublet(kappa,xDoublet,yDoublet,X,Y)

# plotting
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,uDoublet,vDoublet,\
               density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
plt.scatter(xDoublet,yDoublet,c='#CD2305',s=80,marker='o');

Uinf=1.0            #freestream speed
uFreestream = Uinf*np.ones((N,N),dtype=float)
vFreestream = np.zeros((N,N),dtype=float)
psiFreestream=Uinf*Y

#superimposition of the doublet on the freestream flow
u=uFreestream + uDoublet
v=vFreestream + vDoublet
psi=psiFreestream + psiDoublet

#plotting
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.streamplot(X,Y,u,v,\
               density=2.0,linewidth=1,arrowsize=1,arrowstyle='->')
plt.contour(X,Y,psi,levels=[0.0],colors='r',linewidths=2,linestyles='solid')
plt.scatter(xDoublet,yDoublet,c='r',s=80,marker='o')

#stagnation points
xStagn1,yStagn1=+sqrt(kappa/(2*pi*Uinf)),0
xStagn2,yStagn2=-sqrt(kappa/(2*pi*Uinf)),0
plt.scatter([xStagn1,xStagn2],[yStagn1,yStagn2],c='g',s=80,marker='o');

#compute the pressure coefficient
Cp=1.0-(y**2+v**2)/Uinf**2

#plotting
size=10
plt.figure(num=0,figsize=(1.1*size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,yEnd)
plt.ylim(yStart,yEnd)
contf = plt.contourf(X,Y,Cp,levels=np.linspace(-2.0,1.0,100),extend='both')
cbar = plt.colorbar(contf)
cbar.set_label(r'$C_p$',fontsize=16)
cbar.set_ticks([-2.0,-1.0,0.0,1.0])
plt.scatter(xDoublet,yDoublet,c='r',s=80,marker='o')
plt.contour(X,Y,psi,\
            levels=[0.0],\
            colors='r',linewidths=2,linestyles='solid')
plt.scatter([xStagn1,xStagn2],[yStagn1,yStagn2],c='g',s=80,marker='o');
