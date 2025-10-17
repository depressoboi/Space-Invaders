import pygame
from settings import PLAYER_SIZE, ENEMY_SIZE, BULLET_SIZE

class Assets:
    def __init__(self):
        self.background = None
        self.player_img = None
        self.enemy_img = None
        self.bullet_img = None
        self.icon = None
        self.font_hud = None
        self.font_game_over = None
        self.font_small = None
        
    def load_all(self):
        """Load all game assets"""
        # Load images
        self.background = pygame.image.load("bg.jpg")
        
        # Load and scale player image
        self.player_img = pygame.image.load('ufo.png')
        self.player_img = pygame.transform.scale(self.player_img, PLAYER_SIZE)
        
        # Load and scale enemy image
        self.enemy_img = pygame.image.load('aircraft.png')
        self.enemy_img = pygame.transform.scale(self.enemy_img, ENEMY_SIZE)
        
        # Load and scale bullet image
        self.bullet_img = pygame.image.load('bullet.png')
        self.bullet_img = pygame.transform.scale(self.bullet_img, BULLET_SIZE)
        
        # Load icon
        self.icon = pygame.image.load("spaceship.png")
        
        # Load fonts
        self.font_hud = pygame.font.Font(None, 24)
        self.font_game_over = pygame.font.Font(None, 64)
        self.font_small = pygame.font.Font(None, 36)
        
    def get_background(self):
        return self.background
        
    def get_player_img(self):
        return self.player_img
        
    def get_enemy_img(self):
        return self.enemy_img
        
    def get_bullet_img(self):
        return self.bullet_img
        
    def get_icon(self):
        return self.icon