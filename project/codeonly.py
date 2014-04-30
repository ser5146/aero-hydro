#code from project
#used this to compare plots quickly
import numpy as np
import matplotlib.pyplot as plt
from math import *

class Readairfoil:
    def __init__(self,filename):
        self.filename = filename
        self.readcoordinates()
        
    def readcoordinates(self):
        coords = np.loadtxt(self.filename)
        self.x = coords[:,0]
        self.y = coords[:,1]
        self.N = len(self.x)
                
    def plot(self,figNum,color,style,width):
        plt.figure(num=figNum)
        plt.grid(True)
        plt.xlabel('x',fontsize=12)
        plt.ylabel('y',fontsize=12)
        plt.plot(self.x,self.y,c=color,ls=style,lw=width)
        plt.axis('equal')
        plt.xlim(0,1)
airfoil = Readairfoil('../project/faired7%.dat')
airfoil.plot(figNum=0,color='k',style='-',width=1.5)

class section:
    def __init__(self,foil,xle,yle,zle,chord):
        self.xle = xle
        self.yle = yle
        self.zle = zle
        self.chord = chord
        self.getcoordinates(foil)
        self.xte = max(self.x)
        self.yte = self.y[self.x.argmax(axis=0)]
        self.zte = self.yle*np.ones(len(self.x))
    
    def getcoordinates(self,f):
        self.x = self.xle + self.chord*(+f.x)
        self.z = self.yle + self.chord*(+f.y)
        self.y = self.yle*np.ones(len(self.x))

class Topview:
    def __init__(self,topview):
        self.x = 'y'
        self.y = 'x'

class Wing:
    def __init__(self,name):
        self.name = name
        self.sections = []
        self.method = {}
        self.alpha = 0.
    
    def append(self,section):
        self.sections.append(section)
    
    def plot(self,fignum,color,style,width):
        plt.figure(num=fignum,figsize= (12,10))
        plt.grid(True)
        plt.xlabel('y',fontsize=12)
        plt.ylabel('x',fontsize=12)
        plt.axis('equal')
        for s in self.sections:
            plt.plot(s.y,s.x,c=color,ls=style)
        for i in range(len(self.sections)-1):
            plt.plot([self.sections[i].yle,self.sections[i+1].yle],\
                         [self.sections[i].xle,self.sections[i+1].xle],\
                         c=color,lw=width,ls=style)
            plt.plot([self.sections[i].yte,self.sections[i+1].yte],\
                         [self.sections[i].xte,self.sections[i+1].xte],\
                         c=color,lw=width,ls=style)
        plt.ylim(1.5,-1.5)
        print color+style+'('+str(width)+')',':',self.name
    
    def addresults(self,meth,filename):
        data = np.loadtxt(filename,skiprows=8)
        self.method[meth]=np.array\
        ([data[:,0],data[:,1],data[:,4],data[:,11]])
        #[:,0]-alpha,[:,1]-CL,[:,4]-CD,[:,11]-XCP

wing = {}

name = 'bennettbase'
wing[name] = Wing(name)
# parameters: airfoil,xle,yle,zle,chord
wing[name].append(section(airfoil,-0.110, 0.000, 0., 0.600))
wing[name].append(section(airfoil,-0.112, 0.210, 0., 0.850))
wing[name].append(section(airfoil,-0.115, 0.512, 0., 0.610))
wing[name].append(section(airfoil,-0.118, 0.816, 0., 0.485))
wing[name].append(section(airfoil,-0.120, 1.123, 0., 0.410))
wing[name].append(section(airfoil,-0.105, 1.601, 0., 0.363))
wing[name].append(section(airfoil,-0.035, 2.033, 0., 0.320))
wing[name].append(section(airfoil,+0.100, 2.465, 0., 0.255))
wing[name].append(section(airfoil,+0.240, 2.683, 0., 0.180))
wing[name].append(section(airfoil,+0.450, 2.900, 0., 0.030))

name = 'bennett200'
wing[name] = Wing(name)
# parameters: airfoil,xle,yle,zle,chord
wing[name].append(section(airfoil,-0.110, 0.000, 0., 0.600))
wing[name].append(section(airfoil,-0.112, 0.210, 0., 0.850))
wing[name].append(section(airfoil,-0.150, 0.512, 0., 0.610))
wing[name].append(section(airfoil,-0.174, 0.816, 0., 0.485))
wing[name].append(section(airfoil,-0.197, 1.123, 0., 0.410))
wing[name].append(section(airfoil,-0.215, 1.601, 0., 0.363))
wing[name].append(section(airfoil,-0.175, 2.033, 0., 0.320))
wing[name].append(section(airfoil,-0.070, 2.465, 0., 0.255))
wing[name].append(section(airfoil,+0.055, 2.683, 0., 0.180))
wing[name].append(section(airfoil,+0.250, 2.900, 0., 0.030))

name = 'bennett400'
wing[name] = Wing(name)
# parameters: airfoil,xle,yle,zle,chord
wing[name].append(section(airfoil,-0.110, 0.000, 0., 0.600))
wing[name].append(section(airfoil,-0.141, 0.210, 0., 0.850))
wing[name].append(section(airfoil,-0.186, 0.512, 0., 0.610))
wing[name].append(section(airfoil,-0.231, 0.816, 0., 0.485))
wing[name].append(section(airfoil,-0.275, 1.123, 0., 0.410))
wing[name].append(section(airfoil,-0.326, 1.601, 0., 0.363))
wing[name].append(section(airfoil,-0.315, 2.033, 0., 0.320))
wing[name].append(section(airfoil,-0.240, 2.465, 0., 0.255))
wing[name].append(section(airfoil,-0.130, 2.683, 0., 0.180))
wing[name].append(section(airfoil,+0.050, 2.900, 0., 0.030))

name = 'bennett600'
wing[name] = Wing(name)
# parameters: airfoil,xle,yle,zle,chord
wing[name].append(section(airfoil,-0.110, 0.000, 0., 0.600))
wing[name].append(section(airfoil,-0.155, 0.210, 0., 0.850))
wing[name].append(section(airfoil,-0.221, 0.512, 0., 0.610))
wing[name].append(section(airfoil,-0.287, 0.816, 0., 0.485))
wing[name].append(section(airfoil,-0.352, 1.123, 0., 0.410))
wing[name].append(section(airfoil,-0.436, 1.601, 0., 0.363))
wing[name].append(section(airfoil,-0.456, 2.033, 0., 0.320))
wing[name].append(section(airfoil,-0.410, 2.465, 0., 0.255))
wing[name].append(section(airfoil,-0.315, 2.683, 0., 0.180))
wing[name].append(section(airfoil,-0.150, 2.900, 0., 0.030))

name = 'bennett700'
wing[name] = Wing(name)
# parameters: airfoil,xle,yle,zle,chord
wing[name].append(section(airfoil,-0.110, 0.000, 0., 0.600))
wing[name].append(section(airfoil,-0.163, 0.210, 0., 0.850))
wing[name].append(section(airfoil,-0.239, 0.512, 0., 0.610))
wing[name].append(section(airfoil,-0.315, 0.816, 0., 0.485))
wing[name].append(section(airfoil,-0.391, 1.123, 0., 0.410))
wing[name].append(section(airfoil,-0.491, 1.601, 0., 0.363))
wing[name].append(section(airfoil,-0.526, 2.033, 0., 0.320))
wing[name].append(section(airfoil,-0.495, 2.465, 0., 0.255))
wing[name].append(section(airfoil,-0.408, 2.683, 0., 0.180))
wing[name].append(section(airfoil,-0.250, 2.900, 0., 0.030))

name = 'bennett800'
wing[name] = Wing(name)
# parameters: airfoil,xle,yle,zle,chord
wing[name].append(section(airfoil,-0.110, 0.000, 0., 0.600))
wing[name].append(section(airfoil,-0.170, 0.210, 0., 0.850))
wing[name].append(section(airfoil,-0.256, 0.512, 0., 0.610))
wing[name].append(section(airfoil,-0.343, 0.816, 0., 0.485))
wing[name].append(section(airfoil,-0.430, 1.123, 0., 0.410))
wing[name].append(section(airfoil,-0.547, 1.601, 0., 0.363))
wing[name].append(section(airfoil,-0.596, 2.033, 0., 0.320))
wing[name].append(section(airfoil,-0.580, 2.465, 0., 0.255))
wing[name].append(section(airfoil,-0.500, 2.683, 0., 0.180))
wing[name].append(section(airfoil,-0.350, 2.900, 0., 0.030))

num=4
wing['bennettbase'].plot(fignum=num,color='k',style='-',width=2)
wing['bennett200'].plot(fignum=num,color='b',style='-',width=2)
wing['bennett400'].plot(fignum=num,color='g',style='-',width=2)
wing['bennett600'].plot(fignum=num,color='r',style='-',width=2)
wing['bennett700'].plot(fignum=num,color='m',style='-',width=2)
wing['bennett800'].plot(fignum=num,color='c',style='-',width=2)