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
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    graphics.init(DISPLAYSURF)
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
    pygame.quit()
    #sys.quit()

def pauseGame():
    # S's TODO
    running = False
    return

def startGame():
    # init game board here
    running = True
    movingLeft = False
    movingRight = False
    while running == True:
        if game.checkGameEnd():
            # TODO: show scores, restart, give candies, whatever
            return
        
        for event in pygame.event.get(QUIT):
            return

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
        
        # update game state
        game.update()

        # drawing
        graphics.reset()
        graphics.drawStatus(game.score,game.level)
        graphics.drawBoard()
        for piece in game.getPieces():
            graphics.drawPiece(piece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
############
main()
