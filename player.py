import pygame
from settings import PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, SCREEN_WIDTH

class Player:
    def __init__(self, assets):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.assets = assets
        
    def update(self, keys, delta_time, speed_multiplier=1.0):
        """Update player position based on input"""
        x_change = 0
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x_change += self.speed * speed_multiplier
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x_change -= self.speed * speed_multiplier
            
        # Apply delta time for frame-rate independent movement
        # Normalize delta_time to 60 FPS (delta_time is in milliseconds)
        normalized_delta = delta_time / 16.67  # 16.67ms = 1/60th second
        self.x += x_change * normalized_delta
        
        # Keep player within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - 55))  # 55 accounts for sprite width
        
    def draw(self, screen):
        """Draw the player on screen"""
        screen.blit(self.assets.get_player_img(), (self.x, self.y))
        
    def get_position(self):
        """Get player position"""
        return self.x, self.y
        
    def reset(self):
        """Reset player to starting position"""
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y