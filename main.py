import pygame
import sys
from settings import *
from button import Button
from game import Game



BUTTONS = [
    Button("Beginner", (SCREEN_MIDDLE_X_POS, 270)),
    Button("Amateur", (SCREEN_MIDDLE_X_POS, 350)),
    Button("Expert", (SCREEN_MIDDLE_X_POS, 430)),
]



class GUI:
    def __init__(self):
        self.game = Game(screen)


    def display_game_title(self):
        global CURRENT_MENU_TITLE_COLOUR
        CURRENT_MENU_TITLE_COLOUR = "RED_WOOD" 
        text_surface = GAME_MENU_TITLE_FONT.render(
            GAME_NAME, True, COLOURS.get(CURRENT_MENU_TITLE_COLOUR)
        )
        text_rect = text_surface.get_rect(center=(SCREEN_MIDDLE_X_POS, 160))
        screen.blit(text_surface, text_rect)

    def display_winner(self):
        text_surface = GAME_MENU_TITLE_FONT.render(
            self.game.winner, True, COLOURS.get("RED_WOOD")
        )
        text_rect = text_surface.get_rect(center=(SCREEN_MIDDLE_X_POS, 500))
        screen.blit(text_surface, text_rect)

    def run(self):
        while True:
            screen.fill(COLOURS.get("BEIGE"))

            if self.game.winner:
                self.display_winner()
            else:
                self.display_game_title()

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in BUTTONS:
                        if button.is_hovered(mouse_pos):
                            self.game.set_difficulty(button.text)
                            self.game.start_game()

            for button in BUTTONS:
                button.toggle_colour_on_hover(mouse_pos)
                button.draw(screen)

            pygame.display.flip()


if __name__ == "__main__":
    GUI().run()

