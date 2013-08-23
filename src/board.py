import pygame, random
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

def init():
    global board, pendingPieces, fallingPieces, stationaryPieces
    board = [[BLANK]*BOARDROWS for i in range(BOARDCOLS)]
    pendingPieces = [random.randrange(TYPES) for i in range(PENDING_MAX)]
    fallingPieces = []
    stationaryPieces = []

def getPieces():
    return fallingPieces + stationaryPieces

def rotateRight():
    _movePiece(CMD_ROTATE_R)

def rotateLeft():
    _movePiece(CMD_ROTATE_L)

def moveRight():
    _movePiece(CMD_MOVE_R)

def moveLeft():
    _movePiece(CMD_MOVE_L)

def drop():
    '''Handle a drop (spacebar)'''
    global fallingPieces
    while (len(fallingPieces) > 0):
        moveDown()

def moveDown():
    '''
    Move the falling pieces down by distance
    If a line is eaten, then this will inform main.lineEaten([eaten lines])
    If a new Piece is generated after this
    '''
    # TODO: not finished yet
    global board, pendingPieces, fallingPieces, stationaryPieces
    if len(fallingPieces) == 0:
        fallingPieces.append(_generateNewPiece())
        return


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

########################################################################
### Piece
########################################################################

class Piece:
    """
    Piece(bType, x, y): return Piece
    self.splitted is used for breaking up pieces only
    invariant: boxes will be ordered by min y first
    """
    def __init__(self, bType, x, y, direction=DIR_UP, splitted=False):
        self.bType = bType
        self.x = x
        self.y = y
        self.direction = direction
        self.splitted = splitted
        if not splitted:
            self.boxes = self._generateBoxes(bType, x, y, direction)
        else:
            self.boxes = []

    def _generateBoxes(self, bType, x, y, direction):
        boxes = []
        for i in range(4):      #i-correspond_to-y
            for j in range(4):      #j-correspond_to-x
                #if blockShapes[bType][DIR_UP][i][j] != 0:
                if blockShapes[bType][direction][j][i] != 0:
                    boxes.append((x+i, y+j))
        return boxes

    def rotateRight(self):
        if not self.splitted:
            newDir = (self.direction + 1) % 4
            return Piece(self.bType, self.x, self.y, newDir)

    def rotateLeft(self):
        if not self.splitted:
            newDir = (self.direction - 1) % 4
            return Piece(self.bType, self.x, self.y, newDir)

    def moveRight(self):
        """
        Piece.moveRight(): return Piece
        create a new Piece that is to the right of self
        """
        if not self.splitted:
            return Piece(self.bType, self.x + 1, self.y, self.direction)

    def moveLeft(self):
        """
        Piece.moveLeft(): return Piece
        create a new Piece that is to the left of self
        """
        if not self.splitted:
            return Piece(self.bType, self.x - 1, self.y, self.direction)

    def moveDown(self, speed):
        """
        Piece.moveDown(): return Piece
        """
        return Piece(self.bType, self.x, self.y + 1, self.direction, self.splitted)

    def split(self, x, y):
        """
        Piece.split() : return highPiece, lowPiece or None
        """
        if (x, y) in self.boxes:
            highPiece = Piece(self.bType, self.x, self.y, splitted=True)    # x & y aren't important here
            lowPiece = Piece(self.bType, self.x, y+1, splitted=True)
            highPiece.boxes = [b for b in self.boxes if b[1] < y]
            lowPiece.boxes = [b for b in self.boxes if b[1] > y]
            return highPiece, lowPiece

    def getBoxes(self):
        return self.boxes

    def __str__(self):
        rep = ""
        for i in range(4):      # i-correspond_to-y
            for j in range(4):  # j-correspond_to-x
                if (self.x + j, self.y + i) in self.boxes:
                    rep += "1 "
                else:
                    rep +="0 "
            rep += "\n"
        return rep
