import pygame
import random

MATRIX_SIZE = 8
MATRIX_CELL_SIZE = 90

IMAGE_DIMENSIONS = 60
IMAGE_SCALE = (IMAGE_DIMENSIONS, IMAGE_DIMENSIONS)

CELLS = {
    # Empty
    0: pygame.transform.scale(pygame.image.load("assets/empty.png"), IMAGE_SCALE),
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


def generate_random_matrix():
    chosen_positions = random.sample(POSSIBLE_POSITIONS, len(MATRIX_ELEMENTS))

    board = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

    for i, (x, y) in enumerate(chosen_positions):
        board[x][y] = MATRIX_ELEMENTS[i]

    return board


def draw_map(screen, random_matrix):
    for y, row in enumerate(random_matrix):
        for x, cell in enumerate(row):
            image = CELLS.get(cell)
            screen.blit(
                pygame.transform.scale(image, (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE)),
                (x * MATRIX_CELL_SIZE, y * MATRIX_CELL_SIZE),
            )
