import pygame
import math
from settings import COLOR_YELLOW, COLOR_WHITE, COLOR_RED, COLOR_GRAY, COLOR_BLACK

class HUD:
    def __init__(self, assets):
        self.assets = assets
        self.combo_pulse_time = 0
        
    def draw_score(self, screen, score, x=700, y=10):
        """Draw the score on screen"""
        text = self.assets.font_hud.render(f"Score: {score}", True, COLOR_YELLOW)
        screen.blit(text, (x, y))
        
    def draw_lives(self, screen, lives, x=10, y=10):
        """Draw the lives on screen"""
        text = self.assets.font_hud.render(f"Lives: {lives}", True, COLOR_WHITE)
        screen.blit(text, (x, y))
        
    def draw_paused(self, screen):
        """Draw pause indicator"""
        pause_text = self.assets.font_game_over.render("PAUSED", True, COLOR_WHITE)
        instruction_text = self.assets.font_small.render("Press P to Resume", True, COLOR_GRAY)
        
        # Center the text
        pause_rect = pause_text.get_rect(center=(400, 250))
        instruction_rect = instruction_text.get_rect(center=(400, 320))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))
        
        screen.blit(pause_text, pause_rect)
        screen.blit(instruction_text, instruction_rect)
        
    def draw_wave_info(self, screen, wave_info):
        """Draw wave information"""
        wave_text = self.assets.font_hud.render(f"Wave: {wave_info['number']}", True, COLOR_WHITE)
        screen.blit(wave_text, (10, 40))
        
        if wave_info['in_transition']:
            transition_text = self.assets.font_small.render(f"Wave {wave_info['number']} Complete!", True, COLOR_YELLOW)
            next_wave_text = self.assets.font_hud.render(f"Next Wave: {wave_info['number'] + 1}", True, COLOR_WHITE)
            
            # Properly center the transition text
            transition_rect = transition_text.get_rect(center=(400, 250))
            next_wave_rect = next_wave_text.get_rect(center=(400, 290))
            
            # Draw semi-transparent overlay for better visibility
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(64)  # Lighter than pause overlay
            overlay.fill(COLOR_BLACK)
            screen.blit(overlay, (0, 0))
            
            screen.blit(transition_text, transition_rect)
            screen.blit(next_wave_text, next_wave_rect)
        else:
            enemies_text = self.assets.font_hud.render(f"Enemies: {wave_info['enemies_left']}", True, COLOR_WHITE)
            screen.blit(enemies_text, (10, 65))
            
            # Draw progress bar
            progress = wave_info['progress']
            bar_width = 100
            bar_height = 8
            bar_x, bar_y = 150, 45
            
            # Background bar
            pygame.draw.rect(screen, COLOR_GRAY, (bar_x, bar_y, bar_width, bar_height))
            # Progress bar
            pygame.draw.rect(screen, COLOR_YELLOW, (bar_x, bar_y, int(bar_width * progress), bar_height))
            
    def draw_combo_info(self, screen, combo_info):
        """Draw combo multiplier information"""
        if combo_info['is_active']:
            # Pulsing effect for active combo
            self.combo_pulse_time += 1
            pulse = 1.0 + 0.2 * math.sin(self.combo_pulse_time * 0.2)
            
            # Combo multiplier text
            multiplier_text = f"x{combo_info['multiplier']:.1f}"
            color = (255, 100, 100) if combo_info['flash'] else COLOR_YELLOW
            
            # Scale text based on pulse
            font_size = int(32 * pulse) if combo_info['flash'] else 28
            combo_font = pygame.font.Font(None, font_size)
            
            mult_surface = combo_font.render(multiplier_text, True, color)
            screen.blit(mult_surface, (700, 40))
            
            # Combo count
            combo_text = f"Combo: {combo_info['combo_count']}"
            combo_surface = self.assets.font_hud.render(combo_text, True, COLOR_WHITE)
            screen.blit(combo_surface, (650, 65))
            
            # Time remaining bar
            if combo_info['time_left'] > 0:
                time_progress = combo_info['time_left'] / 2500  # 2.5 second window
                bar_width = 80
                bar_height = 4
                bar_x, bar_y = 670, 85
                
                # Background
                pygame.draw.rect(screen, COLOR_GRAY, (bar_x, bar_y, bar_width, bar_height))
                # Time bar
                color = COLOR_YELLOW if time_progress > 0.3 else COLOR_RED
                pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * time_progress), bar_height))
                
    def draw_game_over(self, screen, score, is_new_high_score=False):
        """Draw game over screen"""
        screen.fill(COLOR_BLACK)
        
        game_over_text = self.assets.font_game_over.render("GAME OVER", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(400, 180))
        screen.blit(game_over_text, game_over_rect)
        
        score_text = self.assets.font_small.render(f"Final Score: {score:,}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(400, 240))
        screen.blit(score_text, score_rect)
        
        # Show high score achievement
        if is_new_high_score:
            high_score_text = self.assets.font_small.render("🏆 NEW HIGH SCORE! 🏆", True, COLOR_YELLOW)
            high_score_rect = high_score_text.get_rect(center=(400, 280))
            screen.blit(high_score_text, high_score_rect)
            
        restart_text = self.assets.font_hud.render("R - Restart    ESC - Menu    Q - Quit", True, COLOR_GRAY)
        restart_rect = restart_text.get_rect(center=(400, 520))
        screen.blit(restart_text, restart_rect)
        
    def draw_active_powerups(self, screen, active_powerups):
        """Draw active power-up indicators"""
        if not active_powerups:
            return
            
        start_y = 100
        for i, (powerup_type, time_left) in enumerate(active_powerups):
            y_pos = start_y + (i * 25)
            
            # Power-up name
            name_map = {
                "rapid_fire": "RAPID FIRE",
                "shield": "SHIELD",
                "multi_shot": "MULTI SHOT", 
                "speed_boost": "SPEED BOOST",
                "score_multiplier": "SCORE x2",
                "bullet_time": "⏰ BULLET TIME"
            }
            
            name = name_map.get(powerup_type.value, powerup_type.value.upper())
            time_seconds = time_left // 1000
            
            # Color based on time remaining
            if time_seconds > 3:
                color = COLOR_WHITE
            elif time_seconds > 1:
                color = COLOR_YELLOW
            else:
                color = COLOR_RED
                
            text = self.assets.font_hud.render(f"{name}: {time_seconds}s", True, color)
            screen.blit(text, (10, y_pos))