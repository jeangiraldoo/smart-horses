import pygame
import sys
from board import draw_map, generate_random_matrix, MATRIX_CELL_SIZE, MATRIX_SIZE
from colours import COLOURS
from button import Button

pygame.init()

GAME_NAME = "Smart Horses"
GAME_MENU_TITLE_FONT = pygame.font.Font(None, 70)
current_menu_title_colour = "RED_WOOD"  # Toggle for animating the title

pygame.display.set_caption(GAME_NAME)

SCREEN_DIMENSIONS = MATRIX_CELL_SIZE * MATRIX_SIZE
screen = pygame.display.set_mode((SCREEN_DIMENSIONS, SCREEN_DIMENSIONS))


SCREEN_MIDDLE_X_POS = SCREEN_DIMENSIONS / 2

BUTTONS = [
    Button("Beginner", (SCREEN_MIDDLE_X_POS, 270)),
    Button("Amateur", (SCREEN_MIDDLE_X_POS, 350)),
    Button("Expert", (SCREEN_MIDDLE_X_POS, 430)),
]


def start_game(screen, difficulty):
    random_matrix = generate_random_matrix()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_map(screen, random_matrix)
        pygame.display.flip()


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

        # 2 loops iterate over the buttons to handle presses and looks separately
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
