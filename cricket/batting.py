import numpy as np
import math
import random

A = [1, 2, 3, 4, 6]
index = {1:0, 2:1, 3:2, 4:3, 6:4}
PWmin = [0.01, 0.02, 0.03, 0.1, 0.3]
PWmax = [0.1, 0.2, 0.3, 0.5, 0.7]

#if x wickets in hand, and action a is chosen
def pw(x, a):
	return PWmax[a] + (PWmin[a] - PWmax[a])*(x-1)/9

PRmin = 0.5
PRmax = 0.8

#if x wickets in hand
def pr(x):
	return PRmin + (PRmax - PRmin)*(x-1)/9

TotalBalls = 300
TotalWickets = 10

def Bellman(v):
	Uv = np.copy(v)
	policy = np.reshape([-1]*v.shape[0]*v.shape[1], (v.shape))

	#i+1 balls remaining
	for i in range(1, v.shape[0]):
		#j+1 wickets remaining
		for j in range(1, v.shape[1]):
			maxv = -math.inf
			arg = -1
			#kth action chosen
			for k in range(5):
				val = 0

				#case 1, out
				#if(j < TotalWickets):
				val += pw(j, k)*(0 + Uv[i - 1][j - 1])

				#case 2, success
				val += (1 - pw(j, k))*pr(j)*(A[k] + Uv[i-1][j])

				#case 3, failure
				val += (1 - pw(j, k))*(1 - pr(j))*(0 + Uv[i-1][j])

				if(val > maxv):
					maxv = val
					arg = k
			Uv[i][j] = maxv
			policy[i][j] = A[arg]
	
	return(Uv, policy)

def iteration(n):
	V = np.zeros((TotalBalls + 1, TotalWickets + 1))
	policy = np.reshape([-1]*TotalBalls*TotalWickets, (TotalBalls, TotalWickets))

	V, policy = Bellman(V)
	
	#print(policy[1:, 1:])
	np.savetxt ("policy.txt" , policy[1:, 1:] , fmt = "%i")
	np.savetxt("values.txt", V[1:, 1:], fmt = "%i")

	return V, policy

V, policy = iteration(100)

def simulate(n):
	for i in range(1, n+1):
		fileName = "match" + str(i) + ".txt"

		#ballsLeft = TotalBalls
		wicketsLeft = TotalWickets
		runs = 0
		score = []

		for b in range(TotalBalls):
			ballsLeft = TotalBalls - b
			if(wicketsLeft == 0):
				break;
			#get the action taken by the batsman from the policy
			a = policy[ballsLeft, wicketsLeft]
			
			#get probability of wicket
			w = random.random()
			#out
			if(w < pw(wicketsLeft, index[a])):
				wicketsLeft -= 1
				score.append(str(runs) + "-" + str(TotalWickets - wicketsLeft) + "\tin\t" + str(b + 1) + "\tW")
			else: #not out
				r = random.random()
				#successful
				if(r < pr(wicketsLeft)):
					runs += a
				score.append(str(runs) + "-" + str(TotalWickets - wicketsLeft) + "\tin\t" + str(b + 1) + "\t+" + str(a))
		
		with open(fileName, "w") as f:
			for s in score:
				f.write(s + "\n")

simulate(10)