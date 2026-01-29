import pygame
import random

RED = (255, 0, 0)
BLUE = (0, 120, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ENEMY_SPEED = 1
ENEMY_DROP = 20

class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED
        self.direction = 1
        self.color = random.choice([RED, BLUE, WHITE])
        self.points = 10 if self.color == RED else 20 if self.color == BLUE else 30
        self.frame = 0
        self.animation_timer = 0

    def draw(self, screen):
        self.animation_timer += 1
        if self.animation_timer >= 30:
            self.frame = 1 - self.frame
            self.animation_timer = 0

        if self.frame == 0:
            self.draw_frame1(screen)
        else:
            self.draw_frame2(screen)

    def draw_frame1(self, screen):
        pygame.draw.rect(screen, self.color, (self.x + 5, self.y, self.width - 10, 30))
        pygame.draw.rect(screen, self.color, (self.x, self.y + 10, self.width, 20))

        pygame.draw.rect(screen, self.color, (self.x + 15, self.y + 30, 5, 10))
        pygame.draw.rect(screen, self.color, (self.x + 25, self.y + 30, 5, 10))

        pygame.draw.rect(screen, BLACK, (self.x + 10, self.y + 5, 8, 8))
        pygame.draw.rect(screen, BLACK, (self.x + 25, self.y + 5, 8, 8))

        pygame.draw.rect(screen, BLACK, (self.x + 15, self.y + 20, 12, 3))

    def draw_frame2(self, screen):
        pygame.draw.rect(screen, self.color, (self.x + 5, self.y, self.width - 10, 30))
        pygame.draw.rect(screen, self.color, (self.x, self.y + 10, self.width, 20))

        pygame.draw.rect(screen, self.color, (self.x + 15, self.y + 30, 5, 15))
        pygame.draw.rect(screen, self.color, (self.x + 25, self.y + 30, 5, 15))

        pygame.draw.rect(screen, BLACK, (self.x + 10, self.y + 5, 8, 3))
        pygame.draw.rect(screen, BLACK, (self.x + 25, self.y + 5, 8, 3))

        pygame.draw.rect(screen, BLACK, (self.x + 12, self.y + 20, 18, 5))

    def move(self):
        self.x += self.speed * self.direction

    def change_direction(self):
        self.direction *= -1
        self.y += ENEMY_DROP

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)