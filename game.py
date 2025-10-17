import pygame
import math
from game_states import GameState
from assets import Assets
from player import Player
from bullet import BulletManager
from spawner import EnemySpawner
from hud import HUD
from wave_system import WaveManager
from combo_system import ComboSystem, ParticleSystem, ScreenShake
from menu_system import RetroMenu, HighScoreManager
from powerup_system import PowerUpManager, PowerUpType
from powerup_test_mode import PowerUpTestMode, PowerUpInfoDisplay
from collision import (
    check_bullet_enemy_collision, check_bullet_player_collision,
    check_enemy_player_collision, check_enemy_enemy_collision, check_dodge_bonus
)
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, STARTING_LIVES,
    BG_SPEED_INITIAL, BG_SPEED_MAX, BG_SPEED_INCREASE_RATE,
    SCORE_ENEMY_KILL, SCORE_PERFECT_SHOT, SCORE_CHAIN_KILL, SCORE_DODGE_BONUS,
    PERFECT_SHOT_THRESHOLD
)

class Game:
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        
        # Clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Load assets
        self.assets = Assets()
        self.assets.load_all()
        pygame.display.set_icon(self.assets.get_icon())
        
        # Game state
        self.state = GameState.MENU
        
        # Initialize game objects
        self.player = Player(self.assets)
        self.bullet_manager = BulletManager()
        self.enemy_spawner = EnemySpawner()
        self.hud = HUD(self.assets)
        
        # New gameplay systems
        self.wave_manager = WaveManager()
        self.combo_system = ComboSystem()
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()
        
        # Menu and high score systems
        self.high_score_manager = HighScoreManager()
        self.menu = RetroMenu(self.assets, self.high_score_manager)
        
        # Power-up system
        self.powerup_manager = PowerUpManager()
        
        # Test mode
        self.test_mode = PowerUpTestMode(self.powerup_manager, self.assets)
        self.info_display = PowerUpInfoDisplay(self.assets)
        
        # Background
        self.bg_y = 0
        self.bg_y2 = -SCREEN_HEIGHT
        self.bg_speed = BG_SPEED_INITIAL
        
        # Game variables
        self.lives = STARTING_LIVES
        self.score = 0
        self.start_time = 0
        
        # Shooting system
        self.last_shot_time = 0
        self.normal_shot_cooldown = 300  # 300ms between shots normally
        self.rapid_fire_cooldown = 100   # 100ms with rapid fire
        
        # Dodge bonus tracking
        self.dodge_bonuses_given = {}  # Track which bullets have given bonuses
        
    def reset_game(self):
        """Reset game to initial state"""
        self.player.reset()
        self.bullet_manager.clear_all()
        self.enemy_spawner.clear_all()
        
        self.bg_y = 0
        self.bg_y2 = -SCREEN_HEIGHT
        self.bg_speed = BG_SPEED_INITIAL
        
        self.lives = STARTING_LIVES
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.dodge_bonuses_given.clear()
        
        # Reset new systems
        self.wave_manager = WaveManager()
        self.combo_system = ComboSystem()
        self.particle_system.clear()
        self.screen_shake = ScreenShake()
        self.powerup_manager.clear_all()
        
        self.state = GameState.PLAYING
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # Handle menu events
            if self.state == GameState.MENU:
                menu_action = self.menu.handle_input(event)
                if menu_action == "start_game":
                    self.reset_game()
                elif menu_action == "quit":
                    return False
                    
            elif event.type == pygame.KEYDOWN:
                # Test mode input (works in any state)
                if event.key == pygame.K_t:
                    self.test_mode.toggle()
                elif self.test_mode.handle_input(event):
                    pass  # Test mode handled the input
                    
                elif event.key == pygame.K_SPACE and self.state == GameState.PLAYING:
                    self.try_shoot()
                    
                elif event.key == pygame.K_p:
                    # Toggle pause
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        
                elif event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    # Restart game
                    self.reset_game()
                    
                elif event.key == pygame.K_q and self.state == GameState.GAME_OVER:
                    # Quit game
                    return False
                    
                elif event.key == pygame.K_ESCAPE and self.state == GameState.GAME_OVER:
                    # Return to menu from game over
                    self.state = GameState.MENU
                    
        return True
        
    def update_background(self, delta_time):
        """Update scrolling background"""
        # Normalize delta_time to 60 FPS (delta_time is in milliseconds)
        normalized_delta = delta_time / 16.67  # 16.67ms = 1/60th second
        self.bg_y += self.bg_speed * normalized_delta
        self.bg_y2 += self.bg_speed * normalized_delta
        
        if self.bg_y >= SCREEN_HEIGHT:
            self.bg_y = -SCREEN_HEIGHT
        if self.bg_y2 >= SCREEN_HEIGHT:
            self.bg_y2 = -SCREEN_HEIGHT
            
    def handle_wave_spawning(self, current_time):
        """Handle wave-based enemy spawning"""
        # Ensure we have at least one enemy (fallback for test mode issues)
        if len(self.enemy_spawner.get_enemies()) == 0:
            ai_level = min(5, self.score // 500)
            self.enemy_spawner.spawn_enemy(ai_level)
            
        if self.wave_manager.should_spawn_enemy(current_time):
            spawn_info = self.wave_manager.spawn_enemy(current_time)
            if spawn_info[0]:  # If we got valid spawn info
                pos, ai_level = spawn_info
                # Create enemy at specific position
                enemy = self.enemy_spawner.spawn_enemy_at_position(pos[0], pos[1], ai_level)
                
    def handle_game_over(self):
        """Handle game over - check for high score and transition to game over state"""
        # Check if this is a new high score
        current_wave = self.wave_manager.get_wave_info()['number']
        is_new_high_score = self.high_score_manager.check_and_update_high_score(self.score, current_wave)
        
        # Store whether this was a high score for display
        self.is_new_high_score = is_new_high_score
        
        self.state = GameState.GAME_OVER
        
    def try_shoot(self):
        """Try to shoot with cooldown and power-up effects"""
        current_time = pygame.time.get_ticks()
        
        # Determine cooldown based on rapid fire power-up
        cooldown = self.rapid_fire_cooldown if self.powerup_manager.is_active(PowerUpType.RAPID_FIRE) else self.normal_shot_cooldown
        
        if current_time - self.last_shot_time >= cooldown:
            player_x, player_y = self.player.get_position()
            
            # Multi-shot power-up
            if self.powerup_manager.is_active(PowerUpType.MULTI_SHOT):
                # Fire 3 bullets in spread pattern
                self.bullet_manager.fire_player_bullet(player_x - 10, player_y)
                self.bullet_manager.fire_player_bullet(player_x, player_y)
                self.bullet_manager.fire_player_bullet(player_x + 10, player_y)
            else:
                # Normal single bullet
                self.bullet_manager.fire_player_bullet(player_x, player_y)
                
            self.last_shot_time = current_time
            
    def handle_powerup_collection(self):
        """Handle power-up collection by player"""
        player_x, player_y = self.player.get_position()
        collected = self.powerup_manager.check_collection(player_x, player_y)
        
        for powerup_type in collected:
            if powerup_type == PowerUpType.SCREEN_CLEAR:
                # Clear all enemies and give points
                enemies = self.enemy_spawner.get_enemies()
                for enemy in enemies[:]:
                    enemy_x, enemy_y = enemy.get_position(pygame.time.get_ticks())
                    self.particle_system.add_explosion(enemy_x, enemy_y, (255, 150, 0), 15)
                    self.score += 50  # Bonus points per cleared enemy
                    self.enemy_spawner.remove_enemy(enemy)
                self.screen_shake.add_shake(800, 8)
                
    def update_difficulty(self):
        """Update game difficulty based on time elapsed"""
        time_elapsed = pygame.time.get_ticks() - self.start_time
        self.bg_speed = min(BG_SPEED_MAX, BG_SPEED_INITIAL + (time_elapsed / BG_SPEED_INCREASE_RATE))
        
    def handle_collisions(self, current_time, delta_time):
        """Handle all collision detection and responses"""
        enemies = self.enemy_spawner.get_enemies()
        enemy_bullets = self.bullet_manager.get_enemy_bullets()
        
        # Player bullets vs enemies
        player_bullets = self.bullet_manager.get_player_bullets()
        for player_bullet in player_bullets:
            for enemy in enemies[:]:
                if check_bullet_enemy_collision(player_bullet, enemy, current_time):
                    player_bullet.deactivate()
                    
                    # Calculate base score
                    enemy_x, enemy_y = enemy.get_position(current_time)
                    base_score = SCORE_PERFECT_SHOT if enemy_y < PERFECT_SHOT_THRESHOLD else SCORE_ENEMY_KILL
                    
                    # Add to combo system
                    self.combo_system.add_kill(current_time)
                    
                    # Apply combo multiplier
                    final_score = self.combo_system.apply_multiplier(base_score)
                    
                    # Apply score multiplier power-up
                    if self.powerup_manager.is_active(PowerUpType.SCORE_MULTIPLIER):
                        final_score *= 2
                        
                    self.score += final_score
                    
                    # Visual effects
                    self.particle_system.add_explosion(enemy_x, enemy_y)
                    self.particle_system.add_score_popup(enemy_x, enemy_y, final_score, self.combo_system.get_score_multiplier())
                    self.screen_shake.add_shake(200, 3)
                    
                    # Try to spawn power-up
                    self.powerup_manager.try_spawn_powerup(enemy_x, enemy_y)
                    
                    # Notify wave manager
                    self.wave_manager.enemy_killed()
                    
                    # Remove enemy (wave system handles respawning)
                    self.enemy_spawner.remove_enemy(enemy)
                    break
                    
        # Enemy bullets vs player
        for bullet in enemy_bullets[:]:
            if check_bullet_player_collision(bullet, self.player):
                bullet.deactivate()
                
                # Check shield power-up
                if self.powerup_manager.is_active(PowerUpType.SHIELD):
                    # Shield absorbs hit
                    self.powerup_manager.active_powerups = [p for p in self.powerup_manager.active_powerups 
                                                          if p.type != PowerUpType.SHIELD]
                    self.particle_system.add_explosion(self.player.get_position()[0], 
                                                     self.player.get_position()[1], (100, 150, 255), 12)
                    self.screen_shake.add_shake(300, 4)
                else:
                    # Normal damage (unless in test mode)
                    if not self.test_mode.active:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.handle_game_over()
                    else:
                        # In test mode, just show damage effect but don't lose life
                        self.particle_system.add_explosion(self.player.get_position()[0], 
                                                         self.player.get_position()[1], (255, 0, 0), 8)
                        
                # Clear dodge bonus for this bullet
                if id(bullet) in self.dodge_bonuses_given:
                    del self.dodge_bonuses_given[id(bullet)]
                break
            else:
                # Check for dodge bonus
                is_near_miss, distance = check_dodge_bonus(bullet, self.player)
                bullet_id = id(bullet)
                
                if is_near_miss and bullet_id not in self.dodge_bonuses_given:
                    self.score += SCORE_DODGE_BONUS
                    self.dodge_bonuses_given[bullet_id] = True
                elif distance >= 80:  # Reset if bullet moves away
                    if bullet_id in self.dodge_bonuses_given:
                        del self.dodge_bonuses_given[bullet_id]
                        
        # Player vs enemies
        for enemy in enemies[:]:
            if check_enemy_player_collision(enemy, self.player, current_time):
                if not self.test_mode.active:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.handle_game_over()
                else:
                    # Test mode - just show effect
                    self.particle_system.add_explosion(self.player.get_position()[0], 
                                                     self.player.get_position()[1], (255, 0, 0), 8)
                    
                ai_level = min(5, self.score // 500)
                self.enemy_spawner.remove_enemy(enemy)
                self.enemy_spawner.spawn_enemy(ai_level)
                break
                
        # Enemy vs enemy collisions
        for i, enemy1 in enumerate(enemies):
            for j, enemy2 in enumerate(enemies[i+1:], i+1):
                if check_enemy_enemy_collision(enemy1, enemy2, current_time):
                    # Chain kill bonus with combo multiplier
                    self.combo_system.add_kill(current_time)
                    final_score = self.combo_system.apply_multiplier(SCORE_CHAIN_KILL)
                    self.score += final_score
                    
                    # Visual effects for both enemies
                    enemy1_x, enemy1_y = enemy1.get_position(current_time)
                    enemy2_x, enemy2_y = enemy2.get_position(current_time)
                    
                    self.particle_system.add_explosion(enemy1_x, enemy1_y, (255, 100, 100), 12)
                    self.particle_system.add_explosion(enemy2_x, enemy2_y, (255, 100, 100), 12)
                    self.particle_system.add_score_popup((enemy1_x + enemy2_x) // 2, (enemy1_y + enemy2_y) // 2, 
                                                       final_score, self.combo_system.get_score_multiplier())
                    self.screen_shake.add_shake(400, 5)
                    
                    # Notify wave manager (2 kills)
                    self.wave_manager.enemy_killed()
                    self.wave_manager.enemy_killed()
                    
                    # Remove enemies
                    self.enemy_spawner.remove_enemy(enemy1)
                    self.enemy_spawner.remove_enemy(enemy2)
                    break
                    
    def handle_enemy_shooting(self, current_time, delta_time):
        """Handle enhanced enemy shooting logic"""
        enemies = self.enemy_spawner.get_enemies()
        player_x, player_y = self.player.get_position()
        
        for enemy in enemies:
            if enemy.should_shoot(current_time, player_x, player_y):
                enemy_x, enemy_y = enemy.get_position(current_time)
                bullet_speed = self.bg_speed * 1.75
                
                # Calculate smart aim offset
                aim_offset = enemy.calculate_aim_offset(player_x, player_y, bullet_speed)
                
                # Fire bullet with aim offset
                self.bullet_manager.fire_enemy_bullet(enemy_x + aim_offset, enemy_y, bullet_speed)
                enemy.shoot(current_time)
                
    def update(self, delta_time):
        """Update game logic"""
        if self.state == GameState.MENU:
            self.menu.update(delta_time)
            return
        elif self.state != GameState.PLAYING:
            return
            
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        # Apply bullet time effect to enemies and bullets (not player)
        time_multiplier = self.powerup_manager.get_time_multiplier()
        enemy_delta = delta_time * time_multiplier  # Enemies affected by bullet time
        bullet_delta = delta_time * time_multiplier  # Enemy bullets affected by bullet time
        
        # Update game objects with power-up effects
        speed_multiplier = 1.5 if self.powerup_manager.is_active(PowerUpType.SPEED_BOOST) else 1.0
        self.player.update(keys, delta_time, speed_multiplier)  # Player not affected by bullet time
        
        # Bullets and enemies affected by bullet time
        self.bullet_manager.update(bullet_delta)
        self.enemy_spawner.update_enemies(enemy_delta, current_time, 
                                        self.player.get_position()[0], self.bg_speed)
        
        # Update new systems
        self.wave_manager.update(current_time)
        self.combo_system.update(current_time)
        self.particle_system.update(delta_time)  # Particles not affected by bullet time
        self.screen_shake.update(delta_time)  # Screen shake not affected by bullet time
        self.powerup_manager.update(delta_time, self.bg_speed)
        

        
        # Handle wave-based enemy spawning
        self.handle_wave_spawning(current_time)
        
        # Update background and difficulty (affected by bullet time)
        self.update_background(delta_time * time_multiplier)
        self.update_difficulty()
        
        # Handle enemy shooting (affected by bullet time)
        self.handle_enemy_shooting(current_time, enemy_delta)
        
        # Handle collisions
        self.handle_collisions(current_time, bullet_delta)
        
        # Handle power-up collection
        self.handle_powerup_collection()
        
        # Handle continuous shooting for rapid fire (player not affected by bullet time)
        if keys[pygame.K_SPACE]:
            self.try_shoot()
        
    def draw(self):
        """Draw everything on screen"""
        current_time = pygame.time.get_ticks()
        
        if self.state == GameState.MENU:
            self.menu.draw(self.screen)
            
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Apply screen shake offset
            shake_x, shake_y = self.screen_shake.get_offset()
            
            # Draw background (with shake)
            self.screen.blit(self.assets.get_background(), (shake_x, self.bg_y + shake_y))
            self.screen.blit(self.assets.get_background(), (shake_x, self.bg_y2 + shake_y))
            # Draw game objects (with shake)
            temp_player_pos = self.player.get_position()
            self.screen.blit(self.assets.get_player_img(), (temp_player_pos[0] + shake_x, temp_player_pos[1] + shake_y))
            
            # Draw bullets (with shake applied in bullet manager)
            self.bullet_manager.draw(self.screen, self.assets)
            
            # Draw enemies (with shake)
            for enemy in self.enemy_spawner.get_enemies():
                if enemy.is_visible():
                    enemy_x, enemy_y = enemy.get_position(current_time)
                    self.screen.blit(self.assets.get_enemy_img(), (enemy_x + shake_x, enemy_y + shake_y))
                    
            # Draw particles (no shake - they have their own movement)
            self.particle_system.draw(self.screen, self.assets.font_hud)
            
            # Draw HUD (no shake - UI should be stable)
            self.hud.draw_score(self.screen, self.score)
            self.hud.draw_lives(self.screen, self.lives)
            
            # Draw wave info
            wave_info = self.wave_manager.get_wave_info()
            self.hud.draw_wave_info(self.screen, wave_info)
            
            # Draw combo info
            combo_info = self.combo_system.get_combo_info()
            self.hud.draw_combo_info(self.screen, combo_info)
            
            # Draw power-ups
            self.powerup_manager.draw(self.screen)
            
            # Draw active power-up indicators
            active_powerups = self.powerup_manager.get_active_powerups()
            self.hud.draw_active_powerups(self.screen, active_powerups)
            
            # Draw test mode UI and info
            if self.test_mode.active:
                self.info_display.draw_powerup_info(self.screen, self.powerup_manager)
                self.info_display.draw_effect_descriptions(self.screen)
            
            self.test_mode.draw_ui(self.screen)
            self.test_mode.draw_help_hint(self.screen)
            
            # Draw pause overlay if paused
            if self.state == GameState.PAUSED:
                self.hud.draw_paused(self.screen)
                
        elif self.state == GameState.GAME_OVER:
            is_new_high_score = getattr(self, 'is_new_high_score', False)
            self.hud.draw_game_over(self.screen, self.score, is_new_high_score)
            
        pygame.display.update()
        
    def run(self):
        """Main game loop"""
        # Start in menu state (don't call reset_game which sets to PLAYING)
        running = True
        
        while running:
            # Calculate delta time for frame-rate independent movement
            delta_time = self.clock.tick(FPS)
            
            # Handle events
            running = self.handle_events()
            
            # Update game
            self.update(delta_time)
            
            # Draw everything
            self.draw()
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()