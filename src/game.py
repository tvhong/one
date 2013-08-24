import pygame, random, time
import Piece
from pygame.locals import *
from gameconstants import *

# block direction constants
CMD_ROTATE_R, CMD_ROTATE_L, CMD_MOVE_R, CMD_MOVE_L = range(4)
OCCUPIED = 1
PENDING_MAX = 50  # max number of elements in pendingPieces
PENDING_MIN = 4   # min number of elements in pendingPieces before renewing
SOFT_DROP_INC = 10  # fallingTime offset when softdrop

def start():
    global board, pendingPieces, fallingPieces, staticPieces
    global level, fallingTime, nextLevelScore, score
    board = [[BLANK]*BOARDROWS for i in range(BOARDCOLS)]
    pendingPieces = [random.randrange(TYPES) for i in range(PENDING_MAX)]
    fallingPieces = []
    staticPieces = []
    level = 1
    fallingTime = _getFallingTime(level)
    nextLevelScore = _getNextLvlScore(level)
    score = 0

def update():
    global board, pendingPieces, fallingPieces, staticPieces
    global level, fallingTime, nextLevelScore, score
    # init static variable
    if oldTime not in update.__dict__: update.oldTime = int(time.time() * 1000)

    newtime = int(time.time() * 1000)
    # time to move down
    if (update.oldtime - newTime) > fallingTime:
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
    global softDrop     #TODO: do I need this?
    if not softDrop:
        softDrop = True
        fallingTime -= SOFT_DROP_INC

def stopSoftDrop():
    global softDrop     #TODO: again, do I need this?
    if softDrop:
        softDrop = False
        fallingTime += SOFT_DROP_INC

def hardDrop():
    global fallingPieces
    while (len(fallingPieces) > 0):
        moveDown()

def moveDown():
    global board, pendingPieces, fallingPieces, staticPieces
    fallingPieces.sort(cmp=_cmp, reverse=True)  # order of decending y
    tmpList = []
    for p in fallingPieces:
        pDown = p.moveDown()
        if (_checkCollision(pDown)):
            staticPieces.append(p)
            for x,y in p.boxes:
                board[x][y] = OCCUPIED
        else:
            tmpList.append(pDown)
    fallingPieces = tmpList

def checkGameEnd():
    for x in range(BOARDCOLS):
        if board[x][0] != BLANK:
            return True
    return False

########################################################################
### Helper functions
########################################################################

def _getFallingTime(level):
    return 100 - level * 5; # TODO: need a better function

def _getNextLvlScore(level):
    return level*1000;  # TODO: need a better function

def _removeEatenLines():
    '''only check the static pieces'''
    eateinLines = []
    for y in range(BOARDROWS):
        eaten = True
        for x in range(BOARDCOLS):
            if board[x][y] == BLANK: eaten = False
        if eaten:
            eatenLines.append(y)
            # clear the row in board
            for x in range(BOARDCOLS): board[x][y] = BLANK
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
    global board
    if piece == None:
        return True
    for x, y in piece.boxes:
        if board[x][y] != 0:
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
    if (len(pendingPieces) < PENDING_MIN):
        pendingPieces = pendingPieces + [random.randrange(TYPES) \
                        for i in range(PENDING_MAX - PENDING_MIN)]
    return Piece(pendingPieces.pop(0), (BOARDCOLS - PATTERNSIZE)/2, -3)
    # bad bad bad, -3 is bad

def _cmp(piece1, piece2):
    y1 = piece1.boxes[len(piece1.boxes)]    # get the lowest y
    y2 = piece2.boxes[len(piece2.boxes)]
    if (y1 > y2):
        return 1
    if (y1 < y2):
        return -1
    return 0
