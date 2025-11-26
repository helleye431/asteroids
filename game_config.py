SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)

#корабль
SHIP_SPEED = 5
SHIP_ROTATION_SPEED = 4
SHIP_ACCELERATION = 0.15
SHIP_FRICTION = 0.98

#выстрелы
MISSILE_SPEED = 10
MISSILE_LIFETIME = 45

#астероиды
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 3
ASTEROID_MIN_ROTATION = -2
ASTEROID_MAX_ROTATION = 2
ASTEROID_SPAWN_RATE = 90

# Фоновые астероиды - движение влево с постоянной скоростью
BACKGROUND_ASTEROID_COUNT = 12
BACKGROUND_ASTEROID_SPEED = 1.0  # Постоянная скорость движения влево
BACKGROUND_ASTEROID_ALPHA = 60   # Полупрозрачность
BACKGROUND_ASTEROID_MIN_SIZE = 20
BACKGROUND_ASTEROID_MAX_SIZE = 50

#жизни
INITIAL_LIVES = 3
INITIAL_SCORE = 0
EXPLOSION_DURATION = 30

# Бонусы за разные типы астероидов
ASTEROID_POINTS_SMALL = 100
ASTEROID_POINTS_MEDIUM = 50
ASTEROID_POINTS_LARGE = 25

# Настройки скинов
SHIP_SKINS = [
    'playerShip1_blue', 'playerShip1_green', 'playerShip1_orange', 'playerShip1_red',
    'playerShip2_blue', 'playerShip2_green', 'playerShip2_orange', 'playerShip2_red',
    'playerShip3_blue', 'playerShip3_green', 'playerShip3_orange', 'playerShip3_red'
]
ASTEROID_SKINS = [
    'meteorBrown_big1', 'meteorBrown_big2', 'meteorBrown_big3', 'meteorBrown_big4',
    'meteorGrey_big1', 'meteorGrey_big2', 'meteorGrey_big3', 'meteorGrey_big4'
]
BACKGROUND_SKINS = ['black', 'blue', 'darkPurple', 'purple']
LASER_SKINS = ['laserBlue01', 'laserGreen01', 'laserRed01']