import sys,pygame,graphics,game,time
from pygame.locals import *
from gameconstants import *

FPS = 30
MOVING_DELAY = 0.1
GAME_NAME = 'Tetris!!'

def main():
    global FPSCLOCK, DISPLAYSURF, running
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    graphics.init()
    pygame.display.set_caption(GAME_NAME)
    running = False
    # show main menu or sth

    game.start()
    startGame()
    # by now, the game is over
    terminate()

def lineEaten(lines):
    pass

def newPieceGenerated():
    pass

def nop():
    return

def terminate():
    game.f.close()
    pygame.quit()
    #sys.quit()

def pauseGame():
    # S's TODO
    global running
    running = not running

def handleEvents():
    global movingLeft, movingRight,running,lastMove
    for event in pygame.event.get():
        if event.type == KEYUP: # check key release
            if (event.key == K_p):
                # pause here
                pauseGame()
            elif (event.key in (K_LEFT, K_a)):
                # stop moving left
                movingLeft = False
            elif (event.key in (K_RIGHT, K_d)):
                # stop moving right
                movingRight = False
            elif (event.key in (K_DOWN, K_s)):
                game.stopSoftDrop()
        elif event.type == KEYDOWN: # check key press
            if (event.key in (K_LEFT, K_a)):
                game.moveLeft()
                movingLeft = True
                movingRight = False
                lastMove = time.time()
                    
            elif (event.key in (K_RIGHT, K_d)):
                game.moveRight()
                movingLeft = False
                movingRight = True
                lastMove = time.time()
                
            elif (event.key in (K_UP, K_w, K_x, K_PERIOD)):
                game.rotateRight()                    
            elif (event.key in (K_z, K_COMMA)):
                game.rotateLeft()

            elif (event.key in (K_DOWN, K_s)):
                game.softDrop()
                    
            elif event.key == K_SPACE:
                game.hardDrop()

    # movement from holding a key
    if (movingLeft or movingRight) and time.time()-lastMove>MOVING_DELAY:
        if movingLeft:
            game.moveLeft()
        if movingRight:
            game.moveRight()
        lastMove = time.time()

def handleGlobalEvents ():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get():
        if event.type == KEYUP and event.key == K_p:
            pauseGame()
        elif running:
            pygame.event.post(event)
            
def startGame():
    # init game board here
    global movingLeft,movingRight,running,lastMove
    running = True
    movingLeft = False
    movingRight = False
    while True:
        handleGlobalEvents()
        
        if running:
            if game.checkGameEnd():
                # TODO: show scores, restart, give candies, whatever
                return

            handleEvents()
            
            # update game state
            game.update()

            # drawing
            graphics.reset()
            graphics.drawStatus(game.score,game.level)
            graphics.drawNextPiece(game.getNextPiece())
            graphics.drawBoard()
            for piece in game.getPieces():
                graphics.drawPiece(piece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
############
main()
