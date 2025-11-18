import random
import pygame
import sys
from enum import Enum

from settings import *
from colours import COLOURS

IMAGE_DIMENSIONS = 60
IMAGE_SCALE = (IMAGE_DIMENSIONS, IMAGE_DIMENSIONS)

# MATRIX_SIZE = 8
# MATRIX_CELL_SIZE = 90

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


class Horse:
    class AvailableMovesInL(Enum):
        ONE_RIGHT_TWO_UP = (1, -2)
        TWO_RIGHT_ONE_UP = (2, -1)
        TWO_RIGHT_ONE_DOWN = (2, 1)
        ONE_RIGHT_TWO_DOWN = (1, 2)
        ONE_LEFT_TWO_DOWN = (-1, 2)
        TWO_LEFT_ONE_DOWN = (-2, 1)
        TWO_LEFT_ONE_UP = (-2, -1)
        ONE_LEFT_TWO_UP = (-1, -2)

    def __init__(self, x, y, value, name):
        self.x = x
        self.y = y
        self.value = value
        self.score = 0
        self.name = name
        self.LEGAL_MOVES = [val.value for val in self.AvailableMovesInL]

    def get_position(self):
        return (self.x, self.y)

    def get_value(self):
        return self.value

    def get_score(self):
        return self.score

    def get_name(self):
        return self.name

    def set_score(self, score):
        self.score = score

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y}) with score {self.score}"


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.POSSIBLE_POINTS = [-1, -3, -4, -5, -10, 1, 3, 4, 5, 10]
        self.difficulty = ""

        possible_board_elements = []
        possible_board_elements.extend(CELLS.keys())
        possible_board_elements.extend(self.POSSIBLE_POINTS)

        self.POSSIBLE_BOARD_ELEMENTS = possible_board_elements

        self.board = self.generate_random_matrix()

        # Horses
        self.ai_horse = Horse(*self.find_horse_positions(999), 999, "WHITE")
        self.player_horse = Horse(*self.find_horse_positions(998), 998, "BLACK")
        self.current_player = self.ai_horse

        # Essentials
        self.alert = ""
        self.winner = ""

    def generate_random_matrix(self):
        POSSIBLE_POSITIONS = [
            (x, y) for x in range(MATRIX_SIZE) for y in range(MATRIX_SIZE)
        ]

        chosen_positions = random.sample(
            POSSIBLE_POSITIONS, len(self.POSSIBLE_BOARD_ELEMENTS)
        )

        board = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

        for i, (x, y) in enumerate(chosen_positions):
            board[x][y] = self.POSSIBLE_BOARD_ELEMENTS[i]

        return board

    # MOVEMENT
    def find_horse_positions(self, horse_find=""):
        if not horse_find:
            horse_find = self.current_player.value

        for y in range(MATRIX_SIZE):
            for x in range(MATRIX_SIZE):
                if self.board[y][x] == horse_find:
                    return (x, y)
        return None

    def calculate_player_valid_moves(self):
        valid_moves = []
        horse_x, horse_y = self.current_player.get_position()

        for x, y in self.current_player.LEGAL_MOVES:
            new_x, new_y = horse_x + x, horse_y + y
            if 0 <= new_x < MATRIX_SIZE and 0 <= new_y < MATRIX_SIZE:
                if self.board[new_y][new_x] not in [997, 998, 999]:
                    valid_moves.append((new_x, new_y))

        return valid_moves

    def move_horse(self, new_x, new_y):
        horse_pos = self.current_player.get_position()

        if (new_x, new_y) in self.calculate_player_valid_moves():
            self.board[horse_pos[1]][horse_pos[0]] = 997
            self.current_player.set_score(self.current_player.get_score() + self.board[new_y][new_x])
            self.current_player.set_position(new_x, new_y)
            self.board[new_y][new_x] = self.current_player.get_value()
            self.current_player = (
                self.player_horse if self.current_player == self.ai_horse else self.ai_horse
            )
            self.alert = ""

        else:
            self.alert = "Movimiento inválido"

    # MINIMAX
    def minimax(self, depth, is_maximizing):
        options = self.calculate_player_valid_moves()
        return options[0]

    def play_the_ia(self):
        self.refesh_panel("La ia esta pensando")
        calculate_best_move = self.minimax(3, True)
        pygame.time.wait(2000)  # simulate the time the AI takes to think

        pygame.draw.rect(
            self.screen,
            COLOURS.get("GREEN"),
            pygame.Rect(
                calculate_best_move[0] * MATRIX_CELL_SIZE,
                calculate_best_move[1] * MATRIX_CELL_SIZE,
                MATRIX_CELL_SIZE,
                MATRIX_CELL_SIZE,
            ),
        )
        self.refesh_panel(f"La ia decide {calculate_best_move}")
        pygame.time.wait(1000)  # give time for the player to see the AI move

        self.move_horse(*calculate_best_move)
        self.alert = "AI moved at" + str(self.find_horse_positions())

    # GAME OVER
    def apply_penalty_if_needed(self):
        if not self.calculate_player_valid_moves():
            self.current_player.set_score(self.current_player.get_score() - 4)
            self.refesh_panel(f"{self.current_player.get_name()} -4 point")
            return True
        return False

    def calculate_winner(self):
        ai_score = self.ai_horse.get_score()
        player_score = self.player_horse.get_score()

        if ai_score > player_score:
            self.winner = self.ai_horse
            texto = "Caballo Blanco (IA) gana"
        elif ai_score < player_score:
            self.winner = self.player_horse
            texto = "Caballo Negro (Jugador) gana"
        else:
            self.winner = "Draw"
            texto = "Empate"

        self.refesh_panel(texto)

    def check_game_over(self):
        if self.apply_penalty_if_needed():
            self.calculate_winner()
            pygame.time.wait(2000)
            return True
        return False

    def refesh_panel(self, alert=""):
        self.alert = alert
        self.draw_score_panel()
        pygame.display.flip()

    def draw_score_panel(self):
        panel_x = MATRIX_CELL_SIZE * MATRIX_SIZE + 10
        panel_width = SCREEN_WIDTH - MATRIX_CELL_SIZE * MATRIX_SIZE - 20
        panel_height = self.screen.get_height() - 20

        panel_rect = pygame.Rect(panel_x, 10, panel_width, panel_height)
        pygame.draw.rect(self.screen, (245, 240, 200), panel_rect, border_radius=10)

        title = PANEL_INFO_FONT.render("PUNTUACION", True, (0, 0, 0))
        self.screen.blit(title, (panel_x + 40, 30))

        ai_text = PANEL_INFO_FONT.render(
            f"Caballo Blanco (IA): {self.ai_horse.get_score()}", True, (0, 0, 128)
        )
        player_text = PANEL_INFO_FONT.render(
            f"Caballo Negro (Jugador): {self.player_horse.get_score()}",
            True,
            (128, 0, 0),
        )

        self.screen.blit(ai_text, (panel_x + 20, 100))
        self.screen.blit(player_text, (panel_x + 20, 150))

        pygame.draw.line(
            self.screen,
            (120, 120, 120),
            (panel_x + 10, 200),
            (panel_x + panel_width - 10, 200),
            2,
        )

        status_text = PANEL_INFO_FONT.render("Estado: Jugando...", True, (60, 60, 60))
        self.screen.blit(status_text, (panel_x + 20, 230))

        turn_text = PANEL_INFO_FONT.render(
            f"Es turno de {self.current_player.get_name()}", True, (0, 128, 0)
        )
        self.screen.blit(turn_text, (panel_x + 20, 260))

        alert_test = PANEL_INFO_FONT.render(f"Alert: {self.alert}", True, (255, 0, 0))
        self.screen.blit(alert_test, (panel_x + 20, 300))

    def play_turn(self):
        self.draw_score_panel()
        pygame.display.flip()

        if self.check_game_over():
            return False

        if self.current_player == self.ai_horse:
            self.play_the_ia()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                casilla = pygame.mouse.get_pos()
                board_x, board_y = (
                    casilla[0] // MATRIX_CELL_SIZE,
                    casilla[1] // MATRIX_CELL_SIZE,
                )
                if board_x < MATRIX_SIZE and board_y < MATRIX_SIZE:
                    self.move_horse(board_x, board_y)

        self.draw_score_panel()
        pygame.display.flip()
        return True

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def __str__(self):
        board_str = "\n    ".join("    " + str(row) for row in self.board)
        return f"""
        Game
            difficulty={self.difficulty}
            turn={self.current_player.get_name()}
            white_horse={self.ai_horse}
            black_horse={self.player_horse}
        Board:
            {board_str}
        """
