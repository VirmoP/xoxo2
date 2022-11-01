import pygame, sys
import numpy as np
import random


pygame.init()

BG_COLOUR = (20, 150, 90)
blue = (0,2,150)
orange = (200, 50, 50)
black = (0,0,0)
white = (255, 255, 255)
size = WIDTH, HEIGHT = (800, 800)
cellwidth = WIDTH//4

screen = pygame.display.set_mode( size )
#ehitab maatrixi mida kasutab m'ngulauana, [ks laiem kui peaks ja 22r 9 t'idetud et ''reprobleeme v'ltida
board = np.zeros((5,5))
for i in range(5):
    board[i,4] = 9
    board[4,i] = 9

# Gamestate salvestab millises hetkes mmang on
# 0 - valib flippimistile
# 1 - valib kuhu tile flippida
# 2 - valib uue tile kuhu endaoma panna
# 3 - valib millist v'rvi kasutada. m'ng algab alati 2 pealt
gamestate = 2
# kumma m'ngija kord on, 0 on ring, 1 on rist
player = 0


def draw_lines(size):
    for line_number in range(4):
        pygame.draw.line(screen, black, (line_number * WIDTH//4 ,0),(line_number * WIDTH//4, HEIGHT), WIDTH//200)
    for line_number in range(4):
        pygame.draw.line(screen, black, (0, line_number * HEIGHT//4),(HEIGHT, line_number * WIDTH//4), WIDTH//200)

def draw_tile(colour, shape, spot):
    if shape == 'x':
        pygame.draw.rect(screen, colour, (spot[0]*cellwidth, spot[1]*cellwidth, WIDTH//4, HEIGHT//4))
        pygame.draw.line(screen, black, (spot[0]*cellwidth, spot[1]*cellwidth), (spot[0]*cellwidth+WIDTH//4,spot[1]*cellwidth+HEIGHT//4),width=10)
        pygame.draw.line(screen, black, (spot[0]*cellwidth, spot[1]*cellwidth+HEIGHT//4), (spot[0]*cellwidth+WIDTH//4,spot[1]*cellwidth),width=10)
    elif shape == 'o':
        pygame.draw.rect(screen, colour, (spot[0]*cellwidth, spot[1]*cellwidth, WIDTH//4, HEIGHT//4))
        pygame.draw.circle(screen, black, (spot[0]*cellwidth+WIDTH//8, spot[1]*cellwidth+HEIGHT//8), 80)

def mouse_pos():
    spot = list(pygame.mouse.get_pos())
    for i in range(2):
        spot[i] = spot[i]//cellwidth
    return(spot)

def draw_pick_color(spot):
    pygame.draw.rect(screen, orange, (spot[0]*cellwidth, spot[1]*cellwidth, WIDTH//8, HEIGHT//4))
    pygame.draw.rect(screen, blue, (spot[0]*cellwidth+WIDTH//8, spot[1]*cellwidth, WIDTH//8, HEIGHT//4))

def pick_color():
    if pygame.mouse.get_pos()[0]%cellwidth < 100:
        board[mouse_pos()[1],mouse_pos()[0]] = 1
    if pygame.mouse.get_pos()[0]%cellwidth > 100:
        board[mouse_pos()[1],mouse_pos()[0]] = 2

def flip_pick():
    match player:
        case 0:
            if board[mouse_pos()[1],mouse_pos()[0]] in (1,2):
                for i in (-1,0,1):
                    for j in (-1,0,1):
                        if i*j == 0: 
                            if board[mouse_pos()[1]+i,mouse_pos()[0]+j] == 0:
                                board[mouse_pos()[1]+i,mouse_pos()[0]+j] = 6
                            
                
        case 1:
            if board[mouse_pos()[1],mouse_pos()[0]] in (3,4):
                for i in (-1,0,1):
                    for j in (-1,0,1):
                        if i*j == 0:
                            if board[mouse_pos()[1]+i,mouse_pos()[0]+j] == 0:
                                board[mouse_pos()[1]+i,mouse_pos()[0]+j] = 6


# joonistab igasse ruutu vastava tile, 1, 2 rist 3, 4 ring, nendest paaritud oranz, paaris sinine
# 5 on colorpick, 6-9 tbd 
def draw_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            match board[j,i]:
                case 1:
                    draw_tile(orange, 'x', (i,j))
                case 2:
                    draw_tile(blue, 'x', (i,j))
                case 3:
                    draw_tile(orange, 'o', (i,j))
                case 4:
                    draw_tile(blue, 'o', (i,j))
                case 5:
                    draw_pick_color((i,j))


screen.fill(BG_COLOUR)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            match gamestate:
                case 0:
                    if board[mouse_pos()[1],mouse_pos()[0]] in (1,2,3,4):
                        flip_pick()
                        print("jep sain")
                        gamestate = 1

                case 1:
                    if board[mouse_pos()[1],mouse_pos()[0]] == 0:
                        print('flipid siia sain')# todo flip funktsioon
                        gamestate = 2
                case 2:
                    if board[mouse_pos()[1],mouse_pos()[0]] == 0:
                        board[mouse_pos()[1],mouse_pos()[0]] = 5
                        gamestate = 3
                case 3:
                    if board[mouse_pos()[1],mouse_pos()[0]] == 5:
                        pick_color()
                        gamestate = 0


            #board[mouse_pos()[1],mouse_pos()[0]] = random.randint(1, 5)
            print(board)
            print(gamestate)
            print(mouse_pos())
            print(board[mouse_pos()[0], mouse_pos()[1]])

    draw_lines(size)    
    draw_board(board)
    pygame.display.update()