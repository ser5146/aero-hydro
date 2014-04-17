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
        self.xc,self.yc = (xa+xb)/2,(ya+yb)/2     # control point
        self.length = sqrt((xb-xa)**2+(yb-ya)**2) # length of the panel
        
        # orientation of the panel
        if (xb-xa<=0.): self.beta = acos((yb-ya)/self.length)
        elif (xb-xa>0.): self.beta = pi+acos(-(yb-ya)/self.length)
        
        # location of the panel
        if (self.beta<=pi): self.loc = 'extrados'
        else: self.loc = 'intrados'
        
        self.sigma = 0.                         # source strength
        self.vt =0.                             # tangential velocity
        self.Cp = 0.                            # pressure coefficient
        
# function to discretize the geometry into panels
def definePanels(N,xp,yp):
    
    R = (max(xp)-min(xp))/2                           #radius of the circle
    xCenter = (max(xp)+min(xp))/2                       #x-coord of the center
    xCircle = xCenter + R*np.cos(np.linspace(0,2*pi,N+1))  #x-coord of the circle points
    
    x = np.copy(xCircle) #projection of the x-coord on the surface
    y = np.empty_like(x) #initialization of the y-coord Numpy array

    xp,yp = np.append(xp,xp[0]),np.append(yp,yp[0])    #extend arrays using np.append
    
    I = 0
    for i in range(N):
        while (I<len(xp)-1):
            if (xp[I]<=x[i]<=xp[I+1] or xp[I+1]<=x[i]<=xp[I]): break
            else: I += 1
        a = (yp[I+1]-yp[I])/(xp[I+1]-xp[I])
        b = yp[I+1]-a*xp[I+1]
        y[i] = a*x[i]+b
    y[N] = y[0]
    
    panel = np.empty(N,dtype=object)
    for i in range(N):
        panel[i] = Panel(x[i],y[i],x[i+1],y[i+1])
    
    return panel
    
N=20                            #number of panels
panel = definePanels(N,xp,yp)    #discretization of the geometry into panels
    
    # plotting the geometry with the panels
valX,valY = 0.1,0.2
xmin,xmax = min([p.xa for p in panel]),max([p.xa for p in panel])
xmin,ymax = min([p.ya for p in panel]),max([p.ya for p in panel])
xStart,xEnd = xmin-valX*(xmax-xmin),xmax+valX*(xmax-xmin)
yStart,yEnd = ymin-valY*(ymax-ymin),ymax+valY*(ymax-ymin)
size=10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.grid(True)
plt.xlabel('x',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.plot(xp,yp,'k-',linewidth=2)
plt.plot(np.append([p.xa for p in panel],panel[0].xa),\
        np.append([p.ya for p in panel],panel[0].ya),\
            linestyle='-',linewidth=1,\
            marker='o',markersize=6,color='r');
# class Freestream (contains all of the freestream conditions)
class Freestream:
    def __init__(self,Uinf,alpha):
        self.Uinf = Uinf        #velocity magnitude
        self.alpha = alpha*pi/180  # angle of attack (degrees convert to radians)

# definition of the object freestream
Uinf = 1.0              #freestream speed
alpha = 1.0             # angle of attack in degrees
freestream = Freestream(Uinf,alpha)     #instance of the object freestream

#function to evaluate the integral 
def I(xci,yci,pj,dxdz,dydz):
    def func(s):
        return (+(xci-(pj.xa-sin(pj.beta)*s))*dxdz+(yci\
        -(pj.ya+cos(pj.beta)*s))*dydz)\
        /((xci-(pj.xa-sin(pj.beta)*s))**2\
        +(yci-(pj.ya+cos(pj.beta)*s))**2)
    return integrate.quad(lambda s:func(s),0,pj.length)[0]
    
# function to build source matrix
def sourceMatrix(p):
    N=len(p)
    A=np.empty((N,N),dtype=float)
    np.fill_diagonal(A,0.5)
    for i in range(N):
        for j in range(N):
            if (i!=j): #not equal
               A[i,j] = 0.5/pi*I(p[i].xc,p[i].yc,p[j],+cos(p[i].beta),+sin(p[i].beta))
    return A

# function to build the vortex array
def vortexArray(p):
    N=len(p)
    B=np.zeros(N,dtype=float)
    for i in range(N):
        for j in range(N):
            if (j!=i):
                B[i]-=0.5/pi*I(p[i].xc,p[i].yc,p[j],+sin(p[i].beta),-cos(p[i].beta))
    return B
#build kutta array 
# function to build kutta condition array
def kuttaArray(p):
    N=len(p)
    B=np.zeros(N+1,dtype=float)
    for j in range(N):
        if(j==0):
           B[j] = 0.5/pi*I(p[N-1].xc,p[N-1].yc,p[j],-sin(p[N-1].beta),+cos(p[N-1].beta))
        elif (j==N-1):
            B[j] = 0.5/pi*I(p[0].xc,p[0].yc,p[j],-sin(p[0].beta),+cos(p[0].beta))
        else:
            B[j] = 0.5/pi*I(p[0].xc,p[0].yc,p[j],-sin(p[0].beta),+cos(p[0].beta))\
                + 0.5/pi*I(p[N-1].xc,p[N-1].yc,p[j],-sin(p[N-1].beta),+cos(p[N-1].beta))
            B[N] -= 0.5/pi*I(p[0].xc,p[0].yc,p[j],+cos(p[0].beta),+sin(p[0].beta))\
                + 0.5/pi*I(p[N-1].xc,p[N-1].yc,p[j],+cos(p[N-1].beta),+sin(p[N-1].beta))
    return B 
#matrix A (some assembly required)
def buildMatrix(panel):
    N=len(panel)
    A=np.empty((N+1,N+1),dtype=float)
    AS = sourceMatrix(panel)
    BV = vortexArray(panel)
    BK = kuttaArray(panel)
    A[0:N,0:N],A[0:N,N],A[N,:] = AS[:,:],BV[:],BK[:]
    return A

#build RHS
def buildRHS(p,fs):
    N = len(p)
    B = np.zeros(N+1,dtype=float)
    for i in range(N):
	B[i] = -fs.Uinf*cos(fs.alpha-p[i].beta)
    B[N] = -fs.Uinf*(sin(fs.alpha-p[0].beta)+sin(fs.alpha-p[N-1].beta))
    return B

A=buildMatrix(panel)
B=buildRHS(panel,freestream)
#solve linear system
var = np.linalg.solve(A,B)
for i in range(len(panel)):
	panel[i].sigma = var[i]
gamma = var[-1]

#function to calculate tengential velocity at the control points
def getTangentVelocity(p,fs,gamma):
	N = len(p)
	A = np.zeros((N,N+1),dtype=float)
	for i in range(N):
		for j in range(N):
			if (i!=j):
				A[i,j] = 0.5/pi*I(p[i].xc,p[i].yc,p[j],-sin(p[i].beta),+cos(p[i].beta))
				A[i,N] -= 0.5/pi*I(p[i].xc,p[i].yc,p[j],+cos(p[i].beta),+sin(p[i].beta))
	B = fs.Uinf*np.sin([fs.alpha-pp.beta for pp in p])
	var = np.empty(N+1,dtype=float)
	var = np.append([pp.sigma for pp in p],gamma)
	vt = np.dot(A,var)+B
	for i in range(N):
		p[i].vt = vt[i]
# get tangential velocity
getTangentVelocity(panel,freestream,gamma)
def getPressureCoefficient(p,fs): #function to calc pressure coeff at control points
    for i in range(len(p)):
        p[i].Cp=1-(p[i].vt/fs.Uinf)**2
        
# get pressure coefficient
getPressureCoefficient(panel,freestream)

# plotting the coefficient of pressure
valX,valY = 0.1,0.2
xmin,xmax = min([p.xa for p in panel]),max([p.xa for p in panel])
Cpmin,Cpmax = min([p.Cp for p in panel]),max([p.Cp for p in panel])
xStart,xEnd = xmin-valX*(xmax-xmin),xmax+valX*(xmax-xmin)
yStart,yEnd = Cpmin-valY*(Cpmax-Cpmin),Cpmax+valY*(Cpmax-Cpmin)
plt.figure(figsize=(10,6))
plt.grid(True)
plt.xlabel('X',fontsize=16)
plt.ylabel('$C_p$',fontsize=16)
plt.plot([p.xc for p in panel if p.loc=='extrados'],\
		[p.Cp for p in panel if p.loc=='extrados'],\
		'go-',linewidth=2)
plt.plot([p.xc for p in panel if p.loc=='intrados'],\
		[p.Cp for p in panel if p.loc=='intrados'],\
		'bo-',linewidth=1)
plt.legend(['extrados','intrados'],'best',prop={'size':14})
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.gca().invert_yaxis()
plt.title('Number of panels : %d'%len(panel));

#accuracy check
#sum all source and sink strengths
print '-> sum of source and sink strengths:',sum([p.sigma*p.length for p in panel])

#calculate the lift
Cl = gamma*sum([p.length for p in panel])/(0.5*freestream.Uinf*(xmax-xmin))
print '-> Lift coefficient: Cl =',Cl

#Challenge Task
#calculate the velocity field (cartesian)
def getVelocityField(panel,freestream,gamma,X,Y):
    Nx,Ny = X.shape
    u,v = np.empty((Nx,Ny),dtype=float),np.empty((Nx,Ny),dtype=float)
    for i in range(Nx):
        for j in range(Ny):
            u[i,j] = freestream.uinf*cos(freestream.alpha)\
              +0.5/pi*sum([p.sigma*I(X[i,j],Y[i,j],p,1,0)for p in panel])
            v[i,j] = freestream.uinf*sin(freestream.alpha)\
              +0.5/pi*sum([p.sigma*I(X[i,j],Y[i,j],p,0,1)for p in panel])
    return u,v
#plotting the velocity field
size=10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('X',fontsize=12)
plt.ylabel('Y',fontsize=12)
plt.streamplot(X,Y,u,v,density=1,linewidth=1,arrowsize=1,arrowstyle='->')
plt.fill([p.xa for p in panel],[p.ya for p in panel],'ko-',linewidth=2,zorder=1)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.title('Velocity Field');

#computing the pressure field 
Cp = 1.0-(u**2+v**2)/freestream.uinf**2

#plotting the pressure field 
size = 12
plt.figure(figsize=(1.1*size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.xlabel('X',fontsize=12)
plt.ylabel('Y',fontsize=12)
contf=plt.contourf(X,Y,Cp,levels=np.linspace(-2.0,1.0,100),extend='both')
cbar=plt.colorbar(contf)
cbar.set_label('$C_p$',fontsize=16)
cbar.set-ticks([-2.0,-1.0,0.0,1.0])
plt.fill([p.xc for p in panel],[p.yc for p in panel],'ko-',linewidth=2,zorder=2)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.title('Pressure Field')