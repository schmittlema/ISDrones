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

#experimental parameters
coursesize=(500,400) #size of the viewing windo	w
sensor_max=300 #max distance the sensor is able to detect


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

class Obstacle(Parent):
    '''a basic circular obstacle
    '''
    def __init__(self):
        self.rad=r.randrange(Obst_minsize,Obst_maxsize)
        self.x=r.randrange(0,coursesize[0])
        self.y=r.randrange(0,coursesize[1])
        self.color=RED
        self.geo=Circle(Point(self.x,self.y),self.rad)

class Quad(Parent):
	s1 = 0
	s2 = 0
	s3 = 0
	head = 0

	def __init__(self):
        	self.rad=Quad_size
        	self.color=BLACK
        	self.x=0 #place quad at bottom center of screen
        	self.y=0

	def sense(self,obs):
		#initialize sensors to 0, the default
		s1=0
		s2=0
		s3=0
		head=self.head
		#direction each sensor is pointing
		m1=head-math.pi/3
		m2=head
		m3=head+pi/3
		start1=Point(self.x+Quad_size*math.cos(m1),self.y+Quad_size*math.sin(m1))
		start2=Point(self.x+Quad_size*math.cos(m2),self.y+Quad_size*math.sin(m2))
		start3=Point(self.x+Quad_size*math.cos(m3),self.y+Quad_size*math.sin(m3))
		stop1=Point(self.x+(Quad_size+sensor_max)*math.cos(m1),self.y+(Quad_size+sensor_max)*math.sin(m1))
		stop2=Point(self.x+(Quad_size+sensor_max)*math.cos(m2),self.y+(Quad_size+sensor_max)*math.sin(m2))
		stop3=Point(self.x+(Quad_size+sensor_max)*math.cos(m3),self.y+(Quad_size+sensor_max)*math.sin(m3))
		#segment representing the viewing range of each sensor
		ray1=Segment(start1, stop1)
		ray2=Segment(start2, stop2)
		ray3=Segment(start3, stop3)
		for obstacle in obs:
		    sense1=intersection(ray1,obstacle.geo)
		    sense2=intersection(ray2,obstacle.geo)
		    sense3=intersection(ray3,obstacle.geo)
		    if sense1:
		        for point in sense1:
		            point=point.evalf()
		            d1=sensor_max-(point.distance(start1))
		            if d1>s1:
		                s1=int(d1)
		    if sense2:
		        for point in sense2:
		            point=point.evalf()
		            d2=sensor_max-(point.distance(start1))
		            if d2>s2:
		                s2=int(d2)
		    if sense3:
		        for point in sense3:
		            point=point.evalf()
		            d3=sensor_max-(point.distance(start3))
		            if d3>s3:
		                s3=int(d3)
		    #check for intersection, if there is an intersection,
		    #report the closest distance
		self.s1=s1
		self.s2=s2
		self.s3=s3

	##def sense():
	##    global quad1
	##    global obs
	##    s1=0
	##    h1=quad1.head-math.pi/3
	##    x=quad1.x
	##    y=quad1.y
	##    r_1=(math.cos(h1),math.sin(h1))
	##    for i in range(sensor_max):
	##        x=r_1[0]*(Quad_size+i)
	##        y=r_1[1]*(Quad_size+i)
	##        for obstacle in obs:
	##            obs_x=obstacle.x
	##            obs_y=obstacle.y
	##            obs_rad=obstacle.rad
	##            if Point(x,y).distance(Point(obs_x,obs_y))<obs_rad:
	##                #ray has made a hit
	##                d=100-i
	##                if d>s1:
	##                    s1=int(d)
	##    quad1.s1=s1

	def update(self):
        #updates the x and y coordinates of the quad, contains the learning algorithm
		self.x+=5
		self.y+=5
	    

def	updateEnvironment(obstacles,Quad):
	global Num_Obst
	screen.fill(WHITE)
	Quad.draw()
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
	q = Quad()
	obstacles = makeObstacles()
	initializeEnvironment()	

	while(not(win)):
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
		q.update()
		q.sense(obstacles)
		updateEnvironment(obstacles,q)
	#	print q.s1,q.s2,q.s3
		#time.sleep(1)

main()
