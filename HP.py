import pygame, sys

screen = pygame.display.set_mode((1200, 700))
class Status(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = [pygame.transform.scale(pygame.image.load('asset/HP/HP0.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/HP1.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/HP2.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/HP3.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/HP4.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/HPFULL.png').convert_alpha(),(250, 250))]
        self.mp = [pygame.transform.scale(pygame.image.load('asset/HP/MP0.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/MP1.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/MP2.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/MP3.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/MP4.png').convert_alpha(),(250, 250)),\
            pygame.transform.scale(pygame.image.load('asset/HP/MPFULL.png').convert_alpha(),(250, 250))]

    def full_hearts(self, health):
        screen.blit(self.hp[health],(10, 0))

    def mana_do(self, mana):
        screen.blit(self.mp[mana],(10, 0))

    def update(self, health, mana):
        self.full_hearts(health)
        self.mana_do(mana)
