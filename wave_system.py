import random
from enum import Enum

class WaveState(Enum):
    SPAWNING = "spawning"
    ACTIVE = "active"
    COMPLETE = "complete"
    TRANSITION = "transition"

class Formation(Enum):
    LINE = "line"
    V_SHAPE = "v_shape"
    CIRCLE = "circle"
    SCATTERED = "scattered"

class Wave:
    def __init__(self, wave_number):
        self.wave_number = wave_number
        self.enemy_count = self._calculate_enemy_count()
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.formation = self._select_formation()
        self.ai_level = min(5, wave_number // 2)  # AI improves every 2 waves
        self.spawn_delay = 500  # ms between spawns
        self.last_spawn_time = 0
        self.state = WaveState.SPAWNING
        self.formation_positions = self._generate_formation_positions()
        self.current_formation_index = 0
        
    def _calculate_enemy_count(self):
        """Calculate number of enemies for this wave"""
        base_count = 3
        if self.wave_number <= 3:
            return base_count + self.wave_number
        else:
            return base_count + 3 + ((self.wave_number - 3) // 2)  # Slower growth after wave 3
            
    def _select_formation(self):
        """Select formation based on wave number"""
        if self.wave_number == 1:
            return Formation.LINE
        elif self.wave_number == 2:
            return Formation.SCATTERED
        elif self.wave_number % 3 == 0:
            return Formation.V_SHAPE
        elif self.wave_number % 4 == 0:
            return Formation.CIRCLE
        else:
            return random.choice([Formation.LINE, Formation.SCATTERED, Formation.V_SHAPE])
            
    def _generate_formation_positions(self):
        """Generate spawn positions based on formation"""
        positions = []
        
        if self.formation == Formation.LINE:
            # Horizontal line across top
            spacing = 600 // max(1, self.enemy_count - 1) if self.enemy_count > 1 else 0
            start_x = 100
            for i in range(self.enemy_count):
                x = start_x + (i * spacing)
                positions.append((x, -100 - (i * 20)))  # Slight stagger
                
        elif self.formation == Formation.V_SHAPE:
            # V formation
            center_x = 400
            for i in range(self.enemy_count):
                if i % 2 == 0:  # Right side of V
                    x = center_x + (i // 2) * 80
                else:  # Left side of V
                    x = center_x - ((i + 1) // 2) * 80
                y = -100 - (abs(i - self.enemy_count // 2) * 30)
                positions.append((x, y))
                
        elif self.formation == Formation.CIRCLE:
            # Circular formation
            import math
            center_x, center_y = 400, -200
            radius = 150
            for i in range(self.enemy_count):
                angle = (2 * math.pi * i) / self.enemy_count
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                positions.append((x, y))
                
        else:  # SCATTERED
            # Random positions with minimum spacing
            for i in range(self.enemy_count):
                x = random.randint(100, 700)
                y = random.randint(-200, -50)
                positions.append((x, y))
                
        return positions
        
    def should_spawn_next(self, current_time):
        """Check if it's time to spawn the next enemy"""
        if self.state != WaveState.SPAWNING:
            return False
        if self.enemies_spawned >= self.enemy_count:
            return False
        return current_time - self.last_spawn_time > self.spawn_delay
        
    def get_next_spawn_position(self):
        """Get the next enemy spawn position"""
        if self.current_formation_index < len(self.formation_positions):
            pos = self.formation_positions[self.current_formation_index]
            self.current_formation_index += 1
            return pos
        return (random.randint(100, 700), random.randint(-150, -50))
        
    def enemy_spawned(self, current_time):
        """Mark that an enemy was spawned"""
        self.enemies_spawned += 1
        self.last_spawn_time = current_time
        
        if self.enemies_spawned >= self.enemy_count:
            self.state = WaveState.ACTIVE
            
    def enemy_killed(self):
        """Mark that an enemy was killed"""
        self.enemies_killed += 1
        
        if self.enemies_killed >= self.enemy_count:
            self.state = WaveState.COMPLETE
            
    def is_complete(self):
        """Check if wave is complete"""
        return self.state == WaveState.COMPLETE
        
    def get_progress(self):
        """Get wave completion progress (0.0 to 1.0)"""
        if self.enemy_count == 0:
            return 1.0
        return self.enemies_killed / self.enemy_count

class WaveManager:
    def __init__(self):
        self.current_wave = None
        self.wave_number = 0
        self.transition_start_time = 0
        self.transition_duration = 2000  # 2 seconds between waves
        self.in_transition = False
        
    def start_next_wave(self, current_time):
        """Start the next wave"""
        self.wave_number += 1
        self.current_wave = Wave(self.wave_number)
        self.in_transition = False
        
    def update(self, current_time):
        """Update wave state"""
        if self.current_wave is None:
            self.start_next_wave(current_time)
            return
            
        if self.current_wave.is_complete() and not self.in_transition:
            self.in_transition = True
            self.transition_start_time = current_time
            
        if self.in_transition:
            if current_time - self.transition_start_time > self.transition_duration:
                self.start_next_wave(current_time)
                
    def should_spawn_enemy(self, current_time):
        """Check if an enemy should be spawned"""
        if self.current_wave is None or self.in_transition:
            return False
        return self.current_wave.should_spawn_next(current_time)
        
    def spawn_enemy(self, current_time):
        """Handle enemy spawn"""
        if self.current_wave:
            pos = self.current_wave.get_next_spawn_position()
            self.current_wave.enemy_spawned(current_time)
            return pos, self.current_wave.ai_level
        return None, 0
        
    def enemy_killed(self):
        """Notify that an enemy was killed"""
        if self.current_wave:
            self.current_wave.enemy_killed()
            
    def get_wave_info(self):
        """Get current wave information"""
        if self.current_wave is None:
            return {"number": 0, "progress": 0.0, "enemies_left": 0}
            
        enemies_left = self.current_wave.enemy_count - self.current_wave.enemies_killed
        return {
            "number": self.wave_number,
            "progress": self.current_wave.get_progress(),
            "enemies_left": enemies_left,
            "formation": self.current_wave.formation.value,
            "in_transition": self.in_transition
        }