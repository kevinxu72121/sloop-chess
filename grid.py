class Grid:
    def __init__(self, seed_function):
        self.row = 10
        self.col = 10
        try:
            self.grid = [[seed_function() for c in range(self.row)] for r in range(self.row)]
        except:
            self.grid = [[seed_function(r,c) for c in range(self.col)] for r in range(self.col)]

    def getNeighbors(r,c):
        neighbors = []
        for (y,x) in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
            neighbors.append((y,x))
        return neighbors

    def isValid(r,c):
        return 0 <= r < 10 and 0 <= c < 10

    def iter(self):
        for r in range(10):
            for c in range(10):
                yield (r,c)
                    
