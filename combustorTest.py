import os
import math
import numpy as np
import random
import matplotlib.pyplot as plt
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
dx = .005
lt = 2
cp0 = 1218

#a1 = [0, 2.00604e-06, 1.68778e-01, 2.09479e-01, 1.038647, 8.31101, 1.70367e-01, 3.14518, 6.53232e-03, 0]
a2 = [0, .1, .1, .1, .1, .1, .1, .1, .1, 0]
slope1 = [0.32618688, 0.4646109, 0.59741923, 0.59728165, 0.31057739, 0.22601837, 0.35792988, 0.46239392, 0.10119357, 0.67869688]
#a2 = [0., 0.26407752, 2.40385772, 2.52501919, 0.67906279, 2.58592853, 0.88182265, 2.44289154, 1.26734006, 0.]
a1 = [0, .1, .2, .3, .4, .5, .6, .7, .8, 0]
slope2 = [0.14590859, 0.48537457, 0.55913541, 0.48341576, 0.49775156, 0.69032791, 0.71117747, 0.05999473, 0.58580791, 0.30709216]

c = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope1, a1, P0, cp0)
c.calcPerformance()

c2 = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope2, a2, P0, cp0)
c2.calcPerformance()

array = [c, c2]

print(array[0])
print(array[1])

print(array[0].geta())
print(array[1].geta())

print(array[0].getExitV())
print(array[1].getExitV())

#array = sorted(array, key=lambda Combustor: Combustor.getExitV(), reverse=True)
array.sort(key=lambda Combustor: Combustor.getExitV(), reverse=True)

print('sorted')

print(array[0])
print(array[1])

print(array[0].geta())
print(array[1].geta())

print(array[0].getExitV())
print(array[1].getExitV())

#plt.figure(1)
#plt.subplot(4,2,1)
#plt.plot(np.linspace(0,lt,len(c.getM())),c.getM())
#plt.subplot(4,2,2)
#plt.plot(np.linspace(0,lt,len(c.getM())),c.getT()[0])
#plt.plot(np.linspace(0,lt,len(c.getM())),c.getT()[1])
#plt.subplot(4,2,3)
#plt.semilogy(np.linspace(0,lt,len(c.getM())),c.getP()[0])
#plt.semilogy(np.linspace(0,lt,len(c.getM())),c.getP()[1])
#plt.subplot(4,2,4)
#plt.plot(np.linspace(0,lt,len(c.getM())),c.getv())
#plt.subplot(4,2,5)
#plt.plot(np.linspace(0,lt,len(c.getM())),c.getMassFlow())
#plt.subplot(4,2,6)
#plt.plot(np.linspace(0,lt,len(c.geta())),c.geta())
#plt.subplot(4,2,7)
#plt.plot(np.linspace(0,lt,len(c.getg())),c.getg())
#plt.subplot(4,2,8)
#plt.plot(np.linspace(0,lt,len(c.getA())),c.getA())
#plt.show()
#