import random

class Population :
	def __init__(self, size, pool, target):
		self.size = size
		self.pool = pool
		self.target = target

class Individual :
	def __init__(self, population):
		self.population = population
		