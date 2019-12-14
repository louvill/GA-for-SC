import numpy as np
import random

class Combustor:
    def __init__(self, Ttin, Ptin, mfin, Min, stepSize,l, slope, a, targetExitPressure, cpin):
        self.h = 1.2e8
        self.R = 287
        self.cp = cpin
        self.g = cpin/(cpin-self.R)
        self.T = Ttin
        self.P = Ptin
        self.mf = mfin
        self.M = Min
        self.A = self.mf*np.sqrt(self.R*self.T/self.g)/(self.P*self.M)*(1+(self.g-1)/2*self.M**2)**((self.g+1)/(2*(self.g-1)))
        self.v = self.M*np.sqrt(self.g*self.R*self.T/(1+(self.g-1)/2*self.M**2))
        self.stepSize = stepSize
        self.l = l
        self.slope = slope
        self.a = a
        self.targetExitPressure = targetExitPressure
        self.normFuelCoeff()

    def normFuelCoeff(self):
        desiredmf = self.mf*.029
        currentmf = np.trapz(self.a, dx=self.l/(len(self.a)-1))
        self.a = self.a*desiredmf/currentmf

    def calcPerformance(self):
        if type(self.T) == type(1.0):
            Tstat = self.T/(1+(self.g-1)/2*self.M**2)
            Pstat = self.P/(1+(self.g-1)/2*self.M**2)**(self.g/(self.g-1))
        else:
            Tstat = self.T[0][0]/(1+(self.g[0]-1)/2*self.M[0]**2)
            Pstat = self.P[0][0]/(1+(self.g[0]-1)/2*self.M[0]**2)**(self.g[0]/(self.g[0]-1))
        self.T = self.T*np.ones((2, round(self.l/self.stepSize)+1))
        self.T[1][0] = Tstat
        self.P = self.P*np.ones((2, round(self.l/self.stepSize)+1))
        self.P[1][0] = Pstat
        self.mf = self.mf*np.ones(round(self.l/self.stepSize)+1)
        self.M = self.M*np.ones(round(self.l/self.stepSize)+1)
        self.A = self.A*np.ones(round(self.l/self.stepSize)+1)
        self.g = self.g*np.ones(round(self.l/self.stepSize)+1)
        self.v = self.v*np.ones(round(self.l/self.stepSize)+1)
        self.cp = self.cp*np.ones(round(self.l/self.stepSize)+1)
        self.R = self.R*np.ones(round(self.l/self.stepSize)+1)
        
        for i in range(round(self.l/self.stepSize)):
            cpair = (27.453+6.1838*(self.T[1][i]/1000)+.89932*(self.T[1][i]/1000)**2)/28*1000
            cpH2 = (26.896+4.3501*(self.T[1][i]/1000)-.32674*(self.T[1][i]/1000)**2)/2*1000
            gair = cpair/(cpair-self.R[0])
            gH2 = cpH2/(cpH2-4157)
            alpha = (self.mf[i]-self.mf[0])/self.mf[0]
            self.g[i+1] = (gair+alpha*gH2)/(1+alpha)
            self.cp[i+1] = (cpair+alpha*cpH2)/(1+alpha)
            self.R[i+1] = (self.R[0]+alpha*8314/2)/(1+alpha)
            
            dm = (self.interp(i*self.stepSize)+self.interp((i-1)*self.stepSize))/2*self.stepSize 
            self.mf[i+1] = self.mf[i] + dm
            
            dTt = dm*(self.h-self.T[0][i]*self.cp[i+1])/(self.cp[i+1]*self.mf[i+1])
            self.T[0][i+1] = self.T[0][i] + dTt
            
            slopeIndex = int(np.floor(i*self.stepSize*len(self.slope)/self.l))
            dA = 2*np.sqrt(self.A[i]*np.pi)*np.tan(self.slope[slopeIndex])*self.stepSize
            self.A[i+1] = self.A[i] + dA
            
            dM = self.M[i]*(1+(self.g[i]-1)/2*self.M[i]**2)/(1-self.M[i])*(-1/self.A[i]*dA/self.stepSize+\
                (1+self.g[i]*self.M[i]**2)/2*1/self.T[0][i]*dTt/self.stepSize)*self.stepSize
            self.M[i+1] = self.M[i] + dM
            
            self.T[1][i+1] = self.T[0][i+1]/(1+(self.g[i+1]-1)/2*self.M[i+1]**2)
            
            self.P[1][i+1] = self.mf[i+1]/(self.A[i+1]*self.M[i+1])*np.sqrt(self.R[i+1]*self.T[1][i+1]/self.g[i+1])
            self.P[0][i+1] = self.P[1][i+1]*(self.T[0][i+1]/self.T[1][i+1])**(self.g[i+1]/(self.g[i+1]-1))
            #if self.P[0][i+1] > 1e10:
            #    print()
            #    print(self.P[1][i+1])
            #    print(self.T[0][i+1])
            #    print(self.T[1][i+1])
            #    print(self.g[i+1])
            #    print()
            if self.P[0][i+1] < self.targetExitPressure:
                break
            
            self.v[i+1] = self.M[i+1]*np.sqrt(self.g[i+1]*self.R[i+1]*self.T[1][i+1])
        
        if self.P[1][len(self.P)-1] < self.targetExitPressure or min(self.M) < 1.05:
            for j in range(1, len(self.a)-1):
                self.a[j] = random.random()
            for j in range(len(self.slope)):
                self.slope[j] = np.pi/2*random.random()
            self.calcPerformance()
    
    def interp(self, x):
        adx = self.l/(len(self.a)-1)
        a = 0

        if x == self.l:
            a = self.a(len(self.a))
        else:
            for i in range(len(self.a)):
                if i*adx <= x and x < (i+1)*adx: 
                    m = (self.a[i+1]-self.a[i])/adx
                    a = m*(x-adx*i)+self.a[i]
        return a

    def mutateFuelCoeff(self, mutRate):
        for i in range(1, len(self.a)-1):
            if round(mutRate*random.random()) == 0:
                self.a[i] = random.random()*max(self.a)

        self.normFuelCoeff()
    
    def mutateSlope(self, mutRate):
        for i in range(0, len(self.slope)-1):
            if round(mutRate*random.random()) == 0:
                self.slope[i] = random.random()*np.pi/2
    
    def getExitV(self):
        return self.v[len(self.v)-1]
            
    def getSlope(self):
        return self.slope

    def geta(self):
        return self.a
    
    def getT(self):
        return self.T
    
    def getP(self):
        return self.P
    
    def getv(self):
        return self.v
    
    def getM(self):
        return self.M
    
    def getg(self):
        return self.g