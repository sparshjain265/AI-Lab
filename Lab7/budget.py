import numpy as np
import math
import heapq

class Navigation:
    def __init__(self):
        self.n = -1
        self.edges = -1
        self.node = dict()
        self.graph = []
        self.start = -1
        self.goal = -1
        self.takeInput()

    def takeInput(self):
        #Take input from file
        file = open ("Lab7/input.txt" , "r")
        line = file.readline()
        words = line.strip().split()
        self.n = int (words[0])

        #get coordinates of nodes
        for x in range(self.n):
            line = file.readline()
            words = line.strip().split()
            temp , coordinates = int(words[0]) , (int(words[1]) , int (words[2]))
            temp -= 1
            self.node[temp] = coordinates

        words = file.readline().strip().split()
        self.edges = int(words[0])

        #get edges and edge weights
        self.graph = [[] for _ in range(self.n)]
        for e in range(self.edges):
            line = file.readline()
            words = line.strip().split()
            x , y, weight = int (words[0]) - 1 , int (words[1]) - 1 , float(words[2])
            self.graph[x].append((y , weight))
            self.graph[y].append((x , weight))

        #get start and goal state
        word = file.readline().strip().split()
        self.start = int(word[0]) - 1

        word = file.readline().strip().split()
        self.goal = int(word[0]) - 1

        file.close()
    
    def printGraph(self):
        print("number of nodes : " , self.n)
        print("Nodes with there coordinates : ")
        print(self.node)

        print("Graph : ")
        for i in range(self.n):
            print(i+1, end = " ")
            print(self.graph[i])


        print("Start state : " , self.start)
        print("Goal state : " , self.goal)


    #Euclidean Heuristic
    def heuristic(self, x, speed):
        return math.sqrt((self.node[self.goal][0] - x[0])**2 + (self.node[self.goal][1] - x[1])**2) / speed


    #solve using a star algo
    def astar(self, congestion, budget, cost):
        print("Congestion: " + str(congestion) + "%")
        cycle = 25.0
        bus = 10.0 + 40.0 * (100 - congestion)/100
        speed = max(cycle, bus)
      

        #store the state of each node as parent, g(n), h(n), mode
        #each node is now stored as a tuple of (node, budget) in the search tree
        state = dict()
        Q = []
        heapq.heapify(Q)

        explored = set()
        qcount = 0

        frontier = []				
        
        state[(self.start, budget)] = ((-1, -1), 0, self.heuristic(self.node[self.start], speed), -1)

        heapq.heappush(Q, (state[(self.start, budget)][1] + state[(self.start, budget)][2], budget, qcount, self.start))
        frontier.append((self.start, budget))

        counter = 0
        while Q:
            counter += 1
            print("counter: " + str(counter))
            d, m, w, curr = heapq.heappop(Q)
            frontier.remove((curr, m))
            
            #do not expand a node where money left is less than 0
            if(m < 0):
                continue

            if(curr == self.goal):
                self.printPath(state, m, budget)
                return True

            explored.add(curr)

            for v in self.graph[curr]:
                vertex = v[0]
                weight = v[1]
                s = (vertex, m)

                #add cycle in frontier
                if(s not in explored and s not in frontier):
                    state[s] = ((curr, m), state[(curr, m)][1] + weight/cycle, self.heuristic(self.node[vertex], cycle), 1)
                    qcount += 1
                    heapq.heappush(Q, (state[s][1] + state[s][2], m, qcount, vertex))
                    frontier.append(s)
               
                elif s in frontier:
                    if(state[s][1] > state[(curr, m)][1] + weight/cycle):
                        state[s] = ((curr, m), state[(curr, m)][1] + weight/cycle, self.heuristic(self.node[vertex], cycle), 1)
                        qcount += 1
                        heapq.heappush(Q, (state[s][1] + state[s][2], m, qcount, vertex))
                        frontier.append(s)
                
                #add bus in frontier subject to condition
                b = int(m - (weight/bus)*cost)
                if(weight > 3 and b > 0):
                    s = (vertex, b)
                    if(s not in explored and s not in frontier):
                        state[s] = ((curr, m), state[(curr, m)][1] + weight/bus, self.heuristic(self.node[vertex], bus), 0)
                        qcount += 1
                        heapq.heappush(Q, (state[s][1] + state[s][2], b, qcount, vertex))
                        frontier.append(s)
               
                    elif s in frontier:
                        if(state[s][1] > state[(curr, m)][1] + weight/bus):
                            state[s] = ((curr, m), state[(curr, m)][1] + weight/bus, self.heuristic(self.node[vertex], bus), 0)
                            qcount += 1
                            heapq.heappush(Q, (state[s][1] + state[s][2], b, qcount, vertex))
                            frontier.append(s)
                        
        print("Path not found")
        return False

    def printPath(self, state, m, budget):
        current = (self.goal, m)
        path = []
        while(current[0] != self.start):
            path.insert(0, (current[0], state[current][3]))
            current = state[current][0]
        path.insert(0, (self.start, state[(self.start, budget)][3]))
        print("Path:", end = " ")
        for (i, j) in path:
            if(j == -1):
                j = "Start"
            elif(j == 0):
                j = "Bus"
            else:
                j = "Cycle"
            print(j + " " + str(i + 1), end = " ")
        print()
        print("Total Cost: " + str(state[(self.goal, m)][1] * 60) + " minutes.")
        print("Money Left: " + str(m))
        print()

Travel1 = Navigation()
Travel1.astar(0, 200, 1)

Travel2 = Navigation()
#Travel2.astar(50, 200, 1)

Travel3 = Navigation()
#Travel3.astar(100, 200, 1)