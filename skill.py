import pygame
import sys

screen = pygame.display.set_mode((1200, 700))

base_font = pygame.font.Font(None, 32)
user_text = ""

input_box = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color("chartreuse4")
color = color_passive

active = False
word = None
correct = False 

def skill():
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key != pygame.K_SPACE:
                    user_text += event.unicode
            if user_text == word:
                correct = True
                user_text = ''
                active = False
                word = None
            else:
                correct = False

    screen.fill((255, 255, 255))
    if active:
        color = color_active
    else:
        color = color_passive

    pygame.draw.rect(screen, color, input_box)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))

    input_box.w = text_surface.get_width()+10
    pygame.display.flip()

class skill1:
    """test"""