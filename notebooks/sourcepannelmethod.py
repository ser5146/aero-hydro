#import libraries
import numpy as np
from scipy import integrate
from math import *
import matplotlib.pyplot as plt

#function to read coordinates and store them into two 1D arrays
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


# class Panel containing the info about one panel
class Panel:
    def __init__(self,xa,ya,xb,yb):
        self.xa,self.ya = xa,ya                     # 1st end-point
        self.xb,self.yb = xb,yb                     # 2nd end-point
        self.xc,self.yc = (xa+xb)/2,(ya+yb)/2       # control point
        self.length = sqrt((xb-xa)**2+(yb-ya)**2)   # length of the panel
        
        # orientation of the panel
        if (xb-xa<=0.): self.beta = acos((yb-ya)/self.length)
        elif (xb-xa>0.): self.beta = pi+acos(-(yb-ya)/self.length)
        
        # location of the panel
        if (self.beta<=pi): self.loc = 'extrados'
        else: self.loc = 'intrados'
        
        self.sigma = 0.                             # source strength
        self.vt = 0.                                # tangential velocity
        self.Cp = 0.                                # pressure coefficient
        
        # function to discretize the geometry into panels

def definePanels(N,xp,yp):
    
    R = (max(xp)-min(xp))/2
    xc,yc = (max(xp)+min(xp))/2,(max(yp)+min(yp))/2
    xCircle = xc + R*np.cos(np.linspace(0,2*pi,N+1))
    yCircle = yc + R*np.sin(np.linspace(0,2*pi,N+1))
    
    x = np.copy(xCircle[0:-1])
    y = np.empty_like(x)

    I = 0
    for i in range(N):
        while (I<len(xp)-1):
            if (xp[I]<=x[i]<=xp[I+1] or xp[I+1]<=x[i]<=xp[I]): break
            else: I += 1
        a = (yp[(I+1)%len(yp)]-yp[I])/(xp[(I+1)%len(yp)]-xp[I])
        b = yp[(I+1)%len(yp)]-a*xp[(I+1)%len(xp)]
        y[i] = a*x[i]+b
    
    panel = np.empty(N,dtype=object)
    for i in range(N):
        panel[i] = Panel(x[i],y[i],x[(i+1)%N],y[(i+1)%N])
    
    return panel
    

N = 20                       # number of panels
panel = definePanels(N,xp,yp)  # discretization of the geometry into panels

# plotting the geometry with the panels
valX,valY = 0.1,0.2
xmin,xmax = min([p.xa for p in panel]),max([p.xa for p in panel])
ymin,ymax = min([p.ya for p in panel]),max([p.ya for p in panel])
xStart,xEnd = xmin-valX*(xmax-xmin),xmax+valX*(xmax-xmin)
yStart,yEnd = ymin-valY*(ymax-ymin),ymax+valY*(ymax-ymin)
size = 10
plt.figure(figsize=(size,(yEnd-yStart)/(xEnd-xStart)*size))
plt.grid(True)
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.plot(xp,yp,'k-',linewidth=2)
plt.plot(np.append([p.xa for p in panel],panel[0].xa),\
        np.append([p.ya for p in panel],panel[0].ya),\
        linestyle='-',linewidth=1,\
        marker='o',markersize=6,color='r');
        
# class Freestream containing the freestream conditions
class Freestream:
	def __init__(self,Uinf,alpha):
		self.Uinf = Uinf                   # velocity magnitude
		self.alpha = alpha*pi/180          # angle of attack (degrees --> radians)
		
#definition of the object freestream
Uinf = 1.0                               # freestream speed
alpha = 5.0                              # angle of attack (in degrees)
freestream = Freestream(Uinf,alpha)      # instantiation of the object freestream

# function to evaluate the integral Iij(zi)
def I(xci,yci,pj,dxdz,dydz):
	def func(s):
		return (+(xci-(pj.xa-sin(pj.beta)*s))*dxdz\
				+(yci-(pj.ya+cos(pj.beta)*s))*dydz)\
			   /((xci-(pj.xa-sin(pj.beta)*s))**2\
			   + (yci-(pj.ya+cos(pj.beta)*s))**2)
	return integrate.quad(lambda s:func(s),0.,pj.length)[0]
	
# function to build the source matrix
def buildMatrix(p):
	N = len(p)
	A = np.empty((N,N),dtype=float)
	np.fill_diagonal(A,0.5)
	for i in range(N):
		for j in range(N):
			if (i!=j):
				A[i,j] = 0.5/pi*I(p[i].xc,p[i].yc,p[j],cos(p[i].beta),sin(p[i].beta))
	return A

# function to build the right hand-side of the linear system
def buildRHS(p,fs):
	N = len(p)
	B = np.zeros(N,dtype=float)
	for i in range(N):
		B[i] = -fs.Uinf*cos(fs.alpha-p[i].beta)
	return B
	
A = buildMatrix(panel)					# calculate the singularity matrix
B = buildRHS(panel,freestream)			# calculate the freestream RHS

# solve the linear system
var = np.linalg.solve(A,B)
for i in range(len(panel)):
	panel[i].sigma = var[i]
	
# function to calculate the tangential velocity at each control point
def getTangentVelocity(p,fs,gamma):
	N = len(p)
	A = np.zeros((N,N),dtype=float)
	for i in range(N):
		for j in range(N):
			if (i!=j):
				A[i,j] = 0.5/pi*I(p[i].xc,p[i].yc,p[j],-sin(p[i].beta),cos(p[i].beta))
	B = fs.Uinf*np.sin([fs.alpha-pp.beta for pp in p])
	var = np.array([pp.sigma for pp in p])
	vt = np.dot(A,var)+B
	for i in range(N):
		p[i].vt = vt[i]
		
getTangentVelocity(panel,freestream,gamma)	# get tangential velocity
# function to calculate the pressure coefficient at each control point
def getPressureCoefficient(p,fs):
	for i in range(len(p)):
		p[i].Cp = 1-(p[i].vt/fs.Uinf)**2

getPressureCoefficient(panel,freestream) # get pressure coefficient

# plotting the coefficient of pressure
valX,valY = 0.1,0.2
xmin,xmax = min([p.xa for p in panel]),max([p.xa for p in panel])
Cpmin,Cpmax = min([p.Cp for p in panel]),max([p.Cp for p in panel])
xStart,xEnd = xmin-valX*(xmax-xmin),xmax+valX*(xmax-xmin)
yStart,yEnd = Cpmin-valY*(Cpmax-Cpmin),Cpmax+valY*(Cpmax-Cpmin)
plt.figure(figsize=(10,6))
plt.grid(True)
plt.xlabel('x',fontsize=16)
plt.ylabel('$C_p$',fontsize=16)
plt.plot([p.xc for p in panel if p.loc=='extrados'],\
		[p.Cp for p in panel if p.loc=='extrados'],\
		'ro-',linewidth=2)
plt.plot([p.xc for p in panel if p.loc=='intrados'],\
		[p.Cp for p in panel if p.loc=='intrados'],\
		'bo-',linewidth=1)
plt.legend(['extrados','intrados'],'best',prop={'size':14})
plt.xlim(xStart,xEnd)
plt.ylim(yStart,yEnd)
plt.gca().invert_yaxis()
plt.title('Number of panels : %d'%len(panel));