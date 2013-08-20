import pygame
from pygame.locals import *

class BlockType:
    """
    An Enum for block types
    """
    I, J, L, O, S, T, Z = range(7)

class BlockDir:
    """
    Block Direction.
    Hard coded.
        To rotate right, (direction+1)%4
        To rotate left, (direction-1)%4
    Careful when change
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Square:
    def __init__(self, squareX, squareY):
        self.squareX = squareX
        self.squareY = squareY

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.squareX == other.squareX and 
                    self.squareY == other.squareY)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

REP_SIZE = 4
#TODO: fix, structure for the hardcoded patterns
'''
#string representation of piece's shapes
#TODO: need a lot more
rep = list(list(list(list())))
rep[BlockType.L][BlockDir.UP] = [
        "1000",
        "1000",
        "1100",
        "0000"];
rep[BlockType.J][BlockDir.UP] = [
        "0100",
        "0100",
        "1100",
        "0000"];
'''
L1 = [
    "1000",
    "1000",
    "1100",
    "0000"
    ]


def _generateSquareList(blockType, blockX, blockY, blockDir):
    #TODO: fix, don't use Rect anymore
    # but wtf is a square exactly?
    squares = []
    for i in range(REP_SIZE):       # i-corresponds_to-y
        for j in range(REP_SIZE):   # j-corresponds_to-x
            #if rep[blockType][BlockDir.UP][i][j] != 0:
            if L1[i][j] != 0:
                dx = j*squareSize
                dy = i*squareSize
                square = pygame.Rect(x+dx, y+dy, squareSize, squareSize)
                squares.append(square)
    return squares

#TODO: build up the board

class Piece:
    """
    Piece(blockType, blockX, blockY, blockDir=BlockDir.UP): return Piece
    blockX, blockY: topleft square coordinate
    """
    def __init__(self, blockType, blockX, blockY, blockDir=BlockDir.UP):
        self.blockType = blockType
        self.blockX = blockX
        self.blockY = blockY
        self.squares = _generateSquareList(blockType, blockX, blockY, blockDir)

    def rotateRight(self):
        return Piece(self.blockType, self.blockX, self.blockY,
                     (self.blockDir + 1) % 4)

    def rotateLeft(self):
        return Piece(self.blockType, self.blockX, self.blockY,
                     (self.blockDir - 1) % 4)

    def moveRight(self):
        """
        Piece.moveRight(): return Piece
        create a new Piece that is to the right of self
        """
        return Piece(self.blockType, self.blockX + 1, self.blockY)

    def moveLeft(self):
        """
        Piece.moveLeft(): return Piece
        create a new Piece that is to the left of self
        """
        return Piece(self.blockType, self.blockX - 1, self.blockY)

    def moveDown(self, speed):
        """
        Piece.moveDown(): return Piece
        create a new Piece that down speed px
        """
        return Piece(self.blockType, self.blockX, self.blockY + 1)

    def remove(self, square):
        """
        Piece.remove(square): return bool
        return True if successfully delete a square; False otherwise
        """
        for sqr in squares[:]:
            if (sqr == square):
                #TODO: need to divide the piece as well
                squares.remove(sqr)
                return True
        return False
