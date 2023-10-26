import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asset/HP/pngegg.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(100,200))
        self.rect.centerx = 200
        self.rect.centery = 350
        self.health = 6
        self.max_health = 6
        self.mana = 1
        self.max_mana = 6

    def get_mana(self):
        '''ได้รับมานา'''
        if self.mana < self.max_mana:
            self.mana += 1

    def lost_mana(self):
        '''เสียมานา'''
        if self.mana > 0:
            self.mana -= 1
        if self.mana < 0:
            self.mana = 0

    def get_damage(self):
        '''ได้รับดาเมจ'''
        if self.health > 0:
            self.health -= 1
    
    def get_health(self):
        '''ได้รับเลือด'''
        if self.health < self.max_health:
            self.health += 1

    def full_hearts(self):
        for heart in range(self.health):
            if heart < self.health:
                if heart == 5:
                    screen.blit(full_5,(100, 100))
                elif heart == 4:
                    screen.blit(hp4,(100, 100))
                elif heart == 3:
                    screen.blit(hp3,(100, 100))
                elif heart == 2:
                    screen.blit(hp2,(100, 100))
                elif heart == 1:
                    screen.blit(hp1,(100, 100))
                elif heart == 0:
                    screen.blit(hp0,(100, 100))

    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < self.health:
                if heart == 5:
                    screen.blit(full_5,(100, 100))
                elif heart == 4:
                    screen.blit(hp4,(100, 100))
                elif heart == 3:
                    screen.blit(hp3,(100, 100))
                elif heart == 2:
                    screen.blit(hp2,(100, 100))
                elif heart == 1:
                    screen.blit(hp1,(100, 100))
                elif heart == 0:
                    screen.blit(hp0,(100, 100))
            if heart <= 0:
                screen.blit(hp0,(100, 100))
    def mana_do(self):
        for mana in range(self.max_mana):
            if mana < self.mana:
                if mana == 5:
                    screen.blit(mp5,(100, 100))
                elif mana == 4:
                    screen.blit(mp4,(100, 100))
                elif mana == 3:
                    screen.blit(mp3,(100, 100))
                elif mana == 2:
                    screen.blit(mp2,(100, 100))
                elif mana == 1:
                    screen.blit(mp1,(100, 100))
                elif mana == 0:
                    screen.blit(mp0,(100, 100))
            if mana == 0:
                screen.blit(mp0,(100, 100))

    def update(self):
        self.full_hearts()
        self.empty_hearts()
        self.mana_do()

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

link = pygame.sprite.GroupSingle(Player())
full_5 = pygame.image.load('asset/HP/HPFULL.png').convert_alpha()
full_5 = pygame.transform.scale(full_5,(180,165))
hp4 = pygame.image.load('asset/HP/HP4.png').convert_alpha()
hp4 = pygame.transform.scale(hp4,(180,165))
hp3 = pygame.image.load('asset/HP/HP3.png').convert_alpha()
hp3 = pygame.transform.scale(hp3,(180,165))
hp2 = pygame.image.load('asset/HP/HP2.png').convert_alpha()
hp2 = pygame.transform.scale(hp2,(180,165))
hp1 = pygame.image.load('asset/HP/HP1.png').convert_alpha()
hp1 = pygame.transform.scale(hp1,(180,165))
hp0 = pygame.image.load('asset/HP/HP0.png').convert_alpha()
hp0 = pygame.transform.scale(hp0,(180,165))

mp0 = pygame.image.load('asset/HP/MP0.png').convert_alpha()
mp0 = pygame.transform.scale(mp0,(180,165))
mp1 = pygame.image.load('asset/HP/MP1.png').convert_alpha()
mp1 = pygame.transform.scale(mp1,(180,165))
mp2 = pygame.image.load('asset/HP/MP2.png').convert_alpha()
mp2 = pygame.transform.scale(mp2,(180,165))
mp3 = pygame.image.load('asset/HP/MP3.png').convert_alpha()
mp3 = pygame.transform.scale(mp3,(180,165))
mp4 = pygame.image.load('asset/HP/MP4.png').convert_alpha()
mp4 = pygame.transform.scale(mp4,(180,165))
mp5 = pygame.image.load('asset/HP/MPFULL.png').convert_alpha()
mp5 = pygame.transform.scale(mp5,(180,165))


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

#Text -hp
costom = pygame.font.Font('asset/HP/Coiny.ttf',50)
lost_hp = costom.render("-HP",True,BLUE2)

lost_hp1 = lost_hp.get_rect()
lost_hp1.centerx = 200
lost_hp1.centery = 350

#Text +hp
costom = pygame.font.Font('asset/HP/Coiny.ttf',50)
get_hp = costom.render("+HP",True,BLUE2)

get_hp1 = get_hp.get_rect()
get_hp1.centerx = 1000
get_hp1.centery = 350

#Me
costom = pygame.font.Font('asset/HP/Coiny.ttf',50)
me = costom.render('Me',True,WHITE)

me1 = me.get_rect()
me1.centerx = 600
me1.centery = 350

# +mana
get_mp = pygame.font.Font('asset/HP/Coiny.ttf',50)
get_mp = costom.render('+mana',True,BLUE1)

get_mp1 = get_mp.get_rect()
get_mp1.centerx = 600
get_mp1.centery = 600

# -mana
lost_mp = pygame.font.Font('asset/HP/Coiny.ttf',50)
lost_mp = costom.render('-mana',True,BLUE1)

lost_mp1 = lost_mp.get_rect()
lost_mp1.centerx = 600
lost_mp1.centery = 100

count_hp1 = 0
count_hp2 = 0
count_mp1 = 0
count_mp2 = 0

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # ชน ลดเลือด
    if lost_hp1.colliderect(me1):
        if count_hp1 == 0:
            link.sprite.get_damage()
        elif count_hp1 < 0 :
            pass
        count_hp1 += 1
    else:
        count_hp1 = 0

    # ชน เลือดเพิ่ม
    if get_hp1.colliderect(me1):
        if count_hp2 == 0:
            link.sprite.get_health()
        elif count_hp2 < 0:
            pass
        count_hp2 += 1
    else:
        count_hp2 = 0

    # มานา เพิ่ม
    if get_mp1.colliderect(me1):
        if count_mp1 == 0:
            link.sprite.get_mana()
        elif count_mp1 < 0:
            pass
        count_mp1 += 1
    else:
        count_mp1 = 0

    # มานา เพิ่ม
    if lost_mp1.colliderect(me1):
        if count_mp2 == 0:
            link.sprite.lost_mana()
        elif count_mp2 < 0:
            pass
        count_mp2 += 1
    else:
        count_mp2 = 0

    # meขยับ
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and me1.top>8:
        me1.y -= SPEED
    if keys[pygame.K_DOWN] and me1.bottom<(SCREEN_HEIGHT-8):
        me1.y += SPEED
    if keys[pygame.K_LEFT] and me1.left>8:
        me1.x -= SPEED
    if keys[pygame.K_RIGHT] and me1.right<(SCREEN_WIDTH-4):
        me1.x += SPEED
#create the screen
    pygame.draw.rect(screen,BLUE2,(me1),2)
    screen.fill(PURPLE2)
    link.draw(screen)
    screen.blit(lost_hp,lost_hp1)
    screen.blit(get_hp,get_hp1)
    screen.blit(get_mp,get_mp1)
    screen.blit(lost_mp,lost_mp1)
    screen.blit(me,me1)
    link.update()
    pygame.display.update()
    clock.tick(FPS)