import pygame, sys
import button

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
start_game = False

#color setting
PURPLE2 = (81, 43, 129)
BLUE2 = (140, 171, 255)
WHITE = (255, 255, 255)
BLUE1 =(224, 247, 250)

# ความเร็วการเคลื่อนที่
SPEED = 15

# FPS
FPS = 60
clock = pygame.time.Clock()

# Button start / restart
strat_img = pygame.image.load('asset/HP/start.png').convert_alpha()
exit_img = pygame.image.load('asset/HP/exit.png').convert_alpha()


#create button insrances
start_button = button.Button(250, 300, strat_img, 0.2)
exit_button = button.Button(700, 300, exit_img, 0.2)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if start_game == False:
            #main manu
            screen.fill(BLUE2)
            if exit_button.draw() == True:
                pygame.quit()
                sys.exit()
            if start_button.draw() == True:
                start_game = True
        else:
            screen.fill(PURPLE2)
#create the screen
    pygame.display.update()
    pygame.display.set_caption('Button Demo')
    clock.tick(FPS)