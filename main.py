import pygame, math, random, urllib.request, os

#from pygame.sprite import _Group
from enemyextract import AnimatedEnemy
from level101 import *
from HP import Status
import button
import csv
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
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:    
    high_score = 0


WORDS = txt.splitlines()
FPS = 60
BG = (0, 0, 0)
RED = (255, 0, 0)
GRAVITY = 0.75
ROWS = 16
COLS = 150
TILE_SIZE = 700 // ROWS
#load images
forestbg_img = pygame.image.load('AssetsBG/forestBG.png').convert_alpha()
ground = pygame.image.load('tile/tile_long.png').convert_alpha()
def draw_bg():
    screen.fill(BG)
    screen.blit(forestbg_img, (0, 0))
    screen.blit(ground, (0, 600))

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

    def sfx():
        channel = pygame.mixer.find_channel() 
        sfx_spell =  pygame.mixer.Sound('sound/firecast01.mp3')
        if channel:
            channel.set_volume(0.5)
            channel.play(sfx_spell)
            
    def update(self):
        global score
        global stamina
        self.rect.x += self.direction * self.speed
        if self.rect.x < -200 or self.rect.x > 1500:
            # destroy missle if travel to far
            self.kill()
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.hitbox):
                # collision with enemy
                animated_enemies.remove(enemy)
                enemy.play_death_sound()
                score += 1
                stamina += 0.5
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
        #load all images for the players
        animation_types = ['walk', 'cast']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'image/{self.char_type}/MCMAIN/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'image/{self.char_type}/MCMAIN/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 80, 80)
        
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
            self.vel_y = -18
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
        
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > 1200:
                dx = 0
        
        self.rect.x += dx
        self.rect.y += dy
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y
    
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action == 1:
                    self.action = 0
    
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
    
    def hit_enemies(self, enemies):
        # Check for collision with enemies
        global health
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                health = max(0, health - 1)
                enemies.remove(enemy)
    
    def draw_hitbox(self):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

player = Player('player', 200, 600, 3, 5)

class mana(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = pygame.image.load('asset/HP/big_mana.png')
        self.image = pygame.transform.scale(self.img, (self.img.get_width(), self.img.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
    
    def update(self):
        if self.rect.y + self.speed < 550:
            self.rect.y += self.speed


pygame.display.set_caption("SpellStrikeXIV")
icon = pygame.image.load('asset/HP/big_mana_2.png')
pygame.display.set_icon(icon)
run = True
bg = pygame.image.load('AssetsBG/forestBG.png').convert_alpha()
bg_width = bg.get_width()
tiles = math.ceil(1200 / bg_width) + 1
scroll = 0
skill = False
text = ""
health = 5
stamina = 5
mana_x = random.randrange(0, 1100)
current_mana = mana(mana_x, 0)
last = 0
font = pygame.font.Font('asset/HP/Minecraft.ttf', 36)
is_paused = False
pygame.mixer.music.load('sound/gameost01.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)
# menu button
start_img = pygame.transform.scale(pygame.image.load('manu/start.png').convert_alpha(), (1000, 1000))
exit_img = pygame.transform.scale(pygame.image.load('manu/exit.png').convert_alpha(), (1000, 1000))
start_button = button.Button(400, start_img, 0.2)
exit_button = button.Button(800, exit_img, 0.2)
logo = pygame.transform.scale(pygame.image.load('asset/HP/logo_2.png').convert_alpha(), (300, 300))
start_game = False

# enemy
animated_enemies = []

# to start
magic_group = pygame.sprite.Group()


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not start_game:
            screen.fill((56, 118, 191))
            if exit_button.draw() == True:
                pygame.quit()
            if start_button.draw() == True:
                start_game = True
        screen.blit(logo, logo.get_rect(center=(600, 200)))
        highscore_text = font.render("Your highscore : " + str(high_score), True, (0, 0, 0))
        screen.blit(highscore_text, highscore_text.get_rect(center=(600, 450)))
        if skill:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    skill = False
                    create_mana = True
                    current_mana = mana(mana_x, 0)
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
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
                if event.key == pygame.K_RETURN and stamina > 0 and is_paused == False:
                    skill = True
                    create_mana = False
                    skill_start = pygame.time.get_ticks()
                    check_word = WORDS[random.randint(0, 10000)]
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                if event.key == pygame.K_r and is_paused:
                    score = 0
                    animated_enemies.clear()
                    is_paused = False
                    stamina = 5
                    health = 5
            #keyboard released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False

    if start_game:
        clock.tick(FPS)
        draw_bg()
        player.update_animation()
        player.draw()
        now = pygame.time.get_ticks()

        if skill:
            if now - skill_start > 3000: #มานาก้อนละ 3 วิ
                stamina -= 1
                skill_start = pygame.time.get_ticks()
            if stamina == 0:
                skill = False
                text = ""
                create_mana = True
                current_mana = mana(mana_x, 0)
            if text == check_word:
                magic_group.add(player.create_magic_missle())
                magic_missle.sfx()
                check_word = WORDS[random.randint(0, 10000)]
                text = ""
                player.update_action(1)

        if moving_left or moving_right:
            player.update_action(0)
        player.move(moving_left, moving_right)

        if is_paused:
            screen.fill((0, 0, 0))
            paused_text = font.render("PAUSED", True, (255, 0, 0))
            restart_text = font.render("press \'r\' to restart", True, (255, 255, 255))
            resume_text = font.render("press \'p\' to resume", True, (255, 255, 255))
            screen.blit(paused_text, paused_text.get_rect(center=(600, 300)))
            screen.blit(resume_text, resume_text.get_rect(center=(600, 370)))
            screen.blit(restart_text, restart_text.get_rect(center=(600, 440)))

        else:
            current_mana.update()
            if current_mana.rect.collidepoint(player.rect.center):
                mana_x = random.randrange(0, 1100)
                current_mana = mana(mana_x, 0)
                stamina = min(5, stamina + 1)
                last = pygame.time.get_ticks()
            now = pygame.time.get_ticks()
            if now - last >= 8000: #8 sec
                last = now
                mana_x = random.randrange(0, 1100)
                current_mana = mana(mana_x, 0)

            #update
            magic_group.update()
            player.hit_enemies(animated_enemies)
            #player.draw_hitbox()
            Status().update(health, int(stamina))

            #draw
            magic_group.draw(screen)
            if skill:
                checkword_surface = font.render(check_word, True, (255, 255, 255))
                screen.blit(checkword_surface, checkword_surface.get_rect(center=(600, 50)))
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, text_surface.get_rect(center=(600, 100)))
            if stamina < 5 and create_mana:
                screen.blit(current_mana.image, current_mana.rect)

            #enemy
            if 20 < random.randint(0, 500) < 25:
                new_enemy = AnimatedEnemy()
                animated_enemies.append(new_enemy)
            for enemy in animated_enemies:
                enemy.move()
                enemy.update_animation()
                if enemy.rect.right < 0:
                    animated_enemies.remove(enemy)
            for enemy in animated_enemies:
                enemy.draw()
        
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            score_text = font.render(f"score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (screen_width - 200, 10))
    pygame.display.update()

pygame.quit()
