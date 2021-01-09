import numpy as np
import heapq

#Class puzzle to hold necessary data
class puzzle:
	#initialization
	def __init__(self):
		self.n = int(input("Enter n: "))
		self.mat = np.reshape([-1]*self.n*self.n, (self.n, self.n))
		self.wx = []
		self.wy = []
		self.start = np.copy(self.mat)
		self.count = -1
		self.gx = 0
		self.gy = self.n - 1
		self.rx = -1
		self.ry = -1
		# self.goal = np.arange(1, self.n*self.n + 1).reshape(self.n, self.n)

	#get input
	def getMatrix(self):
		self.count = 0
		print("Enter the elements of the matrix (0 for white, 1 for black, 2 for red): ")
		for i in range(self.n):
			temp = input().strip().split()
			for j, x in zip(range(self.n), temp):
				if(int(x) == 0):
					self.mat[i][j] = int(x)
					self.count += 1
					self.wx.append(i)
					self.wy.append(j)
				elif(int(x) == 2):
					self.mat[i][j] = int(x)
					self.rx = i
					self.ry = j
				else :
					self.mat[i][j] = int(x)
		self.start = np.copy(self.mat)
	
	#update matrix when required
	def updateMatrix(self, mat):
		self.mat = mat
		self.wx = []
		self.wy = []
		for i in range(self.n):
			for j in range(self.n):
				if(self.mat[i][j] == 0):
					self.wx.append(i)
					self.wy.append(j)
				if(self.mat[i][j] == 2):
					self.rx = i
					self.rw = j
	
	#Action functions
	#take input 'i' to select which tile to move
	#don't allow swapping of both blank tiles

	def left(self, i) :
		# edge
		if(self.wy[i] == 0):
			return False
		# swapping empty places
		if(self.mat[self.wx[i]][self.wy[i] - 1] == 0):
			return False
		else:
			self.mat[self.wx[i]][self.wy[i]] = self.mat[self.wx[i]][self.wy[i] - 1]
			self.mat[self.wx[i]][self.wy[i] - 1] = 0
			# checking red block
			if(self.mat[self.wx[i]][self.wy[i]] == 2):
				self.ry += 1
			self.wy[i] -= 1
			return True
	
	def right(self, i):
		# edge
		if(self.wy[i] == self.n - 1):
			return False
		# swapping empty places
		if(self.mat[self.wx[i]][self.wy[i] + 1] == 0):
			return False
		else:
			self.mat[self.wx[i]][self.wy[i]] = self.mat[self.wx[i]][self.wy[i] + 1]
			self.mat[self.wx[i]][self.wy[i] + 1] = 0
			# checking red block
			if(self.mat[self.wx[i]][self.wy[i]] == 2):
				self.ry -= 1
			self.wy[i] += 1
			return True
	
	def up(self, i):
		# edge
		if(self.wx[i] == 0):
			return False
		# swapping empty places
		if(self.mat[self.wx[i] - 1][self.wy[i]] == 0):
			return False
		else:
			self.mat[self.wx[i]][self.wy[i]] = self.mat[self.wx[i] - 1][self.wy[i]]
			self.mat[self.wx[i] - 1][self.wy[i]] = 0
			# checking red block
			if(self.mat[self.wx[i]][self.wy[i]] == 2):
				self.rx += 1
			self.wx[i] -= 1
			return True
		
	def down(self, i):
		# edge
		if(self.wx[i] == self.n - 1):
			return False
		# swapping empty places
		if(self.mat[self.wx[i] + 1][self.wy[i]] == 0):
			return False
		else:
			self.mat[self.wx[i]][self.wy[i]] = self.mat[self.wx[i] + 1][self.wy[i]]
			self.mat[self.wx[i] + 1][self.wy[i]] = 0
			# checking red block
			if(self.mat[self.wx[i]][self.wy[i]] == 2):
				self.rx -= 1
			self.wx[i] += 1
			return True

	#Gives manhattan distance of each misplaced tile summed up as heuristic
	def heuristic(self):
		h = abs(self.rx - self.gx) + abs(self.ry - self.gy)
		return h
	
	#Checks if the current configuration or swapping the blank tiles makes it equivalent to goal, else return false
	def check(self):
		if(self.rx == self.gx and self.ry == self.gy):
			return True
		else:
			return False

#Function Astar to implement the algorithm
def Astar(env):
	state = dict()		#state, a mapping from one configuration to it's matrix, parent, action, gn, hn, via a current
	visited = []		#keep track of visited nodes
	fringe = []			#keep track of fringe (nodes in Q)
	Q = []				#priority queue for fringe
	heapq.heapify(Q)	
	current = np.array_str(np.copy(env.mat))			#initialize current to 0
	#state of a current has item, parent, action, gn, hn respectively
	state[current] = [np.copy(env.mat), np.copy(env.mat), "Start", 0, env.heuristic()]
	#Push current in heap with gn + hn as priority
	heapq.heappush(Q, (0 + env.heuristic(), current))
	#add current in fringe
	fringe.append(current)

	#count variable for debugging
	c = 0
	#While the queue is non empty
	while Q:
		#pop out the most prioritized item and remove it from the fringe
		d, current = heapq.heappop(Q)
		fringe.remove(current)
		
		#count variable for debugging
		c += 1
		print(c)

		#update env matrix to the popped one
		env.updateMatrix(np.copy(state[current][0]))

		#check for goal state
		if(env.check()):
			printPath(current, state, env)
			return c
		
		#mark visited
		visited.append(current)

		#i = 0 means move tile n**2, i = 1 means move tile n**2-1
		for i in range(len(env.wx)):
			#4 possible actions for each tile
			for a in range(4):
				#Take appropriate action
				#after taking action, current will be parent and cstring will be child or new node
				if(a == 0):
					if(env.left(i)):
						cstring = np.array_str(np.copy(env.mat))
						if(cstring not in visited and cstring not in fringe):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Left", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						elif(cstring in fringe and state[cstring][3] > state[current][3] + 1):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Left", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						env.right(i)
				
				elif(a == 1):
					if(env.right(i)):
						cstring = np.array_str(np.copy(env.mat))
						if(cstring not in visited and cstring not in fringe):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Right", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						elif(cstring in fringe and state[cstring][3] > state[current][3] + 1):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Right", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						env.left(i)
				
				elif(a == 2):
					if(env.up(i)):
						cstring = np.array_str(np.copy(env.mat))
						if(cstring not in visited and cstring not in fringe):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Up", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						elif(cstring in fringe and state[cstring][3] > state[current][3] + 1):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Up", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						env.down(i)

				elif(a == 3):
					if(env.down(i)):
						cstring = np.array_str(np.copy(env.mat))
						if(cstring not in visited and cstring not in fringe):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Down", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						elif(cstring in fringe and state[cstring][3] > state[current][3] + 1):
							state[cstring] = [np.copy(env.mat), np.copy(state[current][0]), ("Down", (env.wx[i], env.wy[i])), state[current][3] + 1, env.heuristic()]
							heapq.heappush(Q, (state[cstring][3] + state[cstring][4], cstring))
							fringe.append(cstring)
						env.up(i)

#Print path by backtracking
def printPath(current, state, env):
	p = state[current][3]
	path = []
	while(np.array_equal(state[current][0], env.start) == False):
		path.append(state[current][2])
		path.append(state[current][0])
		current = np.array_str(np.copy(state[current][1]))
	print(str(state[current][0]) + " Start")
	while path:
		print(str(path.pop()) + " " + str(path.pop()))
	print("Steps Taken: " + str(p))
	

env = puzzle()
env.getMatrix()
#print(env.heuristic())
counter = Astar(env)
print("Nodes Explored: " + str(counter))