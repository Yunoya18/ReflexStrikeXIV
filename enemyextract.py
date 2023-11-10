import pygame
import random
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
ENEMY_WIDTH, ENEMY_HEIGHT = 90, 90
SPEED_ENC = 2
ENEMY_SPEED = 2 * SPEED_ENC
SPAWN_HEIGHT = 400

enemy_sets = [
    [pygame.image.load(os.path.join('images', f'fireball_{i}.png')) for i in range(1, 7)],
    [pygame.image.load(os.path.join('images', f'egg_{i}.png')) for i in range(1, 7)],
    [pygame.image.load(os.path.join('images', f'ice_{i}.png')) for i in range(1, 7)],
    [pygame.image.load(os.path.join('images', f'stone_{i}.png')) for i in range(1, 7)]
]

enemy_death_sound = pygame.mixer.Sound('playdead.mp3')

class AnimatedEnemy():
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - ENEMY_WIDTH, SPAWN_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.animation_frames = random.choice(enemy_sets)
        self.current_frame_index = 0

    def move(self):
        self.rect.x -= ENEMY_SPEED  # Move horizontally to the left
        self.hitbox.x = self.rect.x

    def draw(self):
        scaled_frame = pygame.transform.scale(self.animation_frames[self.current_frame_index], (ENEMY_WIDTH, ENEMY_HEIGHT))
        screen.blit(scaled_frame, self.rect)

    def draw_hitbox(self):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)  # Draw the hitbox

    def update_animation(self):
        self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)

    def play_death_sound(self):
        enemy_death_sound.play()


animated_enemies = []