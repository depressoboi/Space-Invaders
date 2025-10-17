# Game Settings and Constants

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Player settings
PLAYER_SPEED = 8.0  # Fine-tuned for responsive but controlled movement
PLAYER_START_X = 370
PLAYER_START_Y = 480
PLAYER_SIZE = (40, 40)

# Bullet settings
BULLET_SPEED = 18.0  # Adjusted for 60 FPS (0.3 * 60)
BULLET_SIZE = (15, 15)

# Enemy settings
ENEMY_SIZE = (45, 45)
ENEMY_SPAWN_MIN_Y = -150
ENEMY_SPAWN_MAX_Y = -50
ENEMY_MIN_SPACING = 100
ENEMY_SHOOT_INTERVAL_MIN = 1500
ENEMY_SHOOT_INTERVAL_MAX = 3000

# AI Enhancement settings
AI_ACCURACY_BASE = 0.3  # Base accuracy (0.0 = random, 1.0 = perfect)
AI_ACCURACY_INCREASE = 0.1  # Accuracy increase per 500 score
AI_PREDICTION_STRENGTH = 0.5  # How much to lead player movement
AI_AGGRESSIVE_DISTANCE = 200  # Distance to become more aggressive
AI_FORMATION_STRENGTH = 0.3  # How much enemies coordinate

# Advanced Movement settings
MOVEMENT_UNPREDICTABILITY = 1.2  # Higher = more chaotic movement
EVASION_REACTION_TIME = 800  # ms before enemies can evade again
FLANKING_DISTANCE_MIN = 100  # Minimum flanking distance
FLANKING_DISTANCE_MAX = 250  # Maximum flanking distance
SWARM_COORDINATION_RANGE = 150  # Distance for enemy coordination

# Background settings
BG_SPEED_INITIAL = 6.0  # Adjusted for 60 FPS (0.1 * 60)
BG_SPEED_MAX = 24.0     # Adjusted for 60 FPS (0.4 * 60)
BG_SPEED_INCREASE_RATE = 100000  # Time factor for speed increase

# Game mechanics
STARTING_LIVES = 5
COLLISION_THRESHOLD_BULLET = 27
COLLISION_THRESHOLD_SHIP = 40
COLLISION_THRESHOLD_PLAYER_BULLET = 30

# Scoring
SCORE_ENEMY_KILL = 100
SCORE_PERFECT_SHOT = 150
SCORE_CHAIN_KILL = 200
SCORE_DODGE_BONUS = 5
PERFECT_SHOT_THRESHOLD = 300

# Enemy spawn thresholds
ENEMY_SPAWN_SCORE_3RD = 300
ENEMY_SPAWN_SCORE_4TH = 700

# Dodge bonus settings
DODGE_DISTANCE_MIN = 50
DODGE_DISTANCE_MAX = 80

# Colors
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (200, 200, 200)
COLOR_BLACK = (0, 0, 0)

# Font sizes
FONT_SIZE_HUD = 24
FONT_SIZE_GAME_OVER = 64
FONT_SIZE_SMALL = 36