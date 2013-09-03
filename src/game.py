import pygame, random, time
from Piece import Piece
from pygame.locals import *
from gameconstants import *

# block direction constants
CMD_ROTATE_R, CMD_ROTATE_L, CMD_MOVE_R, CMD_MOVE_L = range(4)
OCCUPIED_S = '1'
OCCUPIED_F = '0'
BLANK = ' '
PENDING_MAX = 50  # max number of elements in pendings
PENDING_MIN = 4   # min number of elements in pendings before renewing

COL_STATIC  = 1
COL_FALLING = 2
COL_NONE    = 0

REVERSE_CMD = {CMD_ROTATE_R:CMD_ROTATE_L,
               CMD_ROTATE_L:CMD_ROTATE_R,
               CMD_MOVE_R  :CMD_MOVE_L,
               CMD_MOVE_L  :CMD_MOVE_R}

logF = open('gamelog.txt','w')

def init():
    global board, pendings, fallingPieces, staticPieces, softDroping
    global currentPiece,nextPiece
    global level, fallingTime, nextLevelScore, score
    global delaying, lastDrop
    board = [[BLANK]*BOARDCOLS for i in range(BOARDROWS)]
    pendings = [(random.randrange(TYPES), random.randrange(4)) \
            for i in range(PENDING_MAX)]
    fallingPieces = []
    staticPieces = []

    nextPiece = None
    currentPiece = None

    delaying = False
    lastDrop = 0
    
    level = 1
    fallingTime = _getFallingTime(level)
    nextLevelScore = _getNextLvlScore(level)
    score = 0

    softDroping = False
    update.oldTime = int(time.time() * 1000)

def update():
    global fallingTime, score, nextLevelScore, fallingPieces
    global currentPiece
    global delaying,lastDrop
    
    newTime = time.time()
    # time to move down
    if (newTime - lastDrop)*1000 > fallingTime:
        #print 'updating !!!!'
        lastDrop = newTime

        if currentPiece != None:
            _moveDown(currentPiece)

        # check if any line is eaten
        
        lines = _removeEatenLines()
        # print lines;
        if len(lines) != 0:
            delaying = True;
            score += _calculateScore(lines)
            if score >= nextLevelScore:
                levelUp()
        elif delaying:
            hardDrop();
            delaying = False
        elif currentPiece == None:
            #print 'making a new piece !!!! so fun!!!'
            currentPiece = _getNextPiece()
            _addToBoard(currentPiece)
            fallingPieces.append(currentPiece)
        logF.write(_getStrBoard())

def levelUp():
    global level, fallingTime, nextLevelScore
    level += 1
    fallingTime = _getFallingTime(level)
    nextLevelScore = _getNextLvlScore(level)

def getPieces():
    return fallingPieces + staticPieces

def getNextPiece ():
    global nextPiece
    return nextPiece

def rotateRight():
    _movePiece(CMD_ROTATE_R)

def rotateLeft():
    _movePiece(CMD_ROTATE_L)

def moveRight():
    _movePiece(CMD_MOVE_R)

def moveLeft():
    _movePiece(CMD_MOVE_L)

def softDrop():
    global fallingTime, softDroping
    if not softDroping:
        softDroping = True
        fallingTime /= 3

def stopSoftDrop():
    global fallingTime, softDroping
    if softDroping:
        softDroping = False
        fallingTime = _getFallingTime(level)

def hardDrop():
    global fallingPieces,lastDrop
    while (len(fallingPieces) > 0):
        for piece in fallingPieces:
            _moveDown(piece)
    lastDrop = time.time()

def checkGameEnd():
    for x in range(BOARDCOLS):
        if board[PATTERNSIZE-1][x] == OCCUPIED_S:
            return True
    return False

def close():
    logF.close()

########################################################################
### Game helper functions
########################################################################

def _getFallingTime(level):
    return 540 - level * 40; # TODO: need a better function
    # 500, 460, 420, 380, 340 ...

def _getNextLvlScore(level):
    return level*1000;  # TODO: need a better function

def _removeEatenLines():
    '''only check the static pieces'''
    global board, staticPieces
    eatenLines = []
    for y in range(BOARDROWS):
        eaten = True
        for x in range(BOARDCOLS):
            if board[y][x] != OCCUPIED_S: eaten = False
        if eaten:
            eatenLines.append(y)
            
            # clear the row in board
            for x in range(BOARDCOLS): board[y][x] = BLANK
            # clear the row in staticPieces
            for p in staticPieces[:]:
                ptop, pbot = p.split(y)
                if pbot != p:
                    staticPieces.remove(p)
                    if ptop != None:
                        assert len(ptop.boxes)>0
                        fallingPieces.append(ptop)
                        _addToBoard(ptop,OCCUPIED_F)
                    if pbot != None:
                        assert len(pbot.boxes)>0
                        staticPieces.append(pbot)
                        _addToBoard(pbot,OCCUPIED_S)
    return eatenLines

def _calculateScore(eatenLines):
    global level
    n = len(eatenLines);
    baseScore = 100
    if n == 2: baseScore = 300
    elif n == 3: baseScore = 500
    elif n == 4: baseScore = 800
    #TODO: consider combo?
    return n * baseScore * level

def _checkCollision(piece):
    '''return true if collide'''
    #print 'checking collision!!!'
    global board
    assert piece != None
    for x, y in piece.boxes:
        if x>=BOARDCOLS or x<0 or y>=BOARDROWS or board[y][x] == OCCUPIED_S:
            return COL_STATIC
        
    for x, y in piece.boxes:
        if board[y][x] == OCCUPIED_F:
            return COL_FALLING
        
    return COL_NONE

def _movePiece(command):
    '''not for moveDown'''
    global fallingPieces,currentPiece
    if currentPiece == None: return  # try to prune line eating case
    p = currentPiece
    _removeFromBoard(p)
    if command == CMD_ROTATE_R:
        p.rotateRight()
    elif command == CMD_ROTATE_L:
        p.rotateLeft()
    elif command == CMD_MOVE_R:
        p.moveRight()
    elif command == CMD_MOVE_L:
        p.moveLeft()

    # reverse if the command is not possible
    if _checkCollision(p) == True:
        if command == CMD_ROTATE_L:
            p.rotateRight()
        elif command == CMD_ROTATE_R:
            p.rotateLeft()
        elif command == CMD_MOVE_L:
            p.moveRight()
        elif command == CMD_MOVE_R:
            p.moveLeft()
            
    _addToBoard(p)

def _getNextPiece ():
    global nextPiece
    if nextPiece == None:
        nextPiece = _generateNewPiece()

    newPiece = nextPiece
    nextPiece = _generateNewPiece()
    return newPiece
        
def _generateNewPiece():
    global pendings

    # refill if needed
    if (len(pendings) < PENDING_MIN):
        pendings = pendings + [(random.randrange(TYPES),random.randrange(4)) \
                for i in range(PENDING_MAX - PENDING_MIN)]

    pending = pendings.pop(0);
    #print 'im the real new piece here! u imposters!'
    return Piece(pending[0], (BOARDCOLS - PATTERNSIZE)/2, 0, pending[1])
    
'''
def _cmp(piece1, piece2):
    # TODO: error here
    y1 = piece1.boxes[len(piece1.boxes)-1][1]    # get the lowest y
    y2 = piece2.boxes[len(piece2.boxes)-1][1]
    if (y1 > y2):
        return 1
    if (y1 < y2):
        return -1
    return 0
'''

def _moveDown (piece):
    global board, fallingPieces, staticPieces, currentPiece
    assert piece != None
    _removeFromBoard(piece)
    piece.moveDown()
    col = _checkCollision(piece)
    if col==COL_STATIC:
        piece.moveUp()
        fallingPieces.remove(piece)
        staticPieces.append(piece)
        _addToBoard(piece,OCCUPIED_S)
        
        if piece == currentPiece:
            currentPiece = None

    else:
        if col==COL_FALLING:
            piece.moveUp()
        _addToBoard(piece,OCCUPIED_F)

def _getStrBoard():
    s = '\n---+---+---\n'
    for y in range(BOARDROWS):
        for x in range(BOARDCOLS):
            s += str(board[y][x])
        s += '\n'
    return s

def _addToBoard(piece, status=OCCUPIED_F):
    for x,y in piece.boxes:
        board[y][x] = status

def _removeFromBoard(piece):
    for x,y in piece.boxes:
        board[y][x] = BLANK
