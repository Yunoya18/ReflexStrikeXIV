import pygame
import random
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 700
ENEMY_WIDTH, ENEMY_HEIGHT = 90, 90
SPEED_ENC = 2
ENEMY_SPEED = 2 * SPEED_ENC
SPAWN_HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enemy Movement")

class AnimatedEnemy:
    def __init__(self):
        enemy_sets = [
        [pygame.image.load(os.path.join('Enemy/images', f'fireball_{i}.png')) for i in range(1, 7)],
        [pygame.image.load(os.path.join('Enemy/images', f'egg_{i}.png')) for i in range(1, 7)],
        [pygame.image.load(os.path.join('Enemy/images', f'ice_{i}.png')) for i in range(1, 7)],
        [pygame.image.load(os.path.join('Enemy/images', f'stone_{i}.png')) for i in range(1, 7)]
        ]
        self.rect = pygame.Rect(1200 - 90, 600-90, 90, 90)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 90, 90)
        self.animation_frames = random.choice(enemy_sets)
        self.current_frame_index = 0

    def move(self):
        self.rect.x -= 2
        self.hitbox.x = self.rect.x

    def draw(self):
        scaled_frame = pygame.transform.scale(self.animation_frames[self.current_frame_index], (90, 90))
        screen.blit(scaled_frame, self.rect)

    def draw_hitbox(self):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def update_animation(self):
        self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)

    def play_death_sound(self):
        channel = pygame.mixer.find_channel()
        death_sound = pygame.mixer.Sound('sound/playdead.mp3')
        if channel:
            channel.set_volume(0.5)
            channel.play(death_sound)

animated_enemies = []

game_clock = pygame.time.Clock()
animation_clock = pygame.time.Clock()

