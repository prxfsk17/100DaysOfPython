import pygame

GREEN = (0, 255, 0)

PLAYER_SPEED = 8

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

class Player:
    def __init__(self, w = 800, h = 600):
        global SCREEN_HEIGHT, SCREEN_WIDTH
        SCREEN_WIDTH = w
        SCREEN_HEIGHT = h
        self.width = 50
        self.height = 30
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = PLAYER_SPEED
        self.color = GREEN
        self.lives = 3
        self.score = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width // 2, self.y - 15),
            (self.x + self.width // 3, self.y),
            (self.x + 2 * self.width // 3, self.y)
        ])

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)