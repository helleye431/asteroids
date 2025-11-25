import sys
from utils import *
from image_loader import ImageLoader


class AsteroidsGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Астероиды")
        self.clock = pygame.time.Clock()
        self.image_loader = ImageLoader()

        # Статистика игры
        self.high_score = 0
        self.total_asteroids_destroyed = 0

        # ВАЖНО: инициализируем выбранные скины ДО reset_game()
        self.selected_ship = 0
        self.selected_asteroid = 0
        self.selected_background = 0
        self.selected_laser = 0

        # Фоновые астероиды
        self.background_asteroids = []
        self.create_background_asteroids()

        self.reset_game()

    def create_background_asteroids(self):
        """Создание фоновых астероидов"""
        self.background_asteroids = []
        for _ in range(BACKGROUND_ASTEROID_COUNT):
            self.background_asteroids.append(BackgroundAsteroid(self.image_loader))

    def reset_game(self):
        """Сброс состояния игры"""
        self.ship = None
        self.missiles = []
        self.asteroids = []
        self.explosions = []
        self.lives = INITIAL_LIVES
        self.score = 0
        self.game_state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER
        self.asteroid_timer = 0
        self.current_asteroids_destroyed = 0

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "MENU":
                    mouse_pos = pygame.mouse.get_pos()

                    # Кнопка начала игры
                    start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, 420, 150, 40)
                    if start_rect.collidepoint(mouse_pos):
                        self.start_game()

                    # Кнопка статистики
                    stats_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, 470, 150, 40)
                    if stats_rect.collidepoint(mouse_pos):
                        self.game_state = "STATS"

                    # Выбор корабля (центрированно)
                    preview_width = 60 * 4 + 20 * 3  # 4 превью по 60px с отступами 20px
                    start_x = SCREEN_WIDTH // 2 - preview_width // 2
                    for i in range(min(4, len(SHIP_SKINS))):
                        rect = pygame.Rect(start_x + i * 80, 150, 60, 60)
                        if rect.collidepoint(mouse_pos):
                            self.selected_ship = i

                    # Выбор астероида (центрированно)
                    for i in range(min(4, len(ASTEROID_SKINS))):
                        rect = pygame.Rect(start_x + i * 80, 250, 60, 60)
                        if rect.collidepoint(mouse_pos):
                            self.selected_asteroid = i

                    # Выбор фона (центрированно)
                    for i in range(min(4, len(BACKGROUND_SKINS))):
                        rect = pygame.Rect(start_x + i * 80, 350, 60, 30)
                        if rect.collidepoint(mouse_pos):
                            self.selected_background = i

                elif self.game_state == "GAME_OVER":
                    mouse_pos = pygame.mouse.get_pos()
                    restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 80, 150, 40)
                    menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 130, 150, 40)

                    if restart_rect.collidepoint(mouse_pos):
                        self.start_game()
                    elif menu_rect.collidepoint(mouse_pos):
                        self.game_state = "MENU"

                elif self.game_state == "PAUSED":
                    mouse_pos = pygame.mouse.get_pos()
                    resume_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 50, 150, 40)
                    menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 10, 150, 40)

                    if resume_rect.collidepoint(mouse_pos):
                        self.game_state = "PLAYING"
                    elif menu_rect.collidepoint(mouse_pos):
                        self.game_state = "MENU"

                elif self.game_state == "STATS":
                    mouse_pos = pygame.mouse.get_pos()
                    back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 40)
                    if back_rect.collidepoint(mouse_pos):
                        self.game_state = "MENU"

            if event.type == pygame.KEYDOWN:
                if self.game_state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        if self.ship and len(self.missiles) < 5:
                            missile = self.ship.shoot(self.selected_laser)
                            self.missiles.append(missile)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "PAUSED"

                elif self.game_state == "PAUSED":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "PLAYING"

                elif event.key == pygame.K_RETURN and self.game_state in ["MENU", "GAME_OVER"]:
                    self.start_game()

        return True

    def start_game(self):
        """Начало игры"""
        self.reset_game()
        self.game_state = "PLAYING"
        self.ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         self.image_loader, self.selected_ship)
        self.ship.invulnerable = 120

        for _ in range(4):
            asteroid = create_asteroid(self.image_loader, self.selected_asteroid)
            self.asteroids.append(asteroid)

    def update(self):
        """Обновление состояния игры"""
        # Обновляем фоновые астероиды всегда
        for bg_asteroid in self.background_asteroids:
            bg_asteroid.update()

        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if self.ship:
            if keys[pygame.K_LEFT]:
                self.ship.rotate(1)
            if keys[pygame.K_RIGHT]:
                self.ship.rotate(-1)
            if keys[pygame.K_UP]:
                self.ship.thrust()
            self.ship.update()

        for missile in self.missiles[:]:
            missile.update()
            if not missile.active:
                self.missiles.remove(missile)

        for asteroid in self.asteroids:
            asteroid.update()

        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.active:
                self.explosions.remove(explosion)

        self.asteroid_timer += 1
        if self.asteroid_timer >= ASTEROID_SPAWN_RATE and len(self.asteroids) < 8:
            asteroid = create_asteroid(self.image_loader, self.selected_asteroid)
            self.asteroids.append(asteroid)
            self.asteroid_timer = 0

        for missile in self.missiles[:]:
            for asteroid in self.asteroids[:]:
                if missile.collides_with(asteroid):
                    if missile in self.missiles:
                        self.missiles.remove(missile)
                    if asteroid in self.asteroids:
                        # УЛУЧШЕННАЯ СИСТЕМА СЧЕТА
                        points = asteroid.get_points()
                        self.score += points
                        self.current_asteroids_destroyed += 1
                        self.total_asteroids_destroyed += 1

                        # Обновляем рекорд
                        if self.score > self.high_score:
                            self.high_score = self.score

                        self.asteroids.remove(asteroid)
                        self.explosions.append(Explosion(asteroid.x, asteroid.y))
                    break

        if self.ship and self.ship.invulnerable <= 0:
            for asteroid in self.asteroids[:]:
                if self.ship.collides_with(asteroid):
                    self.asteroids.remove(asteroid)
                    self.explosions.append(Explosion(asteroid.x, asteroid.y))
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_state = "GAME_OVER"
                    else:
                        self.ship.respawn()
                    break

    def draw(self):
        """Отрисовка игры"""
        self.screen.blit(self.image_loader.get_background(self.selected_background), (0, 0))

        # Отрисовываем фоновые астероиды всегда
        for bg_asteroid in self.background_asteroids:
            draw_background_asteroid(self.screen, bg_asteroid, self.image_loader)

        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "PLAYING":
            self.draw_game()
        elif self.game_state == "PAUSED":
            self.draw_game()
            self.draw_pause_menu()
        elif self.game_state == "GAME_OVER":
            self.draw_game()
            self.draw_game_over()
        elif self.game_state == "STATS":
            self.draw_stats()

        pygame.display.flip()

    def draw_menu(self):
        """Отрисовка центрированного меню"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Заголовок
        draw_text(self.screen, "АСТЕРОИДЫ", 48, SCREEN_WIDTH // 2, 50)

        # Рекорд
        draw_text(self.screen, f"РЕКОРД: {self.high_score}", 24, SCREEN_WIDTH // 2, 100, YELLOW)

        # Выбор корабля (центрированно)
        draw_text(self.screen, "ВЫБЕРИТЕ КОРАБЛЬ", 28, SCREEN_WIDTH // 2, 130)

        # Расчет позиций для центрирования превью
        preview_width = 60 * 4 + 20 * 3  # 4 превью по 60px с отступами 20px
        start_x = SCREEN_WIDTH // 2 - preview_width // 2

        for i in range(min(4, len(SHIP_SKINS))):
            rect = pygame.Rect(start_x + i * 80, 150, 60, 60)
            color = BLUE if i == self.selected_ship else WHITE
            pygame.draw.rect(self.screen, color, rect, 3)

            image = self.image_loader.get_ship_image(i)
            if image:
                scaled = pygame.transform.scale(image, (50, 50))
                self.screen.blit(scaled, (start_x + i * 80 + 5, 155))

            draw_text(self.screen, str(i + 1), 20, start_x + i * 80 + 30, 215)

        # Выбор астероида (центрированно)
        draw_text(self.screen, "ВЫБЕРИТЕ АСТЕРОИД", 28, SCREEN_WIDTH // 2, 230)

        for i in range(min(4, len(ASTEROID_SKINS))):
            rect = pygame.Rect(start_x + i * 80, 250, 60, 60)
            color = BLUE if i == self.selected_asteroid else WHITE
            pygame.draw.rect(self.screen, color, rect, 3)

            image = self.image_loader.get_asteroid_image(i)
            if image:
                scaled = pygame.transform.scale(image, (50, 50))
                self.screen.blit(scaled, (start_x + i * 80 + 5, 255))

            draw_text(self.screen, str(i + 1), 20, start_x + i * 80 + 30, 315)

        # Выбор фона (центрированно)
        draw_text(self.screen, "ВЫБЕРИТЕ ФОН", 28, SCREEN_WIDTH // 2, 330)

        for i in range(min(4, len(BACKGROUND_SKINS))):
            rect = pygame.Rect(start_x + i * 80, 350, 60, 30)
            color = BLUE if i == self.selected_background else WHITE
            pygame.draw.rect(self.screen, color, rect, 3)
            draw_text(self.screen, str(i + 1), 18, start_x + i * 80 + 30, 355)

        # Кнопка начала игры
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, 420, 150, 40)
        pygame.draw.rect(self.screen, GREEN, start_rect)
        pygame.draw.rect(self.screen, WHITE, start_rect, 2)
        draw_text(self.screen, "НАЧАТЬ ИГРУ", 24, SCREEN_WIDTH // 2, 430)

        # Кнопка статистики
        stats_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, 470, 150, 40)
        pygame.draw.rect(self.screen, ORANGE, stats_rect)
        pygame.draw.rect(self.screen, WHITE, stats_rect, 2)
        draw_text(self.screen, "СТАТИСТИКА", 24, SCREEN_WIDTH // 2, 480)

        # Управление
        draw_text(self.screen, "ESC - пауза/меню", 16, SCREEN_WIDTH // 2, 520)

    def draw_game(self):
        """Отрисовка игрового процесса"""
        # Игровые объекты поверх фоновых астероидов
        for missile in self.missiles:
            draw_missile(self.screen, missile)
        for asteroid in self.asteroids:
            draw_asteroid(self.screen, asteroid)
        for explosion in self.explosions:
            draw_explosion(self.screen, explosion)
        if self.ship:
            draw_ship(self.screen, self.ship)

        # Улучшенный интерфейс во время игры
        if self.game_state == "PLAYING":
            draw_score(self.screen, self.score, SCREEN_WIDTH // 2, 10)
            draw_lives(self.screen, self.lives, 100, 10)

            # Подсказка паузы
            draw_text(self.screen, "ESC - пауза", 16, SCREEN_WIDTH - 60, 10, (200, 200, 200))

    def draw_pause_menu(self):
        """Меню паузы"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "ПАУЗА", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        # Кнопка продолжения
        resume_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 50, 150, 40)
        pygame.draw.rect(self.screen, GREEN, resume_rect)
        pygame.draw.rect(self.screen, WHITE, resume_rect, 2)
        draw_text(self.screen, "ПРОДОЛЖИТЬ", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)

        # Кнопка выхода в меню
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 10, 150, 40)
        pygame.draw.rect(self.screen, BLUE, menu_rect)
        pygame.draw.rect(self.screen, WHITE, menu_rect, 2)
        draw_text(self.screen, "В МЕНЮ", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "ИГРА ОКОНЧЕНА", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text(self.screen, f"Счет: {self.score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        draw_text(self.screen, f"Рекорд: {self.high_score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(self.screen, f"Уничтожено астероидов: {self.current_asteroids_destroyed}", 24, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 + 40)

        # Кнопка новой игры
        restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 80, 150, 40)
        pygame.draw.rect(self.screen, GREEN, restart_rect)
        pygame.draw.rect(self.screen, WHITE, restart_rect, 2)
        draw_text(self.screen, "НОВАЯ ИГРА", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)

        # Кнопка выхода в меню
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 130, 150, 40)
        pygame.draw.rect(self.screen, BLUE, menu_rect)
        pygame.draw.rect(self.screen, WHITE, menu_rect, 2)
        draw_text(self.screen, "В МЕНЮ", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140)

    def draw_stats(self):
        """Экран статистики"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "СТАТИСТИКА", 48, SCREEN_WIDTH // 2, 50)

        # Статистика
        draw_text(self.screen, f"Рекорд: {self.high_score}", 36, SCREEN_WIDTH // 2, 120)
        draw_text(self.screen, f"Всего уничтожено астероидов: {self.total_asteroids_destroyed}", 28, SCREEN_WIDTH // 2,
                  180)
        draw_text(self.screen, f"Доступно кораблей: {len(SHIP_SKINS)}", 24, SCREEN_WIDTH // 2, 230)
        draw_text(self.screen, f"Доступно астероидов: {len(ASTEROID_SKINS)}", 24, SCREEN_WIDTH // 2, 270)

        # Бонусная система
        draw_text(self.screen, "СИСТЕМА БОНУСОВ:", 28, SCREEN_WIDTH // 2, 330, YELLOW)
        draw_text(self.screen, f"Маленькие астероиды: {ASTEROID_POINTS_SMALL} очков", 22, SCREEN_WIDTH // 2, 370)
        draw_text(self.screen, f"Средние астероиды: {ASTEROID_POINTS_MEDIUM} очков", 22, SCREEN_WIDTH // 2, 400)
        draw_text(self.screen, f"Большие астероиды: {ASTEROID_POINTS_LARGE} очков", 22, SCREEN_WIDTH // 2, 430)

        # Кнопка назад
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 40)
        pygame.draw.rect(self.screen, BLUE, back_rect)
        pygame.draw.rect(self.screen, WHITE, back_rect, 2)
        draw_text(self.screen, "НАЗАД", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90)

    def run(self):
        """Главный игровой цикл"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = AsteroidsGame()
    game.run()