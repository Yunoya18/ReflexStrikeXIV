import pygame, sys
from main import screen

class Status(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 6
        self.max_health = 6
        self.mana = 1
        self.max_mana = 6
        self.self.hp = [pygame.transform.scale(pygame.image.load('asset/self.HP/self.HP0.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/self.HP1.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/self.HP2.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/self.HP3.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/self.HP4.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/self.HPFULL.png').convert_alpha(),(180,165))]
        self.mp = [pygame.transform.scale(pygame.image.load('asset/self.HP/MP0.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/MP1.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/MP2.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/MP3.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/MP4.png').convert_alpha(),(180,165)),\
            pygame.transform.scale(pygame.image.load('asset/self.HP/MPFULL.png').convert_alpha(),(180,165))]

    def get_mana(self):
        '''ได้รับมานา'''
        self.mana = min(self.max_mana, self.mana + 1)

    def lost_mana(self):
        '''เสียมานา'''
        self.mana = max(0, self.mana - 1)

    def get_damage(self):
        '''ได้รับดาเมจ'''
        self.health = max(0, self.health - 1)

    def get_health(self):
        '''ได้รับเลือด'''
        self.health = min(self.max_health, self.health + 1)

    def full_hearts(self):
        for heart in range(self.health):
            if heart < self.health:
                screen.blit(self.hp[heart],(100, 100))

    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < self.health:
                screen.blit(self.hp[heart],(100, 100))
            if heart <= 0:
                screen.blit(self.hp[0],(100, 100))

    def mana_do(self):
        for mana in range(self.max_mana):
            if mana < self.mana:
                screen.blit(self.mp[mana],(100, 100))
            if mana == 0:
                screen.blit(self.mp[0],(100, 100))

    def update(self):
        self.full_hearts()
        self.empty_hearts()
        self.mana_do()