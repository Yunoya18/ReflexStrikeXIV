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
RED = (255, 0, 0)
GRAVITY = 0.75
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 600), (1200, 600))

#projectile ---skill---
class magic_missle(pygame.sprite.Sprite):
    def __init__(self, player_pos_x, player_pos_y, speed, direction):
        super().__init__()
        self.direction = direction
        s_img = [pygame.image.load('spell/blueflame.png'), pygame.image.load('spell/dark.png'), \
                 pygame.image.load('spell/holy_arrow.png'), pygame.image.load('spell/slash.png'), pygame.image.load('spell/firespell.png')] #rskil img list
        self.flip = (direction == -1)
        if self.flip:
            #flip random img
            self.image = pygame.transform.scale(pygame.transform.flip(random.choice(s_img), True, False), (100, 100))
            self.rect = self.image.get_rect(center = (player_pos_x-75, player_pos_y))
        else:
            self.image = pygame.transform.scale(random.choice(s_img), (100, 100))
            self.rect = self.image.get_rect(center = (player_pos_x+75, player_pos_y)) #spwan projectile at player location
        self.speed = speed

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.x < -200 or self.rect.x > 1500:
            # destroy missle if travel to far
            self.kill()
        

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jumps = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(5):
            img = pygame.image.load(f'image/{self.char_type}/MCMAIN/walk/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
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
        
        #Jump
        if self.jumps == True:
            self.vel_y = -11
            self.jumps = False

        #GRAVITY
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y 
        dy += self.vel_y

        #check collision floor
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
        
        self.rect.x += dx
        self.rect.y += dy
    
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


    def create_magic_missle(self):
        return magic_missle(self.rect.centerx, self.rect.centery, 15, player.direction)

    def update(self):
        self.rect

player = Player('player', 200, 200, 3, 5)


class toggle_skill(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.color = pygame.Color("lightskyblue3")
        self.box = pygame.Rect(500, 50, 200, 50)

class mana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load('asset/HP/big_mana.png')
        self.image = pygame.transform.scale(self.img, (self.img.get_width(), self.img.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)


pygame.display.set_caption("SpellStrikeXIV")
run = True
bg = pygame.image.load('AssetsBG/forestBG.png').convert_alpha()
bg_width = bg.get_width()
tiles = math.ceil(1200 / bg_width) + 1
scroll = 0
skill = False
text = "testtest"
create_mana = False

# to start
magic_group = pygame.sprite.Group()

while run:
    draw_bg()
    player.draw()
    player.update_animation()
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
            if event.key == pygame.K_UP:
                player.jumps = True
            if event.key == pygame.K_z:
                magic_group.add(player.create_magic_missle())
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
    
    screen.blit(mana().image, mana().rect)   

    pygame.display.update()
    
pygame.quit()
