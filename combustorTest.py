import os
import math
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy import signal
from threading import Thread
from copy import copy
from Combustor import *

os.system("cls")

g = 1.4
T0 = 227
P0 = 1090
M0 = 6
M2 = 2.5
Tt0 = T0*(1+(g-1)/2*M0**2)
#print(Tt0)
Pt0 = P0*(1+(g-1)/2*M0**2)**(g/(g-1))
Pt2 = .7*Pt0
#slope = 10*np.pi/180*np.ones(4)
dx = .0025
lt = 2
cp0 = 1218

#converged, 9 genes
a = [0.24395064033494865, 0.1300407062762727, 0.1493453735976764, 0.17515586838460237, 0.006965463147948475]
slope = [0.04623280000829522, 0.13941282383204998, 0.1864306391438446, 0.44350705374427146]

#converged, 7 genes
#a = [0.163627871, 0.172610837, 0.165539379, 0.156268606, 0.007534485]
#slope = [0.02972402, 0.156326438, 0.191381729, 0.426490538]

#converged, 5 genes
#a = [0.059919566, 0.255296647, 0.00948714]
#slope = [0.060142298, 0.379918576]
#a = [.05, .1, .05]
#slope = [10*3.14/180, 20*3.14/180]

s1 = []
s2 = []

for i in range(len(slope)):
    #if i < 1:
    #    s1.append(0)
    #    s2.append(slope[i])
    #else:
    #    loc = lt/len(slope)*i
    #    s1.append(loc)
    #    s1.append(loc)
    #    s2.append(slope[i-1])
    #    s2.append(slope[i])
    loc1 = lt/len(slope)*i
    loc2 = lt/len(slope)*(i+1)
    s1.append(loc1)
    s1.append(loc2)
    s2.append(slope[i])
    s2.append(slope[i])


#coriginal = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a, P0, cp0)
#coriginal.calcPerformance()

c = Combustor(Tt0, Pt2, 10, M2, dx, lt, slope, a, P0, cp0)
c.calcPerformance()
print(c.getJetThrust())
#aprime = signal.savgol_filter(coriginal.geta(),11,10)
#slopeprime = signal.savgol_filter(coriginal.geta(),11,10)

#c = Combustor(Tt0, Pt2, 100, M2, dx, lt, slopeprime, aprime, P0, cp0)

plt.figure(1)
plt.subplot(3,2,1)
plt.plot(np.linspace(0,lt,len(c.getM())),c.getM(),color='black')
plt.ylabel('Mach Number')
plt.xlabel('Distance Along Flowpath (m)')
plt.subplot(3,2,2)
plt.plot(np.linspace(0,lt,len(c.getM())),c.getT()[0],color='black')
plt.plot(np.linspace(0,lt,len(c.getM())),c.getT()[1],color='black',linestyle='--')
plt.legend(['Total','Static'],loc='upper left')
plt.xlabel('Distance Along Flowpath (m)')
plt.ylabel('Temperature, K')
plt.subplot(3,2,3)
plt.semilogy(np.linspace(0,lt,len(c.getM())),c.getP()[0],color='black')
plt.semilogy(np.linspace(0,lt,len(c.getM())),c.getP()[1],color='black',linestyle='--')
plt.legend(['Total','Static'],loc='lower left')
plt.xlabel('Distance Along Flowpath (m)')
plt.ylabel('Pressure, Pa')
plt.subplot(3,2,4)
plt.plot(np.linspace(0,lt,len(c.getM())),c.getv(),color='black')
plt.xlabel('Distance Along Flowpath (m)')
plt.ylabel('Velocity, m/s')
plt.subplot(3,2,5)
plt.plot(np.linspace(0,lt,len(c.getM())),c.getMassFlow(),color='black')
plt.xlabel('Distance Along Flowpath (m)')
plt.ylabel('Total Mass Flow Rate, kg/s')
plt.subplot(3,2,6)
plt.plot(np.linspace(0,lt,len(c.getg())),c.getg(),color='black')
plt.xlabel('Distance Along Flowpath (m)')
plt.ylabel('$\mathregular{\gamma}$')
plt.show()

plt.figure(2)
plt.subplot(1,2,1)
plt.plot(np.linspace(0,lt,len(c.getA())),c.getA(),color='black')
plt.plot(s1,s2,linestyle='--',color='black')
plt.xlabel('Distance Along Flowpath (m)')
plt.legend(['Cross-sectional Area, m^2','Local Wall Slope, radians'],loc='upper left')
plt.subplot(1,2,2)
plt.plot(np.linspace(0,lt,len(c.geta())),c.geta(),color='black')
plt.xlabel('Distance Along Flowpath (m)')
plt.ylabel('Fuel Addition Coefficient')
plt.show()


