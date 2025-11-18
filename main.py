from calendar import c
import pygame
import sys
from settings import *
from colours import COLOURS
from button import Button
from game import Game

# pygame.init()
TITLE_FONT = pygame.font.Font(None, 70)
SUBTITLE_FONT = pygame.font.Font(None, 40)
# PANEL_INFO_FONT = pygame.font.SysFont("Arial", 24)
GAME_NAME = "Smart Horses"
pygame.display.set_caption(GAME_NAME)

# SIDEBAR_WIDTH = 350
# SCREEN_WIDTH = MATRIX_CELL_SIZE * MATRIX_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = MATRIX_CELL_SIZE * MATRIX_SIZE

SCREEN_MIDDLE_X_POS = SCREEN_WIDTH / 2
SCREEN_MIDDLE_Y_POS = SCREEN_HEIGHT / 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class GUI:
    def __init__(self):
        self.game = Game(screen)
        self.mode = "MENU"  # MENU / PLAYING / WINNER
        self.BUTTONS = [
            Button("Beginner", (SCREEN_MIDDLE_X_POS, 300)),
            Button("Amateur", (SCREEN_MIDDLE_X_POS, 400)),
            Button("Expert", (SCREEN_MIDDLE_X_POS, 500)),
        ]
        self.reset_button = Button("Play Again", (SCREEN_MIDDLE_X_POS, 400))

        self.mouse_pos = pygame.mouse.get_pos()

    def _draw_centered_text(self, text, x, y, font=TITLE_FONT):
        surface = font.render(text, True, COLOURS.get("BLACK"))
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)

    def display_game_title(self):
        self._draw_centered_text(GAME_NAME, SCREEN_MIDDLE_X_POS, 160, font=TITLE_FONT)
        self._draw_centered_text(
            "Choose your difficulty:", SCREEN_MIDDLE_X_POS, 210, font=SUBTITLE_FONT
        )

        for button in self.BUTTONS:
            button.toggle_colour_on_hover(self.mouse_pos)
            button.draw(screen)

    def display_winner_screen(self):
        screen.fill(COLOURS.get("BEIGE"))
        # Caso: Empate
        if isinstance(self.game.winner, str):
            winner_text = "It's a Draw!"
            detail_text = ""
        else:
            loser = (
                self.game.ai_horse
                if self.game.winner == self.game.player_horse
                else self.game.player_horse
            )
            winner_text = f"{self.game.winner.get_name()} wins!"
            detail_text = f"with {self.game.winner.get_score()} points vs {loser.get_score()} of {loser.get_name()} horses"

        # Render title
        self._draw_centered_text(
            winner_text, SCREEN_MIDDLE_X_POS, SCREEN_MIDDLE_Y_POS - 100, font=TITLE_FONT
        )

        # Render details
        self._draw_centered_text(
            detail_text,
            SCREEN_MIDDLE_X_POS,
            SCREEN_MIDDLE_Y_POS - 50,
            font=SUBTITLE_FONT,
        )

        # Render reset button
        self.reset_button.toggle_colour_on_hover(self.mouse_pos)
        self.reset_button.draw(screen)

    def run(self):
        while True:
            screen.fill(COLOURS.get("BEIGE"))
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mode == "MENU":
                        for button in self.BUTTONS:
                            if button.is_hovered(self.mouse_pos):
                                self.game.set_difficulty(button.text)
                                self.game.start_game()
                                self.mode = "PLAYING"

                    elif self.mode == "WINNER":
                        if self.reset_button.is_hovered(self.mouse_pos):
                            self.game = Game(screen)
                            self.mode = "MENU"

            if self.mode == "MENU":
                self.display_game_title()

            elif self.mode == "PLAYING":
                if self.game.winner:
                    self.mode = "WINNER"

            elif self.mode == "WINNER":
                self.display_winner_screen()
            pygame.display.flip()


if __name__ == "__main__":
    game = GUI()
    game.run()
