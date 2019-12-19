#import os
#import math
#import numpy as np
import random
#import matplotlib.pyplot as plt
#from copy import copy
#from Combustor import *
#
#os.system("cls")
#
#g = 1.4
#T0 = 227
#P0 = 1090
#M0 = 6
#M2 = 2.5
#Tt0 = T0*(1+(g-1)/2*M0**2)
##print(Tt0)
#Pt0 = P0*(1+(g-1)/2*M0**2)**(g/(g-1))
#Pt2 = .7*Pt0
##slope = 10*np.pi/180*np.ones(4)
#dx = .001
#lt = 2
#
#cp0 = 1218
#
#a = [0., 4.14776075, 1.51784091, 0.13439834, 0.]
#slope = [0.29116983, 0.46104977, 0.06263356, 0.58965015, 0.28638954]
#
#c = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a, P0, cp0)
#c.calcPerformance()
##print(c.geta())
#
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
#plt.plot(np.linspace(0,lt,len(c.getMassFlow())),c.getMassFlow())
#plt.subplot(4,2,6)
#plt.plot(np.linspace(0,lt,len(c.geta())),c.geta())
#plt.subplot(4,2,7)
#plt.plot(np.linspace(0,lt,len(c.getg())),c.getg())
#plt.subplot(4,2,8)
#plt.plot(np.linspace(0,lt,len(c.getA())),c.getA())
#plt.show()

from threading import Thread
import numpy as np
import time

def test(a, x, b):
    print(a[x])
    a[x] = b
    print(a[x])

def main():
    a = [1, 2]
    processes = np.empty(len(a), dtype=Thread)
    for i in range(len(a)):
        processes[i] = Thread(target=test, args=(a, i, 3,))
        processes[i].start()

    for i in range(len(a)):
        processes[i].join()
        print(a[i])

    for i in range(10):
        print(round(random.random())==1)

if __name__ == "__main__":
    main()

#good result:
#
#[0.         3.25806123 0.24854106 3.48403672 1.8945325  2.38851093
# 0.77314638 0.8736639  0.12950727 0.        ]
#[0.0438278  0.16419715 0.40768724 0.61148441 0.46664118 0.62414804
# 0.57921686 0.66262119 0.74333283 0.77133125]