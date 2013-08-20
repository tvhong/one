import pygame
from pygame.locals import *

class BlockType:
    """
    An Enum for block types
    """
    L, J, I, O, T, S, Z = range(7)

class BlockRotation:
    """
    Block Direction.
    Hard coded.
        To rotate right, (direction+1)%4
        To rotate left, (direction-1)%4
    Careful when change
    """
    UP, RIGHT, DOWN, LEFT = range(4)

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

# blockShapes[7 kinds][4 rotations][REP_SIZE rows][REP_SIZE cols]
blockShapes = [[[[0 for h in range(4)] for k in range(4)] for j in range(4)] for i in range(7)]
blockShapes[BlockType.L][BlockRotation.UP] = [
                [1,0,0,0],
                [1,0,0,0],
                [1,1,0,0],
                [0,0,0,0]];
blockShapes[BlockType.L][BlockRotation.RIGHT] = [
                [0,0,0,0],
                [1,1,1,0],
                [1,0,0,0],
                [0,0,0,0]];
blockShapes[BlockType.L][BlockRotation.DOWN] = [
                [1,1,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,0,0,0]];
blockShapes[BlockType.L][BlockRotation.LEFT] = [
                [0,0,0,0],
                [0,0,1,0],
                [1,1,1,0],
                [0,0,0,0]];

blockShapes[BlockType.J][BlockRotation.UP] = [
                [0,1,0,0],
                [0,1,0,0],
                [1,1,0,0],
                [0,0,0,0]];
blockShapes[BlockType.J][BlockRotation.RIGHT] = [
                [0,0,0,0],
                [1,0,0,0],
                [1,1,1,0],
                [0,0,0,0]];
blockShapes[BlockType.J][BlockRotation.DOWN] = [
                [1,1,0,0],
                [1,0,0,0],
                [1,0,0,0],
                [0,0,0,0]];
blockShapes[BlockType.J][BlockRotation.LEFT] = [
                [0,0,0,0],
                [1,1,1,0],
                [0,0,1,0],
                [0,0,0,0]];
#TODO: insert more patterns

def _generateSquareList(blockType, blockX, blockY, blockRotation):
    squares = []
    for i in range(4):      #i-correspond_to-y
        for j in range(4):      #j-correspond_to-x
            #if blockShapes[blockType][BlockRotation.UP][i][j] != 0:
            if blockShapes[blockType][blockRotation][j][i] != 0:
                squares.append(Square(blockX+i, blockY+j))
    return squares

#TODO: build up the board

class Piece:
    """
    Piece(blockType, blockX, blockY, blockRotation=BlockRotation.UP, oneSquare=False): return Piece
    blockX, blockY: topleft square coordinate
    oneSquare is used for breaking up pieces only
    """
    def __init__(self, blockType, blockX, blockY, blockRotation=BlockRotation.UP, oneSquare=False):
        self.blockType = blockType
        self.blockX = blockX
        self.blockY = blockY
        self.blockRotation = blockRotation
        self.oneSquare = oneSquare
        if oneSquare:
            self.squares = [Square(blockX, blockY)]
        else:
            self.squares = _generateSquareList(blockType, blockX, blockY,
                                               blockRotation)

    def rotateRight(self):
        return Piece(self.blockType, self.blockX, self.blockY,
                     (self.blockRotation + 1) % 4, self.oneSquare)

    def rotateLeft(self):
        return Piece(self.blockType, self.blockX, self.blockY,
                     (self.blockRotation - 1) % 4, self.oneSquare)

    def moveRight(self):
        """
        Piece.moveRight(): return Piece
        create a new Piece that is to the right of self
        """
        return Piece(self.blockType, self.blockX + 1, self.blockY, self.blockRotation, self.oneSquare)

    def moveLeft(self):
        """
        Piece.moveLeft(): return Piece
        create a new Piece that is to the left of self
        """
        return Piece(self.blockType, self.blockX - 1, self.blockY, self.blockRotation, self.oneSquare)

    def moveDown(self, speed):
        """
        Piece.moveDown(): return Piece
        create a new Piece that down speed px
        """
        return Piece(self.blockType, self.blockX, self.blockY + 1, self.blockRotation, self.oneSquare)

    def fallApart(self):
        """
        Piece.fallApart() : return [oneSquare pieces]
        """
        return [Piece(self.blockType, sqr.squareX, sqr.squareY, oneSquare=True)
                for sqr in self.squares]

    def __str__(self):
        rep = ""
        for i in range(4):      # i-correspond_to-y
            for j in range(4):  # j-correspond_to-x
                if Square(self.blockX + j, self.blockY + i) in self.squares:
                    rep += "1 "
                else:
                    rep +="0 "
            rep += "\n"
        return rep
