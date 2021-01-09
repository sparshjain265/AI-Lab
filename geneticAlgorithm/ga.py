import random

populationSize = 100
genes = "abcdefghijklmnopqrstuvwxyz "
mutation_prob = 0.1

target = "sparsh jain"

def fitness(string):
	count = 0
	for letter, i in zip(string, range(len(string))):
		if (letter == target[i]):
			count += 1
	return count

#take 2 parents, and return 2 children
def crossover(a, b):
	r = random.randint(1, len(target) - 2)
	c = ""
	d = ""
	#swap till r
	for i in range (r):
		c = c + a[i]
		d = d + b[i]

	for i in range(r, len(target)):
		c = c + b[i]
		d = d + a[i]
	
	return (c, d)

#take a child, and mutate
def mutation(ind):
	mut = ""
	for i in range(len(ind)):
		if( random.random() < mutation_prob):
			temp = random.randint(0, len(genes) - 1)
			mut = mut + genes[temp]
		else:
			mut = mut + ind[i]
	
	return mut

#return an initializeed population
def initPop():
	population = []
	for i in range(populationSize):
		individual = ""
		for j in range(len(target)):
			individual = individual + genes[random.randint(0, len(genes) - 1)]
		population.append((fitness(individual), individual))
	
	return population

def geneticAlgorithm():
	#initialize the population
	population = initPop()
	#population = sorted(population)
	
	generation = 0
	while(True):
		population = sorted(population)
		#print the most fit element
		print("Generation " + str(generation) + ":" + population[populationSize - 1][1] + " Fitness Score: " + str(population[populationSize - 1][0]))

		if(population[populationSize-1][0] == len(target)):
			break
		generation += 1
		(a, b) = crossover(population[populationSize - 1][1], population[populationSize - 2][1])
		a = mutation(a)
		b = mutation(b)

		population[0] = (fitness(a), a)
		population[1] = (fitness(b), b)



geneticAlgorithm()
