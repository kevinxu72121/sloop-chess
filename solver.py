from claspy import *

ISOLATED = ['.']
LEFT_CONNECTING = [0, 2, 5]
RIGHT_CONNECTING = [0, 3, 4]
UP_CONNECTING = [1, 2, 3]
DOWN_CONNECTING = [1, 4, 5]

class Loop:
    def __init__(self, puzzle):
        puzzle = puzzle.split('\n')
        for i in range(6):
            puzzle[i] = puzzle[i].split(' ')

        self.grid = [[IntVar(0,5) if puzzle[r][c] == '`' else '.' for c in range(6)] for r in range(6)]
        self.loop_graph = [[Atom() for c in range(6)] for r in range(6)]
        self.loop_start = [[BoolVar() for c in range(6)] for r in range(6)]

    def isSolvable(self):
        global ISOLATED, LEFT_CONNECTING, RIGHT_CONNECTING, UP_CONNECTING, DOWN_CONNECTING
        for r in range(6):
            for c in range(6):
                if not self.grid[r][c] == '.':
                    #not leftmost
                    if 0 <= c - 1:
                        #not topmost
                        if 0 <= r - 1:
                            require(var_in(self.grid[r][c-1], RIGHT_CONNECTING) & var_in(self.grid[r-1][c], DOWN_CONNECTING) == (self.grid[r][c] == 2))
                            self.loop_graph[r][c].prove_if(self.loop_start[r][c] | ((self.grid[r][c] == 2) & (self.loop_graph[r][c-1] | self.loop_graph[r-1][c])))
                        #not bottommost
                        if r + 1 < 6:
                            require(var_in(self.grid[r][c-1], RIGHT_CONNECTING) & var_in(self.grid[r+1][c], UP_CONNECTING) == (self.grid[r][c] == 5))
                            self.loop_graph[r][c].prove_if(self.loop_start[r][c] | ((self.grid[r][c] == 5) & (self.loop_graph[r][c-1] | self.loop_graph[r+1][c])))
                        #not rightmost
                        if c + 1 < 6:
                            require(var_in(self.grid[r][c-1], RIGHT_CONNECTING) & var_in(self.grid[r][c+1], LEFT_CONNECTING) == (self.grid[r][c] == 0))
                            self.loop_graph[r][c].prove_if(self.loop_start[r][c] | ((self.grid[r][c] == 0) & (self.loop_graph[r][c-1] | self.loop_graph[r][c+1])))
                    #not rightmost
                    if c + 1 < 6:
                        #not topmost
                        if 0 <= r - 1:
                            require(var_in(self.grid[r][c+1], LEFT_CONNECTING) & var_in(self.grid[r-1][c], DOWN_CONNECTING) == (self.grid[r][c] == 3))
                            self.loop_graph[r][c].prove_if(self.loop_start[r][c] | ((self.grid[r][c] == 3) & (self.loop_graph[r][c+1] | self.loop_graph[r-1][c])))
                        #not bottommost
                        if r + 1 < 6:
                            require(var_in(self.grid[r][c+1], LEFT_CONNECTING) & var_in(self.grid[r+1][c], UP_CONNECTING) == (self.grid[r][c] == 4))
                            self.loop_graph[r][c].prove_if(self.loop_start[r][c] | ((self.grid[r][c] == 4) & (self.loop_graph[r][c+1] | self.loop_graph[r+1][c])))
                    if 0 < r and r + 1 < 6:
                        require(var_in(self.grid[r-1][c], DOWN_CONNECTING) & var_in(self.grid[r+1][c], UP_CONNECTING) == (self.grid[r][c] == 1))
                        self.loop_graph[r][c].prove_if(self.loop_start[r][c] | ((self.grid[r][c] == 1) & (self.loop_graph[r-1][c] | self.loop_graph[r+1][c])))
                    if r == 0:
                        require(~var_in(self.grid[r][c], UP_CONNECTING))
                    if r == 5:
                        require(~var_in(self.grid[r][c], DOWN_CONNECTING))
                    if c == 0:
                        require(~var_in(self.grid[r][c], LEFT_CONNECTING))
                    if c == 5:
                        require(~var_in(self.grid[r][c], RIGHT_CONNECTING))
                    require(self.loop_graph[r][c] | (var_in(self.grid[r][c], ISOLATED)))
        is_loop_start = [(self.loop_start[r][c] & ~var_in(self.grid[r][c], ISOLATED)) for c in range(6) for r in range(6)]
        require(at_least(1, is_loop_start))
        require(at_most(1, is_loop_start))
        return solve()
