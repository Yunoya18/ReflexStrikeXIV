from typing import Any
import pygame, math, random, urllib.request

#from pygame.sprite import _Group
from enemyextract import AnimatedEnemy
from level101 import *
from HP import Status
pygame.init()
screen = pygame.display.set_mode((1200, 700))
#define player action variables
moving_left = False
moving_right = False
clock = pygame.time.Clock()
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = urllib.request.urlopen(word_site)
txt = response.read().decode()
#score
score = 0

WORDS = txt.splitlines()
FPS = 60
BG = (0, 0, 0)
RED = (255, 0, 0)
GRAVITY = 0.75
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 600), (1200, 600))

#projectile ---skill---
class magic_missle(pygame.sprite.Sprite):
    def __init__(self, player_pos_x, player_pos_y, speed, direction, enemies):
        super().__init__()
        self.enemies = enemies
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
        global score
        self.rect.x += self.direction * self.speed
        if self.rect.x < -200 or self.rect.x > 1500:
            # destroy missle if travel to far
            self.kill()
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                # collision with enemy
                animated_enemies.remove(enemy)
                enemy.play_death_sound()
                score += 1
                self.kill()
                break
        

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'image/{self.char_type}/MCMAIN/walk/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'image/{self.char_type}/MCMAIN/cast/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
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
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #GRAVITY
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y 
        dy += self.vel_y

        #check collision floor
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.in_air = False
        
        self.rect.x += dx
        self.rect.y += dy
    
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
    
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()  

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


    def create_magic_missle(self):
        return magic_missle(self.rect.centerx, self.rect.centery, 15, player.direction, animated_enemies)

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
    def __init__(self, x, y):
        super().__init__()
        self.img = pygame.image.load('asset/HP/big_mana.png')
        self.image = pygame.transform.scale(self.img, (self.img.get_width(), self.img.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
    
    def update(self):
        if self.rect.y + self.speed < 550:
            self.rect.y += self.speed


pygame.display.set_caption("SpellStrikeXIV")
run = True
bg = pygame.image.load('AssetsBG/forestBG.png').convert_alpha()
bg_width = bg.get_width()
tiles = math.ceil(1200 / bg_width) + 1
scroll = 0
skill = False
text = ""
health = 5
stamina = 0
create_mana = True
mana_x = random.randrange(0, 1100)
current_mana = mana(mana_x, 0)
check_word = WORDS[random.randint(0, 10000)]
font = pygame.font.Font('asset/HP/Coiny.ttf', 36)
is_paused = False

# enemy
animated_enemies = []

# to start
magic_group = pygame.sprite.Group()

while run:
    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()

    if moving_left or moving_right:
        player.update_action(1)
    else:
        player.update_action(0)
    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if skill:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        else:
            #keyboard press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_paused == False:
                    moving_left = True
                if event.key == pygame.K_RIGHT and is_paused == False:
                    moving_right = True
                if (event.key == pygame.K_UP and player.alive) and is_paused == False:
                    player.jump = True
                if event.key == pygame.K_z and is_paused == False:
                    magic_group.add(player.create_magic_missle())
                if event.key == pygame.K_p:
                    is_paused = not is_paused
            #keyboard released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False
        if text == check_word: #ตรงกับคำที่ generate ยังไม่ได้แก้
            magic_group.add(player.create_magic_missle())
            check_word = WORDS[random.randint(0, 10000)]
            text = ""
            print(check_word)

    if is_paused:
        paused_text = font.render(":)", False, (255, 255, 255))
        screen.blit(paused_text, (screen_width // 2 - 50, screen_height // 2 - 20))

    else:
        if create_mana:
            current_mana.update()
            if current_mana.rect.collidepoint(player.rect.center):
                mana_x = random.randrange(0, 1100)
                current_mana = mana(mana_x, 0)
                stamina = min(5, stamina + 1)
                create_mana = False
                last = pygame.time.get_ticks()
        else:
            now = pygame.time.get_ticks()
            if now - last >= 5000: #delay 5 sec
                last = now
                create_mana = True

        #update
        magic_group.update()
        Status().update(health, stamina)

        #draw
        magic_group.draw(screen)
        if skill:
            pygame.draw.rect(screen, toggle_skill().color, toggle_skill().box)
            text_surface = toggle_skill().font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (toggle_skill().box.x, toggle_skill().box.centery))
        if stamina < 5 and create_mana:
            screen.blit(current_mana.image, current_mana.rect)

        #enemy
        if 20 < random.randint(0, 100) < 25:
            new_enemy = AnimatedEnemy()
            animated_enemies.append(new_enemy)
        for enemy in animated_enemies:
            enemy.move()
            enemy.update_animation()
            if enemy.rect.right < 0:
                enemy.play_death_sound()
                animated_enemies.remove(enemy)

        for enemy in animated_enemies:
            enemy.draw()
            enemy.draw_hitbox()
        score_text = font.render(f"score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width - 200, 10))
        pygame.display.update()

pygame.quit()
