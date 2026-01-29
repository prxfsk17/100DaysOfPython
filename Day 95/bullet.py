import pygame

YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BULLET_SPEED = 10
SCREEN_HEIGHT = 0

class Bullet:
    def __init__(self, x, y, direction="up", h = 600):
        global SCREEN_HEIGHT
        SCREEN_HEIGHT = h
        self.width = 5
        self.height = 15
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.direction = direction
        self.color = YELLOW if direction == "up" else RED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        else:
            self.y += self.speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.y < 0 or self.y > SCREEN_HEIGHT