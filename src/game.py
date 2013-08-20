import pygame
from pygame.locals import *
from gameconstants import *

# block direction constants
DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT = range(4)

# blockShapes[7 kinds][4 rotations][REP_SIZE rows][REP_SIZE cols]
blockShapes = [[[[0 for h in range(4)] for k in range(4)] for j in range(4)] for i in range(7)]
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
#TODO: insert more patterns

fallingPieces = []
stationaryPieces = []
board = [[BLANK]*BOARDROWS for i in range(BOARDCOLS)]

def update(timePassed):
    pass

def getPieces():
    return fallingPieces + stationaryPieces

class Piece:
    """
    Piece(bType, x, y): return Piece
    self.splitted is used for breaking up pieces only
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
