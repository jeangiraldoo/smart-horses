import pygame

pygame.init()
GAME_NAME = "Smart Horses"
GAME_MENU_TITLE_FONT = pygame.font.Font(None, 70)
PANEL_INFO_FONT = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption(GAME_NAME)


COLOURS = {
    "BEIGE": (255, 255, 204),
    "WOOD": (179, 45, 0),
    "RED_WOOD": (255, 64, 0),
    "BLACK": (0, 0, 0),
}


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
SIDEBAR_WIDTH = 350
SCREEN_WIDTH = MATRIX_CELL_SIZE * MATRIX_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = MATRIX_CELL_SIZE * MATRIX_SIZE 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

SCREEN_MIDDLE_X_POS = SCREEN_WIDTH / 2
SCREEN_MIDDLE_Y_POS = SCREEN_HEIGHT / 2









