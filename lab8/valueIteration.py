import numpy as np
import math

class grid:
	def __init__(self):
		self.dimension = int(input("Enter the dimension of the grid: "))
		self.mat = np.reshape([0]*self.dimension*self.dimension, (self.dimension, self.dimension))

		print("Enter the grid matrix containing rewards: ")
		for i in range(self.dimension):
			temp = input().strip().split()
			for j, x in zip(range(self.dimension), temp):
				self.mat[i][j] = int(x)
		
		self.discount = float(input("Enter the discount factor (between 0 and 1, both excluded): "))
		
		self.x = -1
		self.y = -1

		self.action = ["up", "left", "down", "right"]
		self.A = 4

	def take_action(self, a, x, y):
		self.x = x
		self.y = y
		if(a == 0):
			return self.up()
		elif(a == 1):
			return self.left()
		elif(a == 2):
			return self.down()
		elif(a == 3):
			return self.right()

	def up(self):
		if(self.x == 0):
			return False
		#if(self.mat[self.x - 1][self.y] == 0):
		#	return False
		self.x -= 1
		return True
	def down(self):
		if(self.x == self.dimension - 1):
			return False
		#if(self.mat[self.x + 1][self.y] == 0):
		#	return False
		self.x +=1
		return True
	def left(self):
		if(self.y == 0):
			return False
		#if(self.mat[self.x][self.y - 1] == 0):
		#	return False
		self.y -= 1
		return True
	def right(self):
		if(self.y == self.dimension - 1):
			return False
		#if(self.mat[self.x][self.y + 1] == 0):
		#	return False
		self.y += 1
		return True

#	#give some probability to each possible action
#	#double the probability of action tried
#	#give some probability to stay there
#	#normalize the probability to make sum = 1
#	#return probability matrix
#	def calc_probability(self, a, x, y):
#		probability = np.reshape([0]*self.dimension*self.dimension, (self.dimension, self.dimension))
#		for i in range(self.A):
#			if(self.take_action(i, x, y)):
#				p = abs(a - i) + 1
#				if(p == 4):
#					p = 2
#				if(p == 3):
#					p = 5
#				p = 1/p
#				probability[self.x][self.y] = p
#		if(self.take_action(a, x, y)):
#			probability[self.x][self.y] *= 2.0
#		probability[x][y] = 0.3
#		probability = probability / probability.sum()
#		return probability

	def calc_probability(self, a, x, y):
		probability = np.reshape([0]*self.dimension*self.dimension, (self.dimension, self.dimension))
		if(self.take_action(a, x, y)):
			probability[self.x][self.y] = 1
		else:
			probability[x][y] = 1
		return probability

	def Bellman(self, v):
		Uv = np.copy(v)
		policy = np.reshape([-1]*self.dimension*self.dimension, (self.dimension, self.dimension))
		for i in range(self.dimension):
			for j in range(self.dimension):
				max = -math.inf
				arg = -1
				for k in range(self.A):
					val = 0
					prob = self.calc_probability(k, i, j)
					for p in range(self.dimension):
						for q in range(self.dimension):
							val += prob[p][q]*v[p][q]
					val = val * self.discount
					val += self.mat[i][j]
					if(val > max):
						max = val
						arg = k
				Uv[i][j] = max
				policy[i][j] = arg
		return (Uv, policy)
	
	def iteration(self, n):
		V = np.zeros((n, self.dimension, self.dimension))
		policy = np.reshape([-1]*self.dimension*self.dimension, (self.dimension, self.dimension))
		#print(V[0])
		for i in range(n-1):
			V[i + 1] , policy = self.Bellman(V[i])
			print(str(i+1) + ". Value[0][0]: " + str(V[i][0][0]))
		print(str(n) + ". Value[0][0]: " + str(V[n - 1][0][0]))

		print("Optimal Values after " + str(n) + " iterations: ")
		print(V[n - 1])
		p = [" "]*self.dimension
		for i in range(self.dimension):
			p[i] = [" "]*self.dimension
		for i in range(self.dimension):
			for j in range(self.dimension):
				p[i][j] = self.action[policy[i][j]]
		print("Optimal Policy after " + str(n) + " iterations: ")
		for i in range(self.dimension):
			print(p[i])
		#print("Reference: " + str(self.action))

Grid = grid()
Grid.iteration(100)