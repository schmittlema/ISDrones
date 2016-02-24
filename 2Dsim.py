import pygame, sys
from pygame.locals import *
import random
import time
import math
from sympy import *
from sympy.geometry import *

#colors:
WHITE=(255,255,255)
RED=(255,0,0)
BLACK=(0,0,0)

#experimental parameters
coursesize=(500,400) #size of the viewing window
obstsize= 50 #max radius of obstacle
quadsize= 25 #radius of the quad
num_obstacle=5 #number of obstacles in the environment
sensor_max=300 #max distance the sensor is able to detect

class obstacle:
    '''a basic circular obstacle
    '''
    def __init__(self):
        self.rad=random.randrange(0,obstsize)
        self.x=random.randrange(0,coursesize[0])
        self.y=random.randrange(0,coursesize[1])
        self.color=RED
        self.geo=Circle(Point(self.x,self.y),self.rad)

class quad():
    '''a basic quad w/o sonar sensors
    '''
    def __init__(self):
        self.rad=quadsize
        self.color=BLACK
        self.x=0 #place quad at bottom center of screen
        self.y=0
        self.s1=0 #60 degrees CC
        self.s2=0 #straight ahead
        self.s3=0 #60 degrees C
        self.head=0 #face north, will be measured in radians
    def sense(self):
        #initialize sensors to 0, the default
        s1=0
        s2=0
        s3=0
        head=self.head
        #direction each sensor is pointing
        m1=head-math.pi/3
        m2=head
        m3=head+pi/3
        start1=Point(self.x+quadsize*math.cos(m1),self.y+quadsize*math.sin(m1))
        start2=Point(self.x+quadsize*math.cos(m2),self.y+quadsize*math.sin(m2))
        start3=Point(self.x+quadsize*math.cos(m3),self.y+quadsize*math.sin(m3))
        stop1=Point(self.x+(quadsize+sensor_max)*math.cos(m1),self.y+(quadsize+sensor_max)*math.sin(m1))
        stop2=Point(self.x+(quadsize+sensor_max)*math.cos(m2),self.y+(quadsize+sensor_max)*math.sin(m2))
        stop3=Point(self.x+(quadsize+sensor_max)*math.cos(m3),self.y+(quadsize+sensor_max)*math.sin(m3))
        #segment representing the viewing range of each sensor
        ray1=Segment(start1, stop1)
        ray2=Segment(start2, stop2)
        ray3=Segment(start3, stop3)
        global obs
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
##        x=r_1[0]*(quadsize+i)
##        y=r_1[1]*(quadsize+i)
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
                
            

def draw(obj):
    '''draw a circular object in the window
    '''
    pygame.draw.circle(screen,obj.color,(obj.x,obj.y),obj.rad)
    
    

def drawenvironment():
    '''draws obstacles and current position of the quad
    '''
    global quad1
    screen.fill(WHITE)
    drawobstacles()
    draw(quad1)
    pygame.display.update()
    
def update(quad):
    '''updates the x and y coordinates of the quad, contains the
    learning algorithm
    '''
    x=quad.x
    y=quad.x
    x+=5
    y+=5
    quad.x=x
    quad.y=y

def initialize_screen():
    pygame.init()
    global screen
    screen=pygame.display.set_mode(coursesize,0,32)
    pygame.display.set_caption('BatQuad 2D')
    screen.fill(WHITE)

def createobstacles():
    '''creates num_obstacle instances of obstacle
    '''
    global obs
    global num_obstacle
    obs =[obstacle() for i in range(num_obstacle)]

def createquad():
    '''creates  a new instance of quad called quad1
    '''
    global quad1
    quad1=quad()

def drawobstacles():
    '''draws all the obstacles
    '''
    global obs
    global num_obstacle
    for i in range(num_obstacle):
          draw(obs[i])
    
    
def main():
    '''main function
    '''
    initialize_screen()
    createobstacles()
    createquad()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        update(quad1)
        drawenvironment()
        start=time.time()
        quad1.sense()
        stop=time.time()
        #print(stop-start)
        print(quad1.s1, quad1.s2,quad1.s3)
        #time.sleep(0.01)

main()
                

