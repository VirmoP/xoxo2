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
board = np.zeros((4,4))
board[(2,3)] = 4

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
        draw_tile(orange, 'o', mouse_pos())
    if pygame.mouse.get_pos()[0]%cellwidth > 100:
        draw_tile(blue, 'o', mouse_pos())

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
            board[mouse_pos()[1],mouse_pos()[0]] = random.randint(1, 3)
            print(board)

    
    draw_lines(size)    
    draw_board(board)
    pygame.display.update()