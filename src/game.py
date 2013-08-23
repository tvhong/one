import pygame, random, Piece
from pygame.locals import *
from gameconstants import *

# block direction constants
DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT = range(4)
CMD_ROTATE_R, CMD_ROTATE_L, CMD_MOVE_R, CMD_MOVE_L = range(4)

# blockShapes[7 TYPES][4 rotations][PATTERNSIZE rows][PATTERNSIZE cols]
blockShapes = [[[[0]*PATTERNSIZE]*PATTERNSIZE]*4]*TYPES;
blockShapes[TYPE_L][DIR_UP] = [
                [1,0,0,0],
                [1,0,0,0],
                [1,1,0,0],
                [0,0,0,0]];
blockShapes[TYPE_L][DIR_RIGHT] = [
                [0,0,0,0],
                [1,1,1,0],
                [1,0,0,0],
                [0,0,0,0]];
blockShapes[TYPE_L][DIR_DOWN] = [
                [1,1,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,0,0,0]];
blockShapes[TYPE_L][DIR_LEFT] = [
                [0,0,0,0],
                [0,0,1,0],
                [1,1,1,0],
                [0,0,0,0]];

blockShapes[TYPE_J][DIR_UP] = [
                [0,1,0,0],
                [0,1,0,0],
                [1,1,0,0],
                [0,0,0,0]];
blockShapes[TYPE_J][DIR_RIGHT] = [
                [0,0,0,0],
                [1,0,0,0],
                [1,1,1,0],
                [0,0,0,0]];
blockShapes[TYPE_J][DIR_DOWN] = [
                [1,1,0,0],
                [1,0,0,0],
                [1,0,0,0],
                [0,0,0,0]];
blockShapes[TYPE_J][DIR_LEFT] = [
                [0,0,0,0],
                [1,1,1,0],
                [0,0,1,0],
                [0,0,0,0]];
# TODO: insert more patterns

level = 1
interval = 90   # should make a function to change
PENDING_MAX = 50  # max number of elements in pendingPieces
PENDING_MIN = 4   # min number of elements in pendingPieces before renewing

# TODO: need to check line eaten 
'''
TODO: bring this somewhere else
if len(fallingPieces) == 0:
    fallingPieces.append(_generateNewPiece())
    return
'''
def init():
    global board, pendingPieces, fallingPieces, staticPieces
    board = [[BLANK]*BOARDROWS for i in range(BOARDCOLS)]
    pendingPieces = [random.randrange(TYPES) for i in range(PENDING_MAX)]
    fallingPieces = []
    staticPieces = []

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

def hardDrop():
    '''Handle a hard drop (spacebar)'''
    global fallingPieces
    while (len(fallingPieces) > 0):
        moveDown()

def moveDown():
    '''
    Move the falling pieces down by distance
    If a line is eaten, then this will inform main.lineEaten([eaten lines])
    If a new Piece is generated after this
    '''
    global board, pendingPieces, fallingPieces, staticPieces
    fallingPieces.sort(cmp=_cmp, reverse=True)  # order of decending y
    tmpList = []
    for p in fallingPieces:
        p1 = p.moveDown()
        if (_checkCollision(p1)):
            staticPieces.append(p)
            for x,y in p.boxes:
                board[x][y] = 1
        else:
            tmpList.append(p1)
    fallingPieces = tmpList

########################################################################
### Helper functions
########################################################################

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
