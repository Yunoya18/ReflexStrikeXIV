from typing import Any
import pygame, sys
import math
import random

#from pygame.sprite import _Group
from level101 import *
pygame.init()
screen = pygame.display.set_mode((1200, 700))
#define player action variables
moving_left = False
moving_right = False
clock = pygame.time.Clock()
FPS = 60
BG = (0, 0, 0)

def draw_bg():
    screen.fill(BG)


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
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load('MCMAIN/mc_cast_1.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # player movement
        self.direction = 1
        self.flip = False
        self.gravity = 0.8
        self.jump_speed = -16

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx =  -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


    def create_magic_missle(self):
        return magic_missle(self.rect.centerx +1, self.rect.centery, 15)
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.rect
    
    def create_magic_missle(self):
        return magic_missle(self.rect.x +1, self.rect.y, 15)

player = Player(200, 200, 3, 5)


class toggle_skill(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.color = pygame.Color("lightskyblue3")
        self.box = pygame.Rect(500, 50, 200, 50)

class mana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #img = pygame.image.load('')
        #self.image = pygame.transform.scale(img, img.get_width(), img.get_height())
        #self.rect = self.image.get_rect()
        #self.rect.center = (50, random.randrange(0, 650))


pygame.display.set_caption("SpellStrikeXIV")
run = True
bg = pygame.image.load('AssetsBG/forestBG.png').convert_alpha()
bg_width = bg.get_width()
tiles = math.ceil(1200 / bg_width) + 1
scroll = 0
skill = False
text = "testtest"
link = pygame.sprite.GroupSingle()
# object
# current cord
x = 250
y = 250
# to start
magic_group = pygame.sprite.Group()

while run:
    draw_bg()
    player.draw()
    player.move(moving_left, moving_right)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if skill:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        if not text: #ตรงกับคำที่ generate ยังไม่ได้แก้
            magic_group.add(player.create_magic_missle())
        #keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
        #keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    #if mana.colliderect(500, 500):
    #    link.sprite.get_mana()

    #update
    #player.update()
    magic_group.update()
    #link.update()

    #draw
    magic_group.draw(screen)
    if skill:
        pygame.draw.rect(screen, toggle_skill().color, toggle_skill().box)
        text_surface = toggle_skill().font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (toggle_skill().box.x, toggle_skill().box.centery))
    #pygame.draw.rect(screen, (255, 255, 255), mana)

    pygame.display.update()
    
pygame.quit()
