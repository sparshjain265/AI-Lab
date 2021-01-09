import random
import math
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt

get_bin = lambda x, n: format(x, 'b').zfill(n)

class GA :
	def __init__(self, p, m, c):
		self.populationSize = p
		self.bitLength = 10
		self.rangeMin = -204
		self.rangeMax = 204
		self.mutation_prob = m
		self.crossover_prob = c
		self.dimension = 5

	def f1 (self, x):
		l = len(x)
		y = [0.0]*l
		for i in range(l):
			y[i] = x[i]/100

		a = la.norm(y)
		return a * a

	def f2 (self, x):
		l = len(x)
		y = [0]*l
		for i in range(l):
			y[i] = math.floor(x[i]/100)

		return sum(y)

	def f3 (self, x):
		l = len(x)
		y = [0.0]*l
		r = 0
		for i in range(l):
			y[i] = x[i]/100
			r += (i+1)*((y[i])**4)

		return r + random.normalvariate(0, 1)


	def fitness(self, x, y):
		sx = 0
		sy = 0

		if(self.f1(x) > self.f1(y)):
			sx += 1
		else:
			sy += 1

		if(self.f2(x) > self.f2(y)):
			sx += 1
		else:
			sy += 1

		if(self.f3(x) > self.f3(y)):
			sx += 1
		else:
			sy += 1

		if(sx > sy):
			return y
		else :
			return x


	def crossover(self, a, b):
		l = len(a)
		ca = [0]*l
		cb = [0]*l
		for j in range(l):
			pa = get_bin(a[j], self.bitLength)
			pb = get_bin(b[j], self.bitLength)

			r = random.randint(1, self.bitLength - 2)
			c = ""
			d = ""

			for i in range(r):
				c = c + pa[i]
				d = d + pb[i]

			for i in range(r, self.bitLength):
				c = c + pb[i]
				d = d + pa[i]

			ca[j] = int(c, 2)
			cb[j] = int(d, 2)

		return (ca, cb)

	#take a child, and mutate
	def mutation(self, indi):
		l = len(indi)
		mut = [""]*l
		for j in range(l):
			ind = get_bin(indi[j], self.bitLength)
			for i in range(len(ind)):
				if( random.random() < self.mutation_prob):
					temp = ind[i]
					if(temp == '0'):
						temp = '1'
					elif(temp == '1'):
						temp = '0'
					mut[j] = mut[j] + temp
				else:
					mut[j] = mut[j] + ind[i]
			mut[j] = int(mut[j], 2)

		return mut

	#return an initializeed population
	def initPop(self):
		population = []
		for i in range(self.populationSize):
			x = []
			for j in range(self.dimension):
				x.append(random.randint(self.rangeMin, self.rangeMax))
			population.append(x)
		return population

	def best2(self, l):
		x = self.fitness(l[0], l[1])
		x = self.fitness(x, l[2])
		x = self.fitness(x, l[3])

		l.remove(x)
		y = self.fitness(l[0], l[1])
		y = self.fitness(y, l[2])

		return (x, y)

	def geneticAlgorithm(self, epoch):

		population = self.initPop()

		generation = 0
		F1 = []
		F2 = []
		F3 = []

		# while(True):
		for _ in range(epoch):
			random.shuffle(population)
			generation += 1

			best = population[0]
			for i in range(len(population)):
				best = self.fitness(best, population[i])

			# print("Generation " + str(generation) + ": " + str(best))
			F1.append(self.f1(best))
			F2.append(self.f2(best))
			F3.append(self.f3(best))

			for i in range(len(population)//2):
				r = random.random()
				if( r < self.crossover_prob ):
					a, b = self.crossover(population[i], population[i + len(population)//2])
					a = self.mutation(a)
					b = self.mutation(b)
					x, y = self.best2([a, b, population[i], population[i + len(population)//2]])
					population[i] = x
					population[i + len(population)//2] = y

		plt.figure(figsize=(10,10))	
		plt.plot(range(epoch), F1, label = 'f1')
		plt.plot(range(epoch), F2, label = 'f2')
		plt.plot(range(epoch), F3, label = 'f3')
		plt.title("Population Size: " + str(self.populationSize) + " f1=" + str(F1.pop()) + " f2=" + str(F2.pop()) + " f3=" + str(F3.pop()) + "\nCross-Over Probability: " + str(self.crossover_prob) + " Mutation Probability: " + str(self.mutation_prob) + "\nEpoch: " + str(epoch) + " Last Gen: " + str(np.asarray(best)/100))
		plt.legend()
		plt.savefig("basicga/" + "P" + str(self.populationSize) + "C" + str(self.crossover_prob) + "M" + str(self.mutation_prob) + "E" + str(epoch) + ".png")
		# plt.show()
		plt.close()

N = [50, 100, 200]
C = [0.2, 0.3]
M = [0.01, 0.05]
E = [10, 20, 50, 100, 200, 500]
for n in N:
	for c in C:
		for m in M:
			for e in E:
				g = GA(n, m, c)
				g.geneticAlgorithm(e)