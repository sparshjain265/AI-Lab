class Environment :								#class to define actual agent and shore location
	def __init__(self, cl, sl) :				#takes cl and sl and current agent and shore location
		self.currentLocation = cl
		self.shoreLocation = sl
	 
	def updateState(self, action, steps) :	#updates environment depending on agent response
		if(action == "right") :
			self.currentLocation += steps
		elif(action == "left") :
			self.currentLocation -= steps
	
	def providePerception(self) :				#provides perception to the agent
		if(self.currentLocation == self.shoreLocation) :
			return True
		else :
			return False

class Agent :										#class to define agent's view of environment
	def __init__(self) :							#agent thinks he's the center of the world ;)
		self.location = 0
		self.direction = "left"
		self.steps = 0
	
	def getPerception(self, env) :			#funtion to perceive the environment
		return env.providePerception()
	
	def takeAction(self, env) :				#function to take steps in the required direction
		self.steps += 1
		if(self.direction == "left") :
			self.direction = "right"
			self.location += self.steps
		elif(self.direction == "right") :
			self.direction = "left"
			self.location -= self.steps
		env.updateState(self.direction, self.steps)

#Taking input
print("Give starting location ")
startingLocation = int(input())
print("Give shore location ")
shoreLocation = int(input())

#Initializing objects
Sea = Environment(startingLocation, shoreLocation)
Bunny = Agent()

#Running the program
while(Bunny.getPerception(Sea) == False) :
	Bunny.takeAction(Sea)
	condition = "Current Location: " + str(Sea.currentLocation)
	condition += ",\t Bunny Location: " + str(Bunny.location)
	if(Bunny.getPerception(Sea) == False) :
		condition += ",\t Perception: Sea"
	else :
		condition += ",\t Perception: Shore"
	condition += ",\t Action: Move " + Bunny.direction + " " + str(Bunny.steps) + " steps"
	condition += ",\t Shore Location: " + str(Sea.shoreLocation)
	print(condition)

#Hurray!
print("Bunny reached shore!")
