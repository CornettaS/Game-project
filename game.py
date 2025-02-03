import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 20
ENEMY_SPEED = 2
BULLET_SPEED = 7

# Класс игры
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 150)) for _ in range(5)]
        self.bullets = []
        self.game_manager = GameManager()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

            # Проверка завершения игры
            if self.game_manager.game_over:
                self.running = False  # Завершение игры

            # Проверка на победу
            if len(self.enemies) == 0:
                self.game_manager.set_game_win()  
                self.running = False  # Завершение игры

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            self.player.move(PLAYER_SPEED)
        if keys[pygame.K_SPACE]:
            self.bullets.append(self.player.shoot())

    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        for enemy in self.enemies:
            enemy.move()
            if enemy.rect.top > SCREEN_HEIGHT:
                self.game_manager.set_game_over()  

        # Проверка на столкновения
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        pygame.display.flip()

# Класс игрока
class Player:
    def __init__(self):
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Класс врага
class Enemy:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        self.rect.y += ENEMY_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Класс пули
class Bullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Класс менеджера игры
class GameManager:
    def __init__(self):
        self.game_over = False
        self.game_won = False

    def set_game_over(self):  
        self.game_over = True
        print("Game Over!")

    def set_game_win(self):  
        self.game_won = True
        print("Game Win!")

# Запуск игры

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()