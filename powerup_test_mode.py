import pygame
from powerup_system import PowerUpType, PowerUp
from settings import COLOR_WHITE, COLOR_YELLOW, COLOR_RED, COLOR_GRAY, SCREEN_HEIGHT, SCREEN_WIDTH

class PowerUpTestMode:
    def __init__(self, powerup_manager, assets):
        self.powerup_manager = powerup_manager
        self.assets = assets
        self.active = False
        self.selected_powerup = 0
        self.powerup_list = list(PowerUpType)
        self.spawn_position = (400, 100)  # Center top of screen
        
        # Create font for test UI
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
    def toggle(self):
        """Toggle test mode on/off"""
        self.active = not self.active
        
    def handle_input(self, event):
        """Handle test mode input"""
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_powerup = (self.selected_powerup - 1) % len(self.powerup_list)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_powerup = (self.selected_powerup + 1) % len(self.powerup_list)
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Spawn selected power-up
                self.spawn_powerup(self.powerup_list[self.selected_powerup])
                return True
            elif event.key == pygame.K_c:
                # Clear all power-ups
                self.powerup_manager.clear_all()
                return True
            elif event.key == pygame.K_a:
                # Spawn all power-ups
                self.spawn_all_powerups()
                return True
            elif event.key == pygame.K_r:
                # Give random power-up
                import random
                random_type = random.choice(self.powerup_list)
                self.spawn_powerup(random_type)
                return True
                
        return False
        
    def spawn_powerup(self, powerup_type):
        """Spawn a specific power-up at test position"""
        powerup = PowerUp(self.spawn_position[0], self.spawn_position[1], powerup_type)
        self.powerup_manager.powerups.append(powerup)
        
    def spawn_all_powerups(self):
        """Spawn all power-up types in a grid"""
        self.powerup_manager.powerups.clear()  # Clear existing first
        
        cols = 4
        start_x = 200
        start_y = 100
        spacing_x = 100
        spacing_y = 80
        
        for i, powerup_type in enumerate(self.powerup_list):
            col = i % cols
            row = i // cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            
            powerup = PowerUp(x, y, powerup_type)
            self.powerup_manager.powerups.append(powerup)
            
    def draw_ui(self, screen):
        """Draw test mode UI"""
        if not self.active:
            return
            
        # Semi-transparent background
        overlay = pygame.Surface((300, 400))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (10, 10))
        
        # Title
        title = self.font.render("POWER-UP TEST MODE", True, COLOR_YELLOW)
        screen.blit(title, (20, 20))
        
        # Instructions
        instructions = [
            "↑↓ - Select power-up",
            "ENTER/SPACE - Spawn selected",
            "A - Spawn all power-ups",
            "R - Random power-up", 
            "C - Clear all power-ups",
            "T - Toggle test mode"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, COLOR_WHITE)
            screen.blit(text, (20, 50 + i * 20))
            
        # Power-up list
        list_start_y = 170
        screen.blit(self.font.render("Power-ups:", True, COLOR_YELLOW), (20, list_start_y))
        
        for i, powerup_type in enumerate(self.powerup_list):
            y_pos = list_start_y + 30 + i * 18
            
            # Highlight selected
            color = COLOR_YELLOW if i == self.selected_powerup else COLOR_WHITE
            if i == self.selected_powerup:
                pygame.draw.rect(screen, (50, 50, 50), (15, y_pos - 2, 280, 16))
                
            # Power-up name
            name = powerup_type.value.replace('_', ' ').title()
            text = self.small_font.render(f"{i+1:2d}. {name}", True, color)
            screen.blit(text, (20, y_pos))
            
        # Active power-ups count
        active_count = len([p for p in self.powerup_manager.powerups if p.is_active()])
        count_text = self.small_font.render(f"Active: {active_count}", True, COLOR_GRAY)
        screen.blit(count_text, (20, 380))
        
    def draw_help_hint(self, screen):
        """Draw help hint when test mode is off"""
        if self.active:
            return
            
        hint_text = self.small_font.render("Press T for Power-up Test Mode", True, COLOR_GRAY)
        screen.blit(hint_text, (10, SCREEN_HEIGHT - 25))

class PowerUpInfoDisplay:
    def __init__(self, assets):
        self.assets = assets
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        
    def draw_powerup_info(self, screen, powerup_manager):
        """Draw detailed info about power-ups on screen"""
        # Get all power-ups on screen
        powerups_on_screen = [p for p in powerup_manager.powerups if p.is_active()]
        
        if not powerups_on_screen:
            return
            
        # Draw info for each power-up
        for i, powerup in enumerate(powerups_on_screen):
            x, y = powerup.get_position()
            
            # Draw info box above power-up
            info_y = y - 40
            if info_y < 0:
                info_y = y + 30
                
            # Power-up name
            name = powerup.type.value.replace('_', ' ').title()
            name_text = self.small_font.render(name, True, COLOR_WHITE)
            
            # Background for text
            text_rect = name_text.get_rect()
            text_rect.center = (x, info_y)
            text_rect.inflate_ip(10, 4)
            
            pygame.draw.rect(screen, (0, 0, 0), text_rect)
            pygame.draw.rect(screen, COLOR_WHITE, text_rect, 1)
            
            screen.blit(name_text, text_rect)
            
    def draw_effect_descriptions(self, screen):
        """Draw power-up effect descriptions"""
        descriptions = {
            PowerUpType.RAPID_FIRE: "Faster shooting",
            PowerUpType.SHIELD: "Absorbs one hit", 
            PowerUpType.MULTI_SHOT: "3-bullet spread",
            PowerUpType.SPEED_BOOST: "1.5x movement speed",
            PowerUpType.SCREEN_CLEAR: "Destroys all enemies",
            PowerUpType.SCORE_MULTIPLIER: "2x score points",
            PowerUpType.BULLET_TIME: "Slows enemies & bullets 70%"
        }
        
        # Draw legend in corner
        start_x = SCREEN_WIDTH - 250
        start_y = 50
        
        # Background
        bg_rect = pygame.Rect(start_x - 10, start_y - 10, 240, len(descriptions) * 16 + 20)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, COLOR_WHITE, bg_rect, 1)
        
        # Title
        title = self.font.render("Power-up Effects:", True, COLOR_YELLOW)
        screen.blit(title, (start_x, start_y))
        
        # Effects
        for i, (powerup_type, description) in enumerate(descriptions.items()):
            y_pos = start_y + 25 + i * 16
            name = powerup_type.value.replace('_', ' ').title()
            text = self.small_font.render(f"{name}: {description}", True, COLOR_WHITE)
            screen.blit(text, (start_x, y_pos))