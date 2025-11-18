import random
import pygame
import sys

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
    def __init__(self, x, y, value, name):
        self.x = x
        self.y = y
        self.value = value
        self.score = 0
        self.name = name

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
        self.difficulty = ""
        self.board = [
            [0, 0, 0, 0, 0, 0, 997, 0],
            [0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 997, 0, 1, 0, 0, 0],
            [0, 0, 997, 0, 997, 0, 0, 0],
            [997, 1, 998, 0, 0, 997, 1, 997],
            [0, 0, 0, 997, 1, 0, 0, 0],
            [0, 999, 1, 1, 0, 997, 0, 0],
            [0, 0, 997, 997, 997, 1, 1, 0],
        ]
        self.board = self.generate_grid()

        # Horses
        self.ai_horse = Horse(*self.find_horse_positions(999), 999, "WHITE")
        self.player_horse = Horse(*self.find_horse_positions(998), 998, "BLACK")
        self.turn = self.ai_horse

        # Essentials
        self.alert = ""
        self.winner = ""

    # Initialization
    def generate_grid(self):
        # Create an empty 8x8 board
        grid = [[0 for _ in range(8)] for _ in range(8)]

        # Generate random positions for the 10 point cells (from -10 to 10)
        points = [-1, -3, -4, -5, -10, 1, 3, 4, 5, 10]
        random.shuffle(points)

        # Place the point cells on the board
        for point in points:
            while True:
                x, y = random.randint(0, 7), random.randint(0, 7)
                if grid[x][y] == 0:
                    grid[x][y] = point
                    break

        # Generate random positions for the AI and player horses
        for horse in [999, 998]:
            while True:
                x, y = random.randint(0, 7), random.randint(0, 7)
                if grid[x][y] == 0:
                    grid[x][y] = horse
                    break
        return grid

    # MOVEMENT
    def find_horse_positions(self, horse_find=""):
        if not horse_find:
            horse_find = self.turn.value

        for y in range(MATRIX_SIZE):
            for x in range(MATRIX_SIZE):
                if self.board[y][x] == horse_find:
                    return (x, y)
        return None

    def horse_possibilities(self):
        valid_moves = []
        horse_x, horse_y = self.turn.get_position()

        directions = [
            ("L arriba derecha", -2, 1),  # Two up, one right
            ("L derecha arriba", -1, 2),  # One up, two right
            ("L derecha abajo", 1, 2),  # One down, two right
            ("L abajo derecha", 2, 1),  # Two down, one right
            ("L abajo izquierda", 2, -1),  # Two down, one left
            ("L izquierda abajo", 1, -2),  # One down, two left
            ("L izquierda arriba", -1, -2),  # One up, two left
            ("L arriba izquierda", -2, -1),  # Two up, one left
        ]

        for label, y, x in directions:
            new_x, new_y = horse_x + x, horse_y + y
            if 0 <= new_x < MATRIX_SIZE and 0 <= new_y < MATRIX_SIZE:
                if self.board[new_y][new_x] not in [997, 998, 999]:
                    valid_moves.append((new_x, new_y))

        return valid_moves

    def move_horse(self, new_x, new_y):
        horse_pos = self.turn.get_position()

        if (new_x, new_y) in self.horse_possibilities():
            self.board[horse_pos[1]][horse_pos[0]] = 997
            self.turn.set_score(self.turn.get_score() + self.board[new_y][new_x])
            self.turn.set_position(new_x, new_y)
            self.board[new_y][new_x] = self.turn.get_value()
            self.turn = (
                self.player_horse if self.turn == self.ai_horse else self.ai_horse
            )
            self.alert = ""

        else:
            self.alert = "Movimiento inválido"

    # MINIMAX
    def minimax(self, depth, is_maximizing):
        options = self.horse_possibilities()
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
        if not self.horse_possibilities():
            self.turn.set_score(self.turn.get_score() - 4)
            self.refesh_panel(f"{self.turn.get_name()} -4 point")
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
            f"Es turno de {self.turn.get_name()}", True, (0, 128, 0)
        )
        self.screen.blit(turn_text, (panel_x + 20, 260))

        alert_test = PANEL_INFO_FONT.render(f"Alert: {self.alert}", True, (255, 0, 0))
        self.screen.blit(alert_test, (panel_x + 20, 300))

    def play_turn(self):
        self.draw_score_panel()
        pygame.display.flip()

        if self.check_game_over():
            return False

        if self.turn == self.ai_horse:
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
            turn={self.turn.get_name()}
            white_horse={self.ai_horse}
            black_horse={self.player_horse}
        Board:
            {board_str}
        """
