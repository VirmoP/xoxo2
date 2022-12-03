import pygame, sys
import numpy as np
import random
import time
import botplayer

pygame.init()


BG_COLOUR = (20, 150, 90)
blue = (0,2,150)
orange = (200, 50, 50)
black = (0,0,0)
Button_dark = (10,130, 70)
white = (255, 255, 255)
size = WIDTH, HEIGHT = (800, 800)
cellwidth = WIDTH//4
font = pygame.font.Font("freesansbold.ttf",WIDTH//50)


screen = pygame.display.set_mode( size )
#ehitab maatrixi mida kasutab m'ngulauana, [ks laiem kui peaks ja 22r 9 t'idetud et 22reprobleeme v'ltida
board = np.zeros((5,5))
for i in range(5):
    board[i,4] = 9
    board[4,i] = 9

# Gamestate salvestab millises hetkes mang on
# 0 - valib flippimistile
# 1 - valib kuhu tile flippida
# 2 - valib uue tile kuhu endaoma panna
# 3 - valib millist v'rvi kasutada. m'ng algab alati 2 pealt
gamestate = 2
# kumma m'ngija kord on, 0 on ring, 1 on rist
player = 0
#1 t;;tab bot 0 ei t;;ta
bot = 1

def draw_lines(size):
    for line_number in range(4):
        pygame.draw.line(screen, black, (line_number * WIDTH//4 ,0),(line_number * WIDTH//4, HEIGHT), WIDTH//200)
    for line_number in range(4):
        pygame.draw.line(screen, black, (0, line_number * HEIGHT//4),(HEIGHT, line_number * WIDTH//4), WIDTH//200)

def draw_tile(colour, shape, spot):
    if shape == 'x':
        pygame.draw.rect(screen, colour, (spot[0]*cellwidth, spot[1]*cellwidth, WIDTH//4, HEIGHT//4))
        pygame.draw.line(screen, white, (spot[0]*cellwidth, spot[1]*cellwidth), (spot[0]*cellwidth+WIDTH//4,spot[1]*cellwidth+HEIGHT//4),width=10)
        pygame.draw.line(screen, white, (spot[0]*cellwidth, spot[1]*cellwidth+HEIGHT//4), (spot[0]*cellwidth+WIDTH//4,spot[1]*cellwidth),width=10)
    elif shape == 'o':
        pygame.draw.rect(screen, colour, (spot[0]*cellwidth, spot[1]*cellwidth, WIDTH//4, HEIGHT//4))
        pygame.draw.circle(screen, white, (spot[0]*cellwidth+WIDTH//8, spot[1]*cellwidth+HEIGHT//8), WIDTH//10)
        pygame.draw.circle(screen, colour, (spot[0]*cellwidth+WIDTH//8, spot[1]*cellwidth+HEIGHT//8), WIDTH//10-20)
        
def mouse_pos():
    spot = list(pygame.mouse.get_pos())
    for i in range(2):
        spot[i] = spot[i]//cellwidth
    return(spot)

def draw_pick_color(spot):
    pygame.draw.rect(screen, orange, (spot[0]*cellwidth, spot[1]*cellwidth, WIDTH//8, HEIGHT//4))
    pygame.draw.rect(screen, blue, (spot[0]*cellwidth+WIDTH//8, spot[1]*cellwidth, WIDTH//8, HEIGHT//4))

def pick_color():
    if pygame.mouse.get_pos()[0]%cellwidth < WIDTH//8:
        match player:
            case 0:
                board[mouse_pos()[1],mouse_pos()[0]] = 3
            case 1:
                board[mouse_pos()[1],mouse_pos()[0]] = 1
    if pygame.mouse.get_pos()[0]%cellwidth > WIDTH//8:
        match player:  
            case 0:
                board[mouse_pos()[1],mouse_pos()[0]] = 4
            case 1:
                board[mouse_pos()[1],mouse_pos()[0]] = 2

def flip_clear():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i,j] == 6:
                board[i,j] = 0

saved_tile = []
def flip_pick():
    global saved_tile
    match player:
        case 0:
            if board[mouse_pos()[1],mouse_pos()[0]] in (1,2):
                saved_tile = [mouse_pos()[1],mouse_pos()[0]]
                for i in (-1,0,1):
                    for j in (-1,0,1):
                        if i*j == 0: 
                            if board[mouse_pos()[1]+i,mouse_pos()[0]+j] == 0:
                                board[mouse_pos()[1]+i,mouse_pos()[0]+j] = 6
                            
                
        case 1:
            if board[mouse_pos()[1],mouse_pos()[0]] in (3,4):
                saved_tile = [mouse_pos()[1],mouse_pos()[0]]
                for i in (-1,0,1):
                    for j in (-1,0,1):
                        if i*j == 0:
                            if board[mouse_pos()[1]+i,mouse_pos()[0]+j] == 0:
                                board[mouse_pos()[1]+i,mouse_pos()[0]+j] = 6


def tile_flip():
    global gamestate
    if board[mouse_pos()[1],mouse_pos()[0]] == 6:
        match board[saved_tile[0],saved_tile[1]]:
            case 1:
                board[mouse_pos()[1],mouse_pos()[0]] = board[saved_tile[0],saved_tile[1]] + 1
            case 2:
                board[mouse_pos()[1],mouse_pos()[0]] = board[saved_tile[0],saved_tile[1]] - 1
            case 3:
                board[mouse_pos()[1],mouse_pos()[0]] = board[saved_tile[0],saved_tile[1]] + 1
            case 4:
                board[mouse_pos()[1],mouse_pos()[0]] = board[saved_tile[0],saved_tile[1]] - 1
        
        board[saved_tile[0],saved_tile[1]] = 0
        gamestate = 2
    else:
        flip_clear()
        flip_pick()

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

def win_check(board):
    for j in range(4):
        for i in range(4):
            if board[i][j] in (1,2,3,4):
                #vertical
                if i-1 >= 0 and i+1 <= 3:
                    if board[i][j] == board[i+1][j] == board[i-1][j]:
                        return True

                #horizontal
                if j-1 >= 0 and j+1 <= 3:
                    if board[i][j] == board[i][j+1] == board[i][j-1]:
                        return True

                #desc diag
                if i-1 >= 0 and i+1 <= 3 and j-1 >= 0 and j+1 <= 3:
                    if board[i][j] == board[i+1][j+1] == board[i-1][j-1]:
                        return True

                    #asc diag
                    if board[i][j] == board[i+1][j-1] == board[i-1][j+1]:
                        return True
    return False

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

def text( text, X, Y, colour):
    text = font.render(text ,True, colour)
    textRect = text.get_rect()
    textRect.center = (X, Y)
    screen.blit(text,textRect)

def draw_menu():
        #1playerbutton
        pygame.draw.rect(screen,Button_dark,[WIDTH//2-100,WIDTH*4//10+10, 200, 40]) 
        #2playerbutton
        pygame.draw.rect(screen,Button_dark,[WIDTH//2-100,WIDTH*5//10+10, 200, 40]) 
        #tutorial
        pygame.draw.rect(screen,Button_dark,[WIDTH//2-100,WIDTH*6//10+10, 200, 40]) 
        text('1 Player',WIDTH//2,WIDTH * 4//10 + 30,blue)
        text('2 Player',WIDTH//2,WIDTH * 5//10 + 30,blue)
        text('XOXO',WIDTH//2,WIDTH//5, orange)
        text('2',WIDTH//2 + WIDTH//200 * 8, WIDTH//5 - WIDTH//200 * 2, blue)
        text('tutorial', WIDTH//2,WIDTH * 6//10 + 30,blue)

def draw_tutorial():
    screen.fill(BG_COLOUR)
    with open('tekst.txt', encoding='utf8') as f:
        i=0
        for rida in f:
            text(rida.strip(),WIDTH//2,WIDTH//5+30*i,blue)
            i+=1
    pygame.display.flip()
    flag=True
    pygame.event.clear()
    while flag==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                flag=False
    
def bot_menu():

    screen.fill(BG_COLOUR)
    pygame.draw.rect(screen,Button_dark,[WIDTH//2-100,WIDTH*4//10+10, 200, 40])
    pygame.draw.rect(screen,Button_dark,[WIDTH//2-100,WIDTH*5//10+10, 200, 40])
    text('Hea bot',WIDTH//2,WIDTH * 4//10 + 30,blue)
    text('Random bot',WIDTH//2,WIDTH * 5//10 + 30,blue)
    pygame.display.update()
    
    hea_but=pygame.Rect(WIDTH//2-100,WIDTH*4//10+10, 200, 40)
    suva_but=pygame.Rect(WIDTH//2-100,WIDTH*5//10+10, 200, 40)
    
    pygame.event.clear()
    flag=True
    while flag==True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and hea_but.collidepoint(event.pos):
                flag=False  
                #return  ...
                # mida teeb, kui hea bot valida, tuleb siia   
            if event.type == pygame.MOUSEBUTTONDOWN and suva_but.collidepoint(event.pos):
                flag=False
                #return ...
                # random bot tegevus siia

def clear_board():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i,j] != 0:
                board[i,j] = 0
                    

screen.fill(BG_COLOUR)

menu = True #laseb menüü ja mängimise vahel muuta, kui menuu while tehtud ss siin muuda trueks

but1=pygame.Rect(WIDTH//2-100,WIDTH*4//10+10, 200, 40)
but2=pygame.Rect(WIDTH//2-100,WIDTH*5//10+10, 200, 40)
but3=pygame.Rect(WIDTH//2-100,WIDTH*6//10+10, 200, 40)

while True:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and but1.collidepoint(event.pos):
                bot_menu()
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN and but2.collidepoint(event.pos):
                bot=0
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN and but3.collidepoint(event.pos):
                draw_tutorial()
                
                
        
        screen.fill(BG_COLOUR)
        draw_menu()
        pygame.display.update()
            
    while not menu:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                match gamestate:
                    case 0:
                        if bot == 1 and player == 1:
                            board = botplayer.bot_flip(board)
                            gamestate = 2
                            if win_check(board):
                                draw_board(board)
                                draw_lines(size)
                                pygame.display.update()
                                message_display('Good job!')
                                pygame.display.update()
                                
                                
                        
                        else:
                            if board[mouse_pos()[1],mouse_pos()[0]] in (1,2,3,4):
                                flip_clear()
                                flip_pick()
                                gamestate = 1

                    case 1:
                        if bot == 1 and player == 1:
                            gamestate = 2
                        
                        else:
                            tile_flip()
                            if gamestate == 2:
                                flip_clear()
                                if win_check(board):
                                    draw_board(board)
                                    draw_lines(size)
                                    pygame.display.update()
                                    message_display('Good job!')
                                    pygame.display.update()
                                    menu=True
                                
                    case 2:
                        if bot == 1 and player == 1:
                            board = botplayer.bot_newtilerandom(board)
                            gamestate = 0
                            player = 0
                        
                        else:
                            if board[mouse_pos()[1],mouse_pos()[0]] == 0:
                                board[mouse_pos()[1],mouse_pos()[0]] = 5
                                gamestate = 3
                    case 3:
                        if bot == 1 and player == 1:
                            gamestate = 0
                            player = 0
                        
                        else:
                            if board[mouse_pos()[1],mouse_pos()[0]] == 5:
                                pick_color()
                                if player == 0:
                                    player = 1
                                elif player == 1:
                                    player = 0
                                gamestate = 0


                print(board)
                print(saved_tile)
                print(gamestate)
                print(mouse_pos())
                print(board[mouse_pos()[0], mouse_pos()[1]])
        
        screen.fill(BG_COLOUR)
        draw_board(board)
        draw_lines(size)
        pygame.display.update()
        if menu== True:
           clear_board()
           break
    
