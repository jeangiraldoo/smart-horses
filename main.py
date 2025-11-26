from calendar import c
import pygame
import sys
from settings import *
from colours import COLOURS
from button import Button
from game import Game
from enum import Enum, auto

# pygame.init()
TITLE_FONT = pygame.font.Font(None, 70)
SUBTITLE_FONT = pygame.font.Font(None, 40)
GAME_MENU_TITLE_FONT = pygame.font.Font(None, 70)
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


class GUI:
    class Modes(Enum):
        MENU = auto()
        PLAYING = auto()
        WINNER = auto()

    def __init__(self):
        self.game = Game(screen)
        self.mode = self.Modes.MENU
        self.BUTTONS = [
            Button("Beginner", (SCREEN_MIDDLE_X_POS, 300)),
            Button("Amateur", (SCREEN_MIDDLE_X_POS, 400)),
            Button("Expert", (SCREEN_MIDDLE_X_POS, 500)),
        ]
        self.current_menu_title_colour = "RED_WOOD"  # Toggle for animating the title
        self.reset_button = Button("Play Again", (SCREEN_MIDDLE_X_POS, 400))

        self.mouse_pos = pygame.mouse.get_pos()

    def _draw_centered_menu_text(
        self, text, y_pos, font=TITLE_FONT, colour=COLOURS.get("BLACK")
    ):
        surface = font.render(text, True, colour)
        rect = surface.get_rect(center=(SCREEN_MIDDLE_X_POS, y_pos))
        screen.blit(surface, rect)

    def display_game_title(self):
        self.current_menu_title_colour = (
            "RED_WOOD" if not self.current_menu_title_colour == "RED_WOOD" else "WOOD"
        )

        self._draw_centered_menu_text(
            GAME_NAME,
            y_pos=160,
            font=GAME_MENU_TITLE_FONT,
            colour=COLOURS.get(self.current_menu_title_colour),
        )
        self._draw_centered_menu_text(
            "Choose your difficulty:",
            y_pos=210,
            font=GAME_MENU_TITLE_FONT,
        )

        for button in self.BUTTONS:
            button.toggle_colour_on_hover(self.mouse_pos)
            button.draw(screen)

    def _highlight_cell(self, rect):
        color = COLOURS["GOLD"]
        pygame.draw.rect(screen, color, rect)

    def _draw_image_on_cell(self, cell_rect, image):
        screen.blit(
            pygame.transform.scale(image, (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE)),
            cell_rect.topleft,
        )

    def _highlight_current_player(self, cell_rect):
        pygame.draw.ellipse(screen, COLOURS["GOLD"], cell_rect.inflate(10, 10), 6)

    def is_dark_square(self, x, y):
        return (x + y) % 2 == 0

    def _draw_point_on_cell(self, cell_rect, point_value, x, y):
        point_colour = (
            COLOURS.get("BLACK") if self.is_dark_square(x, y) else COLOURS.get("WHITE")
        )

        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(str(point_value), True, point_colour)
        text_rect = text_surface.get_rect(center=cell_rect.center)
        screen.blit(text_surface, text_rect)

    def draw_map(self, available_moves):
        for y, row in enumerate[list[int]](self.game.board):
            for x, cell in enumerate[int](row):
                cell_rect = pygame.Rect(
                    x * MATRIX_CELL_SIZE,
                    y * MATRIX_CELL_SIZE,
                    MATRIX_CELL_SIZE,
                    MATRIX_CELL_SIZE,
                )

                screen.blit(
                    pygame.transform.scale(
                        WHITE_CELL if self.is_dark_square(x, y) else BLACK_CELL,
                        (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE),
                    ),
                    cell_rect.topleft,
                )

                if (x, y) in available_moves:
                    self._highlight_cell(cell_rect)
                elif (
                    special_cell := self.game.ID_TO_CELL.get(cell)
                ) and special_cell.image:
                    self._draw_image_on_cell(cell_rect, special_cell.image)

                if cell == self.game.current_player.value:
                    self._highlight_current_player(cell_rect)
                elif isinstance(cell, int) and cell not in self.game.SPECIAL_CELLS:
                    self._draw_point_on_cell(cell_rect, cell, x, y)

    def display_winner_screen(self):
        screen.fill(COLOURS.get("BEIGE"))
        winner_text = (
            "It's a draw!"
            if self.game.ended_in_draw
            else f"{self.game.winner.get_name()} wins!"
        )

        self._draw_centered_menu_text(
            winner_text, y_pos=SCREEN_MIDDLE_Y_POS - 100, font=TITLE_FONT
        )

        final_points_comparison = (
            f"{self.game.winner.get_score()} VS {self.game.loser.get_score()} points"
        )

        self._draw_centered_menu_text(
            final_points_comparison,
            y_pos=SCREEN_MIDDLE_Y_POS - 50,
            font=SUBTITLE_FONT,
        )

        self.reset_button.toggle_colour_on_hover(self.mouse_pos)
        self.reset_button.draw(screen)

    def ui_loop(self):
        clock = pygame.time.Clock()
        self.game.reset_game()
        while True:
            should_continue_playing = self.game.play_turn()
            if not should_continue_playing:
                return

            self.draw_map(self.game.calculate_player_valid_moves())
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
                    if self.mode == self.Modes.MENU:
                        for button in self.BUTTONS:
                            if button.is_hovered(self.mouse_pos):
                                self.mode = self.Modes.PLAYING
                                self.game.set_difficulty(button.text)
                                self.draw_map(self.game.calculate_player_valid_moves())
                                self.ui_loop()

                    elif self.mode == self.Modes.WINNER:
                        if self.reset_button.is_hovered(self.mouse_pos):
                            self.game = Game(screen)
                            self.mode = self.Modes.MENU

            if self.mode == self.Modes.MENU:
                self.display_game_title()

            elif self.mode == self.Modes.PLAYING and self.game.winner:
                self.mode = self.Modes.WINNER

            elif self.mode == self.Modes.WINNER:
                self.display_winner_screen()
            pygame.display.flip()


if __name__ == "__main__":
    game = GUI()
    game.run()
