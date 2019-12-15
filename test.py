import os
import math
import numpy as np
import random
import matplotlib.pyplot as plt
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
dx = .01
lt = 2

cp0 = 1218

a = [0., 0.11797875, 0.9066613, 0.28873165, 0.]
slope = [0.47035953, 0.41312728, 0.20191052, 0.60060712, 0.65053426]

c = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a, P0, cp0)
c.calcPerformance()
print(c.geta())

plt.figure(1)
plt.subplot(4,2,1)
plt.plot(np.linspace(0,lt,len(c.getM())),c.getM())
plt.subplot(4,2,2)
plt.plot(np.linspace(0,lt,len(c.getM())),c.getT()[0])
plt.plot(np.linspace(0,lt,len(c.getM())),c.getT()[1])
plt.subplot(4,2,3)
plt.semilogy(np.linspace(0,lt,len(c.getM())),c.getP()[0])
plt.semilogy(np.linspace(0,lt,len(c.getM())),c.getP()[1])
plt.subplot(4,2,4)
plt.plot(np.linspace(0,lt,len(c.getM())),c.getv())
plt.subplot(4,2,6)
plt.plot(np.linspace(0,lt,len(c.geta())),c.geta())
plt.subplot(4,2,7)
plt.plot(np.linspace(0,lt,len(c.getg())),c.getg())
plt.subplot(4,2,8)
plt.plot(np.linspace(0,lt,len(c.getA())),c.getA())
plt.show()