import sys,pygame
from pygame.locals import *
from gameconstants import *

# COLORS
COLORDELTA = 20

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)

RED         = (155,   0,   0)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)
YELLOW      = (155, 155,   0)
CYAN        = (  0, 155, 155)
ORANGE      = (155,  77,   0)
PURPLE      = ( 77,   0,  77)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = {TYPE_I: CYAN,
               TYPE_J: BLUE,
               TYPE_L: ORANGE,
               TYPE_O: YELLOW,
               TYPE_S: GREEN,
               TYPE_T: PURPLE,
               TYPE_Z: RED}

GBOARDROWS = 20
# POSITIONS & DIMENSIONS IN PIXEL
BOXSIZE = 30
BOXMG = 3

MARGIN = 20
BORDERWIDTH = 3

BOARDX = MARGIN
BOARDY = MARGIN
BOARDWIDTH = BOARDCOLS*BOXSIZE
BOARDHEIGHT = GBOARDROWS*BOXSIZE

SCOREX = BOARDX+BOARDWIDTH+MARGIN
SCOREY = MARGIN

LEVELX = SCOREX
LEVELY = SCOREY + 50 + MARGIN

NEXTPIECEX = SCOREX
NEXTPIECEY = LEVELY + 50 + MARGIN
# FONTS


def init (surface):
    global SURFACE,BASICFONT,BIGFONT
    SURFACE = surface
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)

def reset ():
    SURFACE.fill(BGCOLOR)

def lighter (color, times=1):
    assert times>=1
    newcolor = list(color)
    for time in range(0,times):
        for i in [0,1,2]:
            newcolor[i] = min(newcolor[i]+COLORDELTA,255)
    return tuple(newcolor)

def darker (color, times=1):
    newcolor = list(color)
    for time in range(0,times):
        for i in [0,1,2]:
            newcolor[i] = max(newcolor[i]-COLORDELTA,0)
    return tuple(newcolor)

def drawBox ((x, y), color):
    if x<=BOARDX-BOXSIZE or y<=BOARDY-BOXSIZE:
        return
    x  = x+1
    y  = y+1
    x2 = x+BOXSIZE-2
    y2 = y+BOXSIZE-2
    x3 = x+BOXMG
    y3 = y+BOXMG
    x4 = x2-BOXMG
    y4 = y2-BOXMG
    pygame.draw.polygon(SURFACE,darker(COLORS[color]),[(x,y),(x2,y),(x2,y2),(x,y2)])
    pygame.draw.polygon(SURFACE,lighter(COLORS[color],3),[(x,y),(x2,y),(x4,y3),(x3,y3)])
    pygame.draw.polygon(SURFACE,darker(COLORS[color],3),[(x3,y4),(x4,y4),(x2,y2),(x,y2)])
    pygame.draw.polygon(SURFACE,lighter(COLORS[color]),[(x3,y3),(x4,y3),(x4,y4),(x3,y4)])

def toPixel ((col, row)):
    return (BOARDX+col*BOXSIZE,BOARDY+row*BOXSIZE)
    
def drawBoard ():
    # draw borders
    pygame.draw.rect(SURFACE,BORDERCOLOR,
                     (BOARDX-BORDERWIDTH,BOARDY-BORDERWIDTH,BOARDWIDTH+BORDERWIDTH*2,BOARDHEIGHT+BORDERWIDTH*2),BORDERWIDTH)
    # draw board background
    for row in range(1,GBOARDROWS):
        for col in range(1,BOARDCOLS):
            pos = toPixel((col,row))
            pygame.draw.circle(SURFACE,darker(BORDERCOLOR,4),pos,2)
    return

def drawPiece (piece,pos=None):
    if (pos==None):
        pos = toPixel((piece.x,piece.y-4))

    #print 'drawing a piece !!!'
    for box in piece.getBoxes():
        bPos = toPixel((box[0],box[1]-4))
        drawBox(bPos,piece.bType)
        #print 'drawing a box at ',bPos

def drawNextPiece (nextPiece):
    drawPiece (nextPiece,(NEXTPIECEX,NEXTPIECEY))

def drawStatus (score,level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (SCOREX, SCOREY)
    SURFACE.blit(scoreSurf, scoreRect)
 
    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (LEVELX, LEVELY)
    SURFACE.blit(levelSurf, levelRect)
