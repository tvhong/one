from gameconstants import *

# blockShapes[7 TYPES][4 rotations][PATTERNSIZE rows][PATTERNSIZE cols]
#blockShapes = [[[[0]*PATTERNSIZE]*PATTERNSIZE]*4]*TYPES;
blockShapes = [[[[0 for h in range(PATTERNSIZE)] for k in range(PATTERNSIZE)] for j in range(4)] for i in range(TYPES)]

# TYPE_L
blockShapes[TYPE_L][DIR_UP] = [
                [0,0,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,1,0]];
blockShapes[TYPE_L][DIR_RIGHT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,1],
                [0,1,0,0]];
blockShapes[TYPE_L][DIR_DOWN] = [
                [0,0,0,0],
                [0,0,1,1],
                [0,0,0,1],
                [0,0,0,1]];
blockShapes[TYPE_L][DIR_LEFT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,1],
                [0,1,1,1]];

# TYPE_J
blockShapes[TYPE_J][DIR_UP] = [
                [0,0,0,0],
                [0,0,1,0],
                [0,0,1,0],
                [0,1,1,0]];
blockShapes[TYPE_J][DIR_RIGHT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,0,0],
                [0,1,1,1]];
blockShapes[TYPE_J][DIR_DOWN] = [
                [0,0,0,0],
                [0,1,1,0],
                [0,1,0,0],
                [0,1,0,0]];
blockShapes[TYPE_J][DIR_LEFT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,1],
                [0,0,0,1]];

# TYPE_O
blockShapes[TYPE_O][DIR_UP] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,0],
                [0,1,1,0]];
blockShapes[TYPE_O][DIR_RIGHT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,0],
                [0,1,1,0]];
blockShapes[TYPE_O][DIR_DOWN] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,0],
                [0,1,1,0]];
blockShapes[TYPE_O][DIR_LEFT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,0],
                [0,1,1,0]];

# TYPE_I
blockShapes[TYPE_I][DIR_UP] = [
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0]];
blockShapes[TYPE_I][DIR_DOWN] = [
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0]];
blockShapes[TYPE_I][DIR_RIGHT] = [
                [0,0,0,0],
                [1,1,1,1],
                [0,0,0,0],
                [0,0,0,0]];
blockShapes[TYPE_I][DIR_LEFT] = [
                [0,0,0,0],
                [1,1,1,1],
                [0,0,0,0],
                [0,0,0,0]];

# TYPE_T
blockShapes[TYPE_T][DIR_UP] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,0,1,0],
                [0,1,1,1]];
blockShapes[TYPE_T][DIR_DOWN] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,1],
                [0,0,1,0]];
blockShapes[TYPE_T][DIR_RIGHT] = [
                [0,0,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,1,0,0]];
blockShapes[TYPE_T][DIR_LEFT] = [
                [0,0,0,0],
                [0,0,0,1],
                [0,0,1,1],
                [0,0,0,1]];

# TYPE_S
blockShapes[TYPE_S][DIR_UP] = [
                [0,0,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0]];
blockShapes[TYPE_S][DIR_DOWN] = [
                [0,0,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0]];
blockShapes[TYPE_S][DIR_RIGHT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,0,1,1],
                [0,1,1,0]];
blockShapes[TYPE_S][DIR_LEFT] = [
                [0,0,0,0],
                [0,0,0,0],
                [0,0,1,1],
                [0,1,1,0]];

# TYPE_Z
blockShapes[TYPE_Z][DIR_UP] = [
                [0,0,0,0],
                [0,0,1,0],
                [0,1,1,0],
                [0,1,0,0]];
blockShapes[TYPE_Z][DIR_DOWN] = [
                [0,0,0,0],
                [0,0,1,0],
                [0,1,1,0],
                [0,1,0,0]];
blockShapes[TYPE_Z][DIR_RIGHT] = [
                [0,0,0,0],
                [0,0,0,0],
                [1,1,0,0],
                [0,1,1,0]];
blockShapes[TYPE_Z][DIR_LEFT] = [
                [0,0,0,0],
                [0,0,0,0],
                [1,1,0,0],
                [0,1,1,0]];

class Piece:
    """
    Piece(bType, x, y): return Piece
    invariant: boxes will be ordered by min y first
    """
    def __init__(self, bType, x, y, direction=DIR_UP, splitted=False, boxes=[]):
        self.bType = bType
        self.x = x
        self.y = y
        self.direction = direction
        self.splitted = splitted
        if not splitted:
            self.boxes = self._generateBoxes(bType, x, y, direction)
        else:
            self.boxes = boxes

    def _generateBoxes(self, bType, x, y, direction):
        boxes = []
        for i in range(PATTERNSIZE):      #i-correspond_to-y
            for j in range(PATTERNSIZE):      #j-correspond_to-x
                #if blockShapes[bType][DIR_UP][i][j] != 0:
                if blockShapes[bType][direction][i][j] != 0:
                    boxes.append((x+j, y+i))
        return boxes

    def rotateRight(self):
        if not self.splitted:
            self.direction = (self.direction + 1) % 4
            self.boxes = self._generateBoxes(self.bType, self.x, self.y, self.direction)

    def rotateLeft(self):
        if not self.splitted:
            self.direction = (self.direction - 1) % 4
            self.boxes = self._generateBoxes(self.bType, self.x, self.y, self.direction)

    def moveRight(self):
        """
        Piece.moveRight(): return Piece
        create a new Piece that is to the right of self
        """
        if not self.splitted:
            self.x += 1
            newBoxes = [(b[0]+1, b[1]) for b in self.boxes]
            self.boxes = newBoxes

    def moveLeft(self):
        """
        Piece.moveLeft(): return Piece
        create a new Piece that is to the left of self
        """
        if not self.splitted:
            self.x -= 1
            newBoxes = [(b[0]-1, b[1]) for b in self.boxes]
            self.boxes = newBoxes

    def moveDown(self):
        """
        Piece.moveDown(): return Piece
        """
        self.y += 1
        newBoxes = [(b[0], b[1]+1) for b in self.boxes]
        self.boxes = newBoxes

    def moveUp(self):
        """
        Piece.moveDown(): return Piece
        """
        self.y -= 1
        newBoxes = [(b[0], b[1]-1) for b in self.boxes]
        self.boxes = newBoxes

    def split(self, y):
        """
        Piece.split() : return highPiece, lowPiece or None, None
        """
        # don't create new Pieces if not have to
        lowestBox = self.boxes[len(self.boxes)-1]  # thanks to the invariant
        if lowestBox[1] < y:
            return self, None
        highestBox = self.boxes[0]  # same, tks to the invariant
        if highestBox[1] > y:
            return None, self

        highPiece = None
        lowPiece = None
        highBoxes = [b for b in self.boxes if b[1] < y]
        lowBoxes = [b for b in self.boxes if b[1] > y]
        if len(highBoxes) > 0:
            # x, y & direction doesn't matter for splitted pieces
            highPiece = Piece(self.bType, self.x, self.y, self.direction, True, highBoxes)
        if len(lowBoxes) > 0:
            lowPiece = Piece(self.bType, self.x, y+1, self.direction, True, lowBoxes)

        return highPiece, lowPiece

    def getBoxes(self):
        return self.boxes

    def __str__(self):
        rep = "x = "+ str(self.x)+ ", y = "+str(self.y)+', type = '+str(self.bType)+'\n'
        for i in range(PATTERNSIZE):      # i-correspond_to-y
            for j in range(PATTERNSIZE):  # j-correspond_to-x
                if (self.x + j, self.y + i) in self.boxes:
                    rep += "1 "
                else:
                    rep += "0 "
            rep += "\n"
        return rep
