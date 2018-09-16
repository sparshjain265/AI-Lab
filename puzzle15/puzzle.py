import pdb
import numpy as np
from collections import defaultdict

#class puzzle to initialize the n^2-1 puzzle with or without given dimension
class puzzle :
	def __init__(self, n = None) :
		if(n == None):
			self.dimension = int(input("Enter the dimension of the matrix: "))
			self.mat = np.reshape([0]*self.dimension*self.dimension, (self.dimension, self.dimension))
		else:
			self.dimension = n
			self.mat = np.reshape([0]*n*n, (n, n))
		n = self.dimension
		self.x = -1
		self.y = -1
		self.start = np.copy(self.mat)
		self.goal = np.arange(1, n*n + 1).reshape(n, n)
	
	#function to get a new matrix as input
	def getMatrix(self, mat = None) :
		print("Enter the elements of the matrix: ")
		for i in range(self.dimension):
			if(mat == None):
				temp = input().strip().split()
			else:
				temp = mat[i]
			for j, x in zip(range(self.dimension), temp):
				if(x == '*'):
					self.mat[i][j] = self.dimension*self.dimension
					#print(self.mat[i][j])
					self.x = i
					self.y = j
				else :
					self.mat[i][j] = int(x)
		self.start = np.copy(self.mat)
	
	#function to update the current state of the matrix
	def updateMatrix(self, mat):
		self.mat = mat
		for i in range(self.dimension):
			for j in range(self.dimension):
				if(self.mat[i][j] == 16 or self.mat[i][j] == '*'):
					self.x = i 
					self.y = j
	
	'''
	def display(self) :
		n = self.dimension
		M = 0
		for i in range(n) :
			for j in range(n) :
				M[i][j] = self.mat[i][j]
		M[self.x][self.y] = '*'
		print(M)
	'''

	#Action functions, take the action if valid

	def left(self) :
		if(self.y == 0):
			return False
		else:
			self.mat[self.x][self.y] = self.mat[self.x][self.y - 1]
			self.mat[self.x][self.y - 1] = self.dimension*self.dimension
			self.y -= 1
			return True
	
	def right(self):
		if(self.y == self.dimension - 1):
			return False
		else:
			self.mat[self.x][self.y] = self.mat[self.x][self.y + 1]
			self.mat[self.x][self.y + 1] = self.dimension*self.dimension
			self.y += 1
			return True
	
	def up(self):
		if(self.x == 0):
			return False
		else:
			self.mat[self.x][self.y] = self.mat[self.x - 1][self.y]
			self.mat[self.x - 1][self.y] = self.dimension*self.dimension
			self.x -= 1
			return True
		
	def down(self):
		if(self.x == self.dimension - 1):
			return False
		else:
			self.mat[self.x][self.y] = self.mat[self.x + 1][self.y]
			self.mat[self.x + 1][self.y] = self.dimension*self.dimension
			self.x += 1
			return True
	
	#Check the parity with the given formula
	def parity(self):
		s = self.dimension*2 - self.x - self.y - 2
		for pi in range(self.dimension * self.dimension) :
			for pj in range(pi + 1, self.dimension*self.dimension):
				xi = pi//self.dimension
				yi = pi%self.dimension
				xj = pj//self.dimension
				yj = pj%self.dimension
				if(self.mat[xj][yj] < self.mat[xi][yi]):
					s += 1
		return s%2

#get input
env = puzzle()
env.getMatrix()

#BFS function to find the optimal path (No visited node checking, so time complexity is affected)
def BFS(env) :
	if(env.parity() == 1):
		return -1
	index = 0
	Q = []

	if(np.array_equal(env.mat, env.goal)) :
		print()
		return index
	Q.insert(0, np.copy(env.mat))

	counter = 0
	while Q :
		s = np.copy(Q.pop())
		counter += 1
		
		if(s.all() == False) :
			index += 4
			for i in range(4) :
				Q.insert(0, False)
			continue

		env.updateMatrix(np.copy(s))
		for i in range(4) :
			index += 1
			if(i == 0) :
				if(env.left()) :
					if(np.array_equal(env.mat, env.goal)) :
						print()
						return index
					Q.insert(0, np.copy(env.mat))
					env.right()
				else :
					Q.insert(0, False)
			elif(i == 1) :
				if(env.right()) :
					if(np.array_equal(env.mat, env.goal)) :
						print()
						return index
					Q.insert(0, np.copy(env.mat))
					env.left()
				else :
					Q.insert(0, False)
			elif(i == 2) :
				if(env.up()) :
					if(np.array_equal(env.mat, env.goal)) :
						print()
						return index
					Q.insert(0, np.copy(env.mat))
					env.down()
				else :
					Q.insert(0, False)
			elif(i == 3) :
				if(env.down()) :
					if(np.array_equal(env.mat, env.goal)) :
						print()
						return index
					Q.insert(0, np.copy(env.mat))
					env.up()
				else :
					Q.insert(0, False)
	print(index)
	return index

#get optimal path
index = BFS(env)

#function path to get path from index
def path(index) :
	if(index == -1):
		print("Parity " + u'≠' + " 0")
		print("Cannot Solve!")
		return

	if(index == 0) :
		env.updateMatrix(np.copy(env.start))
		print(str(env.mat) +  "\t Start ")
		print()
	else :
		curr = (index - 1) % 4
		path((index - 1)//4)
		p = ["Left", "Right", "Up", "Down"]
		if(curr == 0):
			env.left()
			print(str(env.mat) + "\t " + p[curr])
			print()
		if(curr == 1):
			env.right()
			print(str(env.mat) + "\t " + p[curr])
			print()
		if(curr == 2):
			env.up()
			print(str(env.mat) + "\t " + p[curr])
			print()
		if(curr == 3):
			env.down()
			print(str(env.mat) + "\t " + p[curr])
			print()

#print path
path(index)

