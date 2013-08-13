import sys,pygame
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
BLACK = (0,0,0)

BG_COLOR = BLACK

GAME_NAME = 'Tetris!!'

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    # show main menu or sth

    startGame()
    
    # by now, the game is over
    terminate()

def nop():
    return

def terminate():
    pygame.quit()
    sys.quit()

def pauseGame():
    # S's TODO
    return

def startGame():
    # init game board here
    
    while True:
        # check game over / won - V's
        
        # check events - S's & V's
        for event in pygame.event.get(QUIT):
            terminate()
            
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
                    # try to move left
                    nop()
                elif (event.key == K_RIGHT or event.key == K_d):
                    # try to move right
                    nop()
                elif (event.key == K_UP or event.key == K_w):
                    # try to rotate clockwise
                    nop()
                elif (event.key == K_DOWN or event.key == K_s):
                    # try to rotate counter - clockwise
                    nop()
                elif event.key == K_SPACE:
                    # drop the piece right away
                    nop()

        # update game state - V's

        # draw things - S's

        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
