import numpy as np 
import math
import random
import matplotlib.pyplot as plt

#class Grid to define Environment of size L and dimension dim
class Grid :
	def __init__(self, L, dim) :
		self.L = L
		self.dim = dim
		mid = math.ceil(L/2)
		self.state = [mid for _ in range(dim)]
		self.goal = [L for _ in range(dim)]

	#function updateState to update the state based on action taken
	def updateState(self, action) :
		d = action//2	#d = quotient of action/2 for dim dimensions, there are 2 actions possible, this determines the direction
		a = action%2	#a = remainder of action/2, this determines the movement towards positive or negative side in the dimension
		#if a is 0, move towards negative in that dimension, else move towards positive in that dimension
		if(a == 0) :	
			if(self.state[d] > 0) :
				self.state[d] -= 1
		elif(a == 1) :
			if(self.state[d] < self.L) :
				self.state[d] += 1
	
	#function providePerception to tell if goal is reached or not
	def providePerception(self) :
		r = np.sum(self.state)
		if(r == self.dim*self.L) :
			return True
		else :
			return False

#class randomAgent to define random agent to move in dim dimensions
class randomAgent :
	def __init__ (self, dim) :
		self.dim = dim
		self.steps = 0
	
	#take action until you reach goal
	#returns the number of steps taken
	def takeAction(self, env) :
		while(env.providePerception() == False) :
			a = random.randint(0, 2*self.dim - 1)
			env.updateState(a)
			self.steps += 1
		return self.steps

#take input
#print("Enter Max Dimension: ")
dim = int(input("Enter Max Dimension: "))
#print("Enter L: ")
L = int(input("Enter L: "))

#count the number of steps taken for 10 cases and calculate the average
cases = 10
steps = np.zeros((dim, cases))
avg = np.zeros((dim))

for i in range(dim) :
	d = i + 1
	for k in range(cases) :
		print("Dimension: " + str(d) + ", Case: " + str(k + 1))
		grid = Grid(L,d)
		agent = randomAgent(d)
		steps[i][k] = agent.takeAction(grid)
		print("Steps taken: " + str(int(steps[i][k])))
	avg[i] = np.sum(steps[i])
	avg[i] = avg[i]/(cases*1.0)

print("Average steps taken for L = " + str(L) + " from dimensions 1 to " + str(dim))
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print(avg)

#Uncomment the below code to see a graph of avg number of steps taken vs dimensions (dimensions on x axis)
plt.xlabel("Dimensions")
plt.xticks(np.arange(dim + 1))
plt.ylabel("Average Steps Taken")
plt.title("L = " + str(L))
plt.plot(np.arange(1, dim + 1), avg.transpose())
plt.show()