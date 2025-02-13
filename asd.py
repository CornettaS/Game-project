import pygame
import random
from abc import ABC, abstractmethod

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 15
ENEMY_SPEED = 1
BULLET_SPEED = 7

# Абстрактный класс GameObject
class GameObject(ABC):
    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def update(self):
        pass

# Класс игрока
class Player(GameObject):
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

    def update(self):
        pass

# Класс врага
class Enemy(GameObject):
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        self.rect.y += ENEMY_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.move()

# Класс пули
class Bullet(GameObject):
    def __init__(self, x, y):
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def __eq__(self, other):
        return self.rect == other.rect

    def __lt__(self, other):
        return self.rect.y < other.rect.y

    def __add__(self, other):
        return Bullet(self.rect.centerx + other.rect.centerx, self.rect.centery + other.rect.centery)

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

# Основной класс игры
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Галактическая баталия")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 200)) for _ in range(10)]
        self.bullets = []
        self.game_manager = GameManager()
        self.score = 0 
        self.can_shoot = True

    def reset(self):
        """Сброс игры в начальное состояние."""
        self.player = Player()
        self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 200)) for _ in range(10)]
        self.bullets = []
        self.score = 0
        self.game_manager = GameManager()
        self.running = True

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
                # Спавн случайного количества врагов от 1 до 10
                self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 200)) for _ in range(random.randint(1, 10))]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.can_shoot:
                    self.bullets.append(self.player.shoot())
                    self.can_shoot = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.can_shoot = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    self.bullets.append(self.player.shoot())  # Стрельба

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            self.player.move(PLAYER_SPEED)

    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.top > SCREEN_HEIGHT:
                self.game_manager.set_game_over()  

        # Проверка на столкновения и добавление счетчика
        for bullet in self.bullets[:]:  # Используем срез для безопасного удаления
            for enemy in self.enemies[:]:
                try:
                    if bullet.rect.colliderect(enemy.rect):
                        self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score += 1 
                        break
                except Exception as e:
                    print(f"Error during collision detection: {e}")

        # Проверка столкновения с игроком и завершение игры 
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_manager.set_game_over()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))


        pygame.display.flip()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()