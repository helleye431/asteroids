import math
import random
from game_config import *


class GameObject:
    def __init__(self, x, y, image_loader, skin_index=0):
        self.x = x
        self.y = y
        self.image_loader = image_loader
        self.skin_index = skin_index
        self.vx = 0
        self.vy = 0
        self.rotation = 0
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x < -100:
            self.x = SCREEN_WIDTH + 100
        elif self.x > SCREEN_WIDTH + 100:
            self.x = -100
        if self.y < -100:
            self.y = SCREEN_HEIGHT + 100
        elif self.y > SCREEN_HEIGHT + 100:
            self.y = -100

    def collides_with(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < (self.radius + other.radius)


class BackgroundAsteroid:
    """Фоновые астероиды для декорации (без коллизий) - движение влево с постоянной скоростью"""

    def __init__(self, image_loader):
        self.image_loader = image_loader
        self.skin_index = random.randint(0, len(ASTEROID_SKINS) - 1)
        self.reset_position()

    def reset_position(self):
        """Сброс позиции астероида - появляется справа"""
        self.x = SCREEN_WIDTH + random.randint(50, 200)  # Появляется за правой границей
        self.y = random.randint(-50, SCREEN_HEIGHT + 50)  # Случайная высота
        self.radius = random.randint(BACKGROUND_ASTEROID_MIN_SIZE, BACKGROUND_ASTEROID_MAX_SIZE)

        # Постоянная скорость движения влево
        self.vx = -BACKGROUND_ASTEROID_SPEED
        self.vy = 0  # Нет вертикального движения

        # Медленное вращение для красоты
        self.rotation_speed = random.uniform(-0.5, 0.5)
        self.rotation = random.uniform(0, 360)

    def update(self):
        """Обновление позиции фонового астероида - движение влево"""
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed

        # Если астероид ушел за левую границу - пересоздаем его справа
        if self.x < -100:
            self.reset_position()


class Ship(GameObject):
    def __init__(self, x, y, image_loader, ship_skin_index):
        super().__init__(x, y, image_loader, ship_skin_index)
        self.thrusting = False
        self.invulnerable = 0
        img_size = self.image_loader.get_ship_size(self.skin_index)
        self.radius = min(img_size) // 5

    def rotate(self, direction):
        self.rotation -= direction * SHIP_ROTATION_SPEED

    def thrust(self):
        self.thrusting = True
        angle_rad = math.radians(self.rotation)
        self.vx += math.sin(angle_rad) * SHIP_ACCELERATION
        self.vy += -math.cos(angle_rad) * SHIP_ACCELERATION

        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > SHIP_SPEED:
            self.vx = (self.vx / speed) * SHIP_SPEED
            self.vy = (self.vy / speed) * SHIP_SPEED

    def update(self):
        super().update()

        if not self.thrusting:
            self.vx *= SHIP_FRICTION
            self.vy *= SHIP_FRICTION

        self.thrusting = False

        if self.invulnerable > 0:
            self.invulnerable -= 1

    def shoot(self, laser_skin_index):
        angle_rad = math.radians(self.rotation)
        img_size = self.image_loader.get_ship_size(self.skin_index)
        offset = max(img_size) // 2
        missile_x = self.x + math.sin(angle_rad) * offset
        missile_y = self.y - math.cos(angle_rad) * offset
        return Missile(missile_x, missile_y, self.rotation, self.image_loader, laser_skin_index)

    def respawn(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vx = 0
        self.vy = 0
        self.rotation = 0
        self.invulnerable = 120


class Missile(GameObject):
    def __init__(self, x, y, rotation, image_loader, laser_skin_index):
        super().__init__(x, y, image_loader, laser_skin_index)
        self.rotation = rotation
        self.lifetime = MISSILE_LIFETIME
        img_size = self.image_loader.get_laser_size(self.skin_index)
        self.radius = min(img_size) // 4

        angle_rad = math.radians(rotation)
        self.vx = math.sin(angle_rad) * MISSILE_SPEED
        self.vy = -math.cos(angle_rad) * MISSILE_SPEED

    def update(self):
        super().update()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False


class Asteroid(GameObject):
    def __init__(self, x, y, image_loader, asteroid_skin_index):
        super().__init__(x, y, image_loader, asteroid_skin_index)
        img_size = self.image_loader.get_asteroid_size(self.skin_index)
        avg_size = (img_size[0] + img_size[1]) // 2

        # Определяем размер астероида для бонусов
        self.size_type = self.determine_size_type(avg_size)
        self.radius = random.randint(int(avg_size * 0.2), int(avg_size * 0.4))

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.rotation_speed = random.uniform(ASTEROID_MIN_ROTATION, ASTEROID_MAX_ROTATION)

    def determine_size_type(self, size):
        """Определяем тип астероида для системы бонусов"""
        if size > 45:
            return "large"
        elif size > 35:
            return "medium"
        else:
            return "small"

    def get_points(self):
        """Возвращает количество очков за уничтожение астероида"""
        if self.size_type == "small":
            return ASTEROID_POINTS_SMALL
        elif self.size_type == "medium":
            return ASTEROID_POINTS_MEDIUM
        else:
            return ASTEROID_POINTS_LARGE

    def update(self):
        super().update()
        self.rotation += self.rotation_speed


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.duration = EXPLOSION_DURATION
        self.active = True
        self.radius = 5

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.active = False