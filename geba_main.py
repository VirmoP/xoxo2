import pygame, sys

pygame.init()

BG_COLOUR = (20, 150, 90)
blue = (0,2,150)
orange = (200, 50, 50)
black = (0,0,0)
white = (255, 255, 255)
size = WIDTH, HEIGHT = (800, 800)
cellwidth = WIDTH//4

screen = pygame.display.set_mode( size )

def draw_lines(size):
    for line_number in range(4):
        pygame.draw.line(screen, black, (line_number * WIDTH//4 ,0),(line_number * WIDTH//4, HEIGHT), WIDTH//200)
    for line_number in range(4):
        pygame.draw.line(screen, black, (0, line_number * HEIGHT//4),(HEIGHT, line_number * WIDTH//4), WIDTH//200)

def draw_tile(colour, shape, spot):
    if shape == 'x':
        pygame.draw.rect(screen, colour, (spot[0]*cellwidth, spot[1]*cellwidth, WIDTH//4, HEIGHT//4))
        pygame.draw.line(screen, black, (spot[0]*cellwidth, spot[1]*cellwidth), (spot[0]*cellwidth+WIDTH//4,spot[1]*cellwidth+HEIGHT//4))
        pygame.draw.line(screen, black, (spot[0]*cellwidth, spot[1]*cellwidth+HEIGHT//4), (spot[0]*cellwidth+WIDTH//4,spot[1]*cellwidth))
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


screen.fill(BG_COLOUR)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_pick_color(mouse_pos())
            pick_color()
            print(mouse_pos())
    

    draw_lines(size)    
    
    pygame.display.update()