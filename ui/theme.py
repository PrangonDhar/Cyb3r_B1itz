import pygame


WIDTH = 1280
HEIGHT = 720

FPS = 60


# ============================================================
# COLORS
# ============================================================

BACKGROUND = (7, 10, 20)

WHITE = (245, 245, 245)

CYAN = (0, 240, 255)
NEON_BLUE = (40, 120, 255)
NEON_PURPLE = (180, 60, 255)

GREEN = (50, 255, 130)
RED = (255, 70, 90)
YELLOW = (255, 220, 70)

OPTION_BACKGROUND = (25, 32, 50)
OPTION_BORDER = (70, 85, 115)

# ============================================================
# START SCREEN
# ============================================================

START_TITLE = "CYBER RAPID FIRE"
START_SUBTITLE = "TEST YOUR CYBER AWARENESS"

START_BUTTON_TEXT = "▶  PRESS ENTER TO START"

START_FOOTER = "10 QUESTIONS  •  4 SECONDS  •  100 POINTS"


# ============================================================
# TYPOGRAPHY
# ============================================================

FONT_TITLE = 82
FONT_SUBTITLE = 30
FONT_BUTTON = 34
FONT_FOOTER = 22


# ============================================================
# NEON SETTINGS
# ============================================================

NEON_BORDER_WIDTH = 3
NEON_GLOW_RADIUS = 18

NEON_BUTTON_WIDTH = 560
NEON_BUTTON_HEIGHT = 100


# ============================================================
# BACKGROUND EFFECTS
# ============================================================

PARTICLE_COUNT = 45
PARTICLE_MIN_SPEED = 0.2
PARTICLE_MAX_SPEED = 0.8

SCANLINE_ALPHA = 20


def get_font(size):
    return pygame.font.Font(None, size)