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
    print('Thread ' + str(processNum) + ' complete')

def main():
    os.system("cls")

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
    dx = .0025
    #numParents = 240
    #numChildren = 360
    numParents = 200
    numChildren = 20
    generationSize = numParents+numChildren
    numGenerations = round(1e3)
    numFuelCoeff = 5
    numSlope = 4
    numThreads = 5
    baseMutationRate = 30

    carray = []

    #population initialization
    print('Initializing combustor array...')
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
        print('Element ' + str(i+1) + ' initialized with jet thrust of ' + str(carray[i].getJetThrust()))

    #algorithm performance metrics
    genHistory = []
    startTime = time.time()

    for i in range(numGenerations):
        print('Current Generation: ' + str(i+1))

        #population sort
        carray.sort(key=lambda Combustor: Combustor.getJetThrust(), reverse=True)

        #generation performance reporting
        genHistory.append(carray[0].getJetThrust())
        for j in range(10):
            print('Jet thrust for element ' + str(j+1) + ': ' + str(carray[j].getJetThrust()))

        #breeding
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

        #performance calculations
        processes = []

        for j in range(numThreads):
            processes.append(Thread(target=performanceThreads, args=(carray, j, numParents, numChildren, numThreads,)))
            processes[j].start()
            print('Thread ' + str(j) + ' started')

        for j in range(len(processes)):
            processes[j].join()

        #plotting
        figNum = 0
        plt.figure(1)
        plt.clf()
        plt.subplot(4,2,1)
        plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getM())
        plt.grid()
        plt.subplot(4,2,2)
        plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getT()[0])
        plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getT()[1])
        plt.grid()
        plt.subplot(4,2,3)
        plt.semilogy(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getP()[0])
        plt.semilogy(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getP()[1])
        plt.grid()
        plt.subplot(4,2,4)
        plt.plot(np.linspace(0,lt,len(carray[figNum].getM())),carray[figNum].getv())
        plt.grid()
        plt.subplot(4,2,5)
        plt.semilogx(np.linspace(1,len(genHistory),len(genHistory)),genHistory)
        plt.grid()
        plt.subplot(4,2,6)
        plt.plot(np.linspace(0,lt,len(carray[figNum].geta())),carray[figNum].geta())
        plt.grid()
        plt.subplot(4,2,7)
        plt.plot(np.linspace(0,lt,len(carray[figNum].getg())),carray[figNum].getg())
        plt.grid()
        plt.subplot(4,2,8)
        plt.plot(np.linspace(0,lt,len(carray[figNum].getA())),carray[figNum].getA())
        plt.grid()
        #diagnostic graphs
        #plt.subplot(4,2,6)
        #plt.plot(np.linspace(0,lt,len(carray[figNum].getdA())),carray[figNum].getdA())
        #plt.grid()
        #plt.subplot(4,2,7)
        #plt.plot(np.linspace(0,lt,len(carray[figNum].getdM()[0])),carray[figNum].getdM()[0])
        #plt.plot(np.linspace(0,lt,len(carray[figNum].getdM()[0])),carray[figNum].getdM()[1])
        #plt.plot(np.linspace(0,lt,len(carray[figNum].getdM()[0])),carray[figNum].getdM()[2])
        #plt.grid()
        #plt.subplot(4,2,8)
        #plt.plot(np.linspace(0,lt,len(carray[figNum].getdTt())),carray[figNum].getdTt())
        #plt.grid()

        plt.pause(.01)

    #runtime report
    print(time.time()-startTime)

    #most fit genes
    print(carray[0].geta())
    print(carray[0].getSlope())

    plt.show()

if __name__ == "__main__":
    main()