class Grid:
    def __init__(self, seed_function):
        self.row = 10
        self.col = 10
        try:
            self.grid = [[seed_function() for c in range(self.row)] for r in range(self.row)]
        except:
            self.grid = [[seed_function(r,c) for c in range(self.col)] for r in range(self.col)]
                    
