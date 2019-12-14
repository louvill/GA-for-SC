import os
import math
import numpy as np
import random
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
slope = 10*np.pi/180*np.ones(10)
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

cp0 = 1308

numParents = 20
numChildren = 20
generationSize = numParents+numChildren
numGenerations = round(1e2)
graphUpdateFrequency = 10
numFuelCoeff = 10
baseMutationRate = 5
mutationRate = baseMutationRate

carray = np.empty(generationSize, dtype=Combustor)

for i in range(0, generationSize-1):
    a = np.zeros(numFuelCoeff)
    for j in range(0, numFuelCoeff-1):
        if j == 0 or j == numFuelCoeff-1:
            a[j] = 0
        else:
            a[j] = random.random()

    slope = np.zeros(len(slope))
    for j in range(0, len(slope)-1):
        slope[j] = np.pi/2*random.random()
    carray[i] = Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a, P0, cp0)
    carray[i].calcPerformance()
    print(carray[i].getExitV())
    
genHistory = np.zeros(numGenerations)