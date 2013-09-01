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
WINDOWWIDTH = 1000
WINDOWHEIGHT = 650

TEXTAREAWIDTH = 400

BOXSIZE = 30
BOXMG = 3

MARGIN = 20
BORDERWIDTH = 3

BOARDX = MARGIN
BOARDY = MARGIN
BOARDWIDTH = BOARDCOLS*BOXSIZE
BOARDHEIGHT = GBOARDROWS*BOXSIZE

NEXTPIECEX = BOARDX+BOARDWIDTH+MARGIN
NEXTPIECEY = MARGIN

SCOREX = NEXTPIECEX
SCOREY = NEXTPIECEY + 150 + MARGIN

LEVELX = SCOREX
LEVELY = SCOREY + 50 + MARGIN

# FONTS

# INSTRUCTION TEXT
INS = ['Complete a row to gain points',
        'and avoid reaching the top!',
        'Arrow left / right: move horizontally',
        'Z and X: rotate',
        'Arrow down: fasten the falling rate',
        'Space: drop immediately',
        'P: pause the game',
        '- - -',
        'Have fun!!!']

def init ():
    global SURFACE,BASICFONT,BIGFONT
    WINDOW = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    SURFACE = WINDOW.subsurface((TEXTAREAWIDTH,0,WINDOWWIDTH-TEXTAREAWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    dy = 50
    for insLine in INS:
        drawText(insLine,(MARGIN,MARGIN+dy),surface=WINDOW)
        dy += 40

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
    assert piece != None
    if (pos==None):
        for box in piece.getBoxes():
            bPos = toPixel((box[0],box[1]-4))
            drawBox(bPos,piece.bType)

    else:
        for box in piece.getBoxes():
            bPos = (pos[0]+(box[0]-piece.x)*BOXSIZE,pos[1]+box[1]*BOXSIZE)
            drawBox(bPos,piece.bType)
            #print 'drawing a box at ',bPos

def drawNextPiece (nextPiece):
    pygame.draw.rect(SURFACE,BORDERCOLOR,
                     (NEXTPIECEX,NEXTPIECEY,150,150),1)
    drawText('Next',(NEXTPIECEX+20,NEXTPIECEY),bgcolor=BLACK)
    if nextPiece!=None:
        drawPiece (nextPiece,(NEXTPIECEX+10,NEXTPIECEY+10))

def drawStatus (score,level):
    # draw the score text
    drawText('Score: %s' % score,(SCOREX, SCOREY))
 
    # draw the level text
    drawText('Level: %s' % level,(LEVELX,LEVELY))

def drawText (text,pos,color=TEXTCOLOR,font=None,bgcolor=None,surface=None):
    global BASICFONT,SURFACE
    if font==None: fone = BASICFONT
    if surface==None: surface = SURFACE
    textSurf = BASICFONT.render(text,True,color)
    textRect = textSurf.get_rect()
    textRect.topleft = (pos[0],pos[1])
    surface.blit(textSurf, textRect)    
