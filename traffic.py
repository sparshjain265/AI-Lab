#!/usr/bin/python
import numpy as np
import pickle as pk
import math

road = pk.load(open("road", "r"))
time = pk.load(open("time", "r"))
vehicle = pk.load(open("vehicle", "r"))

#print(road)
#print(time)
#print(vehicle)

min = np.argmin(time)

timeStamp = np.zeros((len(time), 4))
timeStamp = np.insert(timeStamp, [0], time, axis = 1)
#print timeStamp

status = np.reshape([0]*len(time) * 3, (len(time), 3))
#print status

v = np.reshape([0]*road.shape[0]*road.shape[1], (road.shape))
#print v

completed = 0
while(completed < len(time)) :
	min = np.argmin(time)
	if(status[min, 0] != 0) :
		v[status[min, 1], status[min, 2]] -= 1
	if(status[min, 0] == 4) :
		completed += 1
		time[min] = float("inf")
		continue
	source = vehicle[min, status[min, 0]]
	#print source
	destination = vehicle[min, status[min, 0] + 1]
	#print destination
	d = road[source, destination]
	#print distance
	x = v[source, destination]
	#print x
	s = math.exp(0.5*x)/(1 + math.exp(0.5*x)) + 15/(1 + math.exp(0.5*x))
	#print s
	t = d/s
	t = t*60
	#print t
	time[min] += t
	status[min, 0] += 1
	status[min, 1] = source
	status[min, 2] = destination
	timeStamp[min, status[min, 0]] = time[min]
	v[source, destination] += 1

print timeStamp
arr = np.array(timeStamp)
np.savetxt("output.csv", arr, delimiter=",")