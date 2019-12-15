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
dx = .001
lt = 2


#def f(x):
#    f1 = (27.453+6.1838*(x[2]/1000)+.89932*(x[2]/1000)**2)/28.*1000.
#    f2 = x[0]/(x[0]-287)
#    f3 = Tt0/(1.+(x[1]-1.)/2.*M2**2)
#    return [f1, f2, f3]

#guess = np.array([1200, 1.3, 950])
#print(f([1218,1.308,948.5]))
#guess = np.array([1000,1,1000])
#z = newton_krylov(f, guess)
#print(z)

cp0 = 1218

numParents = 20
numChildren = 20
generationSize = numParents+numChildren
numGenerations = round(1e3)
graphUpdateFrequency = 10
numFuelCoeff = 5
numSlope = 5
baseMutationRate = 5
mutationRate = baseMutationRate

carray = np.empty(generationSize, dtype=Combustor)

print('Initializing combustor array...')
for i in range(generationSize):
    a = np.zeros(numFuelCoeff)
    for j in range(1,numFuelCoeff-1):
        a[j] = random.random()
    slope = np.zeros(numSlope)
    for j in range(0, numSlope):
        slope[j] = np.pi/4*random.random()
    carray[i] = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a, P0, cp0)
    carray[i].calcPerformance()
    #print(carray[i].getExitV())
    
genHistory = np.zeros(numGenerations)

for i in range(numGenerations):
    print('Current Generation: ' + str(i+1))

    sortComplete = False
    while not sortComplete:
        sortComplete = True
        for j in range(len(carray)-1):
            if carray[j].getExitV() < carray[j+1].getExitV():
                ctemp = copy(carray[j])
                carray[j] = copy(carray[j+1])
                carray[j+1] = copy(ctemp)
                sortComplete = False

    for j in range(1):
        print('Exit velocity for element ' + str(j+1) + ': ' + str(carray[j].getExitV()))

    genHistory[i] = carray[0].getExitV()

    #plt.show()

    for j in range(numParents, generationSize):
        done = False
        while not done:
            p1 = round(random.random()*numParents)
            p2 = round(random.random()*numParents)
            while p2 == p1:
                p2 = round(random.random()*numParents)

            a1 = carray[p1].geta()
            a2 = carray[p2].geta()
            xop = round(random.random()*(len(a)-2))+1
            a1 = np.concatenate((a1[0:xop],a2[xop:len(a2)]))

            slope1 = carray[p1].getSlope()
            slope2 = carray[p2].getSlope()
            xop = round(random.random()*(len(slope1)-1))
            slope1 = np.concatenate((slope1[0:xop],slope2[xop:len(slope2)]))

            #if not np.array_equal(carray[p1].geta(),a1) and not np.array_equal(carray[p2].geta(),a1):
            #    done = True

            carray[j] = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a1, P0, cp0)
            carray[j].mutateFuelCoeff(3)
            carray[j].normFuelCoeff()
            carray[j].mutateSlope(3)
            carray[j].calcPerformance()

            done = True

print(carray[0].geta())
print(carray[0].getSlope())

plt.figure(1)
plt.subplot(4,2,1)
plt.plot(np.linspace(0,lt,len(carray[0].getM())),carray[0].getM())
plt.subplot(4,2,2)
plt.plot(np.linspace(0,lt,len(carray[0].getM())),carray[0].getT()[0])
plt.plot(np.linspace(0,lt,len(carray[0].getM())),carray[0].getT()[1])
plt.subplot(4,2,3)
plt.semilogy(np.linspace(0,lt,len(carray[0].getM())),carray[0].getP()[0])
plt.semilogy(np.linspace(0,lt,len(carray[0].getM())),carray[0].getP()[1])
plt.subplot(4,2,4)
plt.plot(np.linspace(0,lt,len(carray[0].getM())),carray[0].getv())
plt.subplot(4,2,5)
plt.plot(np.linspace(1,len(genHistory),len(genHistory)),genHistory)
plt.subplot(4,2,6)
plt.plot(np.linspace(0,lt,len(carray[0].geta())),carray[0].geta())
plt.subplot(4,2,7)
plt.plot(np.linspace(0,lt,len(carray[0].getg())),carray[0].getg())
plt.subplot(4,2,8)
plt.plot(np.linspace(0,lt,len(carray[0].getA())),carray[0].getA())
plt.show()