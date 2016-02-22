from abc import ABCMeta
import time
import random as r

Quad_x = 0
Quad_y = 0
Quad_size = 2
Quad_color = 1

Num_Obst = 3
Obst_maxsize = 2
Obst_minsize = 1

win = False
Width = 10
Height = 10


class Parent(object):
	__metaclass__ = ABCMeta
	
	def __init__(self,x,y,size,color):
		self.x = x
		self.y = y
		self.size = size
		self.color = color

	def draw(self):
		x = 2+1
		#needs code
	
	def getx(self):
		return self.x
	
	def gety(self):
		return self.y

class Obstacle(Parent):
	#included to eliminate indentaion error
	var = 0

class Quad(Parent):
	s1 = 0
	s2 = 0
	s3 = 0

	def getData(self):
		x = 1+1	
		#needs code
	
	def update(Parent):
		Parent.x+=1
		#needs code

# Testing
#q = Quad(2,3,3,1)
#q.getData()
#q.draw()

def drawenvironment(obstacles,Quad):
	#needs code
	x = 1

def updateenvironment(Quad):
	#needs code
	x =1

def makeObstacles():
	obst = []
	r.seed()
	for o in range(0,Num_Obst):
		s = r.randint(Obst_minsize,Obst_maxsize)
		obst.append( Obstacle(r.randint(0,Width),r.randint(0,Height),s,2))
		
	return obst

def main():
	global win
	q = Quad(Quad_x,Quad_y,Quad_size,Quad_color)
	obstacles = makeObstacles()
	drawenvironment(obstacles,q)	

	while(not(win)):
		updateenvironment(Quad)
		q.update()
		time.sleep(1)
		win = True #tempory

	#Temporary
	for o in obstacles:
		print o.getx(),  " " , o.gety()


main()
