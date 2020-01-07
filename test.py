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
#PC0 = 1218
#
#a = [0., 4.14776075, 1.51784091, 0.13439834, 0.]
#slope = [0.29116983, 0.46104977, 0.06263356, 0.58965015, 0.28638954]
#
#c = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a, P0, PC0)
#c.calPCerformance()
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
#
#from threading import Thread
#from multiprocessing.pool import ThreadPool
#import numpy as np
#import time
#
#def test(a, x, b):
#    print(a[x])
#    a[x] = b
#    print(a[x])
#
#def main():
#    pool = ThreadPool(2)
#
#    a = [1, 2]
#    #processes = np.empty(len(a), dtype=Thread)
#    for i in range(len(a)):
#        #processes[i] = Thread(target=test, args=(a, i, 3,))
#        #processes[i].start()
#        pool.map(test, [a, i, 3])
#
#    #for i in range(len(a)):
#    #    processes[i].join()
#    #    print(a[i])
#
#    #for i in range(10):
    #    print(round(random.random())==1)

#if __name__ == "__main__":
#    main()

#good result:
#
#[0.         3.25806123 0.24854106 3.48403672 1.8945325  2.38851093
# 0.77314638 0.8736639  0.12950727 0.        ]
#[0.0438278  0.16419715 0.40768724 0.61148441 0.46664118 0.62414804
# 0.57921686 0.66262119 0.74333283 0.77133125]

import matplotlib.pyplot as plt
import numpy as np
import csv
import os

os.system("cls")

P = []
C = []
G = []
t = []
EJT = []
PC = []
S = []

with open('bowhisker.csv') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            P.append(float(row[0]))
            C.append(float(row[1]))
            G.append(float(row[2]))
            t.append(float(row[3]))
            EJT.append(float(row[4]))
            PC.append(float(row[5])*100)
            S.append(float(row[6]))
            line_count += 1
        else:
            line_count += 1

plt.figure(1)
#data = np.concatenate((S,C))
#plt.boxplot([S[0:20],S[20:40],S[40:60],S[60:80],S[80:100]],positions=[1,4,7])
#plt.boxplot([S[100:120],S[120:140],S[140:160],S[160:180],S[180:200]],positions=[2,5,8])
plt.boxplot([PC[0:20],PC[100:120],PC[200:220]],positions=[1,2,3])
plt.boxplot([PC[20:40],PC[120:140],PC[220:240]],positions=[5,6,7])
plt.boxplot([PC[40:60],PC[140:160],PC[240:260]],positions=[9,10,11])
plt.boxplot([PC[60:80],PC[160:180],PC[260:280]],positions=[13,14,15])
plt.boxplot([PC[80:100],PC[180:200],PC[280:300]],positions=[17,18,19])
plt.xlim((0,20))
plt.xticks([1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],['10, 20 Parents','10, 30 Parents','10, 40 Parents','20, 20 Parents',\
    '20, 30 Parents','20, 40 Parents','30, 20 Parents','30, 30 Parents','30, 40 Parents','40, 20 Parents','40, 30 Parents',\
    '40, 40 Parents','50, 20 Parents','50, 30 Parents','50, 40 Parents'],rotation=90)
plt.ylabel('Convergence Rate Score')
#plt.xlim((0,9))
#plt.xticks([.5,1.5,2.5,3.5,4.5],[10,20.30,40,50])
plt.show()