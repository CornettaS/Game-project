import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 15
ENEMY_SPEED = 1
BULLET_SPEED = 7

# Класс игры
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Галактическая баталия")
        self.background = pygame.image.load("D:\Project\Game-project/background.png")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 200)) for _ in range(15)]
        self.bullets = []
        self.game_manager = GameManager()
        self.score = 0 
        self.can_shoot = True
        

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
                 # Проверка на количество врагов
              if len(self.enemies) == 0:
            # Спавн случайного количества врагов от 1 до 15
                self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(50, 200)) for _ in range(random.randint(1, 15))]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

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
            

        # Проверка на столкновения и добавления счетчика
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1 
                    break
                
        # Проверка столкновения с игроком и завершение игры 
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_manager.set_game_over()
        
        for i in range(len(self.enemies)):
            for j in range(i + 1, len(self.enemies)):
                if self.enemies[i].rect.colliderect(self.enemies[j].rect):
                    # Удаляем одного из пересекающихся врагов
                    self.enemies.pop(j)
                break  # Выходим из внутреннего цикла, так как список изменился

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (150, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

         # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Отображаем счет в верхнем левом углу


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
        self.image = pygame.image.load('D:\Project\Game-project\enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        self.rect.y += ENEMY_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Класс пули
class Bullet(pygame.sprite.Sprite):
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
