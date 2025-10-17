import random
from enemy import Enemy
from settings import ENEMY_MIN_SPACING, ENEMY_SPAWN_SCORE_3RD, ENEMY_SPAWN_SCORE_4TH

class EnemySpawner:
    def __init__(self):
        self.enemies = []
        self.existing_positions = []
        
    def spawn_enemy(self, ai_level=0):
        """Spawn a new enemy with proper spacing and AI level"""
        attempts = 0
        while attempts < 50:
            base_x = random.randint(100, 700)
            too_close = any(abs(base_x - pos) < ENEMY_MIN_SPACING for pos in self.existing_positions)
            if not too_close:
                self.existing_positions.append(base_x)
                enemy = Enemy(base_x, ai_level)
                self.enemies.append(enemy)
                return enemy
            attempts += 1
            
        # Fallback if too many attempts
        fallback_x = random.randint(100, 700)
        self.existing_positions.append(fallback_x)
        enemy = Enemy(fallback_x, ai_level)
        self.enemies.append(enemy)
        return enemy
        
    def update_enemies(self, delta_time, current_time, player_x, bg_speed):
        """Update all enemies"""
        # Get list of all enemies for coordination
        all_enemies = [e for e in self.enemies if e.is_visible()]
        
        # Update existing enemies
        for enemy in self.enemies[:]:  # Use slice to avoid modification during iteration
            enemy.update(delta_time, current_time, player_x, bg_speed, all_enemies)
            if not enemy.is_visible():
                self.remove_enemy(enemy)
                # Calculate AI level based on current game state (can be passed from game)
                ai_level = getattr(self, 'current_ai_level', 0)
                self.spawn_enemy(ai_level)  # Replace destroyed enemy
                
    def remove_enemy(self, enemy):
        """Remove an enemy and update positions list"""
        if enemy in self.enemies:
            # Remove from position tracking
            enemy_x = enemy.base_x
            if enemy_x in self.existing_positions:
                self.existing_positions.remove(enemy_x)
            # Remove from enemies list
            self.enemies.remove(enemy)
            
    def get_enemies(self):
        """Get all active enemies"""
        return [enemy for enemy in self.enemies if enemy.is_visible()]
        
    def check_spawn_conditions(self, score):
        """Check if more enemies should be spawned based on score"""
        active_count = len(self.get_enemies())
        
        if active_count < 3 and score > ENEMY_SPAWN_SCORE_3RD:
            self.spawn_enemy()
        elif active_count < 4 and score > ENEMY_SPAWN_SCORE_4TH:
            self.spawn_enemy()
            
    def initialize_enemies(self, count=1, ai_level=0):
        """Initialize starting enemies"""
        for _ in range(count):
            self.spawn_enemy(ai_level)
            
    def spawn_enemy_at_position(self, x, y, ai_level=0):
        """Spawn enemy at specific position (for wave system)"""
        from enemy import Enemy
        enemy = Enemy(x, ai_level)
        enemy.y = y  # Override the random Y position
        self.enemies.append(enemy)
        self.existing_positions.append(x)
        return enemy
        
    def clear_all(self):
        """Clear all enemies"""
        self.enemies.clear()
        self.existing_positions.clear()