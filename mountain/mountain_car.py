import numpy as np 
import math
import matplotlib.pyplot as plt
#define constants

vsteps = 100
vmax = 0.07
vmin = -0.07
velocity = np.linspace(vmin, vmax, vsteps)

psteps = 100
pmax = 0.6
pmin = -1.2
position = np.linspace(pmin, pmax, psteps)

reward = -1

pstart = -0.5
vstart = 0

#get index of that position and velocity in the array
def getIndex(pos, vel):

	div = (vmax - vmin) / (vsteps - 1)
	y = (vel - vmin) / div

	div = (pmax - pmin) / (psteps - 1)
	x = (pos - pmin) / div

	return (int(x), int(y))

#given initial position, velocity, and action taken
#return final position and velocity
def simulate(pos, vel, action):

	v = vel + action*0.002 + math.cos(3*pos) * (-0.0025)
	v = min(max(vmin, v), vmax)

	p = pos + v
	p = min(max(pmin, p), pmax)

	if(p == pmin or p == pmax):
		v = 0

	return (p, v)

#given an initial value, optimize it by iteration
#return the optimal value and corresponding policy
def valueIteration(value):
	policy = np.ones(value.shape)

	count = 0
	flag = True
	e = -math.inf
	while(flag or count < 500):
		count += 1
		
		e = -math.inf

		for r in range(psteps):
			for c in range(vsteps):
				pos = position[r]
				vel = velocity[c]

				val = -math.inf
				temp = -1

				for action in [-1, 0, 1]:
					p, v = simulate(pos, vel, action)
					x, y = getIndex(p, v)
					temp = value[x][y]
					
					if(p < 0.6):
						temp += reward
					
					if(temp > val):
						val = temp
						policy[r][c] = action
				
				e = max(e, abs(val - value[r][c]))
				value[r][c] = val

		print("#Iterations: " + str(count) + "\te: " + str(e))

		if(e <= 1):
			flag = False
		
		if(e <= 0.001):
			break
		
		
	return (value, policy)

#after getting the policy, simulate the game till you reach final position
def play(policy):
	p = pstart
	v = vstart
	print()
	print()
	print("Let's Start")
	while(p < pmax):
		x, y = getIndex(p, v)
		print("Position: " + str(p) + "\tVelocity: " + str(v) + "\tAction: " + str(policy[x][y]))
		p, v = simulate(p, v, policy[x][y])
	
	print("Position: " + str(p) + "\tVelocity: " + str(v) + "\tReached Goal")
		

value = np.zeros((psteps, vsteps))
value, policy = valueIteration(value)
np.savetxt ("policy.txt" , policy , fmt = "%i")
np.savetxt ("values.txt", value, fmt = "%i")
play(policy)

plt.imshow(value, cmap="hot")
plt.show()