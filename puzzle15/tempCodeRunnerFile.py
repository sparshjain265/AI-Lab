print("Enter the elements of the matrix: ")
        for i in range(self.dimension):
            temp = input().strip().split()
            for j, x in zip(range(self.dimension), temp):
                if(x == '*'):
                    self.mat[i][j] = self.dimension*self.dimension
                    #print(self.mat[i][j])
                    self.x = i
                    self.y = j
                else :
                    self.mat[i][j] = int(x)