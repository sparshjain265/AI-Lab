class Environment :
	def __init__(self, cl, sl) :
		self.currentLocation = cl
		self.shoreLocation = sl
	 
	def updateState(self, action, steps) :
		if(action == "right") :
			self.currentLocation += steps
		elif(action == "left") :
			self.currentLocation -= steps
	
	def providePerception(self) :
		if(self.currentLocation == self.shoreLocation) :
			return True
		else :
			return False

class Agent :
	def __init__(self) :
		self.location = 0
		self.direction = "left"
		self.steps = 0
	
	def getPerception(self, env) :
		return env.providePerception()
	
	def takeAction(self, env) :
		self.steps += 1
		if(self.direction == "left") :
			self.direction = "right"
			self.location += self.steps
		elif(self.direction == "right") :
			self.direction = "left"
			self.location -= self.steps
		env.updateState(self.direction, self.steps)

print("Give starting location ")
startingLocationX, startingLocationY = map(int, input().split())
print("Give shore location ")
shoreLocation = int(input())

Sea = Environment(startingLocationX, shoreLocation)
Bunny = Agent()

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

print("Bunny reached shore!")
