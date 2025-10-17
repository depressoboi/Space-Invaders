import pygame
from settings import BULLET_SPEED, SCREEN_HEIGHT

class Bullet:
    def __init__(self, x, y, direction=1, speed=None):
        """
        Initialize bullet
        direction: 1 for up (player bullet), -1 for down (enemy bullet)
        """
        self.x = x
        self.y = y
        self.direction = direction  # 1 = up, -1 = down
        self.speed = speed if speed else BULLET_SPEED
        self.active = True
        
    def update(self, delta_time):
        """Update bullet position"""
        if self.active:
            # Normalize delta_time to 60 FPS (delta_time is in milliseconds)
            normalized_delta = delta_time / 16.67  # 16.67ms = 1/60th second
            self.y -= self.direction * self.speed * normalized_delta
            
            # Remove bullet if it goes off screen
            if self.y <= 0 or self.y >= SCREEN_HEIGHT:
                self.active = False
                
    def draw(self, screen, assets):
        """Draw bullet on screen"""
        if self.active:
            if self.direction == 1:  # Player bullet
                screen.blit(assets.get_bullet_img(), (self.x + 15, self.y + 10))
            else:  # Enemy bullet
                screen.blit(assets.get_bullet_img(), (self.x + 22, self.y + 40))
                
    def get_position(self):
        """Get bullet position"""
        return self.x, self.y
        
    def is_active(self):
        """Check if bullet is still active"""
        return self.active
        
    def deactivate(self):
        """Deactivate the bullet"""
        self.active = False

class BulletManager:
    def __init__(self):
        self.player_bullets = []  # Changed to support multiple bullets
        self.enemy_bullets = []
        self.max_player_bullets = 5  # Limit for performance
        
    def fire_player_bullet(self, x, y):
        """Fire a player bullet"""
        if len(self.player_bullets) < self.max_player_bullets:
            bullet = Bullet(x, y, direction=1)
            self.player_bullets.append(bullet)
            return True
        return False
        
    def fire_enemy_bullet(self, x, y, speed=None):
        """Fire an enemy bullet"""
        bullet = Bullet(x, y, direction=-1, speed=speed)
        self.enemy_bullets.append(bullet)
        
    def update(self, delta_time):
        """Update all bullets"""
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet.update(delta_time)
            if not bullet.is_active():
                self.player_bullets.remove(bullet)
            
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:  # Use slice to avoid modification during iteration
            bullet.update(delta_time)
            if not bullet.is_active():
                self.enemy_bullets.remove(bullet)
                
    def draw(self, screen, assets):
        """Draw all bullets"""
        # Draw player bullets
        for bullet in self.player_bullets:
            if bullet.is_active():
                bullet.draw(screen, assets)
            
        # Draw enemy bullets
        for bullet in self.enemy_bullets:
            bullet.draw(screen, assets)
            
    def get_player_bullets(self):
        """Get all active player bullets"""
        return [bullet for bullet in self.player_bullets if bullet.is_active()]
        
    def get_enemy_bullets(self):
        """Get all active enemy bullets"""
        return [bullet for bullet in self.enemy_bullets if bullet.is_active()]
        
    def clear_all(self):
        """Clear all bullets"""
        self.player_bullets.clear()
        self.enemy_bullets.clear()