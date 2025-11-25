import pygame
import random
import math
from game_objects import *


def create_asteroid(image_loader, asteroid_skin_index):
    side = random.randint(0, 3)
    padding = 100

    if side == 0:
        x = random.randint(-padding, SCREEN_WIDTH + padding)
        y = -padding
    elif side == 1:
        x = SCREEN_WIDTH + padding
        y = random.randint(-padding, SCREEN_HEIGHT + padding)
    elif side == 2:
        x = random.randint(-padding, SCREEN_WIDTH + padding)
        y = SCREEN_HEIGHT + padding
    else:
        x = -padding
        y = random.randint(-padding, SCREEN_HEIGHT + padding)

    return Asteroid(x, y, image_loader, asteroid_skin_index)


def create_background_asteroids(image_loader, count):
    """Создание фоновых астероидов"""
    asteroids = []
    for _ in range(count):
        asteroids.append(BackgroundAsteroid(image_loader))
    return asteroids


def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_ship(surface, ship):
    if ship.invulnerable > 0 and ship.invulnerable % 10 < 5:
        return

    image = ship.image_loader.get_ship_image(ship.skin_index)
    if image:
        original_size = ship.image_loader.get_ship_size(ship.skin_index)
        scale_factor = 50 / max(original_size)
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        scaled_image = pygame.transform.scale(image, new_size)
        rotated_image = pygame.transform.rotate(scaled_image, -ship.rotation)
        rect = rotated_image.get_rect(center=(ship.x, ship.y))
        surface.blit(rotated_image, rect)


def draw_asteroid(surface, asteroid):
    image = asteroid.image_loader.get_asteroid_image(asteroid.skin_index)
    if image:
        target_size = asteroid.radius * 2
        original_size = asteroid.image_loader.get_asteroid_size(asteroid.skin_index)
        scale_x = target_size / original_size[0]
        scale_y = target_size / original_size[1]
        scale = min(scale_x, scale_y)
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        scaled_image = pygame.transform.scale(image, new_size)
        rotated_image = pygame.transform.rotate(scaled_image, asteroid.rotation)
        rect = rotated_image.get_rect(center=(asteroid.x, asteroid.y))
        surface.blit(rotated_image, rect)


def draw_background_asteroid(surface, asteroid, image_loader):
    """Отрисовка фонового астероида с прозрачностью"""
    image = image_loader.get_asteroid_image(asteroid.skin_index)
    if image:
        # Создаем поверхность с альфа-каналом
        target_size = asteroid.radius * 2
        original_size = image_loader.get_asteroid_size(asteroid.skin_index)
        scale_x = target_size / original_size[0]
        scale_y = target_size / original_size[1]
        scale = min(scale_x, scale_y)
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))

        # Масштабируем изображение
        scaled_image = pygame.transform.scale(image, new_size)

        # Создаем поверхность с прозрачностью
        transparent_surface = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)

        # Копируем изображение на прозрачную поверхность
        transparent_surface.blit(scaled_image, (0, 0))

        # Устанавливаем прозрачность
        transparent_surface.set_alpha(BACKGROUND_ASTEROID_ALPHA)

        # Поворачиваем и отрисовываем
        rotated_image = pygame.transform.rotate(transparent_surface, asteroid.rotation)
        rect = rotated_image.get_rect(center=(asteroid.x, asteroid.y))
        surface.blit(rotated_image, rect)


def draw_missile(surface, missile):
    image = missile.image_loader.get_laser_image(missile.skin_index)
    if image:
        original_size = missile.image_loader.get_laser_size(missile.skin_index)
        scale_factor = 20 / max(original_size)
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        scaled_image = pygame.transform.scale(image, new_size)
        rotated_image = pygame.transform.rotate(scaled_image, -missile.rotation)
        rect = rotated_image.get_rect(center=(missile.x, missile.y))
        surface.blit(rotated_image, rect)
    else:
        pygame.draw.circle(surface, GREEN, (int(missile.x), int(missile.y)), 4)


def draw_explosion(surface, explosion):
    progress = 1 - (explosion.duration / EXPLOSION_DURATION)
    max_radius = 30
    radius = int(max_radius * (1 - abs(progress - 0.5) * 2))
    explosion_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(explosion_surface, (255, 200, 0, 200), (radius, radius), radius)
    pygame.draw.circle(explosion_surface, (255, 100, 0, 150), (radius, radius), radius // 2)
    surface.blit(explosion_surface, (explosion.x - radius, explosion.y - radius))


def draw_score(surface, score, x, y):
    """Улучшенная отрисовка счета"""
    # Фон для счета
    score_bg = pygame.Surface((120, 40), pygame.SRCALPHA)
    score_bg.fill((0, 0, 0, 128))
    surface.blit(score_bg, (x - 60, y - 5))

    # Текст счета
    draw_text(surface, f"ОЧКИ: {score}", 28, x, y, YELLOW)


def draw_lives(surface, lives, x, y):
    """Улучшенная отрисовка жизней"""
    # Фон для жизней
    lives_bg = pygame.Surface((120, 40), pygame.SRCALPHA)
    lives_bg.fill((0, 0, 0, 128))
    surface.blit(lives_bg, (x - 60, y - 5))

    # Текст жизней
    draw_text(surface, f"ЖИЗНИ: {lives}", 28, x, y, GREEN)