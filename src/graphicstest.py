import graphics,pygame,sys,game
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

    game.start()
    
    while (True):
        if game.checkGameEnd():
            print 'the game has ended!!'
            FPSCLOCK.tick(FPS)
            continue
        for event in pygame.event.get(QUIT):
            terminate()
        for piece in game.getPieces():
            # print 'drawing a piece!!!'
            print piece
            graphics.drawPiece(piece)

        for y in range(BOARDROWS):
            for x in range(BOARDCOLS):
                print game.board[y][x],
            print ''
            
        print 'number of pieces: ',len(game.getPieces())
        #graphics.drawBoard(board)
        graphics.drawStatus(1000,20)
        pygame.display.update()
        game.update()
        FPSCLOCK.tick(FPS)
    
def terminate():
    pygame.quit()
    sys.quit()

main()
