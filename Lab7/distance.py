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
        file = open ("input.txt" , "r")
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
    def heuristic(self, x):
        return math.sqrt((self.node[self.goal][0] - x[0])**2 + (self.node[self.goal][1] - x[1])**2)


    #solve using a star algo
    def astar(self):
        #store the state of each node as parent, g(n), h(n)
        state = dict()
        visited = set()
        Q = []
        heapq.heapify(Q)

        for i in range(self.n):
            state[i] = (-1, math.inf, self.heuristic(self.node[i]))
        state[self.start] = (-1, 0, self.heuristic(self.node[self.start]))
        heapq.heappush(Q, (state[self.start][1] + state[self.start][2], self.start))

        counter = 0
        while Q:
            counter += 1
            d, curr = heapq.heappop(Q)

            if(curr == self.goal):
                self.printPath(state)
                return True

            visited.add(curr)

            for v in self.graph[curr]:
                vertex = v[0]
                weight = v[1]
                if(vertex not in visited and state[vertex][1] > state[curr][1] + weight):
                    state[vertex] = (curr, state[curr][1] + weight, self.heuristic(self.node[vertex]))
                    heapq.heappush(Q, (state[vertex][1] + state[vertex][2], vertex))

        print("Path not found")
        return False

    def printPath(self, state):
        current = self.goal
        path = []
        while(current != -1):
            path.insert(0, current)
            current = state[current][0]
        print("Path:", end = " ")
        for i in path:
            print(i + 1, end = " ")
        print()
        print("Total Cost: " + str(state[self.goal][1]))

Road = Navigation()
Road.astar()


