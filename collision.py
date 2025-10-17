import math
from settings import (
    COLLISION_THRESHOLD_BULLET, COLLISION_THRESHOLD_SHIP, 
    COLLISION_THRESHOLD_PLAYER_BULLET, DODGE_DISTANCE_MIN, DODGE_DISTANCE_MAX
)

def is_collision(x1, y1, x2, y2, threshold=COLLISION_THRESHOLD_BULLET):
    """Check if two objects are colliding based on distance"""
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < threshold

def check_bullet_enemy_collision(bullet, enemy, current_time):
    """Check collision between bullet and enemy"""
    if not bullet or not bullet.is_active() or not enemy.is_visible():
        return False
        
    bullet_x, bullet_y = bullet.get_position()
    enemy_x, enemy_y = enemy.get_position(current_time)
    
    return is_collision(bullet_x, bullet_y, enemy_x, enemy_y, COLLISION_THRESHOLD_BULLET)

def check_bullet_player_collision(bullet, player):
    """Check collision between enemy bullet and player"""
    if not bullet or not bullet.is_active():
        return False
        
    bullet_x, bullet_y = bullet.get_position()
    player_x, player_y = player.get_position()
    
    return is_collision(bullet_x, bullet_y, player_x, player_y, COLLISION_THRESHOLD_PLAYER_BULLET)

def check_enemy_player_collision(enemy, player, current_time):
    """Check collision between enemy and player"""
    if not enemy.is_visible():
        return False
        
    enemy_x, enemy_y = enemy.get_position(current_time)
    player_x, player_y = player.get_position()
    
    return is_collision(enemy_x, enemy_y, player_x, player_y, COLLISION_THRESHOLD_SHIP)

def check_enemy_enemy_collision(enemy1, enemy2, current_time):
    """Check collision between two enemies"""
    if not enemy1.is_visible() or not enemy2.is_visible():
        return False
        
    enemy1_x, enemy1_y = enemy1.get_position(current_time)
    enemy2_x, enemy2_y = enemy2.get_position(current_time)
    
    return is_collision(enemy1_x, enemy1_y, enemy2_x, enemy2_y, COLLISION_THRESHOLD_SHIP)

def check_dodge_bonus(bullet, player):
    """Check if player deserves a dodge bonus for near-miss"""
    if not bullet or not bullet.is_active():
        return False, 0
        
    bullet_x, bullet_y = bullet.get_position()
    player_x, player_y = player.get_position()
    
    distance = math.sqrt((bullet_x - player_x)**2 + (bullet_y - player_y)**2)
    
    if DODGE_DISTANCE_MIN < distance < DODGE_DISTANCE_MAX:
        return True, distance
    
    return False, distance