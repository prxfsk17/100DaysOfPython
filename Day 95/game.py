import sys
import random
import pygame
from player import Player
from enemy import Enemy
from bullet import Bullet

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ENEMY_SPEED = 1

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("impact", 36)
        self.small_font = pygame.font.SysFont("impact", 24)
        self.player = None
        self.bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.game_over = False
        self.level = 1

        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.bullets = []
        self.enemy_bullets = []
        self.game_over = False
        self.level = 1
        self.create_enemies()

    def create_enemies(self):
        self.enemies = []
        rows = 3 + self.level % 7
        cols = 8

        for row in range(rows):
            for col in range(cols):
                x = 100 + col * 70
                y = 50 + row * 50
                enemy = Enemy(x, y)
                enemy.speed = ENEMY_SPEED + self.level * 0.5  # Увеличиваем скорость с уровнем
                self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:

                    bullet = Bullet(
                        self.player.x + self.player.width // 2 - 2,
                        self.player.y
                    )
                    self.bullets.append(bullet)

                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move("left")
        if keys[pygame.K_d]:
            self.player.move("right")

        # uncomment for fun and big score
        # if keys[pygame.K_SPACE] and not self.game_over:
        #     bullet = Bullet(
        #         self.player.x + self.player.width // 2 - 2,
        #         self.player.y
        #     )
        #     self.bullets.append(bullet)

    def update(self):
        if self.game_over:
            return

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)

        change_direction = False
        for enemy in self.enemies:
            enemy.move()

            if enemy.x <= 0 or enemy.x + enemy.width >= SCREEN_WIDTH:
                change_direction = True

            if random.random() < 0.0005 + self.level * 0.0002:
                enemy_bullet = Bullet(
                    enemy.x + enemy.width // 2 - 2,
                    enemy.y + enemy.height,
                    "down"
                )
                self.enemy_bullets.append(enemy_bullet)

        if change_direction:
            for enemy in self.enemies:
                enemy.change_direction()

        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:
                if bullet_rect.colliderect(enemy.get_rect()):
                    self.player.score += enemy.points
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    break

        for bullet in self.enemy_bullets[:]:
            if bullet.get_rect().colliderect(self.player.get_rect()):
                self.player.lives -= 1
                self.enemy_bullets.remove(bullet)
                if self.player.lives <= 0:
                    self.game_over = True

        for enemy in self.enemies:
            if enemy.get_rect().colliderect(self.player.get_rect()):
                self.game_over = True

        for enemy in self.enemies:
            if enemy.y + enemy.height >= SCREEN_HEIGHT - 50:
                self.game_over = True
                break

        if not self.enemies:
            self.level += 1
            self.create_enemies()

    def draw(self):
        self.screen.fill(BLACK)

        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)

        self.player.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        score_text = self.font.render(f"Score: {self.player.score}", False, GREEN)
        lives_text = self.font.render(f"Lives: {self.player.lives}", False, GREEN)
        level_text = self.font.render(f"Level: {self.level}", False, GREEN)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - 60, 10))

        controls_text = self.small_font.render("Control: A/D for move, SPACE for shoot", False, WHITE)
        self.screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", False, RED)
            restart_text = self.font.render("Press R for restart", False, WHITE)

            self.screen.blit(game_over_text,
                             (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text,
                             (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                              SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)