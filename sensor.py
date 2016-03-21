from abc import ABCMeta
import pygame, sys
from pygame.locals import *
import time
import random as r
import math
from sympy import *
from sympy.geometry import *

Quad_x = 0
Quad_y = 0
Quad_size = 25
Quad_color = 1

Num_Obst = 0
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
        self.x=r.randrange(75,coursesize[0])
        self.y=r.randrange(75,coursesize[1])
        #self.x = 100
        #self.y = 100
        self.color=RED
        self.geo=Circle(Point(self.x,self.y),self.rad)
        action = 0

class Quad(Parent):
	s1 = 0
	s2 = 0
	s3 = 0
	head = 0 #(math.pi *7)/4

	def __init__(self):
                self.rad=Quad_size
        	self.color=BLACK
        	self.x=0 #place quad at bottom center of screen
        	self.y=200

        def draw(self):
                r_1=[math.cos(self.head),math.sin(self.head)]
                r_2=[math.cos(self.head+math.pi/3),math.sin(self.head+math.pi/3)]
                r_3=[math.cos(self.head-math.pi/3),math.sin(self.head-math.pi/3)]
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
                return math.sqrt((x-obstacle.x)**2+(y-obstacle.y)**2)<obstacle.rad
                

        def crash(self):
                return (self.y - self.rad <= 0) or (self.y+self.rad >=400)

        def reset(self):
                self.x = 0
                self.y = 200

	def sense(self,obstacles):
            self.s1=0
            self.s2=0
            self.s3=0
            s1done = False
            s2done = False
            s3done = False
	    r_1=[math.cos(self.head),math.sin(self.head)]
	    r_2=[math.cos(self.head+math.pi/3),math.sin(self.head+math.pi/3)]
	    r_3=[math.cos(self.head-math.pi/3),math.sin(self.head-math.pi/3)]

	    for i in range(0,sensor_max):
                if(self.s1 != 0):
                        s1done = True
                if(self.s2 != 0):
                        s2done = True
                if(self.s3 !=0):
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
	                    
			
	def updateNetwork(self,reward):
                z = 1
	                    
	def reward(self,crash,win):
                z = 1

        def actionSelect(self,actions):
                z = 1
                
        def runNetwork(self):
                z = 1
                
	def update(self):
        #updates the x and y coordinates of the quad, contains the learning algorithm
		self.x+=int(math.cos(self.head) *5)
		self.y-=int(math.sin(self.head) *5)
	    

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

def main():
	global win
	global crash
	global end
	global reward
	end = False
	win = False
	crash = False
	q = Quad()
	obstacles = makeObstacles()
	initializeEnvironment()	
	finish = Finish(475,200,20,GREEN)
        while(not(end)):
                q.reset()
                win = False
                crash = False
                while(not(win)and not(crash)):
                        for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_e: #to stop siimulation press "e"
                                                end = True
                                if event.type==QUIT:
                                        pygame.quit()
                                        sys.exit()
                        reward = 0
                        q.update()
                        q.sense(obstacles)
                        updateEnvironment(obstacles,q,finish)
                        time.sleep(.1)
                        #print q.x,q.y
                        #print q.s1,q.s2,q.s3
                        if(q.intersect(q.x,q.y,finish)):
                                win = True
                        crash = q.crash()
                        reward = q.reward(crash,win)
                        q.updateNetwork(reward)
			
		

main()
