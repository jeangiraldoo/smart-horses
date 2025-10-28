import pygame
import sys
from colours import COLOURS
from button import Button

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Difficulty Menu")


BUTTONS = [
    Button("Beginner", (250, 150)),
    Button("Amateur", (250, 230)),
    Button("Expert", (250, 310)),
]


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

        for button in BUTTONS:
            button.toggle_colour_on_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
