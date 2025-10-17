import pygame
import random
import math
from enum import Enum
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_WHITE, COLOR_RED

class PowerUpType(Enum):
    RAPID_FIRE = "rapid_fire"
    SHIELD = "shield"
    MULTI_SHOT = "multi_shot"
    SPEED_BOOST = "speed_boost"
    SCREEN_CLEAR = "screen_clear"
    SCORE_MULTIPLIER = "score_multiplier"
    # Advanced power-up
    BULLET_TIME = "bullet_time"

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.active = True
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000  # 8 seconds before despawn
        self.size = 20
        self.pulse_time = 0
        self.float_offset = random.uniform(0, math.pi * 2)
        
        # Visual properties based on type
        self.color, self.shape, self.symbol = self._get_visual_properties()
        
    def _get_visual_properties(self):
        """Get color, shape, and symbol for each power-up type"""
        if self.type == PowerUpType.RAPID_FIRE:
            return (255, 100, 100), "circle", "R"  # Red circle
        elif self.type == PowerUpType.SHIELD:
            return (100, 150, 255), "hexagon", "S"  # Blue hexagon
        elif self.type == PowerUpType.MULTI_SHOT:
            return (255, 255, 100), "triangle", "M"  # Yellow triangle
        elif self.type == PowerUpType.SPEED_BOOST:
            return (100, 255, 100), "diamond", "+"  # Green diamond
        elif self.type == PowerUpType.SCREEN_CLEAR:
            return (255, 150, 0), "star", "!"  # Orange star
        elif self.type == PowerUpType.SCORE_MULTIPLIER:
            return (255, 100, 255), "square", "X"  # Purple square
        # New advanced power-ups
        elif self.type == PowerUpType.BULLET_TIME:
            return (100, 255, 255), "hourglass", "T"  # Cyan hourglass
        else:
            return (255, 255, 255), "circle", "?"
            
    def update(self, delta_time, bg_speed=None):
        """Update power-up animation and lifetime"""
        current_time = pygame.time.get_ticks()
        self.pulse_time += delta_time
        
        # Fall down towards player (same speed as background + a bit extra)
        normalized_delta = delta_time / 16.67
        fall_speed = (bg_speed or 6.0) * 1.2  # Slightly faster than background
        
        # Add floating animation on top of falling
        float_animation = math.sin((current_time * 0.003) + self.float_offset) * 0.3
        
        self.y += (fall_speed + float_animation) * normalized_delta
        
        # Remove if goes off screen
        if self.y > SCREEN_HEIGHT + 50:
            self.active = False
            
        # Check lifetime
        if current_time - self.spawn_time > self.lifetime:
            self.active = False
            
    def draw(self, screen):
        """Draw the power-up with pulsing animation"""
        if not self.active:
            return
            
        # Pulsing effect
        pulse = 1.0 + 0.3 * math.sin(self.pulse_time * 0.01)
        current_size = int(self.size * pulse)
        
        # Blinking effect when about to expire
        current_time = pygame.time.get_ticks()
        time_left = self.lifetime - (current_time - self.spawn_time)
        if time_left < 2000:  # Last 2 seconds
            blink_rate = max(0.1, time_left / 2000)  # Faster blinking as time runs out
            if math.sin(current_time * 0.01) > blink_rate:
                return  # Skip drawing (blink effect)
                
        # Draw shape based on type
        center = (int(self.x), int(self.y))
        
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color, center, current_size)
            pygame.draw.circle(screen, COLOR_WHITE, center, current_size, 2)
            
        elif self.shape == "hexagon":
            points = self._get_hexagon_points(center, current_size)
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, COLOR_WHITE, points, 2)
            
        elif self.shape == "triangle":
            points = self._get_triangle_points(center, current_size)
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, COLOR_WHITE, points, 2)
            
        elif self.shape == "diamond":
            points = self._get_diamond_points(center, current_size)
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, COLOR_WHITE, points, 2)
            
        elif self.shape == "star":
            points = self._get_star_points(center, current_size)
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, COLOR_WHITE, points, 2)
            
        elif self.shape == "square":
            rect = pygame.Rect(center[0] - current_size, center[1] - current_size, 
                             current_size * 2, current_size * 2)
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, COLOR_WHITE, rect, 2)
            
        elif self.shape == "hourglass":
            points = self._get_hourglass_points(center, current_size)
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, COLOR_WHITE, points, 2)
            
        # Draw symbol
        font = pygame.font.Font(None, max(16, current_size))
        text = font.render(self.symbol, True, COLOR_WHITE)
        text_rect = text.get_rect(center=center)
        screen.blit(text, text_rect)
        
    def _get_hexagon_points(self, center, size):
        """Generate hexagon points"""
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            points.append((x, y))
        return points
        
    def _get_triangle_points(self, center, size):
        """Generate triangle points"""
        return [
            (center[0], center[1] - size),
            (center[0] - size * 0.866, center[1] + size * 0.5),
            (center[0] + size * 0.866, center[1] + size * 0.5)
        ]
        
    def _get_diamond_points(self, center, size):
        """Generate diamond points"""
        return [
            (center[0], center[1] - size),
            (center[0] + size, center[1]),
            (center[0], center[1] + size),
            (center[0] - size, center[1])
        ]
        
    def _get_star_points(self, center, size):
        """Generate star points"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            radius = size if i % 2 == 0 else size * 0.5
            x = center[0] + radius * math.cos(angle - math.pi / 2)
            y = center[1] + radius * math.sin(angle - math.pi / 2)
            points.append((x, y))
        return points
        
    def _get_hourglass_points(self, center, size):
        """Generate hourglass points"""
        return [
            (center[0] - size, center[1] - size),      # Top left
            (center[0] + size, center[1] - size),      # Top right
            (center[0] + size * 0.3, center[1]),      # Middle right
            (center[0] + size, center[1] + size),      # Bottom right
            (center[0] - size, center[1] + size),      # Bottom left
            (center[0] - size * 0.3, center[1])       # Middle left
        ]
        


        
    def get_position(self):
        """Get power-up position"""
        return self.x, self.y
        
    def is_active(self):
        """Check if power-up is still active"""
        return self.active
        
    def collect(self):
        """Mark power-up as collected"""
        self.active = False

class ActivePowerUp:
    def __init__(self, powerup_type, duration):
        self.type = powerup_type
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.active = True
        
    def update(self):
        """Update active power-up"""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.active = False
            
    def get_time_left(self):
        """Get remaining time in milliseconds"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        return max(0, self.duration - elapsed)
        
    def is_active(self):
        """Check if power-up is still active"""
        return self.active

class PowerUpManager:
    def __init__(self):
        self.powerups = []
        self.active_powerups = []
        self.last_spawn_time = 0
        self.spawn_interval = 15000  # 15 seconds between spawns
        self.spawn_chance = 0.25  # 25% chance per enemy kill
        
        # Power-up durations (in milliseconds)
        self.durations = {
            PowerUpType.RAPID_FIRE: 8000,      # 8 seconds
            PowerUpType.SHIELD: 12000,         # 12 seconds
            PowerUpType.MULTI_SHOT: 10000,     # 10 seconds
            PowerUpType.SPEED_BOOST: 6000,     # 6 seconds
            PowerUpType.SCREEN_CLEAR: 0,       # Instant
            PowerUpType.SCORE_MULTIPLIER: 15000, # 15 seconds
            # Advanced power-up
            PowerUpType.BULLET_TIME: 5000      # 5 seconds
        }
        
    def try_spawn_powerup(self, enemy_x, enemy_y):
        """Try to spawn a power-up at enemy death location"""
        current_time = pygame.time.get_ticks()
        
        # Check spawn conditions
        if (random.random() < self.spawn_chance and 
            current_time - self.last_spawn_time > 3000):  # Min 3 seconds between spawns
            
            # Select power-up type based on rarity
            powerup_type = self._select_powerup_type()
            
            # Create power-up slightly above enemy position
            powerup = PowerUp(enemy_x, enemy_y - 20, powerup_type)
            self.powerups.append(powerup)
            self.last_spawn_time = current_time
            
            return True
        return False
        
    def _select_powerup_type(self):
        """Select power-up type with weighted probabilities"""
        weights = {
            # Basic power-ups
            PowerUpType.RAPID_FIRE: 20,      # Common
            PowerUpType.SPEED_BOOST: 20,     # Common
            PowerUpType.MULTI_SHOT: 15,      # Uncommon
            PowerUpType.SHIELD: 12,          # Uncommon
            PowerUpType.SCORE_MULTIPLIER: 8, # Rare
            PowerUpType.SCREEN_CLEAR: 3,     # Very rare
            # Advanced power-up
            PowerUpType.BULLET_TIME: 6       # Rare
        }
        
        total_weight = sum(weights.values())
        rand = random.randint(1, total_weight)
        
        current_weight = 0
        for powerup_type, weight in weights.items():
            current_weight += weight
            if rand <= current_weight:
                return powerup_type
                
        return PowerUpType.RAPID_FIRE  # Fallback
        
    def update(self, delta_time, bg_speed=None):
        """Update all power-ups"""
        # Update pickup power-ups
        for powerup in self.powerups[:]:
            powerup.update(delta_time, bg_speed)
            if not powerup.is_active():
                self.powerups.remove(powerup)
                
        # Update active power-ups
        for active_powerup in self.active_powerups[:]:
            active_powerup.update()
            if not active_powerup.is_active():
                self.active_powerups.remove(active_powerup)
                
    def check_collection(self, player_x, player_y, collection_radius=30):
        """Check if player collected any power-ups"""
        collected = []
        
        for powerup in self.powerups[:]:
            powerup_x, powerup_y = powerup.get_position()
            distance = math.sqrt((player_x - powerup_x)**2 + (player_y - powerup_y)**2)
            
            if distance < collection_radius:
                powerup.collect()
                self.powerups.remove(powerup)
                collected.append(powerup.type)
                
                # Activate power-up
                self._activate_powerup(powerup.type)
                
        return collected
        
    def _activate_powerup(self, powerup_type):
        """Activate a collected power-up"""
        duration = self.durations[powerup_type]
        
        # Remove existing power-up of same type (no stacking)
        self.active_powerups = [p for p in self.active_powerups if p.type != powerup_type]
        
        # Add new active power-up
        if duration > 0:  # Not instant
            active_powerup = ActivePowerUp(powerup_type, duration)
            self.active_powerups.append(active_powerup)
            
    def draw(self, screen):
        """Draw all power-ups"""
        for powerup in self.powerups:
            powerup.draw(screen)
            
    def is_active(self, powerup_type):
        """Check if a specific power-up type is currently active"""
        return any(p.type == powerup_type and p.is_active() for p in self.active_powerups)
        
    def get_active_powerups(self):
        """Get list of currently active power-ups with time remaining"""
        return [(p.type, p.get_time_left()) for p in self.active_powerups if p.is_active()]
        
    def clear_all(self):
        """Clear all power-ups"""
        self.powerups.clear()
        self.active_powerups.clear()
        
    def trigger_screen_clear(self):
        """Trigger screen clear effect (returns True if should clear enemies)"""
        # This will be called from the game when screen clear is collected
        return True
        
    def get_time_multiplier(self):
        """Get time multiplier for bullet time effect"""
        return 0.3 if self.is_active(PowerUpType.BULLET_TIME) else 1.0
        
