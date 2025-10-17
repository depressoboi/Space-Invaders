import pygame
import math

class ComboSystem:
    def __init__(self):
        self.multiplier = 1.0
        self.combo_count = 0
        self.last_kill_time = 0
        self.combo_window = 2500  # 2.5 seconds to maintain combo
        self.max_multiplier = 5.0
        self.multiplier_increment = 0.5
        self.combo_threshold = 2  # Kills needed to start combo
        
        # Visual feedback
        self.combo_display_time = 0
        self.combo_display_duration = 1000  # Show combo for 1 second
        self.combo_flash = False
        
    def add_kill(self, current_time):
        """Add a kill to the combo system"""
        time_since_last = current_time - self.last_kill_time
        
        if time_since_last <= self.combo_window or self.combo_count == 0:
            # Continue or start combo
            self.combo_count += 1
            self.last_kill_time = current_time
            
            # Update multiplier
            if self.combo_count >= self.combo_threshold:
                old_multiplier = self.multiplier
                self.multiplier = min(
                    self.max_multiplier,
                    1.0 + ((self.combo_count - self.combo_threshold + 1) * self.multiplier_increment)
                )
                
                # Flash effect when multiplier increases
                if self.multiplier > old_multiplier:
                    self.combo_flash = True
                    self.combo_display_time = current_time
                    
        else:
            # Combo broken, reset
            self.reset_combo()
            self.combo_count = 1
            self.last_kill_time = current_time
            
    def update(self, current_time):
        """Update combo system"""
        # Check if combo has expired
        if self.combo_count > 0:
            time_since_last = current_time - self.last_kill_time
            if time_since_last > self.combo_window:
                self.reset_combo()
                
        # Update visual effects
        if self.combo_flash and current_time - self.combo_display_time > 200:
            self.combo_flash = False
            
    def reset_combo(self):
        """Reset the combo system"""
        self.multiplier = 1.0
        self.combo_count = 0
        self.combo_flash = False
        
    def get_score_multiplier(self):
        """Get the current score multiplier"""
        return self.multiplier
        
    def get_combo_info(self):
        """Get combo information for display"""
        return {
            "multiplier": self.multiplier,
            "combo_count": self.combo_count,
            "is_active": self.combo_count >= self.combo_threshold,
            "flash": self.combo_flash,
            "time_left": max(0, self.combo_window - (pygame.time.get_ticks() - self.last_kill_time)) if self.combo_count > 0 else 0
        }
        
    def apply_multiplier(self, base_score):
        """Apply multiplier to a score value"""
        return int(base_score * self.multiplier)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_explosion(self, x, y, color=(255, 255, 0), count=8):
        """Add explosion particles at position"""
        import random
        for _ in range(count):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 1.0,
                'decay': random.uniform(0.02, 0.04),
                'color': color,
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)
            
    def add_score_popup(self, x, y, score, multiplier=1.0):
        """Add floating score text"""
        color = (255, 255, 0) if multiplier == 1.0 else (255, 100, 100)
        particle = {
            'x': x,
            'y': y,
            'vx': 0,
            'vy': -1,
            'life': 1.0,
            'decay': 0.015,
            'text': f"+{score}",
            'multiplier_text': f"x{multiplier:.1f}" if multiplier > 1.0 else "",
            'color': color,
            'type': 'score'
        }
        self.particles.append(particle)
        
    def update(self, delta_time):
        """Update all particles"""
        normalized_delta = delta_time / 16.67
        
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * normalized_delta
            particle['y'] += particle['vy'] * normalized_delta
            particle['life'] -= particle['decay'] * normalized_delta
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen, font=None):
        """Draw all particles"""
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            color = (*particle['color'], alpha)
            
            if particle.get('type') == 'score':
                # Draw score text
                if font:
                    text_surface = font.render(particle['text'], True, particle['color'])
                    # Apply alpha
                    text_surface.set_alpha(alpha)
                    screen.blit(text_surface, (particle['x'], particle['y']))
                    
                    # Draw multiplier text if present
                    if particle['multiplier_text']:
                        mult_surface = font.render(particle['multiplier_text'], True, (255, 100, 100))
                        mult_surface.set_alpha(alpha)
                        screen.blit(mult_surface, (particle['x'] + 40, particle['y'] - 15))
            else:
                # Draw explosion particle
                try:
                    pygame.draw.circle(screen, particle['color'], 
                                     (int(particle['x']), int(particle['y'])), 
                                     particle['size'])
                except:
                    pass  # Skip if position is invalid
                    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()

class ScreenShake:
    def __init__(self):
        self.shake_duration = 0
        self.shake_intensity = 0
        self.shake_x = 0
        self.shake_y = 0
        
    def add_shake(self, duration, intensity):
        """Add screen shake effect"""
        self.shake_duration = max(self.shake_duration, duration)
        self.shake_intensity = max(self.shake_intensity, intensity)
        
    def update(self, delta_time):
        """Update screen shake"""
        if self.shake_duration > 0:
            self.shake_duration -= delta_time
            
            if self.shake_duration > 0:
                import random
                self.shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
                self.shake_y = random.randint(-self.shake_intensity, self.shake_intensity)
            else:
                self.shake_x = 0
                self.shake_y = 0
                self.shake_intensity = 0
                
    def get_offset(self):
        """Get current shake offset"""
        return self.shake_x, self.shake_y
        
    def is_shaking(self):
        """Check if currently shaking"""
        return self.shake_duration > 0