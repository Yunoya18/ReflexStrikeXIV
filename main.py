from typing import Any
import pygame, sys
import math
import random

#from pygame.sprite import _Group
from level101 import *
from tiles import Tile

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
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('MCMAIN/MCCAST1.1.jpg')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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

class Level:
    def __init__(self,level_data,surface):

        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile =Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player(200, 200, 0.25)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self, skill):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Player
        if not skill:
            self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

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
    skill = False
    text = "testtest"
    link = pygame.sprite.GroupSingle()
    # object

    # to start
    player = Player(200, 200, 0.25)
    magic_group = pygame.sprite.Group()

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
            if skill:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            if not text: #ตรงกับคำที่ generate ยังไม่ได้แก้
                magic_group.add(player.create_magic_missle())

        #if mana.colliderect(500, 500):
        #    link.sprite.get_mana()

        level.run(skill)

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
        clock.tick(60)
    pygame.quit()

main()
