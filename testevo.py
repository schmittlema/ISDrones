from abc import ABCMeta
import pygame, sys
from pygame.locals import *
import time
import random as r
from sympy import *
from sympy.geometry import *
import numpy  as np
import random as r
import pylab as pl
import copy as cp
import math as m

Quad_x = 0
Quad_y = 0
Quad_size = 25
Quad_color = 1

Num_Obst = 5
Obst_maxsize = 50
Obst_minsize = 1

win = False
Width = 10
Height = 10

#colors:
WHITE=(255,255,255)
RED=(255,0,0)
BLACK=(0,0,0)
GREEN = (0,255,0)

#experimental parameters
coursesize=(500,400) #size of the viewing windo	w
sensor_max=100 #max distance the sensor is able to detect


class Parent(object):
	__metaclass__ = ABCMeta
	
	def __init__(self,x,y,size,color):
		self.x = x
		self.y = y
		self.rad = size
		self.color = color

	def draw(self):
		pygame.draw.circle(screen,self.color,(self.x,self.y),self.rad)
	
	def getx(self):
		return self.x
	
	def gety(self):
		return self.y


class Finish(Parent):
        #no code needed
        test = 1
        
class Obstacle(Parent):
    '''a basic circular obstacle
    '''
    def __init__(self):
        self.rad=r.randrange(Obst_minsize,Obst_maxsize)
        self.x=r.randrange(75,coursesize[0] - 75)
        self.y=r.randrange(75,coursesize[1])
        #self.x = 100
        #self.y = 100
        self.color=RED
        self.geo=Circle(Point(self.x,self.y),self.rad)
        action = 0
        
def MatrixCreate(x,y):
     return np.zeros([x, y], float)

def MatrixRandomizeNeg(z):
    #x is a list;
    x= cp.deepcopy(z)
    i=0
    while i<len(x):
        for j in range(0,len(x[0,:])):
            x[i,j] = r.uniform(-1,1)
        i=i+1
    return x

def printMatrix(y):
    x = cp.deepcopy(y)
    for i in range(len(x)):
        print " "
        for j in range(0,len(x[0,:])):
            print x[i,j]
    

class Quad(Parent):
            s1 = 0
            s2 = 0
            s3 = 0
            head = 0 #m.pi/6
            brain = MatrixRandomizeNeg(MatrixCreate(5,3))

            def __init__(self):
                self.rad=Quad_size
                self.color=BLACK
                self.x=0 #place quad at bottom center of screen
                self.y=200

            def draw(self):
                r_1=[m.cos(self.head),m.sin(self.head)]
                r_2=[m.cos(self.head+m.pi/3),m.sin(self.head+m.pi/3)]
                r_3=[m.cos(self.head-m.pi/3),m.sin(self.head-m.pi/3)]
                x1=(r_1[0]*(Quad_size+sensor_max))+self.x
                y1=(r_1[1]*-1*(Quad_size+sensor_max))+self.y
                x2=(r_2[0]*(Quad_size+sensor_max))+self.x
                y2=(r_2[1]*-1*(Quad_size+sensor_max))+self.y
                x3=(r_3[0]*(Quad_size+sensor_max))+self.x
                y3=(r_3[1]*-1*(Quad_size+sensor_max))+self.y
                pygame.draw.circle(screen,self.color,(self.x,self.y),self.rad)
                pygame.draw.line(screen,GREEN,(self.x,self.y),(x1,y1),1)
                pygame.draw.line(screen,GREEN,(self.x,self.y),(x2,y2),1)
                pygame.draw.line(screen,GREEN,(self.x,self.y),(x3,y3),1)

            def intersect(self,x, y, obstacle):
                return m.sqrt((x-obstacle.x)**2+(y-obstacle.y)**2)<obstacle.rad
                        
            def crash(self,obstacles):
                val = False
                for obstacle in obstacles:
                        if(m.sqrt((self.x-obstacle.x)**2+(self.y-obstacle.y)**2)<(obstacle.rad+self.rad)):
                                val = True
                if (self.y - self.rad <= 0) or (self.y+self.rad >=400) or (self.x + self.rad >= 500) or (self.x < -10):
                        val = True
                return val

            def reset(self):
                self.x = 0
                self.y = 200

            def sense(self,obstacles):
                self.s1=-1
                self.s2=-1
                self.s3=-1
                s1done = False
                s2done = False
                s3done = False
                r_1=[m.cos(self.head),m.sin(self.head)]
                r_2=[m.cos(self.head+m.pi/3),m.sin(self.head+m.pi/3)]
                r_3=[m.cos(self.head-m.pi/3),m.sin(self.head-m.pi/3)]

                for i in range(0,sensor_max):
                        if(self.s1 != -1):
                                        s1done = True
                        if(self.s2 != -1):
                                        s2done = True
                        if(self.s3 !=-1):
                                        s3done = True
                        x1=(r_1[0]*(Quad_size+i))+self.x
                        y1=(r_1[1]*-1*(Quad_size+i))+self.y
                        x2=(r_2[0]*(Quad_size+i))+self.x
                        y2=(r_2[1]*-1*(Quad_size+i))+self.y
                        x3=(r_3[0]*(Quad_size+i))+self.x
                        y3=(r_3[1]*-1*(Quad_size+i))+self.y
                        
                        for obstacle in obstacles:
                                if not(s1done) and self.intersect(x1,y1,obstacle):
                                        #ray has made a hit
                                        self.s1 = i
                                        
                                if not(s2done) and self.intersect(x2,y2,obstacle):
                                        #ray has made a hit
                                                self.s2 = i
                                                
                                if not(s3done) and self.intersect(x3,y3,obstacle):
                                        #ray has made a hit
                                                self.s3 = i
	                    
	                    
            def reward(self,crash,win,forward):
                if(crash or not(forward)):
			return -1*distance(self.x,self.y,475,200)
		if(win):
			return 1
                
	    def update(self):
                global forwardprogress
                o = self.runNetwork()
                if o == 0:
                    forwardprogress = 0
                    self.x+=int(m.cos(self.head) *5)
                    self.y-=int(m.sin(self.head) *5)              
                else:
                    forwardprogress+= 1
                    self.head = self.head + (o*m.pi/6)
		

            def runNetwork(self):
                a1 = self.s1 * self.brain[0,0]+ self.s2 * self.brain[1,0]+ self.s3 * self.brain[2,0] + self.head * self.brain[3,0]
                a2 = self.s1 * self.brain[0,1]+self.s2 * self.brain[1,1]+ self.s3 * self.brain[2,1] + self.head * self.brain[3,1]
                a3 = self.s1 * self.brain[0,2]+self.s2 * self.brain[1,2]+self.s3 * self.brain[2,2] +self.head * self.brain[3,2]
                output = a1 * self.brain[4,0]+a2*self.brain[4,1]+a3*self.brain[4,2]
                if output >= 1:
                        return 1
                if output > -1 and output < 1:
                        return 0
                else:
                        return -1




def MatrixPerturb(p,y):
    #p is a matrix
    c=cp.deepcopy(p)
    for i in range(0,len(c[0,:])):
        for n in range(0,len(c[:,0])):
            if (r.random()< y):
                c[n,i]=r.random()
    return c

def distance(x1,y1,x2,y2):
	return m.sqrt((x2-x1)**2 + (y2-y1)**2)

def updateEnvironment(obstacles,Quad,fin):
	screen.fill(WHITE)
	Quad.draw()
	fin.draw()
	for i in range(Num_Obst):
		obstacles[i].draw()
	pygame.display.update()

def initializeEnvironment():
	pygame.init()
	global screen
	screen=pygame.display.set_mode(coursesize,0,32)
	pygame.display.set_caption('BatQuad 2D')
	screen.fill(WHITE)

def makeObstacles():
	global Num_Obst
	obs =[]
	for i in range(Num_Obst):
		obs.append(Obstacle())
	return obs

def run(delay,obstacles,finish,child):
        global forward,crash,win,forwardprogress
        child.reset()
        win = False
        crash = False
        forwardprogress = 0
        child.head = 0
        forward = True
        while(not(win)and not(crash) and forward):
                child.sense(obstacles)
                child.update()
                updateEnvironment(obstacles,child,finish)
                if(child.intersect(child.x,child.y,finish)):
                        win = True
                if(forwardprogress > 12):
                        forward = False
                crash = child.crash(obstacles)
                time.sleep(delay)

def main():
	global win
	Generations = 1000
	global crash
	parent = Quad()
	child = parent
	obstacles = makeObstacles()
	initializeEnvironment()	
	finish = Finish(475,200,20,GREEN)
	fitnessnew = 0
	fitnessold = -1000
	global forwardprogress
	global forward
	parentgen = 0
	#forward = True
        for currentGeneration in range (Generations):
                run(0,obstacles,finish,child)
                
                fitnessnew = child.reward(crash,win,forward)
                print currentGeneration, fitnessnew,fitnessold
		if (fitnessnew > fitnessold):
                        child.brain = cp.copy(MatrixPerturb(parent.brain,0.9))
                        printMatrix(parent.brain)
                        print "----------------------------------------------------"
                        parent.brain = cp.deepcopy(child.brain)
                        printMatrix(child.brain)
                        print " ---------------------------------------------------"
                        printMatrix(parent.brain)
                        parentgen = currentGeneration
                        fitnessold = fitnessnew
               	child.brain = cp.copy(MatrixPerturb(parent.brain,0.1))
        run(.1,obstacles,finish,parent)
        print parentgen, fitnessold
        printMatrix(parent.brain)

main()

