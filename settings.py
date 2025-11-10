import pygame
from button import Button

MATRIX_SIZE = 8
MATRIX_CELL_SIZE = 90

IMAGE_DIMENSIONS = 60
IMAGE_SCALE = (IMAGE_DIMENSIONS, IMAGE_DIMENSIONS)

CELLS = {
    # Empty
    0: pygame.transform.scale(pygame.image.load("assets/empty.png"), IMAGE_SCALE),
    # Destroyer
    997: pygame.transform.scale(
        pygame.image.load("assets/destroyed.png"), IMAGE_SCALE
    ),
    # White knight
    999: pygame.transform.scale(
        pygame.image.load("assets/knight/white.png"), IMAGE_SCALE
    ),
    # Black knight
    998: pygame.transform.scale(
        pygame.image.load("assets/knight/black.png"), IMAGE_SCALE
    ),
    -10: pygame.transform.scale(
        pygame.image.load("assets/points/negative/10.png"), IMAGE_SCALE
    ),
    # Cells with points
    -5: pygame.transform.scale(
        pygame.image.load("assets/points/negative/5.png"), IMAGE_SCALE
    ),
    -4: pygame.transform.scale(
        pygame.image.load("assets/points/negative/4.png"), IMAGE_SCALE
    ),
    -3: pygame.transform.scale(
        pygame.image.load("assets/points/negative/3.png"), IMAGE_SCALE
    ),
    -1: pygame.transform.scale(
        pygame.image.load("assets/points/negative/1.png"), IMAGE_SCALE
    ),
    1: pygame.transform.scale(
        pygame.image.load("assets/points/positive/1.png"), IMAGE_SCALE
    ),
    3: pygame.transform.scale(
        pygame.image.load("assets/points/positive/3.png"), IMAGE_SCALE
    ),
    4: pygame.transform.scale(
        pygame.image.load("assets/points/positive/4.png"), IMAGE_SCALE
    ),
    5: pygame.transform.scale(
        pygame.image.load("assets/points/positive/5.png"), IMAGE_SCALE
    ),
    10: pygame.transform.scale(
        pygame.image.load("assets/points/positive/10.png"), IMAGE_SCALE
    ),
}

MATRIX_ELEMENTS = []
MATRIX_ELEMENTS.extend(CELLS.keys())

POSSIBLE_POSITIONS = [(x, y) for x in range(MATRIX_SIZE) for y in range(MATRIX_SIZE)]



GAME_NAME = "Smart Horses"
CURRENT_MENU_TITLE_COLOUR = "RED_WOOD"  # Toggle for animating the title


SCREEN_DIMENSIONS = MATRIX_CELL_SIZE * MATRIX_SIZE
SCREEN_MIDDLE_X_POS = SCREEN_DIMENSIONS / 2

BEGGIN_DEPTH = 2
AMATEUR_DEPTH = 4
EXPERT_DEPTH = 6