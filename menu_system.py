import pygame
import json
import os
import math
from datetime import datetime
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_WHITE, 
    COLOR_RED, COLOR_GRAY, COLOR_BLACK
)

class HighScoreManager:
    def __init__(self):
        self.scores_file = "high_score.json"
        self.high_score_data = self.load_high_score()
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"score": 0, "wave": 0, "date": ""}
        
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.high_score_data, f, indent=2)
        except Exception as e:
            print(f"Could not save high score: {e}")
            
    def check_and_update_high_score(self, score, wave):
        """Check if this is a new high score and update if so"""
        if score > self.high_score_data["score"]:
            self.high_score_data = {
                "score": score,
                "wave": wave,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.save_high_score()
            return True  # New high score!
        return False  # Not a high score
        
    def get_high_score(self):
        """Get the current high score"""
        return self.high_score_data["score"]
        
    def get_high_score_info(self):
        """Get complete high score information"""
        return self.high_score_data
        
    def is_high_score(self, score):
        """Check if score qualifies as a high score"""
        return score > self.high_score_data["score"]

class RetroMenu:
    def __init__(self, assets, high_score_manager):
        self.assets = assets
        self.high_score_manager = high_score_manager
        self.selected_option = 0
        self.options = ["START GAME", "QUIT"]
        self.animation_time = 0
        self.stars = self._generate_stars()
        self.title_glow = 0
        self.show_high_scores = False
        
        # Create retro fonts
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)
        
    def _generate_stars(self):
        """Generate background stars for retro effect"""
        import random
        stars = []
        for _ in range(100):
            star = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(100, 255)
            }
            stars.append(star)
        return stars
        
    def update(self, delta_time):
        """Update menu animations"""
        self.animation_time += delta_time
        self.title_glow = (math.sin(self.animation_time * 0.003) + 1) * 0.5
        
        # Update stars
        normalized_delta = delta_time / 16.67
        for star in self.stars:
            star['y'] += star['speed'] * normalized_delta
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = -5
                import random
                star['x'] = random.randint(0, SCREEN_WIDTH)
                
    def handle_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                return "menu_move"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                return "menu_move"
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:

                    option = self.options[self.selected_option]
                    if option == "START GAME":
                        return "start_game"
                    elif option == "QUIT":
                        return "quit"
            elif event.key == pygame.K_ESCAPE:
                return "quit"
        return None
        
    def draw(self, screen):
        """Draw the menu"""
        # Clear screen
        screen.fill(COLOR_BLACK)
        
        # Draw animated stars
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), 1)
            
        self._draw_main_menu(screen)
            
    def _draw_main_menu(self, screen):
        """Draw the main menu screen"""
        # Title with glow effect
        title_color = (
            int(255 * (0.8 + 0.2 * self.title_glow)),
            int(255 * (0.6 + 0.4 * self.title_glow)),
            int(100 * (0.5 + 0.5 * self.title_glow))
        )
        
        title_text = self.title_font.render("SPACE INVADERS", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.small_font.render("RETRO EDITION", True, COLOR_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(subtitle_text, subtitle_rect)
        
        # High score display
        high_score_info = self.high_score_manager.get_high_score_info()
        if high_score_info["score"] > 0:
            high_score_text = self.small_font.render(f"HIGH SCORE: {high_score_info['score']:,}", True, COLOR_YELLOW)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(high_score_text, high_score_rect)
            
            # Show wave and date info
            wave_text = self.tiny_font.render(f"Wave {high_score_info['wave']} • {high_score_info['date']}", True, COLOR_GRAY)
            wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
            screen.blit(wave_text, wave_rect)
        else:
            # No high score yet
            no_score_text = self.small_font.render("No high score yet - Play to set one!", True, COLOR_GRAY)
            no_score_rect = no_score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(no_score_text, no_score_rect)
            
        # Menu options
        menu_start_y = 280
        for i, option in enumerate(self.options):
            color = COLOR_YELLOW if i == self.selected_option else COLOR_WHITE
            
            # Add selection indicator
            if i == self.selected_option:
                # Pulsing selection
                pulse = 1.0 + 0.1 * math.sin(self.animation_time * 0.01)
                font_size = int(48 * pulse)
                option_font = pygame.font.Font(None, font_size)
                
                # Selection arrows
                arrow_text = self.menu_font.render(">", True, COLOR_YELLOW)
                arrow_rect = arrow_text.get_rect(center=(SCREEN_WIDTH // 2 - 120, menu_start_y + i * 60))
                screen.blit(arrow_text, arrow_rect)
                
                arrow_text2 = self.menu_font.render("<", True, COLOR_YELLOW)
                arrow_rect2 = arrow_text2.get_rect(center=(SCREEN_WIDTH // 2 + 120, menu_start_y + i * 60))
                screen.blit(arrow_text2, arrow_rect2)
            else:
                option_font = self.menu_font
                
            option_text = option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, menu_start_y + i * 60))
            screen.blit(option_text, option_rect)
            
        # Removed navigation instructions - they're too obvious
            
