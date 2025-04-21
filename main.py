import random
import math
import pygame

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("bg.jpg")
bgY = 0
bgY2 = -600
bg_speed = 0.25

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player setup
playerImg = pygame.image.load('ufo.png')
playerImg = pygame.transform.scale(playerImg, (40, 40))

# Enemy setup
enemyImg = pygame.image.load('aircraft.png')
enemyImg = pygame.transform.scale(enemyImg, (45, 45))

# Bullet setup
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (15, 15))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    screen.blit(bulletImg, (x + 15, y + 10))


def fire_enemy_bullet(x, y):
    screen.blit(bulletImg, (x + 22, y + 40))


def isCollision(x1, y1, x2, y2, threshold=27):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < threshold


def spawn_enemy(existing_positions):
    attempts = 0
    while attempts < 50:
        baseX = random.randint(100, 700)
        too_close = any(abs(baseX - pos) < 100 for pos in existing_positions)
        if not too_close:
            existing_positions.append(baseX)
            return {
                'baseX': baseX,
                'Y': random.randint(-150, -50),
                'Y_change': random.uniform(0.2, 0.4),  # faster descent
                'visible': True,
                'bulletX': None,
                'bulletY': None,
                'bullet_active': False,
                'x_drift': random.uniform(-0.2, 0.2),
                'target_offset': random.randint(-100, 100),
                'osc_amplitude': random.randint(10, 30),  # tighter wave
                'osc_freq': random.uniform(0.002, 0.004),
                'osc_time_offset': random.uniform(0, math.pi * 2)
            }
        attempts += 1

    return {
        'baseX': random.randint(100, 700),
        'Y': random.randint(-150, -50),
        'Y_change': 0.3,
        'visible': True,
        'bulletX': None,
        'bulletY': None,
        'bullet_active': False,
        'x_drift': random.uniform(-0.2, 0.2),
        'target_offset': random.randint(-100, 100),
        'osc_amplitude': random.randint(10, 30),
        'osc_freq': random.uniform(0.002, 0.004),
        'osc_time_offset': random.uniform(0, math.pi * 2)
    }


def main():
    global bgY, bgY2
    playerX, playerY = 370, 480

    existing_positions = []
    enemies = [spawn_enemy(existing_positions) for _ in range(3)]

    bulletX, bulletY = 0, 480
    bulletY_change = 0.3
    bullet_state = "ready"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bullet_state = "fire"

        keys = pygame.key.get_pressed()
        playerX_change = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            playerX_change += 0.2
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            playerX_change -= 0.2

        playerX += playerX_change
        playerX = max(0, min(playerX, 745))

        bgY += bg_speed
        bgY2 += bg_speed
        if bgY >= 600:
            bgY = -600
        if bgY2 >= 600:
            bgY2 = -600

        screen.blit(background, (0, bgY))
        screen.blit(background, (0, bgY2))

        time_now = pygame.time.get_ticks()

        for i, enemy_data in enumerate(enemies):
            if enemy_data['visible']:
                wave = enemy_data['osc_amplitude'] * math.sin(enemy_data['osc_freq'] * time_now + enemy_data['osc_time_offset'])
                enemyX = enemy_data['baseX'] + wave
                enemyY = enemy_data['Y']
                enemy_data['Y'] += enemy_data['Y_change']

                if enemyY > 600:
                    enemies[i] = spawn_enemy([e['baseX'] for e in enemies if e['visible']])
                    continue

                if bullet_state == "fire" and isCollision(enemyX, enemyY, bulletX, bulletY):
                    bulletY = 480
                    bullet_state = "ready"
                    enemies[i] = spawn_enemy([e['baseX'] for e in enemies if e['visible']])
                    continue

                if isCollision(enemyX, enemyY, playerX, playerY, threshold=40):
                    print("Player crashed with enemy!")
                    enemies[i] = spawn_enemy([e['baseX'] for e in enemies if e['visible']])
                    continue

                for j, other in enumerate(enemies):
                    if i != j and other['visible']:
                        otherX = other['baseX'] + other['osc_amplitude'] * math.sin(other['osc_freq'] * time_now + other['osc_time_offset'])
                        otherY = other['Y']
                        if isCollision(enemyX, enemyY, otherX, otherY, threshold=40):
                            print(f"Enemy {i} and Enemy {j} crashed!")
                            enemies[i] = spawn_enemy([e['baseX'] for e in enemies if e['visible']])
                            enemies[j] = spawn_enemy([e['baseX'] for e in enemies if e['visible']])
                            break

                if not enemy_data['bullet_active'] and random.randint(0, 120) == 1:
                    enemy_data['bulletX'] = enemyX
                    enemy_data['bulletY'] = enemyY + 40
                    enemy_data['bullet_active'] = True

                if enemy_data['bullet_active']:
                    enemy_data['bulletY'] += 0.45
                    fire_enemy_bullet(enemy_data['bulletX'], enemy_data['bulletY'])

                    if isCollision(enemy_data['bulletX'], enemy_data['bulletY'], playerX, playerY, threshold=30):
                        print("Player hit by enemy bullet!")
                        enemy_data['bullet_active'] = False

                    if enemy_data['bulletY'] > 600:
                        enemy_data['bullet_active'] = False

                enemy(enemyX, enemyY)

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        player(playerX, playerY)
        pygame.display.update()


if __name__ == "__main__":
    main()