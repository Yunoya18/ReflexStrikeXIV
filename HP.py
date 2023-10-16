import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asset/HP/pngegg.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(100,200))
        self.rect.center=(875,1000)
        self.health = 10
        self.max_health = 10

    def get_damage(self):
        if self.health > 0:
            self.health -= 1

    def get_health(self):
        if self.health < self.max_health:
            self.health += 1

    def full_hearts(self):
        for heart in range(self.health):
            if heart < self.health:
                screen.blit(full_heart,(heart * 50 + 10,5))
            else:
                screen.blit(empty_heart,(heart * 50 + 10,5))

    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < self.health:
                screen.blit(full_heart,(heart * 50 + 10,5))
            else:
                screen.blit(empty_heart,(heart * 50 + 10,5))

    def update(self):
        self.full_hearts()
        self.empty_hearts()

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

link = pygame.sprite.GroupSingle(Player())
full_heart = pygame.image.load('asset/HP/full_heart.png').convert_alpha()
empty_heart = pygame.image.load('asset/HP/empty_heart.png').convert_alpha()


#color setting
PURPLE2 = (81, 43, 129)
BLUE2 = (140, 171, 255)
WHITE = (255, 255, 255)
# ความเร็วการเคลื่อนที่
SPEED = 5

# FPS
FPS = 120
clock = pygame.time.Clock()

#Text
costom = pygame.font.Font('asset/HP/Coiny.ttf',50)
power = costom.render("Power",True,BLUE2)

power1 = power.get_rect()
power1.centerx = 200
power1.centery = 350

#Me
costom = pygame.font.Font('asset/HP/Coiny.ttf',50)
me = costom.render('Me',True,WHITE)

me1 = me.get_rect()
me1.centerx = 600
me1.centery = 350

count = 0

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # ชน
    if power1.colliderect(me1):
        if count == 0:
            link.sprite.get_damage()
        elif count < 0 :
            pass
        count += 1
    else:
        count = 0
        
    # พลังขยับได้
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and power1.top>8:
        power1.y -= SPEED
    if keys[pygame.K_DOWN] and power1.bottom<(SCREEN_HEIGHT-8):
        power1.y += SPEED
    if keys[pygame.K_LEFT] and power1.left>8:
        power1.x -= SPEED
    if keys[pygame.K_RIGHT] and power1.right<(SCREEN_WIDTH-4):
        power1.x += SPEED

#create the screen
    pygame.draw.rect(screen,BLUE2,(power1),2)
    screen.fill(PURPLE2)
    link.draw(screen)
    screen.blit(power,power1)
    screen.blit(me,me1)
    link.update()
    pygame.display.update()
    clock.tick(FPS)