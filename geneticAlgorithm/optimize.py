import random

populationSize = 2
# genes = "abcdefghijklmnopqrstuvwxyz"
bitLength = 11
rangeMin = -1023
rangeMax = 1024
mutation_prob = 0.1
crossover_prob = 1

get_bin = lambda x, n: format(x, 'b').zfill(n)

# target = "sparsh"

# def fitness(string):
# 	count = 0
# 	for letter, i in zip(string, range(len(string))):
# 		if (letter == target[i]):
# 			count += 1
# 	return count

def f1 (x):
	return x * x

def f2 (x):
	return (x - 2) * (x - 2)

def fitness(x, y):
	if(f1(x) > f1(y) and f2(x) > f2(y)):
		return y
	else:
		return x


def crossover(a, b):
	pa = get_bin(a, bitLength)
	pb = get_bin(b, bitLength)

	r = random.randint(1, bitLength - 2)
	c = ""
	d = ""

	for i in range(r):
		c = c + pa[i]
		d = d + pb[i]
	
	for i in range(r, bitLength):
		c = c + pb[i]
		d = d + pa[i]

	ca = int(c, 2)
	cb = int(d, 2)

	return (ca, cb)

#take a child, and mutate
def mutation(ind):
	ind = get_bin(ind, bitLength)
	mut = ""
	for i in range(len(ind)):
		if( random.random() < mutation_prob):
			temp = ind[i]
			if(temp == '0'):
				temp = '1'
			elif(temp == '1'):
				temp = '0'
			mut = mut + temp
		else:
			mut = mut + ind[i]
	
	return int(mut, 2)

#return an initializeed population
def initPop():
	population = []
	for i in range(populationSize):
		population.append(random.randint(rangeMin, rangeMax))
	return population

def best2(l):
	x = fitness(l[0], l[1])
	x = fitness(x, l[2])
	x = fitness(x, l[3])

	l.remove(x)
	y = fitness(l[0], l[1])
	y = fitness(y, l[2])

	return (x, y)

def geneticAlgorithm():
	
	population = initPop()

	generation = 0

	# while(True):
	for _ in range(100):
		random.shuffle(population)
		generation += 1

		best = population[0]
		for i in range(len(population)):
			best = fitness(best, population[i])
		
		print("Generation " + str(generation) + ": " + str(best))

		for i in range(len(population)//2):
			r = random.random()
			if( r < crossover_prob ):
				a, b = crossover(population[i], population[i + len(population)//2])
				a = mutation(a)
				b = mutation(b)
				x, y = best2([a, b, population[i], population[i + len(population)//2]])
				population[i] = x
				population[i + len(population)//2] = y

geneticAlgorithm()
