import random
import math
import pygame
from settings import (
    ENEMY_SPAWN_MIN_Y, ENEMY_SPAWN_MAX_Y, ENEMY_MIN_SPACING,
    ENEMY_SHOOT_INTERVAL_MIN, ENEMY_SHOOT_INTERVAL_MAX, SCREEN_HEIGHT
)

class Enemy:
    def __init__(self, base_x, ai_level=0):
        self.base_x = base_x
        self.original_base_x = base_x  # Store original for some patterns
        self.y = random.randint(ENEMY_SPAWN_MIN_Y, ENEMY_SPAWN_MAX_Y)
        self.y_change = 0.0
        self.visible = True
        
        # Enhanced movement system
        self.movement_type = self._select_movement_type(ai_level)
        self.ai_level = ai_level
        self.accuracy = 0.3 + (ai_level * 0.1)
        self.aggression = random.uniform(0.5, 1.0)
        self.last_player_x = 0
        self.player_velocity = 0
        self.shots_fired = 0
        
        # Advanced movement attributes
        self.movement_state = "entering"  # entering, active, retreating, flanking
        self.state_change_time = 0
        self.next_state_change = random.randint(2000, 5000)  # ms
        self.evasion_cooldown = 0
        self.last_evasion = 0
        
        # Dynamic movement parameters
        self.current_speed_x = 0
        self.current_speed_y = 0
        self.target_x = base_x
        self.target_y = self.y
        self.movement_intensity = random.uniform(0.5, 1.5)
        
        # Pattern-specific initialization
        self._init_movement_pattern()
        
        # Shooting
        self.last_shot = 0
        self.shoot_interval = random.randint(ENEMY_SHOOT_INTERVAL_MIN, ENEMY_SHOOT_INTERVAL_MAX)
        
    def _select_movement_type(self, ai_level):
        """Select movement type based on AI level"""
        if ai_level == 0:
            return random.choice(["basic_wave", "simple_zigzag"])
        elif ai_level <= 2:
            return random.choice(["adaptive_wave", "hunting", "evasive"])
        elif ai_level <= 4:
            return random.choice(["flanking", "unpredictable", "aggressive_dive"])
        else:
            return random.choice(["master_evasion", "tactical_positioning", "swarm_coordination"])
            
    def _init_movement_pattern(self):
        """Initialize pattern-specific attributes"""
        if self.movement_type == "basic_wave":
            self.osc_amplitude = random.randint(15, 35)
            self.osc_freq = random.uniform(0.003, 0.006)
            self.osc_offset = random.uniform(0, math.pi * 2)
            
        elif self.movement_type == "adaptive_wave":
            self.osc_amplitude = random.randint(20, 50)
            self.osc_freq = random.uniform(0.002, 0.008)
            self.osc_offset = random.uniform(0, math.pi * 2)
            self.amplitude_change_rate = random.uniform(0.001, 0.003)
            
        elif self.movement_type == "hunting":
            self.hunt_aggression = random.uniform(0.3, 0.8)
            self.hunt_distance = random.randint(150, 300)
            
        elif self.movement_type == "evasive":
            self.evasion_sensitivity = random.uniform(0.5, 1.2)
            self.evasion_speed = random.uniform(2.0, 4.0)
            
        elif self.movement_type == "flanking":
            self.flank_side = random.choice([-1, 1])
            self.flank_distance = random.randint(100, 200)
            self.flank_speed = random.uniform(1.5, 3.0)
            
        elif self.movement_type == "unpredictable":
            self.chaos_factor = random.uniform(0.8, 1.5)
            self.direction_change_timer = 0
            self.current_direction = random.uniform(-1, 1)
            
        elif self.movement_type == "aggressive_dive":
            self.dive_trigger_distance = random.randint(200, 350)
            self.dive_speed = random.uniform(3.0, 5.0)
            self.is_diving = False
            
        elif self.movement_type == "master_evasion":
            self.prediction_accuracy = 0.9
            self.evasion_prediction_time = random.uniform(0.5, 1.0)
            
        elif self.movement_type == "tactical_positioning":
            self.optimal_distance = random.randint(180, 280)
            self.positioning_speed = random.uniform(2.0, 3.5)
            
        elif self.movement_type == "swarm_coordination":
            self.coordination_range = 150
            self.swarm_influence = random.uniform(0.3, 0.7)
        
    def update(self, delta_time, current_time, player_x, bg_speed, other_enemies=None):
        """Update enemy position and behavior with advanced AI"""
        if not self.visible:
            return
            
        normalized_delta = delta_time / 16.67
        
        # Update player tracking
        player_velocity = player_x - self.last_player_x
        self.player_velocity = player_velocity * 0.7 + self.player_velocity * 0.3
        self.last_player_x = player_x
        
        # Base descent speed
        base_descent = bg_speed * random.uniform(1.1, 1.4)
        
        # Advanced movement based on type
        self._update_advanced_movement(current_time, player_x, normalized_delta, other_enemies)
        
        # Apply movement
        self.base_x += self.current_speed_x * normalized_delta
        self.y += (base_descent + self.current_speed_y) * normalized_delta
        
        # Keep within screen bounds (with some tolerance for advanced maneuvers)
        self.base_x = max(-50, min(850, self.base_x))
        
        # Remove enemy if it goes off screen
        if self.y > SCREEN_HEIGHT + 50:
            self.visible = False
            
    def _update_advanced_movement(self, current_time, player_x, delta_time, other_enemies):
        """Handle advanced movement patterns"""
        current_x = self.get_x_position(current_time)
        distance_to_player = abs(current_x - player_x)
        
        if self.movement_type == "basic_wave":
            self._move_basic_wave(current_time)
            
        elif self.movement_type == "adaptive_wave":
            self._move_adaptive_wave(current_time, distance_to_player)
            
        elif self.movement_type == "hunting":
            self._move_hunting(player_x, distance_to_player)
            
        elif self.movement_type == "evasive":
            self._move_evasive(player_x, current_time)
            
        elif self.movement_type == "flanking":
            self._move_flanking(player_x, current_time)
            
        elif self.movement_type == "unpredictable":
            self._move_unpredictable(current_time)
            
        elif self.movement_type == "aggressive_dive":
            self._move_aggressive_dive(player_x, distance_to_player)
            
        elif self.movement_type == "master_evasion":
            self._move_master_evasion(player_x, current_time)
            
        elif self.movement_type == "tactical_positioning":
            self._move_tactical_positioning(player_x, distance_to_player)
            
        elif self.movement_type == "swarm_coordination":
            self._move_swarm_coordination(player_x, other_enemies)
            
    def _move_basic_wave(self, current_time):
        """Basic sine wave movement"""
        offset = self.osc_amplitude * math.sin(self.osc_freq * current_time + self.osc_offset)
        self.current_speed_x = (self.original_base_x + offset - self.base_x) * 0.1
        self.current_speed_y = 0
        
    def _move_adaptive_wave(self, current_time, distance_to_player):
        """Adaptive wave that changes amplitude based on player distance"""
        # Amplitude increases when closer to player
        dynamic_amplitude = self.osc_amplitude * (1 + (300 - distance_to_player) / 300)
        offset = dynamic_amplitude * math.sin(self.osc_freq * current_time + self.osc_offset)
        self.current_speed_x = (self.original_base_x + offset - self.base_x) * 0.15
        self.current_speed_y = 0
        
    def _move_hunting(self, player_x, distance_to_player):
        """Actively hunt the player"""
        if distance_to_player > self.hunt_distance:
            # Move towards player
            direction = 1 if player_x > self.base_x else -1
            self.current_speed_x = direction * self.hunt_aggression * 2.0
        else:
            # Maintain distance
            self.current_speed_x *= 0.8
        self.current_speed_y = 0
        
    def _move_evasive(self, player_x, current_time):
        """Evasive movement that tries to avoid being directly above player"""
        if current_time - self.last_evasion > self.evasion_cooldown:
            if abs(self.base_x - player_x) < 80:  # Too close to player
                # Evade quickly
                direction = 1 if self.base_x > player_x else -1
                self.current_speed_x = direction * self.evasion_speed
                self.last_evasion = current_time
                self.evasion_cooldown = random.randint(1000, 2000)
            else:
                self.current_speed_x *= 0.9
        self.current_speed_y = 0
        
    def _move_flanking(self, player_x, current_time):
        """Flanking movement - try to attack from the side"""
        target_x = player_x + (self.flank_side * self.flank_distance)
        
        if abs(self.base_x - target_x) > 20:
            direction = 1 if target_x > self.base_x else -1
            self.current_speed_x = direction * self.flank_speed
        else:
            self.current_speed_x *= 0.7
        self.current_speed_y = 0
        
    def _move_unpredictable(self, current_time):
        """Chaotic, unpredictable movement"""
        if current_time - self.direction_change_timer > random.randint(500, 1500):
            self.current_direction = random.uniform(-1, 1) * self.chaos_factor
            self.direction_change_timer = current_time
            
        # Add some noise
        noise = random.uniform(-0.5, 0.5) * self.chaos_factor
        self.current_speed_x = (self.current_direction + noise) * 2.0
        self.current_speed_y = random.uniform(-0.5, 0.5)
        
    def _move_aggressive_dive(self, player_x, distance_to_player):
        """Aggressive dive towards player when close"""
        if not self.is_diving and distance_to_player < self.dive_trigger_distance:
            self.is_diving = True
            
        if self.is_diving:
            # Dive towards player
            direction = 1 if player_x > self.base_x else -1
            self.current_speed_x = direction * self.dive_speed
            self.current_speed_y = self.dive_speed * 0.5  # Faster descent
        else:
            # Normal movement
            self.current_speed_x *= 0.95
            self.current_speed_y = 0
            
    def _move_master_evasion(self, player_x, current_time):
        """Master-level evasion with prediction"""
        # Predict where player will be
        predicted_player_x = player_x + (self.player_velocity * self.evasion_prediction_time)
        
        # Avoid predicted position
        if abs(self.base_x - predicted_player_x) < 100:
            direction = 1 if self.base_x > predicted_player_x else -1
            self.current_speed_x = direction * 3.0
        else:
            self.current_speed_x *= 0.85
        self.current_speed_y = 0
        
    def _move_tactical_positioning(self, player_x, distance_to_player):
        """Maintain optimal distance for shooting"""
        if distance_to_player < self.optimal_distance - 30:
            # Too close, move away
            direction = 1 if self.base_x > player_x else -1
            self.current_speed_x = direction * self.positioning_speed
        elif distance_to_player > self.optimal_distance + 30:
            # Too far, move closer
            direction = 1 if player_x > self.base_x else -1
            self.current_speed_x = direction * self.positioning_speed
        else:
            # Good position, minor adjustments
            self.current_speed_x *= 0.9
        self.current_speed_y = 0
        
    def _move_swarm_coordination(self, player_x, other_enemies):
        """Coordinate with other enemies"""
        if other_enemies:
            # Calculate average position of nearby enemies
            nearby_enemies = [e for e in other_enemies if e != self and 
                            abs(e.base_x - self.base_x) < self.coordination_range]
            
            if nearby_enemies:
                avg_x = sum(e.base_x for e in nearby_enemies) / len(nearby_enemies)
                # Move slightly away from swarm center to spread out
                direction = 1 if self.base_x > avg_x else -1
                swarm_force = direction * self.swarm_influence
                
                # Also move towards player
                player_force = (1 if player_x > self.base_x else -1) * (1 - self.swarm_influence)
                
                self.current_speed_x = (swarm_force + player_force) * 1.5
            else:
                # No nearby enemies, move towards player
                direction = 1 if player_x > self.base_x else -1
                self.current_speed_x = direction * 1.0
        else:
            self.current_speed_x *= 0.9
        self.current_speed_y = 0
            
    def get_x_position(self, current_time):
        """Calculate current X position - now uses base_x directly"""
        return self.base_x
        
    def should_shoot(self, current_time, player_x, player_y):
        """Check if enemy should shoot with smart timing"""
        if current_time - self.last_shot < self.shoot_interval:
            return False
            
        # Calculate distance to player
        enemy_x = self.get_x_position(current_time)
        enemy_y = self.y
        distance_to_player = math.sqrt((enemy_x - player_x)**2 + (enemy_y - player_y)**2)
        
        # More aggressive shooting when closer to player
        if distance_to_player < 200:  # AI_AGGRESSIVE_DISTANCE
            shoot_chance = 0.8 * self.aggression
        else:
            shoot_chance = 0.3 * self.aggression
            
        # Higher AI levels shoot more strategically
        if self.ai_level > 2:
            # Don't shoot if player is moving away rapidly
            if abs(self.player_velocity) > 5 and self.player_velocity * (player_x - enemy_x) > 0:
                shoot_chance *= 0.5
                
        return random.random() < shoot_chance
        
    def calculate_aim_offset(self, player_x, player_y, bullet_speed):
        """Calculate where to aim based on player movement prediction"""
        enemy_x = self.get_x_position(pygame.time.get_ticks())
        
        # Update player velocity tracking
        player_velocity = player_x - self.last_player_x
        self.player_velocity = player_velocity * 0.7 + self.player_velocity * 0.3  # Smooth velocity
        self.last_player_x = player_x
        
        # Calculate time for bullet to reach player
        distance_y = player_y - self.y
        if bullet_speed > 0:
            time_to_target = distance_y / bullet_speed
        else:
            time_to_target = 1.0
            
        # Predict where player will be
        predicted_x = player_x + (self.player_velocity * time_to_target * self.accuracy)
        
        # Add some randomness based on AI level (lower level = more random)
        randomness = (5 - self.ai_level) * 20
        aim_x = predicted_x + random.uniform(-randomness, randomness)
        
        # Calculate aim offset
        aim_offset = aim_x - enemy_x
        return max(-50, min(50, aim_offset))  # Limit extreme aiming
        
    def shoot(self, current_time):
        """Mark that enemy has shot"""
        self.last_shot = current_time
        self.shots_fired += 1
        
    def draw(self, screen, assets, current_time):
        """Draw enemy on screen"""
        if self.visible:
            x = self.get_x_position(current_time)
            screen.blit(assets.get_enemy_img(), (x, self.y))
            
    def get_position(self, current_time):
        """Get enemy position"""
        return self.get_x_position(current_time), self.y
        
    def is_visible(self):
        """Check if enemy is visible"""
        return self.visible
        
    def destroy(self):
        """Destroy the enemy"""
        self.visible = False