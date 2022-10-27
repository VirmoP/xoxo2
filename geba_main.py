import pygame, sys

pygame.init()

BG_COLOUR = (20, 150, 90)
blue = (0,2,200)
orange = (200, 50, 50)
black = (0,0,0)
white = (255, 255, 255)
size = WIDTH, HEIGHT = (800, 800)

screen = pygame.display.set_mode( size )

def draw_lines(size):
    for line_number in range(4):
        pygame.draw.line(screen, black, (line_number * WIDTH//4 ,0),(line_number * WIDTH//4, HEIGHT), WIDTH//200)
    for line_number in range(4):
        pygame.draw.line(screen, black, (0, line_number * HEIGHT//4),(HEIGHT, line_number * WIDTH//4), WIDTH//200)

def draw_tile(colour, shape, spot):
    if shape == 'x':
        pygame.draw.rect(screen, colour, (spot[0]*200, spot[1]*200, WIDTH//4, HEIGHT//4))
        pygame.draw.line(screen, black, (spot[0]*200, spot[1]*200), (spot[0]*200+WIDTH//4,spot[1]*200+HEIGHT//4))
        pygame.draw.line(screen, black, (spot[0]*200, spot[1]*200+HEIGHT//4), (spot[0]*200+WIDTH//4,spot[1]*200))
    elif shape == 'o':
        pygame.draw.rect(screen, colour, (spot[0], spot[1], WIDTH//4, HEIGHT//4))
        pygame.draw.circle(screen, black, (spot[0]*200+WIDTH//8, spot[1]*200+HEIGHT//8), 80)

def mouse_pos():
    spot = list(pygame.mouse.get_pos())
    for i in range(2):
        spot[i] = spot[i]//200
    return(spot)

screen.fill(BG_COLOUR)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_tile(orange, 'x', mouse_pos())
            print(mouse_pos())
    
    
    
    #screen.fill(BG_COLOUR)
    
    draw_lines(size)    
    
    pygame.display.update()