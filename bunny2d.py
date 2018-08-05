class Environment :
	def __init__(self, clx, cly, sl, sd) :
		self.currentLocationX = clx
		self.currentLocationY = cly
		self.shoreLocation = sl
		self.shoreDirection = sd
	 
	def updateState(self, direction, steps) :
		if(direction == "left") :
			self.currentLocationX -= steps
		elif(direction == "right") :
			self.currentLocationX += steps
		elif(direction == "up") :
			self.currentLocationY += steps
		elif(direction == "down") :
			self.currentLocationY -= steps
	
	def providePerception(self) :
		if(self.shoreDirection == "left") :
			if(self.currentLocationX <= self.shoreLocation) :
				return True
			else :
				return False
		elif(self.shoreDirection == "right") :
			if(self.currentLocationX >= self.shoreLocation) :
				return True
			else :
				return False
		elif(self.shoreDirection == "up") :
			if(self.currentLocationY >= self.shoreLocation) :
				return True
			else :
				return False
		elif(self.shoreDirection == "down") :
			if(self.currentLocationY <= self.shoreLocation) :
				return True
			else :
				return False

class Agent :
	def __init__(self) :
		self.locationX = 0
		self.locationY = 0
		self.direction = "left"
		self.steps = 0
	
	def getPerception(self, env) :
		return env.providePerception()
	
	def takeAction(self, env) :
		if(self.direction == "left") :
			self.steps += 1
			self.direction = "up"
			self.locationY += self.steps
		elif(self.direction == "up") :
			self.direction = "right"
			self.locationX += self.steps
		elif(self.direction == "right") :
			self.steps += 1
			self.direction = "down"
			self.locationY -= self.steps
		elif(self.direction == "down") :
			self.direction = "left"
			self.locationX -= self.steps
		env.updateState(self.direction, self.steps)

print("Give starting location (x y) ")
startingLocationX, startingLocationY = map(int, input().split())
print("Give shore location ")
shoreLocation = int(input())
print("Give shore direction (left, right, up or down) ")
shoreDirection = str(input())

Sea = Environment(startingLocationX, startingLocationY, shoreLocation, shoreDirection)
Bunny = Agent()

while(Bunny.getPerception(Sea) == False) :
	Bunny.takeAction(Sea)
	condition = "Current Location: (" + str(Sea.currentLocationX) + ", " + str(Sea.currentLocationY) + ")"
	condition += ",\t Bunny Location: (" + str(Bunny.locationX) + ", " + str(Bunny.locationY) + ")"
	if(Bunny.getPerception(Sea) == False) :
		condition += ",\t Perception: Sea"
	else :
		condition += ",\t Perception: Shore"
	condition += ",\t Action: Move " + Bunny.direction + " " + str(Bunny.steps) + " steps"
	condition += ",\t Shore Location: " + str(Sea.shoreLocation) + " (" + str(Sea.shoreDirection) + ")"
	print(condition)

print("Bunny reached shore!")
