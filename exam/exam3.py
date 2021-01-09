import numpy as np
import math
import random

# max cars allowed in A, B, C locations
A = int(input("Enter max cars in location A: "))
B = int(input("Enter max cars in location B: "))
C = int(input("Enter max cars in location C: "))

# reward (represented negative to minimize)
reward = -10

# cost (represented positive)
cost = 2

# discount
discount = 0.9

# threshold
threshold = 0.1

# Poisson lambdas
ARequest = 3
BRequest = 2
CRequest = 2
AReturn = 3
BReturn = 1
CReturn = 1

# there are 20*10*10 states, each corresponding to number of cars in a location
# generate states
state = []
for i in range(A + 1):
	for j in range(B + 1):
		for k in range(C + 1):
			state.append([i, j, k])

# max cars allowed to move from 1 location
delta = int(input("Enter max cars allowed to move from or to one location: "))

# actions can be represented as 3-tuple of (i, j, k) where i, j, k are integers, i + j + k = 0, and -5 <= i, j, k <= 5
action = []
for i in range(-delta, delta + 1):
	for j in range(-delta, delta + 1):
		for k in range(-delta, delta + 1):
			if((i+j+k) == 0):
				action.append((i, j, k))

# this probability is going to be accessed a lot, hence using dictionary for faster reference since factorial and power functions are exactly fast
poissonProbability = dict()
def probability(l, n):
	if (l, n) not in poissonProbability.keys():
		poissonProbability[(l, n)] = ((l**n) / (math.factorial(n))) * math.exp(-l)
	return poissonProbability[(l, n)]

# value can be defined as negative of total credits, and minimize it (meaning maximize total credits)
# policy can be represented as 3-tuple of (i, j, k) where i, j, k are integers, i + j + k = 0, and they satisfy other constraints
def Bellman(v, policy):
	Uv = np.copy(v)

	for i in range(len(state)):
		a, b, c = state[i]
		# print("\tState: " + str(i))
		minv = math.inf
		arg = -1

		for j in range(len(action)):
			p, q, r = action[j]
			# print("\t\tAction" + str(j))
			# ignore actions which are not possible
			if(-p > a or -q > b or -r > c):
				continue

			# note: only 'p' will cost, q and r will not since only the change in location A costs
			# a1, b1, c1 will be the state after action is taken, should be sum of previous cars and change, but maintain the limit of max
			a1 = min(a + p, A)	
			b1 = min(b + q, B)
			c1 = min(c + r, C)

			val = cost*p #cost of the action
			# reach kth state after rental
			for k in range(len(state)):
				x1, y1, z1 = state[k]

				# if new states have more cars, not possible
				if(x1 > a1 or y1 > b1 or z1 > c1):
					continue
				
				Prob = probability(ARequest, a1 - x1) * probability(BRequest, b1 - y1) * probability(CRequest, c1 - z1)
				val += Prob * (a1 + b1 + c1 - x1 - y1 - z1) * reward

				tVal = 0
				# reach lth state after return
				for l in range(len(state)):
					x2, y2, z2 = state[l]

					# if new states have less cars, not possible
					if(x2 < x1 or y2 < y1 or z2 < z1):
						continue
					
					prob = probability(AReturn, x2 - x1) * probability(BReturn, y2 - y1) * probability(CReturn, z2 - z1)
					tVal += prob * v[x2, y2, z2]
				
				val += Prob * tVal * discount
			
			if(val < minv):
				minv = val
				arg = j
		
		Uv[a][b][c] = minv
		policy[a][b][c] = arg
	
	return Uv, policy

def valueIteration():
	v = np.zeros((A+1, B+1, C+1))
	
	policy = [[[0]*(C + 1)] * (B + 1)] * (A + 1)
	Uv = np.zeros_like(v)

	i = 0
	e = math.inf
	while (e > threshold):
		i += 1
		Uv, policy = Bellman(v, policy)
		e = np.linalg.norm(Uv.reshape(Uv.size) - v.reshape(v.size), np.inf)
		v = np.copy(Uv)
		print("Iteration: " + str(i) + "\te: " + str(e))

	print()
	print("State : Policy : Value")
	for i in range(len(state)):
		a, b, c = state[i]
		print(str(state[i]) + " : " + str(action[policy[a][b][c]]) + " : " + str(v[a][b][c]))



valueIteration()





			
			
			
			
