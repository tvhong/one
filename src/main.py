import sys,pygame,graphics,game
from pygame.locals import *
from gameconstants import *

FPS = 30
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
                    nop()
                elif (event.key in (K_RIGHT, K_d)):
                    # stop moving right
                    nop()
                elif (event.key in (K_DOWN, K_s)):
                    game.stopSoftDrop();

            elif event.type == KEYDOWN: # check key press
                if (event.key in (K_LEFT, K_a)):
                    game.moveLeft()
                    
                elif (event.key in (K_RIGHT, K_d)):
                    game.moveRight()
                    
                elif (event.key in (K_UP, K_w, K_x, K_PERIOD)):
                    game.rotateRight()
                    
                elif (event.key in (K_z, K_COMMA)):
                    game.rotateRight()

                elif (event.key in (K_DOWN, K_s)):
                    game.softDrop()
                    
                elif event.key == K_SPACE:
                    game.hardDrop()

        
        # update game state
        game.update()

        # drawing
        graphics.reset()
        graphics.drawStatus(game.score,game.level)
        for piece in game.getPieces():
            graphics.drawPiece(piece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
############
main()
