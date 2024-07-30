# -*- coding: cp936 -*-
from claspy import *
import Tkinter as tk
import time as t
import itertools, copy, random, math
from solver import *

#properties of each cell in the grid
class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.changeable = True
        self.color = "white"
        self.button = w.create_rectangle(5+40*self.x, 5+40*self.y, 45+40*self.x, 45+40*self.y, fill="white", outline = 'black')

#general operation, including switching players, terminating the game after the result is determined
class Game:
    def __init__(self):
        self.round = 1
        self.currentPlayer = "human"

    def switch(self, player1, player2):
        if self.currentPlayer == player1:
            self.currentPlayer == player2
        else:
            self.currentPlayer == player1
        self.round += 1

    def win(self):
        w.itemconfig(label, text="You Won!")
        w.unbind("<Button-1>")

    def lose(self):
        w.itemconfig(label, text="You Lost!")
        w.unbind("<Button-1>")

#make a hypothetical move
def move(state, p1, p2):
    temp = copy.deepcopy(state)
    if p1 != None and p2 != None:
        r1 = p1[0]
        r2 = p2[0]
        c1 = p1[1]
        c2 = p2[1]
        if state[r1][c1].color == "white" and state[r2][c2].color == "white" and not (r1 == r2 and c1 == c2):
            temp[r1][c1].color = "black"
            temp[r2][c2].color = "black"
    return temp

#the score of each move is based on the number of legal moves that the board would have after making that move
#the less move there are the larger the score is
def evaluate(legalmoves):
    return -len(legalmoves)

#properties of each state
class Node:
    def __init__(self, parent, initialState, p1, p2, isMax):
        self.parent = parent
        self.p1 = p1
        self.p2 = p2
        self.state = move(initialState, p1, p2)
        self.legalmoves = legalMove(self.state)
        self.value = evaluate(self.legalmoves)
        self.children = []
        self.isMax = isMax
        print(self.value, p1, p2, isMax)

#create the tree for minimax searching, has a 100 second time limit
def createTree(node, tick):
    if len(node.legalmoves) == 0 or t.time() - tick > 100:
        return
    else:
        for i in node.legalmoves:
            temp = Node(node, node.state, i[0], i[1], not node.isMax)
            createTree(temp,tick)
            node.children.append(temp)

class AI:
    def __init__(self):
        pass

    #minimax algorithm, determine the best move
    def alphaBeta(self, node, alpha=-float('inf'), beta=float('inf')):
        if len(node.children) == 0:
            return node.value
        if not node.isMax:
            best = float('inf')
            for i in node.children:
                value = ai.alphaBeta(i, alpha, beta)
                best = min(best, value)
                beta = min(beta, best)
                if alpha >= beta:
                    break
        else:
            best = -float('inf')
            for i in node.children:
                value = ai.alphaBeta(i, alpha, beta)
                best = max(best, value)
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best

    #change the board
    def AImove(self, p1, p2):
        w.itemconfig(buttons[p1[0]][p1[1]].button, fill="black")
        buttons[p1[0]][p1[1]].color = "black"
        buttons[p1[0]][p1[1]].changeable = False
        w.itemconfig(buttons[p2[0]][p2[1]].button, fill="black")
        buttons[p2[0]][p2[1]].color = "black"
        buttons[p2[0]][p2[1]].changeable = False
        game.switch("human", "AI")

#return a list of legal moves based on the simple loop solver
def legalMove(buttons):
    legalmoves = []
    if Loop(transform(buttons)).isSolvable():
        reset()
        temp = copy.deepcopy(buttons)
        tick = t.time()
        for p1 in list(itertools.product(range(6), range(6))):
            for p2 in list(itertools.product(range(6), range(6)))[list(itertools.product(range(6), range(6))).index(p1):]:
                if (game.round == 2 and t.time() - tick < 8) or (game.round > 2 and t.time() - tick < 4): #time constraint
                    r1 = p1[0]
                    r2 = p2[0]
                    c1 = p1[1]
                    c2 = p2[1]
                    if buttons[r1][c1].color == "white" and buttons[r2][c2].color == "white" and not (r1 == r2 and c1 == c2):
                        #a simple pattern to reduce the amount of checks
                        #if a white cell has more than 2 black cells surrounding it, the board would evidently have no solution
                        checking = True
                        temp[r1][c1].color = "black"
                        temp[r2][c2].color = "black"
                        
                        for i in list(itertools.product(range(6), range(6))):
                            if temp[i[0]][i[1]].color == "white" and countBlack(i[0],i[1],temp) >= 3:
                                checking = False
                                break
                        
                        if checking:
                            puzzle = Loop(encode(buttons, r1, c1, r2, c2))
                            if puzzle.isSolvable():
                                legalmoves.append((p1, p2))
                            reset()
                        
                        temp[r1][c1].color = "white"
                        temp[r2][c2].color = "white"
    return legalmoves

#locking the board after the player confirms the move
def confirm():
    for i in range(6):
        for j in range(6):
            if buttons[i][j].changeable and buttons[i][j].color == "black":
                buttons[i][j].changeable = False
    game.switch("human", "AI")

#count how many black cells are selected before a move is confirmed
def getPicked():
    n = 0
    for i in range(6):
        for j in range(6):
            if buttons[i][j].changeable and buttons[i][j].color == "black":
                n += 1
    return n

#transform the board into a format analyzable by the solver
def transform(buttons):
    puzzle = ''
    for i in range(6):
        for j in range(6):
            if buttons[i][j].color == "white":
                puzzle += '`'
            else:
                puzzle += '.'
            if j < 5:
                puzzle += ' '
        puzzle += '\n'
    return puzzle

#transform the board after a hypothetical move into a format analyzable by the solver
def encode(buttons, r1, c1, r2, c2):
    puzzle = ''
    for i in range(6):
        for j in range(6):
            if buttons[i][j].color == "black" or (i == r1 and j == c1) or (i == r2 and j == c2):
                puzzle += '.'
            else:
                puzzle += '`'
            if j < 5:
                puzzle += ' '
        puzzle += '\n'
    return puzzle

#get the number of surrounding black cells of a white cell (including the border)
def getSurrounding(r, c):
    surrounding = []
    if r >= 1:
        surrounding.append((r-1, c))
    if r <= 4:
        surrounding.append((r+1, c))
    if c >= 1:
        surrounding.append((r, c-1))
    if c <= 4:
        surrounding.append((r, c+1))
    return surrounding
def countBlack(r, c, buttons):
    count = 0
    if r == 0 or r == 5:
        count += 1
    if c == 0 or c == 5:
        count += 1
    for i in getSurrounding(r, c):
        if buttons[i[0]][i[1]].color == "black":
            count += 1
    return count

#making the cells interactive
def buttonBehavior(eventorigin):
    mouseX = eventorigin.x
    mouseY = eventorigin.y
    if 5 < mouseX and mouseX < 245 and 5 < mouseY and mouseY < 245:
        if buttons[(mouseX-5)//40][(mouseY-5)//40].changeable:
            if buttons[(mouseX-5)//40][(mouseY-5)//40].color == "white" and getPicked() < 2:
                w.itemconfig(buttons[(mouseX-5)//40][(mouseY-5)//40].button, fill="black")
                buttons[(mouseX-5)//40][(mouseY-5)//40].color = "black"
            else:
                w.itemconfig(buttons[(mouseX-5)//40][(mouseY-5)//40].button, fill="white")
                buttons[(mouseX-5)//40][(mouseY-5)//40].color = "white"
    if 80 < mouseX and mouseX < 170 and 270 < mouseY and mouseY < 300 and getPicked() == 2:
        confirm()
        picked = 0
        puzzle = transform(buttons)
        puzzle = Loop(puzzle)
        if not puzzle.isSolvable():
            reset()
            game.lose()
        else:
            reset()
            if game.round == 2:
                legalmoves = legalMove(buttons)
                opmove = legalmoves[random.randint(0,len(legalmoves)-1)]
                ai.AImove(opmove[0], opmove[1])
            else:
                temp = Node(None, buttons, None, None, False)
                if len(temp.legalmoves) == 0:
                    game.win()
                else:
                    tick = t.time()
                    createTree(temp, tick)
                    best = ai.alphaBeta(temp)
                    compval = abs(temp.children[0].value - best)
                    bestp1 = temp.children[0].p1
                    bestp2 = temp.children[0].p2
                    for i in temp.children:
                        if abs(i.value - best) < compval:
                            compval = abs(i.value - best)
                            bestp1 = i.p1
                            bestp2 = i.p2
                    ai.AImove(bestp1, bestp2)
        reset()

#tkinter configuration
if __name__=='__main__':
    root = tk.Tk()
    root.title('SLoop Chess')
    w = tk.Canvas(root, width=250,height=310)
    buttons = [[None for j in range(6)] for i in range(6)]
    game = Game()
    ai = AI()
    for i in range(6):
        for j in range(6):
            buttons[i][j] = Button(i, j)
    w.create_rectangle(70, 270, 180, 300, fill="white", outline = 'black')
    label = w.create_text(125, 285, text="confirm", font=('Helvetica 15 bold'))
    w.bind("<Button-1>", buttonBehavior)
    w.pack()
    root.mainloop()
