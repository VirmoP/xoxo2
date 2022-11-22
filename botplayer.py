import random

def bot_flip(board):
    while True:
        x = random.randint(0,4)
        y = random.randint(0,4)
        
        #[les 0, parem 1, all 2, vasak 3
        if board[x][y] in (3,4):
            if 0 in (board[x-1][y],board[x][y+1],board[x+1][y],board[x][y-1]):
                while True:
                    suund = random.randint(0,4)
                    match suund:
                        case 0:
                            if board[x-1][y] == 0:
                                if board[x][y] == 3:
                                    board[x-1][y] = 4
                                elif board[x][y] == 4:
                                    board[x-1][y] = 3
                                board[x][y] = 0
                                break
                        case 1:
                            if board[x][y+1] == 0:
                                if board[x][y] == 3:
                                    board[x][y+1] = 4
                                elif board[x][y] == 4:
                                    board[x][y+1] = 3
                                board[x][y] = 0
                                break
                        case 2:
                            if board[x+1][y] == 0:
                                if board[x][y] == 3:
                                    board[x+1][y] = 4
                                elif board[x][y] == 4:
                                    board[x+1][y] = 3
                                board[x][y] = 0
                                break
                        case 3:
                            if board[x][y-1] == 0:
                                if board[x][y] == 3:
                                    board[x][y-1] = 4
                                elif board[x][y] == 4:
                                    board[x][y-1] = 3
                                board[x][y] = 0
                                break
                break        
    return board                  


def bot_newtile(board):
    while True:
        x = random.randint(0,4)
        y = random.randint(0,4)
        if board[x][y] == 0:
            while True:
                color = random.randint(0,2)
                if color == 0:
                    board[x][y] = 1
                else:
                    board[x][y] = 2
                break
            break
        
    return board
        
        