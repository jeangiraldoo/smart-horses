import pygame
import sys
from board import (
    draw_map,
    generate_random_matrix,
    MATRIX_CELL_SIZE,
    MATRIX_SIZE,
    get_cell_points,
    draw_score_panel,
)
from colours import COLOURS
from button import Button

pygame.init()

GAME_NAME = "Smart Horses"
GAME_MENU_TITLE_FONT = pygame.font.Font(None, 70)
current_menu_title_colour = "RED_WOOD"  

pygame.display.set_caption(GAME_NAME)

SIDEBAR_WIDTH = 300  # espacio para la barra lateral
SCREEN_WIDTH = MATRIX_CELL_SIZE * MATRIX_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = MATRIX_CELL_SIZE * MATRIX_SIZE + 100  

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


SCREEN_MIDDLE_X_POS = (MATRIX_CELL_SIZE * MATRIX_SIZE) / 2

BUTTONS = [
    Button("Beginner", (SCREEN_MIDDLE_X_POS, 270)),
    Button("Amateur", (SCREEN_MIDDLE_X_POS, 350)),
    Button("Expert", (SCREEN_MIDDLE_X_POS, 430)),
]

# Puntajes
font = pygame.font.SysFont("Arial", 24)
ai_score = 0
player_score = 0


def start_game(screen, difficulty):
    global ai_score, player_score
    random_matrix = generate_random_matrix()
    ai_score, player_score = 0, 0  # Reiniciar puntajes al iniciar nueva partida

    running = True
    clock = pygame.time.Clock()

    # Posiciones iniciales 
    white_knight_pos = [1, 1]  # IA
    black_knight_pos = [3, 2]  # Jugador

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Deteccion de puntos (solo ejemplo para mostrar el panel)
        ai_points = get_cell_points(random_matrix, white_knight_pos)
        player_points = get_cell_points(random_matrix, black_knight_pos)
        ai_score += ai_points
        player_score += player_points

        # Dibuja tablero
        draw_map(screen, random_matrix)

        # Barra lateral de puntajes 
        draw_score_panel(
            screen,
            font,
            ai_score,
            player_score,
            SCREEN_WIDTH,
            MATRIX_CELL_SIZE * MATRIX_SIZE,  # ← Este es el ancho del tablero
        )

        pygame.display.flip()
        clock.tick(2)  # velocidad lenta para visualizar mejor 


def display_game_title():
    """Anima el titulo del menu"""
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
    """Pantalla del menu principal"""
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
