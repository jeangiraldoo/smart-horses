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


def get_cell_points(board, pos):
    """Devuelve los puntos de una celda si los hay y limpia la casilla"""
    x, y = pos
    cell_value = board[y][x]
    if isinstance(cell_value, int):  # Es una celda vacia o normal
        return 0
    try:
        points = int(cell_value)
        board[y][x] = 0  # Se limpia la casilla
        return points
    except ValueError:
        return 0


def draw_score_panel(screen, font, scores, screen_width, board_width):
    panel_x = screen_width + 10
    panel_width = board_width - 20
    panel_height = screen.get_height() - 20

    panel_rect = pygame.Rect(panel_x, 10, panel_width, panel_height)
    pygame.draw.rect(screen, (245, 240, 200), panel_rect, border_radius=10)

    title = font.render("PUNTUACION", True, (0, 0, 0))
    screen.blit(title, (panel_x + 40, 30))

    ai_text = font.render(f"Caballo Blanco (IA): {scores['ai']}", True, (0, 0, 128))
    player_text = font.render(
        f"Caballo Negro (Jugador): {scores['player']}", True, (128, 0, 0)
    )

    screen.blit(ai_text, (panel_x + 20, 100))
    screen.blit(player_text, (panel_x + 20, 150))

    pygame.draw.line(
        screen,
        (120, 120, 120),
        (panel_x + 10, 200),
        (panel_x + panel_width - 10, 200),
        2,
    )

    status_text = font.render("Estado: Jugando...", True, (60, 60, 60))
    screen.blit(status_text, (panel_x + 20, 230))
