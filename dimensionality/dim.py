import numpy as np
import math
import random

class Line :
	def __init__(self, L) :
		self.goal = L
		self.state = math.ceil(L/2)
	
	def updateState(self, action) :
		if(action == "left") :
			if(self.state > 0) :
				self.state -= 1
		elif(action == "right") :
			if(self.state < self.goal) :
				self.state += 1

	def providePerception(self) :
		if(self.state == self.goal) :
			return 1
		else :
			return 0
	
class Grid2D :
	def __init__(self, L) :
		self.goal = (L, L)
		self.state = (math.ceil(L/2), math.ceil(L/2))
	
	def updateState(self, action) :
		if(action == "up") :
			if(self.state[1] < self.goal[1]) :
				self.state = (self.state[0], self.state[1] + 1)
		elif(action == "down") :
			if(self.state[1] > 0) :
				self.state = (self.state[0], self.state[1] - 1)
		elif(action == "left") :
			if(self.state[0] > 0) :
				self.state = (self.state[0] - 1, self.state[1])
		elif(action == "right") :
			if(self.state[0] < self.goal[0]) :
				self.state = (self.state[0] + 1, self.state[1])
	
	def providePerception(self) :
		if(self.state == self.goal) :
			return 1
		else :
			return 0
	
class Grid3D :
	def __init__(self, L) :
		self.goal = (L, L, L)
		self.state = (math.ceil(L/2), math.ceil(L/2), math.ceil(L/2))
	
	def updateState(self, action) :
		if(action == "up") :
			if(self.state[1] < self.goal[1]) :
				self.state = (self.state[0], self.state[1] + 1, self.state[2])
		elif(action == "down") :
			if(self.state[1] > 0) :
				self.state = (self.state[0], self.state[1] - 1, self.state[2])
		elif(action == "left") :
			if(self.state[0] > 0) :
				self.state = (self.state[0] - 1, self.state[1], self.state[2])
		elif(action == "right") :
			if(self.state[0] < self.goal[0]) :
				self.state = (self.state[0] + 1, self.state[1], self.state[2])
		elif(action == "forward") :
			if(self.state[2] < self.goal[2]) :
				self.state = (self.state[0], self.state[1], self.state[2] + 1)
		elif(action == "backward") :
			if(self.state[2] > 0) :
				self.state = (self.state[0], self.state[1], self.state[2] - 1)
	
	def providePerception(self) :
		if(self.state == self.goal) :
			return 1
		else :
			return 0

class randomAgent :
	def __init__(self, dim) :
		self.dim = dim
		self.steps = 0
		self.actions = ["left", "right", "up", "down", "forward", "backward"]

	def takeAction(self, env) :
		while(env.providePerception() == 0) :
			a = random.randint(0, 2*self.dim - 1)
			env.updateState(self.actions[a])
			self.steps += 1
		print self.steps

line2 = Line(2)
grid2d2 = Grid2D(2)
grid3d2 = Grid3D(2)

agent1 = randomAgent(1)
agent2 = randomAgent(2)
agent3 = randomAgent(3)

agent1.takeAction(line2)
agent2.takeAction(grid2d2)
agent3.takeAction(grid3d2)