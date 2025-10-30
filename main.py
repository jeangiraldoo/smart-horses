import pygame
import sys
from board import draw_map, generate_random_matrix, MATRIX_CELL_SIZE, MATRIX_SIZE
from colours import COLOURS
from button import Button

GAME_NAME = "Smart Horses"

pygame.init()
pygame.display.set_caption(GAME_NAME)

SCREEN_DIMENSIONS = MATRIX_CELL_SIZE * MATRIX_SIZE
screen = pygame.display.set_mode((SCREEN_DIMENSIONS, SCREEN_DIMENSIONS))


BUTTONS_X_POSITION = SCREEN_DIMENSIONS / 2
BUTTONS = [
    Button("Beginner", (BUTTONS_X_POSITION, 220)),
    Button("Amateur", (BUTTONS_X_POSITION, 300)),
    Button("Expert", (BUTTONS_X_POSITION, 380)),
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


def main():
    while True:
        screen.fill(COLOURS.get("BEIGE"))
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
