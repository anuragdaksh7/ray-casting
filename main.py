import pygame
import math
from math import sin, cos, tan
import numpy as np
H = 50
def sigmoid(x):
	return 1/(1+e**(-x))
HINV = 1/H
PI = math.pi
WHITE = (255,)*3
BLACK = (0,)*3
print(WHITE,BLACK)
pygame.init()


def collisionPoint(x1,y1,x2,y2,x3,y3,x4,y4):
	a = x1*y2-y1*x2
	b = x3*y4-y3*x4
	c = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
	px = (a*(x3-x4)-b*(x1-x2))/c
	py = (a*(y3-y4)-b*(y1-y2))/c
	return (px,py)

def lineCollisionPoint(x1,y1,x2,y2,x3,y3,x4,y4):
	t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
	u = ((x1-x3)*(y1-y2) - (y1-y3)*(x1-x2))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
	px = x1+t*(x2-x1)
	py = y1+t*(y2-y1)
	if 0<=t<=1 and 0<=u<=1:
		return px,py
	return False
#print(lineCollisionPoint(0,0,2,2,2,0,0,2))




class Cam:
	def __init__(self,x,y,quality,win,angle_initial,angle_final,lines,speed,offset = 0,size = 100):
		self.x = x
		self.y = y
		self.win = win
		self.size = size
		self.speed = speed
		self.offset = offset
		self.lines = lines
		self.angle_initial,self.angle_final = min([angle_initial,angle_final]),max([angle_initial,angle_final])
		self.quality = int(quality)
		self.angles = []

	def project(self):
		angle_ = self.angle_initial + self.offset \
		+ self.angle_final + self.offset
		angle_ = angle_/2
		
		angle = self.angle_initial + self.offset
		while angle<self.angle_final+self.offset:
			ks = []
			ds = []
			for line in lines:
				x2,y2 = (self.x - sin(angle) * self.size,self.y + cos(angle) * self.size)
				#line = self.lines[0]
				k = lineCollisionPoint(self.x, self.y, x2, y2, line[0], line[1], line[2], line[3])
				ks.append(k)
				if k:
					ds.append(((self.x-k[0])**2+(self.y-k[1])**2)**0.5)
				else:
					ds.append(1000000000000)
			if any(ks):
				zz = ds.index(min(ds))
				x2,y2 = ks[zz]
				size = min(ds)*cos(angle-angle_)
				distance = 1-min(ds)/1000
				size = 30000/(10+size)
				#size = math.e**(size)*200
				#print(size)
				#size = ((math.acos(size)))*200
				#print(angle)
				#print(self.offset)
				#self.angles.append(angle)
				#pygame.draw.rect(win, WHITE, pygame.Rect(75*angle+180-2,300-size/2,4,size))
				hmm = pygame.Rect(600*angle/11+300-2,300-size/2,4,size)
				#print(hmm,angle)
				pygame.draw.rect(win, (int(255*distance),)*3,hmm )

			#print(ks)

			pygame.draw.line(self.win, WHITE, (600+self.x, self.y), \
			(600+x2,y2),1)
			angle += (self.angle_final-self.angle_initial)/self.quality

	def move(self):
		pos = np.array([self.x,self.y])
		angle = self.angle_initial + self.offset \
		+ self.angle_final + self.offset
		angle = angle/2
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			pos = np.add(pos,np.array([self.speed*sin(-angle),self.speed*cos(-angle)]))
			self.x = float(pos[0])
			self.y = float(pos[1])
		if keys[pygame.K_s]:
			pos = np.add(pos,np.array([-self.speed*sin(-angle),-self.speed*cos(-angle)]))
			self.x = float(pos[0])
			self.y = float(pos[1])

			
		if keys[pygame.K_a]:
			self.offset-=0.005
		if keys[pygame.K_d]:
			self.offset+=0.005
		if self.offset>2*PI:
			self.offset = 0
		elif self.offset<-2*PI:
			self.offset = 0
		
	def collisionDetector(self):
		
		for i in self.lines:
			pygame.draw.line(self.win, WHITE, (i[0]+600,i[1]), (i[2]+600,i[3]),5)
		

lines = [[100,200,300,400],[400,50,500,500],[50,400,500,300]]
lines = [lines[0]]
lines = [
[0,0,0,600],
[120,80,600,80],
[600,80,600,430],
[600,230,115,220],
[115,220,240,280],
[530,330,150,340],
[50,380,300,575]
]
win = pygame.display.set_mode((1300,600))
cam = Cam(500, 300, 60, win, -PI/2-PI/4, -PI/2+PI/4,lines, 0.4, offset=0, size = 600)
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	win.fill(BLACK)
	cam.move()
	cam.collisionDetector()
	cam.project()
	pygame.display.update()
pygame.quit()
