import numpy as np
from collections import defaultdict
import queue
import heapq
import math

#Class grid for Environment
class grid :
	def __init__(self):
		self.dimension = int(input("Enter the dimension of the grid: "))
		self.mat = np.reshape([0]*self.dimension*self.dimension, (self.dimension, self.dimension))
	
		print("Enter the grid matrix (0 for black, 1 for white): ")
		for i in range(self.dimension):
			temp = input().strip().split()
			for j, x in zip(range(self.dimension), temp):
				self.mat[i][j] = int(x)
		
		print("Enter the starting position ")
		temp = input().strip().split()
		self.x = int(temp[0])
		self.y = int(temp[1])
		self.sx = self.x
		self.sy = self.y
		self.mat[self.x][self.y] = 1;
		
		self.fx = 0
		self.fy = self.dimension - 1
		
		if(self.mat[self.fx][self.fy] == 0):
			print("Final position blocked!")
			return None

	#percept returns true if goal found, else false
	def percept(self):
		if(self.x == self.fx and self.y == self.fy):
			return True
		else:
			return False

	#Action functions

	def up(self):
		if(self.x == 0):
			return False
		if(self.mat[self.x - 1][self.y] == 0):
			return False
		self.x -= 1
		return True
	def down(self):
		if(self.x == self.dimension - 1):
			return False
		if(self.mat[self.x + 1][self.y] == 0):
			return False
		self.x +=1
		return True
	def left(self):
		if(self.y == 0):
			return False
		if(self.mat[self.x][self.y - 1] == 0):
			return False
		self.y -= 1
		return True
	def right(self):
		if(self.y == self.dimension - 1):
			return False
		if(self.mat[self.x][self.y + 1] == 0):
			return False
		self.y += 1
		return True

	#Update function to change the position of agent during bfs
	def update(self, sx, sy):
		self.x = sx
		self.y = sy

	#Reset function to reset the coordinates to start
	def reset(self):
		self.x = self.sx
		self.y = self.sy

	#function heu to give heuristic
	def heuristic(self, counter):
		return abs(self.fx - self.x) + abs(self.fy - self.y)		

#Agent class
class Agent:
	#0 = start, 1 = up, 2 = down, 3 = left, 4 = right
	def __init__(self, env):
		self.visited = np.reshape([-1]*env.dimension*env.dimension, (env.dimension, env.dimension))
		self.parent = np.copy(self.visited)
		self.p = 0
		self.Q = []
		heapq.heapify(self.Q)
	
	#Function astar to calculate optimal path
	#heu = 0 : BFS, 1 : euclidean, 2 : manhattan
	def astar(self, env):
		self.visited = np.reshape([-1]*env.dimension*env.dimension, (env.dimension, env.dimension))
		self.parent = np.copy(self.visited)
		self.p = 0
		self.Q = []
		heapq.heapify(self.Q)
		counter = 0
		heapq.heappush(self.Q, (self.p + env.heuristic(counter), [env.x, env.y, self.p, 0]))
		while(self.Q):
			_, [sx, sy, self.p, action] = heapq.heappop(self.Q)
			
			env.update(sx, sy)
			if(env.percept() == True):
				self.printPath(env, action)
				return [self.p, counter]
			if(self.visited[sx][sy] == 1):
				continue
			self.visited[sx][sy] = 1
			self.parent[sx][sy] = action

			if(env.up()):
				counter += 1
				heapq.heappush(self.Q, (self.p + 1 + env.heuristic(counter), [env.x, env.y, self.p + 1, 1]))
				env.down()
			if(env.down()):
				counter += 1
				heapq.heappush(self.Q, (self.p + 1 + env.heuristic(counter), [env.x, env.y, self.p + 1, 2]))
				env.up()
			if(env.left()):
				counter += 1
				heapq.heappush(self.Q, (self.p + 1 + env.heuristic(counter), [env.x, env.y, self.p + 1, 3]))
				env.right()
			if(env.right()):
				counter += 1
				heapq.heappush(self.Q, (self.p + 1 + env.heuristic(counter), [env.x, env.y, self.p + 1, 4]))
				env.left()

		return -1


	#Print path by backtracking
	def printPath(self, env, action):
		path = []
		while(action != 0):
			if(action == 1):
				path.append("Up")
				env.down()
			if(action == 2):
				path.append("Down")
				env.up()
			if(action == 3):
				path.append("Left")
				env.right()
			if(action == 4):
				path.append("Right")
				env.left()
			action = self.parent[env.x][env.y]
		print("Start")
		while(path):
			print(path.pop())

G = grid()
A = Agent(G)
print()
print("By Manhattan Heuristic")
steps, counter = A.astar(G)
print("Number of steps: " + str(steps))
print("Manhattan Counter: " + str(counter))


