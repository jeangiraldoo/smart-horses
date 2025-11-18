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

IMAGE_DIMENSIONS = 60
IMAGE_SCALE = (IMAGE_DIMENSIONS, IMAGE_DIMENSIONS)

WHITE_CELL = pygame.transform.scale(
    pygame.image.load("assets/white_cell.png"), IMAGE_SCALE
)
BLACK_CELL = pygame.transform.scale(
    pygame.image.load("assets/black_cell.png"), IMAGE_SCALE
)

CELLS = {
    # Destroyer
    997: pygame.transform.scale(pygame.image.load("assets/destroyed.png"), IMAGE_SCALE),
    # White knight
    999: pygame.transform.scale(
        pygame.image.load("assets/knight/white_wobg.png"), IMAGE_SCALE
    ),
    # Black knight
    998: pygame.transform.scale(
        pygame.image.load("assets/knight/black_wobg.png"), IMAGE_SCALE
    ),
}


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

    def draw_text_on_board(self, text, pos, color=(2, 2, 2)):
        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

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

    def draw_map(self, avalibe_moves):
        for y, row in enumerate[list[int]](self.game.board):
            for x, cell in enumerate[int](row):
                rect = pygame.Rect(
                    x * MATRIX_CELL_SIZE,
                    y * MATRIX_CELL_SIZE,
                    MATRIX_CELL_SIZE,
                    MATRIX_CELL_SIZE,
                )
                image = CELLS.get(cell, CELLS.get(0))

                # First draw the board
                screen.blit(
                    pygame.transform.scale(
                        WHITE_CELL if (x + y) % 2 == 0 else BLACK_CELL,
                        (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE),
                    ),
                    rect.topleft,
                )

                # Draw the assets
                if image:
                    screen.blit(
                        pygame.transform.scale(
                            image, (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE)
                        ),
                        rect.topleft,
                    )

                if (x, y) in avalibe_moves:  # feedback for valid moves
                    color = COLOURS[
                        "GOLD"
                    ]  # COLOURS["GOLD"] if cell == 0 else COLOURS["BLUE"] # if you want point cells to give a different feedback
                    pygame.draw.rect(screen, color, rect)

                if isinstance(cell, int) and cell not in [
                    997,
                    999,
                    998,
                    0,
                ]:  # draw the points
                    self.draw_text_on_board(
                        str(cell),
                        rect.center,
                        (0, 0, 0) if (x + y) % 2 == 0 else (255, 255, 255),
                    )

                if (
                    cell == self.game.turn.value
                ):  # feedback for the horse whose turn it is
                    pygame.draw.ellipse(
                        screen, COLOURS["GOLD"], rect.inflate(10, 10), 6
                    )

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

    def ui_loop(self):
        clock = pygame.time.Clock()
        while True:
            should_continue_playing = self.game.play_turn()
            if not should_continue_playing:
                return

            self.draw_map(self.game.horse_possibilities())
            clock.tick(75)

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
                                self.mode = "PLAYING"
                                self.game.set_difficulty(button.text)
                                self.draw_map(self.game.horse_possibilities())
                                self.ui_loop()

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
