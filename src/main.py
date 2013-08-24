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
    print 'xxx'
    while running == True:
        # check game over / won - V's
        if game.checkGameEnd():
            # do something here: show scores, restart, give candies, whatever
            return
        
        # check events - S's & V's
        for event in pygame.event.get(QUIT):
            return

        for event in pygame.event.get():
            if event.type == KEYUP: # check key release
                if (event.key == K_p):
                    # pause here
                    pauseGame()
                elif (event.key == K_LEFT or event.key == K_a):
                    # stop moving left
                    nop()
                elif (event.key == K_RIGHT or event.key == K_d):
                    # stop moving right
                    nop()

            elif event.type == KEYDOWN: # check key press
                if (event.key == K_LEFT or event.key == K_a):
                    game.moveLeft()
                    
                elif (event.key == K_RIGHT or event.key == K_d):
                    game.moveRight()
                    
                elif (event.key == K_UP or event.key == K_w):
                    game.rotateRight()
                    
                elif (event.key == K_DOWN or event.key == K_s):
                    game.rotateLeft()
                    
                elif event.key == K_SPACE:
                    game.hardDrop()

        
        # update game state - V's
        game.update()
        # draw things - S's
        print 'yyy'
        graphics.reset()
        graphics.drawBoard(game.board)
        graphics.drawStatus(game.score,game.level)
        FPSCLOCK.tick(FPS)
        
############
main()
