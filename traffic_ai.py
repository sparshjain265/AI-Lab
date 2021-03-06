#!/usr/bin/python
#	Program Name: traffic.py
#	Programmer	: Sparsh Jain
#	Roll No		: 111601026
#	Date			: August 12, 2018
#	Description	: Creates a csv file named output.csv where each column gives the time of entry of a vehicle at the corresponding node in its path

import numpy as np
import pickle as pk
import math
import Queue as Q

#class Environment contains matrix of road network, a matrix of road status (number of vehicles in the corresponding road), 
class Environment :
	def __init__(self, road) :
		self.road = road
		self.state = np.reshape([0]*road.shape[0]*road.shape[1], (road.shape))

	#function updateState defined to update the status (number of vehicles in a road) when a vehicle enters/exits a road
	def updateState(self, status, source, destination) :
		if(status[0] != 0) :	#if the vehicle is starting the journey, no need to reduce the number of vehicles on any road
			self.state[status[1], status[2]] -= 1
		if(status[0] < 4) :	#if the vehicle has not finished the journey, increment the number of vehicles on next road it takes
			self.state[source][destination] += 1
	
	#function providePerception to return the distance of the road and the number of cars already on the road
	def providePerception(self, source, destination) :
		return [self.road[source][destination], self.state[source][destination]]

#class Agent contains the data of each vehicle including 
#the time it's next scheduled to move as time
#the timeStamp vector with each value indicating the timeStamp of the vehicle at the corresponding path it has to cover
#a status vector with first element as the ith node it is currently on (or going to) corresponding to the path vector,
#second element as the source node, and third element as the destination node to store the previous road it was travelling
#a path vector indicating it's path across the city
#a key value 'i' to store the index of the vehicle
#a boolean value completed to store whether the vehicle has completed the journey or not
class Agent :
	def __init__(self, time, path, i) :
		self.time = time/60.0	#given time is in minutes, store in hours
		self.timeStamp = np.zeros(4)
		self.timeStamp = np.insert(self.timeStamp, [0], self.time)
		self.status = np.array([0, 0, 0])
		self.path = path
		self.i = i
		self.completed = False

	#function getPerception defined to get the distance and the number of vehicles currently between the source and destination
	def getPerception(self, env) :
		source = self.path[self.status[0]]
		destination = self.path[self.status[0] + 1]
		return env.providePerception(source, destination)
	
	#function __cmp__ defined to enable priorityQueue
	def __cmp__(self, other) :
		return cmp(self.time, other.time)
	
	#function takeAction to take an Action based on the current status of the car
	#returns whethe the vehicle has completed the journey or not
	def takeAction(self, env) :
		#if the car has not finished it's journey
		if(self.status[0] < 4) :
			#get source, destination, the distance, and number of cars on that road
			source = self.path[self.status[0]]
			destination = self.path[self.status[0] + 1]
			[d, x] = self.getPerception(env)
			#update self and city status as the car moves
			env.updateState(self.status, source, destination)
			self.status[0] += 1
			self.status[1] = source
			self.status[2] = destination
			#determine speed and time taken (in hours) and update next move time and the timeStamp
			s = math.exp(0.5*x)/(1 + math.exp(0.5*x)) + 15/(1 + math.exp(0.5*x))
			t = d/s
			self.time += t
			self.timeStamp[self.status[0]] = self.time
		#else, the car has finished it's journey! update self and city status
		else :
			source = 0
			destination = 0
			self.completed = True
			env.updateState(self.status, source, destination)
		return self.completed

#load road network, starting time, and paths for vehicles
road = np.array(pk.load(open("road", "r")))
time = np.array(pk.load(open("time", "r")))
paths = np.array(pk.load(open("vehicle", "r")))
#store the total number of cars
n = len(time)

#create a city and place vehicles in the city with the given information in a priority queue
#the queue takes next instant the vehicle changes the road as priority
city = Environment(road)
vehicle = Q.PriorityQueue()
for i in range(n) :
	vehicle.put(Agent(time[i], paths[i], i))

#create an empty output matrix (to be filled as vehicles complete their journey)
output = np.zeros((n, 5))

#while the vehicles who have not completed the journey exist
while not vehicle.empty() :
	#get the vehicle with next time instance
	min = vehicle.get()
	#take action and check whether it has completed it's journey
	min_completed = min.takeAction(city)
	#if not, put it back in the queue
	if(not min_completed) :
		vehicle.put(min)
	#else update the corresponding entry in the output matrix as it's timeStamp
	else :
		output[min.i] = min.timeStamp

#store the output in a csv format
np.savetxt("output.csv", output, delimiter=",")