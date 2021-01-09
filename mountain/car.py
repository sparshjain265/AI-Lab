# vel = (-0.07, 0.07)
# pos = (-1.2, 0.6)
# dicretise the vel and pos
# use round function
# states = {(vel, pos)}
# action is to accelerate = {back, neutral, forward} = {-1, 0, 1}
# vel+ = vel + acc*0.001 + cos(3*pos)*(-0.0025)
# vel+ = vel + acc*0.01 + cos(3*pos)*(-0.025)
# pos+ = pos + vel
# gamma = 0.99
# goal >= 0.55, reward +1, reward otherwise is 0

import numpy as np 
import math

class mountain:
	def __init__(self):
		self.vmin = -0.07
		self.vmax = 0.07
		self.vsteps = 20
		self.vdel = 0.001
		self.v = np.arange(self.vmin, self.vmax, self.vdel)
		
		self.pmin = -1.2
		self.pmax = 0.6
		self.psteps = 20
		self.pdel = 0.001
		self.p = np.arange(self.pmin, self.pmax, self.pdel)

		self.goal = 0.55

		self.action = [-1, 0, 1]

	def pindex(self, val):
		if(val < self.pmax):
			return (val - self.pmin)/pdel
		else:
			return self.p.size - 1

	def vindex(self, val):
		if(val < self.vmax):
			return (val - self.vmin)/vdel
		else:
			return self.v.size - 1

	def reward(self, state):
		if(p[state[0]] >= self.goal):
			return 1
		else:
			return 0

	def Bellman(self, v):
		UV = np.copy(v)
		policy = np.zeros_like(v)

		for pos in self.p:
			for vel in self.v:
				
