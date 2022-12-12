import random
import copy

def bot_fliprandom(board):
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


def bot_newtilerandom(board):
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

#1,2 risti ehk boti oma 3,4 ring ehk player
def board_value(board):
    value = 0
    for j in range(4):
        for i in range(4):
            if i in (1,2) and j in (1,2) and board[i][j] in (1,2):
                value += 10
            if board[i][j] in (1,2,3,4):
                
                #vertical
                if i-1 >= 0 and i+1 <= 3:
                    if board[i][j] == board[i+1][j] == board[i-1][j]:
                        if board[i][j] in (1,2):
                            value += 50
                        else:
                            value -= 100

                #horizontal
                if j-1 >= 0 and j+1 <= 3:
                    if board[i][j] == board[i][j+1] == board[i][j-1]:
                        if board[i][j] in (1,2):
                            value += 50
                        else:
                            value -= 100

                #desc diag
                if i-1 >= 0 and i+1 <= 3 and j-1 >= 0 and j+1 <= 3:
                    if board[i][j] == board[i+1][j+1] == board[i-1][j-1]:
                        if board[i][j] in (1,2):
                            value += 50
                        else:
                            value -= 100

                    #asc diag
                    if board[i][j] == board[i+1][j-1] == board[i-1][j+1]:
                        if board[i][j] in (1,2):
                            value += 50
                        else:
                            value -= 100
    
    return value


#arvutab iga flippimise v]imaluse kasulikkuse e.g value
def bot_flip(board):
    valueboard = {}
    hetkboard = copy.copy(board)
    for i in range(4):
        for j in range(4):
            if board[i][j] in (3,4):
                valueboard[(i,j)] = [-10,-10,-10,-10]
                if 0 in (board[i-1][j],board[i][j+1],board[i+1][j],board[i][j-1]):
                    if board[i-1][j] == 0:
                        hetkboard = copy.copy(board)
                        if board[i][j] == 3:
                            hetkboard[i-1][j] = 4
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][0] = board_value(hetkboard)
                            
                        if board[i][j] == 4:
                            hetkboard[i-1][j] = 3
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][0] = board_value(hetkboard)
                            
                    if board[i][j+1] == 0:
                        hetkboard = copy.copy(board)
                        if board[i][j] == 3:
                            hetkboard[i][j+1] = 4
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][1] = board_value(hetkboard)
                            
                        if board[i][j] == 4:
                            hetkboard[i][j+1] = 3
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][1] = board_value(hetkboard)
                            
                    if board[i+1][j] == 0:
                        hetkboard = copy.copy(board)
                        if board[i][j] == 3:
                            hetkboard[i+1][j] = 4
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][2] = board_value(hetkboard)

                        if board[i][j] == 4:
                            hetkboard[i+1][j] = 3
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][2] = board_value(hetkboard)
                            
                    if board[i][j-1] == 0:
                        hetkboard = copy.copy(board)
                        if board[i][j] == 3:
                            hetkboard[i][j-1] = 4
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][3] = board_value(hetkboard)
                            
                        if board[i][j] == 4:
                            hetkboard[i][j-1] = 3
                            hetkboard[i][j] = 0
                            valueboard[(i,j)][3] = board_value(hetkboard)
                    
            else:
                valueboard[(i,j)] = [-10,-10,-10,-10]
    suurim = [(0,0), 0]
    for tile in valueboard:
        for suund in range(len(valueboard[tile])):
            if valueboard[tile][suund] > valueboard[suurim[0]][suurim[1]]:
                suurim = [tile, suund]

    save = board[suurim[0][0]][suurim[0][1]]
    match suurim[1]:
        case 0:
            if save == 3:
                board[suurim[0][0]-1][suurim[0][1]] = 4
                board[suurim[0][0]][suurim[0][1]] = 0
            if save == 4:
                board[suurim[0][0]-1][suurim[0][1]] = 3
                board[suurim[0][0]][suurim[0][1]] = 0
        case 1:
            if save == 3:
                board[suurim[0][0]][suurim[0][1]+1] = 4
                board[suurim[0][0]][suurim[0][1]] = 0
            if save == 4:
                board[suurim[0][0]][suurim[0][1]+1] = 3
                board[suurim[0][0]][suurim[0][1]] = 0
        case 2:
            if save == 3:
                board[suurim[0][0]+1][suurim[0][1]] = 4
                board[suurim[0][0]][suurim[0][1]] = 0
            if save == 4:
                board[suurim[0][0]+1][suurim[0][1]] = 3
                board[suurim[0][0]][suurim[0][1]] = 0
        case 3:
            if save == 3:
                board[suurim[0][0]][suurim[0][1]-1] = 4
                board[suurim[0][0]][suurim[0][1]] = 0
            if save == 4:
                board[suurim[0][0]][suurim[0][1]-1] = 3
                board[suurim[0][0]][suurim[0][1]] = 0
    return board
    
    
#arvutab parima koha kuhu uus tile panna ja mis v'rvi see on (valueboardi v;;rtuse esimene oranz, teine sinine)
def bot_newtile(board):
    valueboard = {}
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                valueboard[(i,j)] = [-10,-10]
            else:
                orangeboard = copy.copy(board)
                blueboard = copy.copy(board)
                orangeboard[i][j] = 1
                blueboard[i][j] = 2
                valueboard[(i,j)] = [board_value(orangeboard), board_value(blueboard)] 
    
    maksimal = [(0,0), 0]
    for tile in valueboard:
        for varv in range(2):
            if valueboard[tile][varv] > valueboard[maksimal[0]][maksimal[1]]:
                maksimal = [tile, varv]
    
    match maksimal[1]:
        case 0:
            board[maksimal[0][0]][maksimal[0][1]] = 1
        case 1:
            board[maksimal[0][0]][maksimal[0][1]] = 2
        
    return board
    