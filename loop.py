from claspy import *
from grid import *

puzzle = """\
. ` ` ` ` ` ` ` ` `
` ` ` ` ` ` ` ` ` `
` ` ` ` ` ` ` ` . `
` ` ` ` ` ` ` ` ` `
` ` ` ` ` ` ` ` ` `
` ` ` ` ` ` ` ` ` `
` ` ` ` ` ` ` ` . `
` ` ` ` ` . ` ` ` `
` ` ` ` ` ` ` ` ` `
` ` ` ` ` ` ` ` ` `"""

puzzle = puzzle.split('\n')
for i in range(10):
    puzzle[i] = puzzle[i].split(' ')

'''
0 = -
1 = |
2 = ┛
3 =┖
4 =┎
5 = ┒
'''

ISOLATED = ['.', '']
LEFT_CONNECTING = [0, 2, 5]
RIGHT_CONNECTING = [0, 3, 4]
UP_CONNECTING = [1, 2, 3]
DOWN_CONNECTING = [1, 4, 5]

grid = [[IntVar(0,5) if puzzle[r][c] == '`' else '.' for c in range(10)] for r in range(10)]
loop_graph = [[Atom() for c in range(10)] for r in range(10)]
loop_start = [[BoolVar() for c in range(10)] for r in range(10)]
    
for r in range(10):
    for c in range(10):
        if not grid[r][c] == '.':
            #not leftmost
            if 0 <= c - 1:
                #not topmost
                if 0 <= r - 1:
                    require(var_in(grid[r][c-1], RIGHT_CONNECTING) & var_in(grid[r-1][c], DOWN_CONNECTING) == (grid[r][c] == 2))
                    loop_graph[r][c].prove_if(loop_start[r][c] | ((grid[r][c] == 2) & (loop_graph[r][c-1] | loop_graph[r-1][c])))
                #not bottommost
                if r + 1 < 10:
                    require(var_in(grid[r][c-1], RIGHT_CONNECTING) & var_in(grid[r+1][c], UP_CONNECTING) == (grid[r][c] == 5))
                    loop_graph[r][c].prove_if(loop_start[r][c] | ((grid[r][c] == 5) & (loop_graph[r][c-1] | loop_graph[r+1][c])))
                #not rightmost
                if c + 1 < 10:
                    require(var_in(grid[r][c-1], RIGHT_CONNECTING) & var_in(grid[r][c+1], LEFT_CONNECTING) == (grid[r][c] == 0))
                    loop_graph[r][c].prove_if(loop_start[r][c] | ((grid[r][c] == 0) & (loop_graph[r][c-1] | loop_graph[r][c+1])))
            #not rightmost
            if c + 1 < 10:
                #not topmost
                if 0 <= r - 1:
                    require(var_in(grid[r][c+1], LEFT_CONNECTING) & var_in(grid[r-1][c], DOWN_CONNECTING) == (grid[r][c] == 3))
                    loop_graph[r][c].prove_if(loop_start[r][c] | ((grid[r][c] == 3) & (loop_graph[r][c+1] | loop_graph[r-1][c])))
                #not bottommost
                if r + 1 < 10:
                    require(var_in(grid[r][c+1], LEFT_CONNECTING) & var_in(grid[r+1][c], UP_CONNECTING) == (grid[r][c] == 4))
                    loop_graph[r][c].prove_if(loop_start[r][c] | ((grid[r][c] == 4) & (loop_graph[r][c+1] | loop_graph[r+1][c])))
            if 0 < r and r + 1 < 10:
                require(var_in(grid[r-1][c], DOWN_CONNECTING) & var_in(grid[r+1][c], UP_CONNECTING) == (grid[r][c] == 1))
                loop_graph[r][c].prove_if(loop_start[r][c] | ((grid[r][c] == 1) & (loop_graph[r-1][c] | loop_graph[r+1][c])))
            if r == 0:
                require(~var_in(grid[r][c], UP_CONNECTING))
            if r == 9:
                require(~var_in(grid[r][c], DOWN_CONNECTING))
            if c == 0:
                require(~var_in(grid[r][c], LEFT_CONNECTING))
            if c == 9:
                require(~var_in(grid[r][c], RIGHT_CONNECTING))
            require(loop_graph[r][c] | (var_in(grid[r][c], ISOLATED)))
while solve():
    print('solution:')
    print(grid)
    x = BoolVar(True)
    for r in range(9):
        for c in range(9):
            x = x & (grid[r][c] == grid[r][c].value())
    require(~x)

