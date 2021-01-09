import numpy as np
import math
import random
import itertools

# define constants

TotalWickets = 3
TotalOvers = 10
TotalBowlers = 5
OversPerBowler = 2

economy = [3, 3.5, 4, 4.5, 5]
strike = [33, 30, 24, 18, 15]

s = [''.join(i) for i in itertools.product("012", repeat = TotalBowlers)]
# S = dict()
# for i in range(len(s)):
# 	S[s[i]] = i

#generate states
state = []
for i in range(1, TotalWickets + 1):
	for x in s:
		state.append((i, x))

# value can be defined as runs made, and we have to minimise the value function
# a state can be a tuple of wickets remaining, bowler remaining

# define bellman operator
def Bellman(v):

	#Uv = dict()
	policy = dict()

	for i in range(len(state)):
		w, b = state[i]

		minv = math.inf
		arg = -1

		for j in range(TotalBowlers):
			val = economy[j]

			if(b[j] == '0'):
				continue
			
			br = ""
			for x in range(len(b)):
				if(x == j):
					if(b[x] == '1'):
						br += '0'
					else:
						br += '1'
				else:
					br += b[x]
			
			#case 1, wicket
			val += (6/strike[j])*v[(w-1, br)]

			#case 2, no wicket
			val += (1 - 6/strike[j])*v[(w, br)]

			if(val < minv):
				minv = val
				arg = j
		
		if(minv == math.inf):
			minv = 0
		v[state[i]] = minv
		policy[state[i]] = arg
	
	return v, policy

# perform value iteration
# by properties of dynamic programming, in only 1 iteration the solution will converge
def valueIteration():
	v = dict()
	for i in range(TotalWickets + 1):
		for x in s:
			v[(i, x)] = 0
	
	policy = dict()

	v, policy = Bellman(v)
	
	return v, policy

#simulate n number of matches
def simulate(n):
	for i in range(1, n+1):
		fileName = "match" + str(i) + ".txt"

		wicketsLeft = TotalWickets
		runs = 0
		score = []
		overs = "22222"
		o = 0
		while(True):
			o += 1
			if(overs == "00000"):
				break
			if(wicketsLeft == 0):
				break
			
			b = policy[(wicketsLeft, overs)]
			runs += economy[b]

			w = random.random()
			if(w < 6/strike[b]):
				wicketsLeft -= 1
				
			score.append(str(runs) + "-" + str(TotalWickets - wicketsLeft) + "\tin\t" + str(o))

			temp = ""
			for i in range(len(overs)):
				if(i == b):
					if(overs[i] == '1'):
						temp += '0'
					else:
						temp += '1'
				else:
					temp += overs[i]
			overs = temp

		with open(fileName, "w") as f:
			for x in score:
				f.write(x + "\n")

#get optimum value and policy
value, policy = valueIteration()

#print the policy in a text file
with open("policy.txt", "w") as f:
		for i in range(1, TotalWickets + 1):
			for x in s:
				f.write("Wickets Left: " + str(i) + "\tBowlers Left:" + str(x) + "\tPolicy: " + str(policy[(i, x)]) + "\tValue: " + str(value[(i, x)]) + "\n")

#simulate 10 matches and print the score in text files
simulate(10)
