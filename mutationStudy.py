import os
import math
import numpy as np
import random
import matplotlib.pyplot as plt
import time
from threading import Thread
from copy import copy
from Combustor import *

def performanceThreads(carray, processNum, numParents, numChildren, numThreads):
    for i in range(round(numChildren/numThreads)):
        carray[round(numChildren/numThreads)*processNum+i+numParents].calcPerformance()
    #print('Thread ' + str(processNum) + ' complete')

def main():
    os.system("cls")

    for iterations in range(10):

        #physcial inputs
        g = 1.4
        T0 = 227
        P0 = 1090
        M0 = 6
        M2 = 2.5
        Tt0 = T0*(1+(g-1)/2*M0**2)
        Pt0 = P0*(1+(g-1)/2*M0**2)**(g/(g-1))
        Pt2 = .7*Pt0
        lt = 2
        cp0 = 1218
        
        #genetic alogrithm parameters
        dx = .01
        numParents = 100
        numChildren = 100
        generationSize = numParents+numChildren
        numGenerations = round(1e1)
        numFuelCoeff = 10
        numSlope = 10
        numThreads = 5
        baseMutationRate = 3

        carray = []

        for i in range(generationSize):
            a = []
            slope = []
            for j in range(numFuelCoeff):
                a.append(5*random.random())
            for j in range(numSlope):
                slope.append(np.pi/4*random.random())
            carray.append(Combustor(Tt0, Pt2, 10, M2, dx, lt, slope, a, P0, cp0))
            carray[i].normFuelCoeff()
            carray[i].calcPerformance()

        for i in range(numGenerations):

            carray.sort(key=lambda Combustor: Combustor.getJetThrust(), reverse=True)

            for j in range(numChildren):
                done = False
                while not done:
                    p1 = round(random.random()*numParents)
                    p2 = round(random.random()*numParents)
                    while p2 == p1:
                        p2 = round(random.random()*numParents)

                    a1 = carray[p1].geta()
                    a2 = carray[p2].geta()
                    anew = []
                    for k in range(len(a1)):
                        if round(random.random()) == 1:
                            anew.append(a1[k])
                        else:
                            anew.append(a2[k])

                    slope1 = carray[p1].getSlope()
                    slope2 = carray[p2].getSlope()
                    slopenew = []
                    for k in range(len(slope1)):
                        if round(random.random()) == 1:
                            slopenew.append(slope1[k])
                        else:
                            slopenew.append(slope2[k])

                    carray[j+numParents].seta(anew)
                    carray[j+numParents].setSlope(slopenew)
                    carray[j+numParents].mutateFuelCoeff(baseMutationRate)
                    carray[j+numParents].mutateSlope(baseMutationRate)

                    if not (np.array_equal(anew, a1) or np.array_equal(anew, a2) or np.array_equal(slopenew, slope1) or\
                        np.array_equal(slopenew, slope2)):
                        done = True

            processes = []

            for j in range(numThreads):
                processes.append(Thread(target=performanceThreads, args=(carray, j, numParents, numChildren, numThreads,)))
                processes[j].start()

            for j in range(len(processes)):
                processes[j].join()

        print(iterations)
        print(carray[0].getJetThrust())

if __name__ == "__main__":
    main()