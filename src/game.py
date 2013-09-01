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

f = open('output.txt','w')

def start():
    global board, pendings, fallingPieces, staticPieces, softDroping
    global currentPiece,nextPiece
    global level, fallingTime, nextLevelScore, score
    board = [[BLANK]*BOARDCOLS for i in range(BOARDROWS)]
    pendings = [(random.randrange(TYPES), random.randrange(4)) \
            for i in range(PENDING_MAX)]
    fallingPieces = []
    staticPieces = []

    nextPiece = None
    currentPiece = None

    
    level = 1
    fallingTime = _getFallingTime(level)
    nextLevelScore = _getNextLvlScore(level)
    score = 0

    softDroping = False
    update.oldTime = int(time.time() * 1000)

    #DEBUGGING:
    for x in range(BOARDCOLS):
        board[15][x] = OCCUPIED_S

def update():
    global fallingTime, score, nextLevelScore, fallingPieces
    global currentPiece

    newTime = int(time.time() * 1000)
    # time to move down
    if (newTime - update.oldTime) > fallingTime:
        #print 'updating !!!!'
        update.oldTime = newTime

        if currentPiece != None:
            moveDown(currentPiece)

        # check if any line is eaten
        while True:
            lines = _removeEatenLines()
            # print lines;
            if len(lines) == 0: break;
            # Call main.lineEaten() here
            score += _calculateScore(lines)
            if score >= nextLevelScore:
                levelUp()
            hardDrop();

        # make sure we have new pieces
        if currentPiece == None:
            #print 'making a new piece !!!! so fun!!!'
            currentPiece = _getNextPiece()
            addToBoard(currentPiece)
            fallingPieces.append(currentPiece)
        f.write(printBoard())

def printBoard ():
    s = '\n---+---+---\n'
    for y in range(BOARDROWS):
        for x in range(BOARDCOLS):
            s += str(board[y][x])
        s += '\n'
    return s

def addToBoard (piece, status=OCCUPIED_F):
    for x,y in piece.boxes:
        board[y][x] = status

def removeFromBoard (piece):
    for x,y in piece.boxes:
        board[y][x] = BLANK

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
    global fallingTime, softDroping     #TODO: do I need this?
    if not softDroping:
        softDroping = True
        fallingTime /= 2

def stopSoftDrop():
    global fallingTime, softDroping     #TODO: again, do I need this?
    if softDroping:
        softDroping = False
        fallingTime *= 2

def hardDrop():
    global fallingPieces
    while (len(fallingPieces) > 0):
        for piece in fallingPieces:
            moveDown(piece)

def moveDown (piece):
    global board, fallingPieces, staticPieces, currentPiece
    assert piece != None
    removeFromBoard(piece)
    piece.moveDown()
    col = _checkCollision(piece)
    if col==COL_STATIC:
        piece.moveUp()
        fallingPieces.remove(piece)
        staticPieces.append(piece)
        addToBoard(piece,OCCUPIED_S)
        
        if piece == currentPiece:
            currentPiece = None

    else:
        if col==COL_FALLING:
            piece.moveUp()
        addToBoard(piece,OCCUPIED_F)

def checkGameEnd():
    for x in range(BOARDCOLS):
        if board[PATTERNSIZE-1][x] == OCCUPIED_S:
            return True
    return False

########################################################################
### Helper functions
########################################################################

def _getFallingTime(level):
    return 500 - level * 50; # TODO: need a better function
    # 1st level: 950

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
                # DEBUGGING 
                print ptop
                print pbot
                if pbot != p:
                    staticPieces.remove(p)
                    if ptop != None:
                        assert len(ptop.boxes)>0
                        fallingPieces.append(ptop)
                        addToBoard(ptop,OCCUPIED_F)
                    if pbot != None:
                        assert len(pbot.boxes)>0
                        staticPieces.append(pbot)
                        addToBoard(pbot,OCCUPIED_S)
    return eatenLines

def _calculateScore(eatenLines):
    return len(eatenLines) * 100


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
    removeFromBoard(p)
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
            
    addToBoard(p)

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
    

def _cmp(piece1, piece2):
    # TODO: error here
    y1 = piece1.boxes[len(piece1.boxes)-1][1]    # get the lowest y
    y2 = piece2.boxes[len(piece2.boxes)-1][1]
    if (y1 > y2):
        return 1
    if (y1 < y2):
        return -1
    return 0
