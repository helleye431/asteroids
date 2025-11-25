import pygame
import os
import random
from game_config import *


class ImageLoader:
    def __init__(self):
        self.images = {}
        self.image_sizes = {}
        self.load_all_images()

    def load_all_images(self):
        """Загрузка всех ассетов из папки assets"""
        # Фоны
        for bg in BACKGROUND_SKINS:
            path = f'assets/Backgrounds/{bg}.png'
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                self.images[bg] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.image_sizes[bg] = (SCREEN_WIDTH, SCREEN_HEIGHT)

        # Корабли
        for ship in SHIP_SKINS:
            path = f'assets/PNG/{ship}.png'
            if os.path.exists(path):
                original_image = pygame.image.load(path).convert_alpha()
                self.images[ship] = original_image
                self.image_sizes[ship] = original_image.get_size()

        # Астероиды
        for asteroid in ASTEROID_SKINS:
            path = f'assets/PNG/Meteors/{asteroid}.png'
            if os.path.exists(path):
                original_image = pygame.image.load(path).convert_alpha()
                self.images[asteroid] = original_image
                self.image_sizes[asteroid] = original_image.get_size()

        # Лазеры
        for laser in LASER_SKINS:
            path = f'assets/PNG/Lasers/{laser}.png'
            if os.path.exists(path):
                original_image = pygame.image.load(path).convert_alpha()
                self.images[laser] = original_image
                self.image_sizes[laser] = original_image.get_size()

        # Создание недостающих изображений
        self.create_missing_images()

    def create_missing_images(self):
        """Обработка заглушек"""
        # Фон если нету
        if not any(bg in self.images for bg in BACKGROUND_SKINS):
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            surf.fill(BLACK)
            for _ in range(100):
                x = random.randint(0, SCREEN_WIDTH - 1)
                y = random.randint(0, SCREEN_HEIGHT - 1)
                size = random.randint(1, 2)
                brightness = random.randint(100, 255)
                pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), size)
            self.images['custom_bg'] = surf
            self.image_sizes['custom_bg'] = (SCREEN_WIDTH, SCREEN_HEIGHT)

        # Корабль если нету
        if not any(ship in self.images for ship in SHIP_SKINS):
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            points = [(32, 8), (12, 52), (52, 52)]
            pygame.draw.polygon(surf, BLUE, points)
            pygame.draw.polygon(surf, WHITE, points, 2)
            self.images['custom_ship'] = surf
            self.image_sizes['custom_ship'] = (64, 64)

        # Астероид если нету
        if not any(asteroid in self.images for asteroid in ASTEROID_SKINS):
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            center = (32, 32)
            pygame.draw.circle(surf, (139, 69, 19), center, 30)
            for i in range(8):
                angle = 6.28 * i / 8
                dist = random.randint(15, 25)
                x = center[0] + int(dist * 0.7 * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x)
                y = center[1] + int(dist * 0.7 * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y)
                size = random.randint(3, 8)
                pygame.draw.circle(surf, (120, 60, 10), (x, y), size)
            self.images['custom_asteroid'] = surf
            self.image_sizes['custom_asteroid'] = (64, 64)

        # Лазер если нету
        if not any(laser in self.images for laser in LASER_SKINS):
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(surf, GREEN, (16, 16), 8)
            pygame.draw.circle(surf, YELLOW, (16, 16), 4)
            self.images['custom_laser'] = surf
            self.image_sizes['custom_laser'] = (32, 32)

    def get_ship_image(self, skin_index):
        key = SHIP_SKINS[skin_index] if skin_index < len(SHIP_SKINS) else SHIP_SKINS[0]
        return self.images.get(key, self.images.get('custom_ship'))

    def get_ship_size(self, skin_index):
        key = SHIP_SKINS[skin_index] if skin_index < len(SHIP_SKINS) else SHIP_SKINS[0]
        return self.image_sizes.get(key, self.image_sizes.get('custom_ship', (50, 50)))

    def get_asteroid_image(self, skin_index):
        key = ASTEROID_SKINS[skin_index] if skin_index < len(ASTEROID_SKINS) else ASTEROID_SKINS[0]
        return self.images.get(key, self.images.get('custom_asteroid'))

    def get_asteroid_size(self, skin_index):
        key = ASTEROID_SKINS[skin_index] if skin_index < len(ASTEROID_SKINS) else ASTEROID_SKINS[0]
        return self.image_sizes.get(key, self.image_sizes.get('custom_asteroid', (64, 64)))

    def get_background(self, skin_index):
        key = BACKGROUND_SKINS[skin_index] if skin_index < len(BACKGROUND_SKINS) else BACKGROUND_SKINS[0]
        return self.images.get(key, self.images.get('custom_bg'))

    def get_laser_image(self, skin_index):
        key = LASER_SKINS[skin_index] if skin_index < len(LASER_SKINS) else LASER_SKINS[0]
        return self.images.get(key, self.images.get('custom_laser'))

    def get_laser_size(self, skin_index):
        key = LASER_SKINS[skin_index] if skin_index < len(LASER_SKINS) else LASER_SKINS[0]
        return self.image_sizes.get(key, self.image_sizes.get('custom_laser', (32, 32)))