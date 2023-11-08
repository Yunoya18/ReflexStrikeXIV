from typing import Any
import pygame, sys
import math

#from pygame.sprite import _Group
from level101 import *
from level import Level

#normal projectile ---not skill---
class magic_missle(pygame.sprite.Sprite):
    def __init__(self, player_pos_x, player_pos_y, speed):
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center = (player_pos_x,player_pos_y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((32,64))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)

        # player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.jump()

    def create_magic_missle(self):
        return magic_missle(self.rect.centerx +1, self.rect.centery, 15)
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.rect
    
    def create_magic_missle(self):
        return magic_missle(self.rect.x +1, self.rect.y, 15)

class toggle_skill(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.color = pygame.Color("lightskyblue3")
        self.box = pygame.Rect(500, 50, 200, 50)

    def check_text(self, text, keys):
        if keys[pygame.K_BACKSPACE]:
            text = text[:-1]
        else:
            text += keys.unicode
        return text
    
    def check_skill(self):
        pass

def main():
    pygame.init()

    screen = pygame.display.set_mode((1200, 700))
    clock = pygame.time.Clock()
    level = Level(level_map,screen)
    pygame.display.set_caption("SpellStrikeXIV")
    run = True
    bg = pygame.image.load('AssetsBG/forestBG.png').convert_alpha()
    bg_width = bg.get_width()
    tiles = math.ceil(1200 / bg_width) + 1
    scroll = 0
    # object

    # current cord
    x = 250
    y = 250

    # to start
    player = Player((x, y))
    magic_group = pygame.sprite.Group()
    active_skill = toggle_skill()

    while run:
        pygame.time.delay(10)
        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))
        scroll -= 5
        if abs(scroll) > bg_width:
            scroll = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            magic_group.add(player.create_magic_missle())

        level.run()
        
        #update
        player.update()
        magic_group.update()

        #draw
        magic_group.draw(screen)
        pygame.draw.rect(screen, active_skill.color, active_skill.box)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

main()
