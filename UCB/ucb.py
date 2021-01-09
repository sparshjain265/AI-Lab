import numpy as np 
import math
import random
import matplotlib.pyplot as plt

#multi armed bandits with K arms each with bernoulli distribution of reward[0,1]
#R is the rewards at success while F is the reward at failure
class bandit:
	def __init__(self, K, P, R, F):
		self.K = K
		self.S = [0]*K
		self.N = [0]*K
		self.P = P
		self.F = F
		self.R = R
		self.proportion = []
		self.regret = []
	

	def pull(self, arm):
		self.N[arm] += 1
		r = random.random()
		if(r < self.P[arm]):
			self.S[arm] += self.R[arm]
		else:
			self.S[arm] += self.F[arm]

		p = [0]*self.K
		for i in range(self.K):
			p[i] = self.N[i]/sum(self.N)
		
		self.proportion.append(p)		
	
	def UCB(self, rounds):
		t = 1
		#pull each arm once
		for i in range(self.K):
			self.pull(i)
			t += 1
			self.regret.append(t * max(self.P) - sum(self.S))
		
		# p = self.proportion.pop()
		# self.proportion = []
		# self.proportion.append(p)

		#pull according to the algorithm
		ucb = [0]*self.K
		while(t <= rounds):
			
			for i in range(self.K):
				ucb[i] = (self.S[i]/self.N[i]) + math.sqrt((2 * math.log(t))/self.N[i])
			
			ucb = np.asarray(ucb)
			k = np.argmax(ucb)
			self.pull(k)
			t += 1
		
		self.plotFlow()	

	def plotFinal(self):
		plt.bar(x = range(self.K), height = self.N)
		plt.show()


	def plotFlow(self):
		t = 1
		self.proportion = np.asarray(self.proportion)
		# print(self.proportion[0])
		for i in range(self.K):
			plt.plot(range(1, len(self.proportion[:, i]) + 1), self.proportion[:, i], label = "arm " + str(i))
		plt.legend()
		plt.show()

P = [0.5, 0.9, 0.7, 0.8, 0.09]
R = [2, 0.5, 2, 1, 10, 1.1]
F = [-0.5, -1, -1, -5, -5]

b = bandit(5, P, R, F)
b.UCB(10000)
# b.plotFinal()