import graphics,pygame,sys
from pygame.locals import *
from gameconstants import *
FPS = 30
def main():
    global surface,FPSCLOCK
    pygame.init()
    surface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    FPSCLOCK = pygame.time.Clock()
    graphics.init(surface)
    board = []
    for i in range(BOARDROWS):
        board.append([BLANK]*BOARDCOLS)
    assert len(board) == BOARDROWS
    for i in range(BOARDROWS):
        assert len(board[i]) == BOARDCOLS
    board[0][0] = TYPE_O
    board[0][1] = TYPE_O
    board[1][0] = TYPE_O
    board[1][1] = TYPE_O

    board[5][5] = TYPE_I
    board[6][5] = TYPE_I
    board[7][5] = TYPE_I
    board[8][5] = TYPE_I
    
    while (True):
        for event in pygame.event.get(QUIT):
            terminate()
        graphics.drawBoard(board)
        graphics.drawStatus(1000,20)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
def terminate():
    pygame.quit()
    sys.quit()

main()
