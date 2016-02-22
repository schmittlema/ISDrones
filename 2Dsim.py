import pygame, sys
from pygame.locals import *
import random
import time

#colors:
WHITE=(255,255,255)
RED=(255,0,0)
BLACK=(0,0,0)

#experimental parameters
coursesize=(500,400) #size of the viewing window
obstsize= 50 #max radius of obstacle
quadsize= 25 #radius of the quad
num_obstacle=5 #number of obstacles in the environment

class obstacle:
    '''a basic circular obstacle
    '''
    def __init__(self):
        self.rad=random.randrange(0,obstsize)
        self.x=random.randrange(0,coursesize[0])
        self.y=random.randrange(0,coursesize[1])
        self.color=RED

class quad():
    '''a basic quad w/o sonar sensors
    '''
    def __init__(self):
        self.rad=quadsize
        self.color=BLACK
        self.x=0
        self.y=0
        
    
def getdata():
    '''updates s1, s2, s3
    '''

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
    x+=1
    y+=1
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
        time.sleep(.01)

main()
                

