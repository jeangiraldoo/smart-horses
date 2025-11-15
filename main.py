import pygame
import sys
import random
from board import draw_map, generate_random_matrix, MATRIX_CELL_SIZE, MATRIX_SIZE
from colours import COLOURS
from button import Button

pygame.init()

GAME_NAME = "Smart Horses"
GAME_MENU_TITLE_FONT = pygame.font.Font(None, 70)
current_menu_title_colour = "RED_WOOD"

pygame.display.set_caption(GAME_NAME)

SCREEN_DIMENSIONS = MATRIX_CELL_SIZE * MATRIX_SIZE
screen = pygame.display.set_mode((SCREEN_DIMENSIONS, SCREEN_DIMENSIONS))

SCREEN_MIDDLE_X_POS = SCREEN_DIMENSIONS / 2

BUTTONS = [
    Button("Beginner", (SCREEN_MIDDLE_X_POS, 270)),
    Button("Amateur", (SCREEN_MIDDLE_X_POS, 350)),
    Button("Expert", (SCREEN_MIDDLE_X_POS, 430)),
]

scores = {
    "white": {"name": "Caballo Blanco", "score": 0},
    "black": {"name": "Caballo Negro", "score": 0},
}


def apply_penalty_if_needed(current_player, other_player, moves_current, moves_other):
    """
    Aplica la penalización si el jugador actual no tiene movimientos
    pero el otro sí puede seguir jugando.
    """
    if not moves_current and moves_other:
        current_player["score"] -= 4
        print(f"{current_player['name']} no tiene movimientos. Penalización -4 puntos.")
        return True
    return False


def is_coordinate_within_matrix_bounds(coordinate):
    x, y = coordinate

    def is_within_bounds(n_pos):
        return 0 <= n_pos < MATRIX_SIZE

    if not is_within_bounds(x):
        return False

    if not is_within_bounds(y):
        return False

    return True


def display_game_result(scores):
    if scores["white"]["score"] == scores["black"]["score"]:
        print("🤝 Empate!")
        return

    white_has_higher_score = scores["white"]["score"] > scores["black"]["score"]
    winner = "Blanco" if white_has_higher_score else "Negro"

    print(f"🏆 Gana el Caballo {winner}!")


def get_valid_moves(position, destroyed_cells):
    """
    Devuelve una lista de movimientos válidos del caballo desde su posición actual.
    El caballo se mueve en L como en el ajedrez.
    """
    move_offsets = [
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    ]

    valid_moves = []

    x, y = position
    for dx, dy in move_offsets:
        new_pos = (x + dx, y + dy)
        is_new_pos_destroyed = new_pos in destroyed_cells
        if is_new_pos_destroyed or not is_coordinate_within_matrix_bounds(new_pos):
            continue

        valid_moves.append(new_pos)

    return valid_moves


def start_game(screen, difficulty):
    random_matrix = generate_random_matrix()

    turn = "white"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_map(screen, random_matrix)

        # white_moves = get_valid_moves(white_pos, destroyed_cells)
        # black_moves = get_valid_moves(black_pos, destroyed_cells)

        # if apply_penalty_if_needed(
        #     scores["white"], scores["black"], white_moves, black_moves
        # ):
        #     turn = "black"
        # elif apply_penalty_if_needed(
        #     scores["black"], scores["white"], black_moves, white_moves
        # ):
        #     turn = "white"
        # elif not white_moves and not black_moves:
        #     running = False

        pygame.display.flip()

    display_game_result(scores)


def display_game_title():
    global current_menu_title_colour
    current_menu_title_colour = (
        "RED_WOOD" if not current_menu_title_colour == "RED_WOOD" else "WOOD"
    )
    text_surface = GAME_MENU_TITLE_FONT.render(
        GAME_NAME, True, COLOURS.get(current_menu_title_colour)
    )
    text_rect = text_surface.get_rect(center=(SCREEN_MIDDLE_X_POS, 160))
    screen.blit(text_surface, text_rect)


def main():
    while True:
        screen.fill(COLOURS.get("BEIGE"))
        display_game_title()

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in BUTTONS:
                    if button.is_hovered(mouse_pos):
                        print(f"Selected difficulty: {button.text}")
                        start_game(screen, button.text)

        for button in BUTTONS:
            button.toggle_colour_on_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
