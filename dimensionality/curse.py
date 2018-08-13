import numpy as np 
import math
import random
import matplotlib.pyplot as plt

class Grid :
	def __init__(self, L, dim) :
		self.L = L
		self.dim = dim
		mid = math.ceil(L/2)
		self.state = [mid for _ in range(dim)]
		self.goal = [L for _ in range(dim)]

	def updateState(self, action) :
		d = action//2
		a = action%2
		if(a == 0) :
			if(self.state[d] > 0) :
				self.state[d] -= 1
		elif(a == 1) :
			if(self.state[d] < self.L) :
				self.state[d] += 1
	
	def providePerception(self) :
		r = np.sum(self.state)
		if(r == self.dim*self.L) :
			return 1
		else :
			return 0

class randomAgent :
	def __init__ (self, dim) :
		self.dim = dim
		self.steps = 0
	
	def takeAction(self, env) :
		while(env.providePerception() == 0) :
			a = random.randint(0, 2*self.dim - 1)
			env.updateState(a)
			self.steps += 1
		return self.steps

steps = np.zeros((5,10,100))
avg = np.zeros((5,10))
for i in range(5) :
	dim = i + 1
	for j in range(10) :
		L = j + 1
		for k in range(100) :
			grid = Grid(L, dim)
			agent = randomAgent(dim)
			steps[i][j][k] = agent.takeAction(grid)
		avg[i][j] = np.sum(steps[i][j])
		avg[i][j] = avg[i][j]/100.0

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(avg)

#plt.plot(np.arange(1,11), avg[2])
plt.plot(np.arange(1, 6), avg.transpose()[10])
plt.show()