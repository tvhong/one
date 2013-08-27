import pygame, random, time
from Piece import Piece
from pygame.locals import *
from gameconstants import *

# block direction constants
CMD_ROTATE_R, CMD_ROTATE_L, CMD_MOVE_R, CMD_MOVE_L = range(4)
OCCUPIED = 1
PENDING_MAX = 50  # max number of elements in pendings
PENDING_MIN = 4   # min number of elements in pendings before renewing
SOFT_DROP_INC = 100  # fallingTime offset when softdrop

def start():
    global board, pendings, fallingPieces, staticPieces, softDroping
    global level, fallingTime, nextLevelScore, score
    board = [[BLANK]*BOARDCOLS for i in range(BOARDROWS)]
    pendings = [(random.randrange(TYPES), random.randrange(4)) \
            for i in range(PENDING_MAX)]
    fallingPieces = []
    staticPieces = []

    level = 1
    fallingTime = _getFallingTime(level)
    nextLevelScore = _getNextLvlScore(level)
    score = 0

    softDroping = False
    update.oldTime = int(time.time() * 1000)

def update():
    newTime = int(time.time() * 1000)
    # time to move down
    if (newTime - update.oldTime) > fallingTime:
        update.oldTime = newTime
        #print 'updating !!!!'
        moveDown()
        # check if any line is eaten
        while True:
            lines = _removeEatenLines()
            if len(lines) == 0: break;
            # Call main.lineEaten() here
            score += _calculateScore(lines)
            if score >= nextLevelScore:
                levelUp()
            drop();
        # make sure we have new pieces
        if len(fallingPieces) == 0:
            #print 'making a new piece !!!! so fun!!!'
            fallingPieces.append(_generateNewPiece())

def levelUp():
    global level, fallingTime, nextLevelScore
    level += 1
    fallingTime = _getFallingTime(level)
    nextLevelScore = _getNextLvlScore(level)

def getPieces():
    return fallingPieces + staticPieces

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
        fallingTime -= SOFT_DROP_INC

def stopSoftDrop():
    global fallingTime, softDroping     #TODO: again, do I need this?
    if softDroping:
        softDroping = False
        fallingTime += SOFT_DROP_INC

def hardDrop():
    global fallingPieces
    while (len(fallingPieces) > 0):
        moveDown()

def moveDown():
    global board, fallingPieces, staticPieces
    fallingPieces.sort(cmp=_cmp, reverse=True)  # order of decending y
    tmpList = []
    for p in fallingPieces:
        pDown = p.moveDown()
        if (_checkCollision(pDown)):
            staticPieces.append(p)
            for x,y in p.boxes:
                board[y][x] = OCCUPIED
        else:
            tmpList.append(pDown)
            #print 'dropping one piece down!!!'
    fallingPieces = tmpList

def checkGameEnd():
    for x in range(BOARDCOLS):
        if board[PATTERNSIZE-1][x] != BLANK:
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
    eatenLines = []
    for y in range(BOARDROWS):
        eaten = True
        for x in range(BOARDCOLS):
            if board[y][x] == BLANK: eaten = False
        if eaten:
            eatenLines.append(y)
            # clear the row in board
            for x in range(BOARDCOLS): board[y][x] = BLANK
            # clear the row in staticPieces
            for p in staticPieces[:]:
                ptop, pbot = p.split()
                if (ptop,pbot) == (None,None):
                    continue
                staticPieces.remove(p)
                if ptop != None: fallingPieces.append(ptop)
                if pbot != None: staticPieces.append(pbot)
    return eatenLines

def _calculateScore(eatenLines):
    return len(eatenLines) * 100


def _checkCollision(piece):
    '''return true if collide'''
    #print 'checking collision!!!'
    global board
    if piece == None:
        return True
    for x, y in piece.boxes:
        if x>=BOARDCOLS or x<0 or y>=BOARDROWS:
            return True
        if board[y][x] != BLANK:
            return True        
    return False

def _movePiece(command):
    '''not for moveDown'''
    global fallingPieces
    if len(fallingPieces) > 1: return  # try to prune line eating case
    if command == CMD_ROTATE_R:
        newPiece = fallingPieces[0].rotateRight()
    elif command == CMD_ROTATE_L:
        newPiece = fallingPieces[0].rotateLeft()
    elif command == CMD_MOVE_R:
        newPiece = fallingPieces[0].moveRight()
    elif command == CMD_MOVE_L:
        newPiece = fallingPieces[0].moveLeft()

    if _checkCollision(newPiece) == False:
        fallingPieces = [newPiece]

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
    y1 = piece1.boxes[len(piece1.boxes)]    # get the lowest y
    y2 = piece2.boxes[len(piece2.boxes)]
    if (y1 > y2):
        return 1
    if (y1 < y2):
        return -1
    return 0
