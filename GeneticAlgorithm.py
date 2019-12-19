import os
import math
import numpy as np
import random
import matplotlib.pyplot as plt
from threading import Thread
from copy import copy
from Combustor import *

def performanceThreads(carray, processNum, numParents, numChildren, numThreads):
    for i in range(round(numChildren/numThreads)):
        carray[round(numChildren/numThreads)*processNum+i+numParents].calcPerformance(0)
    print('Thread ' + str(processNum) + ' complete')

def main():
    os.system("cls")

    #inputs
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
    dx = .005
    numParents = 50
    numChildren = 50
    generationSize = numParents+numChildren
    numGenerations = round(1e3)
    numFuelCoeff = 5
    numSlope = 5
    numThreads = 10
    baseMutationRate = 7

    carray = []

    #population initialization
    print('Initializing combustor array...')
    for i in range(generationSize):
        #complete = False
        #while not complete:
        a = []
        slope = []
        for j in range(numFuelCoeff):
            a.append(5*random.random())
        for j in range(numSlope):
            slope.append(np.pi/4*random.random())
        carray.append(Combustor(Tt0, Pt2, 100, M2, dx, lt, slope, a, P0, cp0))
        carray[i].normFuelCoeff()
        carray[i].calcPerformance(0)
        #    if carray[i].getExitV() > -1:
        #        complete = True
        print('Element ' + str(i+1) + ' initialized with exit velocity of ' + str(carray[i].getExitV()))
        #print(carray[i].geta())
   
    genHistory = np.zeros(numGenerations)

    for i in range(numGenerations):
        print('Current Generation: ' + str(i+1))

        carray.sort(key=lambda Combustor: Combustor.getExitV(), reverse=True)

        #generation performance
        genHistory[i] = carray[0].getExitV()
        for j in range(numChildren+numParents):
            #carray[j].calcPerformance()
            print('Exit velocity for element ' + str(j+1) + ': ' + str(carray[j].getExitV()))
            #print(carray[j].geta())
            #print(j)

        #input('Press enter')

        for j in range(numChildren):
            p1 = round(random.random()*numParents)
            p2 = round(random.random()*numParents)
            while p2 == p1:
                p2 = round(random.random()*numParents)

            #print(p1)
            #print(p2)

            a1 = carray[p1].geta()
            a2 = carray[p2].geta()
            #print(carray[p1].geta())
            #print(carray[p2].geta())
            #xop = round(random.random()*(len(a1)-2))+1
            #a1 = np.concatenate((a1[0:xop],a2[xop:len(a2)]))
            for k in range(len(a1)):
                if round(random.random()) == 1:
                    a1[k] = a2[k]
            #print(a1)

            slope1 = carray[p1].getSlope()
            slope2 = carray[p2].getSlope()
            #print(slope1)
            #print(slope2)
            #xop = round(random.random()*(len(slope1)-1))
            #slope1 = np.concatenate((slope1[0:xop],slope2[xop:len(slope2)]))
            for k in range(len(slope1)):
                if round(random.random()) == 1:
                    slope1[k] = slope2[k]
            #print(slope1)

            carray[j+numParents].seta(a1)
            carray[j+numParents].setSlope(slope1)
            carray[j+numParents].mutateFuelCoeff(baseMutationRate)
            #print(carray[j+numParents].geta())
            carray[j+numParents].mutateSlope(baseMutationRate)

        
        processes = np.empty(numThreads, dtype=Thread)

        for j in range(len(processes)):
            processes[j] = Thread(target=performanceThreads, args=(carray, j, numParents, numChildren, numThreads,))
            processes[j].start()
            print('Thread ' + str(j) + ' started')

        for j in range(len(processes)):
            processes[j].join()

        #input('Press enter')

    print(carray[0].geta())
    print(carray[0].getSlope())

    figNum = 0

    plt.figure(1)
    plt.subplot(4,2,1)
    plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getM())
    plt.subplot(4,2,2)
    plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getT()[0])
    plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getT()[1])
    plt.subplot(4,2,3)
    plt.semilogy(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getP()[0])
    plt.semilogy(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getP()[1])
    plt.subplot(4,2,4)
    plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getv())
    plt.subplot(4,2,5)
    plt.plot(np.linspace(1,len(genHistory),len(genHistory)),genHistory)
    plt.subplot(4,2,6)
    plt.plot(np.linspace(0,lt,len(carray[figNum].geta())),carray[figNum].geta())
    plt.subplot(4,2,7)
    plt.plot(np.linspace(0,lt,len(carray[figNum].getg())),carray[figNum].getg())
    plt.subplot(4,2,8)
    plt.plot(np.linspace(0,lt,len(carray[figNum].getA())),carray[figNum].getA())
    plt.show()

if __name__ == "__main__":
    main()