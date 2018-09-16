class Environment :
	def __init__(self, xd, yd, xs, ys) :
		self.xd = xd
		self.yd = yd
		self.xr = xs
		self.yr = ys
	
	def updateState(self, direction) :
		if(direction == "left") :
			self.xr -= 1
		elif(direction == "right") :
			self.xr += 1
		elif(direction == "up") :
			self.yr += 1
		elif(direction == "down") :
			self.yr -= 1

	def providePerception(self) :
		if(self.xr == self.xd and self.yr == self.yd) :
			return True
		else :
			return False

class Agent :
	def __init__(self) :
		self.x = 0
		self.y = 0
		self.direction = "up"
		self.steps = 1
		self.s = 0

	def getPerception(self, env) :
		return env.providePerception()

	def takeAction(self, env) :
		if(self.direction == "up") :
			if(self.s < self.steps) :
				self.y += 1
				self.s += 1
				env.updateState(self.direction)
			elif(self.s == self.steps) :
				self.direction = "right"
				self.s = 0
		elif(self.direction == "right") :
			if(self.s < self.steps) :
				self.x += 1
				self.s += 1
				env.updateState(self.direction)
			elif(self.s == self.steps) :
				self.direction = "down"
				self.s = 0
				self.steps += 1
		elif(self.direction == "down") :
			if(self.s < self.steps) :
				self.y -= 1
				self.s += 1
				env.updateState(self.direction)
			elif(self.s == self.steps) :
				self.direction = "left"
				self.s = 0
		elif(self.direction == "left") :
			if(self.s < self.steps) :
				self.x -= 1
				self.s += 1
				env.updateState(self.direction)
			elif(self.s == self.steps) :
				self.direction = "up"
				self.s = 0
				self.steps += 1
		
print("Give starting location (x y) ")
xs, ys = map(int, input().split())
print("Give dirt location (x y) ")
xd, yd = map(int, input().split())

Room = Environment(xd, yd, xs, ys)
Robot = Agent()

while(Robot.getPerception(Room) == False) :
	condition = "Current Location: (" + str(Room.xr) + ", " + str(Room.yr) + ")"
	condition += ", Robot Location: (" + str(Robot.x) + ", " + str(Robot.y) + ")"
	condition += ", Perception: No Dirt"
	Robot.takeAction(Room)
	condition += ", Action Taken: Move " + Robot.direction
	condition += ", Dirt Location: (" + str(Room.xd) + ", " + str(Room.yd) + ")"
	if(Robot.s > 0) :
		print(condition)
	
condition = "Current Location: (" + str(Room.xr) + ", " + str(Room.yr) + ")"
condition += ", Robot Location: (" + str(Robot.x) + ", " + str(Robot.y) + ")"
condition += ", Perception: Dirt Found"
condition += ", Action Taken: Dirt Cleaned "
condition += ", Dirt Location: (" + str(Room.xd) + ", " + str(Room.yd) + ")"
print(condition)