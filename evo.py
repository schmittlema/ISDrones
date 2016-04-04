import numpy  as np
import random as r
import pylab as pl
import copy as cp
import math as m

color={0:'b-',1:'g-',2:'r-',3:'m-',4:'y-'}

def MatrixCreate(x,y):
     return np.zeros([x, y], float)

def MatrixRandomize(x):
    #x is a list
    i=0
    while i<len(x):
        x[i] = r.random()
        i=i+1
    return x

def MatrixRandomizeNeg(z):
    #x is a list;
    x= cp.deepcopy(z)
    i=0
    while i<len(x):
        for j in range(0,len(x[0,:])):
            x[i,j] = r.uniform(-1,1)
        i=i+1
    return x

def Fitness(x):
    #x is a matrix
    global neuronValues
    global desiredNeuronValues
    global actualNeuronValues
    f = 0
    neuronValues=MatrixCreate(10,10)
    for i in range(0,10):
        neuronValues[0,i]=0.5
    for i in range(1,10):
        neuronValues=NeuronUpdate(neuronValues,x,i)
    actualNeuronValues = neuronValues[9,:]
    f = (1-(MeanDistance(desiredNeuronValues,actualNeuronValues)))
    return f

def Fitness2(x):
    #x is a matrix
    global neuronValues
    dif = 0
    neuronValues=MatrixCreate(10,10)
    for i in range(0,10):
        neuronValues[0,i]=0.5
    for j in range(1,10):
        neuronValues=NeuronUpdate(neuronValues,x,j)
    dif=AverageDistance(neuronValues)
    return dif

def MatrixPerturb(p,y):
    #p is a matrix
    c=cp.deepcopy(p)
    for i in range(0,len(c[0,:])):
        for n in range(0,len(c[:,0])):
            if (r.random()< y):
                c[i,n]=r.random()
    return c

def PlotVectorAsLine(x):
    #x is a matrix
    pl.figure()
    pl.plot(x)

def NeuronUpdate(value,s,i):
     z = 0
     val = cp.deepcopy(value)
     for j in range(0,len(val[0,:])):
          z=0
          for n in range(0,len(val[0,:])):
               z = (val[i-1,n]*s[n,j])+z
          if (z<0):
               z=0
          if (z>1):
               z=1
          val[i,j] = z
     return val
    
def VectorCreate2(y):
     z = np.zeros([1, y], float)
     z = z[0,:]
     return z

def VectorCreate(x):
    return np.zeros(x, dtype='f')

def MeanDistance(v1,v2):
    d = 0
    for i in range(0,len(v1)):
        d = d + abs((v1[i]-v2[i]))
    d = d/(len(v1))
    return d

def GrayPlot(x):
    pl.figure()
    pl.imshow(x,cmap='gray',aspect='auto',interpolation='nearest')

def AverageDistance(x):
    diff = 0.0
    for i in range(0,9):
        for j in range(0,9):
            diff = diff + abs(x[i,j] - x[i,(j+1)])
            diff = diff + abs(x[(i+1),j] - x[i,j])
    diff = diff/(2*9*9)
    return diff

    
desiredNeuronValues = VectorCreate(10)
for i in range(0,len(desiredNeuronValues),2):
    desiredNeuronValues[i]=1.0



Generations = 1000
FitnessVector=VectorCreate(Generations)
parent = MatrixCreate(10,10)
parent = MatrixRandomizeNeg(parent)
parentFitness = Fitness2(parent)
GrayPlot(neuronValues)
for currentGeneration in range (0,Generations):
#    print currentGeneration,parentFitness
    child = MatrixPerturb(parent,0.05)
    childFitness = Fitness2(child)
    if (childFitness > parentFitness):
        parent = child
        parentFitness = childFitness
    FitnessVector[currentGeneration]= parentFitness
#print actualNeuronValues
    
neuronValues2=MatrixCreate(10,10)
for i in range(0,10):
     neuronValues2[0,i]=0.5
for i in range(1,10):
     neuronValues2=NeuronUpdate(neuronValues2,parent,i)
GrayPlot(neuronValues2)
print parentFitness

PlotVectorAsLine(FitnessVector)






pl.show()
