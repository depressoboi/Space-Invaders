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
bg_speed = 0.3

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player setup
playerImg = pygame.image.load('ufo.png')
playerImg = pygame.transform.scale(playerImg, (55, 55))

# Enemy setup
enemyImg = pygame.image.load('aircraft.png')
enemyImg = pygame.transform.scale(enemyImg, (55, 55))

# Bullet setup
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (25, 25))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    screen.blit(bulletImg, (x + 15, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    return distance < 27


def main():
    global bgY, bgY2
    playerX, playerY = 370, 480

    enemyX = random.randint(0, 745)
    enemyY = random.randint(50, 150)
    enemyX_change = 0.2
    enemyY_change = 40

    bulletX, bulletY = 0, 480
    bulletY_change = 0.5
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
            playerX_change += 0.25
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            playerX_change -= 0.25

        playerX += playerX_change
        playerX = max(0, min(playerX, 745))


        # Background scrolling
        bgY += bg_speed
        bgY2 += bg_speed
        if bgY >= 600:
            bgY = -600
        if bgY2 >= 600:
            bgY2 = -600

        screen.blit(background, (0, bgY))
        screen.blit(background, (0, bgY2))

        playerX += playerX_change
        playerX = max(0, min(playerX, 745))

        enemyX += enemyX_change
        if enemyX <= 0 or enemyX >= 745:
            enemyX_change *= -1
            enemyY += enemyY_change

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if isCollision(enemyX, enemyY, bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"
            enemyX = random.randint(0, 745)
            enemyY = random.randint(50, 150)

        player(playerX, playerY)
        enemy(enemyX, enemyY)

        pygame.display.update()


if __name__ == "__main__":
    main()
