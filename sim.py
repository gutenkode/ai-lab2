# six nodes, A through F
# 15 edges (6 choose 2)
# 20 possible triangles (6 choose 3)

import math
from graphics import *

edges = [
    'AB', 'AC', 'AD', 'AE', 'AF',
    'BC', 'BD', 'BE', 'BF',
    'CD', 'CE', 'CF',
    'DE', 'DF',
    'EF'
]
triangles = [
    ('AB','BC','AC'), #ABC
    ('AB','BD','AD'), #ABD
    ('AB','BE','AE'), #ABE
    ('AB','BF','AF'), #ABF
    ('AC','CD','AD'), #ACD

    ('AC','CE','AE'), #ACE
    ('AC','CF','AF'), #ACF
    ('AD','DE','AE'), #ADE
    ('AD','DF','AF'), #ADF
    ('AE','EF','AF'), #AEF

    ('BC','CD','BD'), #BCD
    ('BC','CE','BE'), #BCE
    ('BC','CF','BF'), #BCF
    ('BD','DE','BE'), #BDE
    ('BD','DF','BF'), #BDF

    ('BE','EF','BF'), #BEF
    ('CD','DE','CE'), #CDE
    ('CD','DF','CF'), #CDF
    ('CE','EF','CF'), #CEF
    ('DE','EF','DF')  #DEF
]

def pol2cart(rho, phi):
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return(x, y)

win = GraphWin('Sim', 256, 256)
points = []
for i in range(0,6):
    x,y = pol2cart(100, i/3*math.pi -math.pi*2/3)
    x += 128
    y += 128
    point = Point(x,y)
    points.append(point)
    x,y = pol2cart(110, i/3*math.pi -math.pi*2/3)
    x += 128
    y += 128
    label = Text(Point(x,y), chr(ord('A')+points.index(point)))
    label.draw(win)

for pt1 in points:
    for pt2 in points:
        line = Line(pt1, pt2)
        line.setFill('light gray')
        line.draw(win)
for pt in points:
    pt.draw(win)

def isTriangle(state):
    for tri in triangles:
        if state.get(tri[0]) != None and state.get(tri[0]) == state.get(tri[1]) and state.get(tri[1]) == state.get(tri[2]):
            return state.get(tri[0])
    return False

def heuristic(state, weight):
    tri = isTriangle(state)
    if tri == 'P':
        return 1-weight
    elif tri == 'C':
        return -1+weight
    return weight

def getAdjacentStates(state, player):
    adjStates = []
    for edge in edges:
        if edge not in state:
            newState = state.copy()
            newState[edge] = player
            adjStates.append((newState, edge))
    return adjStates

def minimax(state, depth, maxDepth, maxPlayer):
    if (depth == 0) or isTriangle(state):
        return heuristic(state, (maxDepth-depth)/(maxDepth+1))
    if maxPlayer:
        bestValue = -0xFFFF
        for child, edge in getAdjacentStates(state, 'C'):
            v = minimax(child, depth-1, maxDepth, False)
            bestValue = max(bestValue, v)
    else: # min
        bestValue = 0xFFFF
        for child, edge in getAdjacentStates(state, 'P'):
            v = minimax(child, depth-1, maxDepth, True)
            bestValue = min(bestValue, v)
    return bestValue

def calculateMove(state):
    moves = getAdjacentStates(state, 'C')
    scores = []
    searchDepth = 4
    for move, edge in moves:
        scores += [(minimax(move, searchDepth, searchDepth, False), (move, edge))]
    return max(scores, key=lambda item:item[0])[1]

def updateWindow(state):
    for edge, player in state.items():
        pt1 = points[ord(edge[0])-ord('A')]
        pt2 = points[ord(edge[1])-ord('A')]
        line = Line(pt1, pt2)
        line.setWidth(2)
        if (playerRed):
            if (player is 'P'):
                line.setFill('red')
            else:
                line.setFill('blue')
        else:
            if (player is 'P'):
                line.setFill('blue')
            else:
                line.setFill('red')
        line.draw(win)

def endGame(playerWin):
    if playerWin:
        print('You won!')
        text = Text(Point(128,16), 'You won!  Click anywhere to exit.')
        text.draw(win)
    else:
        print('You lost!')
        text = Text(Point(128,16), 'You lost!  Click anywhere to exit.')
        text.draw(win)
    win.getMouse()
    win.close()
    exit()

def compMove(state):
    state, compMove = calculateMove(state)
    print('Comp move:',compMove)
    updateWindow(state)
    if isTriangle(state):
        endGame(True)
    return state

def playerMove(state):
    playerMove = ''
    while playerMove not in edges or playerMove in state.keys():
        playerMove = input('Your move: ')
        if playerMove == 'exit':
            win.close()
            exit()
    state[playerMove] = 'P'
    updateWindow(state)
    if isTriangle(state):
        endGame(False)
    return state

state = {}
playerRed = ''
while playerRed != 'Y' and playerRed != 'N':
    playerRed = input('Are you playing Red? (Y/N): ')
playerRed = (playerRed == 'Y')

print('Type moves as \'AB\' in alphabetical order.\nType \'exit\' to close the game.')
while True:
    print()
    if playerRed:
        state = playerMove(state)
        state = compMove(state)
    else:
        state = compMove(state)
        state = playerMove(state)
