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

    def add_to_current_score(self, value):
        self.score += value

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y}) with score {self.score}"

    def copy(self):
        new_horse = Horse(self.x, self.y, self.value, self.name)
        new_horse.score = self.score
        return new_horse


class Game:
    class SpecialCells(Enum):
        EMPTY = (0, None)
        DESTROYED = (
            997,
            pygame.transform.scale(
                pygame.image.load("assets/destroyed.png"), IMAGE_SCALE
            ),
        )
        WHITE_PIECE = (
            999,
            pygame.transform.scale(
                pygame.image.load("assets/knight/white_wobg.png"), IMAGE_SCALE
            ),
        )
        BLACK_PIECE = (
            998,
            pygame.transform.scale(
                pygame.image.load("assets/knight/black_wobg.png"), IMAGE_SCALE
            ),
        )

        @property
        def id(self):
            return self.value[0]

        @property
        def image(self):
            return self.value[1]

    def __init__(self, screen):
        self.screen = screen
        self.POSSIBLE_POINTS = [-1, -3, -4, -5, -10, 1, 3, 4, 5, 10]
        self.difficulty = ""
        self.ILLEGAL_CELLS_TO_GO = [
            self.SpecialCells.WHITE_PIECE.id,
            self.SpecialCells.BLACK_PIECE.id,
            self.SpecialCells.DESTROYED.id,
        ]
        self.SPECIAL_CELLS = [cell.id for cell in self.SpecialCells]
        self.ID_TO_CELL = {cell.id: cell for cell in self.SpecialCells}

        possible_board_elements = [
            cell_id
            for cell_id in self.SPECIAL_CELLS
            if cell_id is not self.SpecialCells.DESTROYED.id
        ]
        possible_board_elements.extend(self.POSSIBLE_POINTS)

        self.POSSIBLE_BOARD_ELEMENTS = possible_board_elements

        self.board = self.generate_random_matrix()

        self.ai_horse = Horse(
            *self.find_horse_positions(self.SpecialCells.WHITE_PIECE.id),
            self.SpecialCells.WHITE_PIECE.id,
            "WHITE",
        )
        self.player_horse = Horse(
            *self.find_horse_positions(self.SpecialCells.BLACK_PIECE.id),
            self.SpecialCells.BLACK_PIECE.id,
            "BLACK",
        )
        self.current_player = self.ai_horse

        # Essentials
        self.alert = ""
        self.winner = ""
        self.loser: None | Horse = None
        self.ended_in_draw = False

    def reset_game(self):
        self.winner = None
        self.loser = None
        self.ended_in_draw = False

    def generate_random_matrix(self):
        POSSIBLE_POSITIONS = [
            (x, y) for x in range(MATRIX_SIZE) for y in range(MATRIX_SIZE)
        ]

        chosen_positions = random.sample(
            POSSIBLE_POSITIONS, len(self.POSSIBLE_BOARD_ELEMENTS)
        )

        board = [
            [self.SpecialCells.EMPTY.id for _ in range(MATRIX_SIZE)]
            for _ in range(MATRIX_SIZE)
        ]

        for i, (x, y) in enumerate(chosen_positions):
            board[x][y] = self.POSSIBLE_BOARD_ELEMENTS[i]

        print(board)

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

    def calculate_player_valid_moves(self, player=None):
        if player is None:
            player = self.current_player
        valid_moves = []
        horse_x, horse_y = player.get_position()

        for x, y in player.LEGAL_MOVES:
            new_x, new_y = horse_x + x, horse_y + y
            if (
                self.is_coordinate_valid(new_x, new_y)
                and self.board[new_y][new_x] not in self.ILLEGAL_CELLS_TO_GO
            ):
                valid_moves.append((new_x, new_y))

        return valid_moves

    def get_valid_moves(self, board, horse):
        valid_moves = []
        horse_x, horse_y = horse.get_position()

        for x, y in horse.LEGAL_MOVES:
            new_x, new_y = horse_x + x, horse_y + y
            if (
                self.is_coordinate_valid(new_x, new_y)
                and board[new_y][new_x] not in self.ILLEGAL_CELLS_TO_GO
            ):
                valid_moves.append((new_x, new_y))

        return valid_moves

    def toggle_current_player(self):
        self.current_player = (
            self.player_horse if self.current_player == self.ai_horse else self.ai_horse
        )

    def move_horse(self, new_x, new_y):
        horse_pos = self.current_player.get_position()

        if not (new_x, new_y) in self.calculate_player_valid_moves(self.current_player):
            self.alert = "Movimiento inválido"
            return

        self.board[horse_pos[1]][horse_pos[0]] = self.SpecialCells.DESTROYED.id
        self.current_player.add_to_current_score(self.board[new_y][new_x])

        self.current_player.set_position(new_x, new_y)
        self.board[new_y][new_x] = self.current_player.get_value()
        self.alert = ""

    # MINIMAX
    def evaluate(self, board, ai_horse, player_horse):
        ai_moves = self.get_valid_moves(board, ai_horse)
        player_moves = self.get_valid_moves(board, player_horse)

        ai_score = ai_horse.get_score()
        player_score = player_horse.get_score()

        # Penalty rule: if a player has no moves but opponent does, -4 points
        if not ai_moves and player_moves:
            ai_score -= 4
        elif not player_moves and ai_moves:
            player_score -= 4

        score_diff = ai_score - player_score
        mobility_diff = (len(ai_moves) - len(player_moves)) * 0.1

        return score_diff + mobility_diff

    def minimax(self, board, depth, maximizing_player, ai_horse, player_horse):
        ai_moves = self.get_valid_moves(board, ai_horse)
        player_moves = self.get_valid_moves(board, player_horse)

        # Terminal conditions: depth 0 or game over (no moves for either)
        if depth == 0 or (not ai_moves and not player_moves):
            return None, self.evaluate(board, ai_horse, player_horse)

        if maximizing_player:
            # AI Turn
            if not ai_moves:
                # Pass turn if no moves, but check if game is over (handled above if both no moves)
                # If only AI has no moves, it's effectively a pass, but we recurse with same board
                # However, the rules say "En cada turno el jugador debe mover su caballo, a no ser que no tengo movimientos posibles."
                # If no moves, we skip turn.
                return self.minimax(board, depth - 1, False, ai_horse, player_horse)

            max_eval = float("-inf")
            best_move = ai_moves[0]  # Default

            for move in ai_moves:
                # Clone state
                new_board = [row[:] for row in board]
                new_ai_horse = ai_horse.copy()

                # Apply move
                old_x, old_y = new_ai_horse.get_position()
                new_x, new_y = move

                # Logic from move_horse: destroy old, add score, set new pos, set new val
                new_board[old_y][old_x] = self.SpecialCells.DESTROYED.id
                new_ai_horse.add_to_current_score(new_board[new_y][new_x])
                new_ai_horse.set_position(new_x, new_y)
                new_board[new_y][new_x] = new_ai_horse.get_value()

                # Recurse
                _, eval = self.minimax(
                    new_board, depth - 1, False, new_ai_horse, player_horse
                )

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

            return best_move, max_eval

        else:
            # Player Turn
            if not player_moves:
                return self.minimax(board, depth - 1, True, ai_horse, player_horse)

            min_eval = float("inf")
            best_move = player_moves[0]

            for move in player_moves:
                # Clone state
                new_board = [row[:] for row in board]
                new_player_horse = player_horse.copy()

                # Apply move
                old_x, old_y = new_player_horse.get_position()
                new_x, new_y = move

                new_board[old_y][old_x] = self.SpecialCells.DESTROYED.id
                new_player_horse.add_to_current_score(new_board[new_y][new_x])
                new_player_horse.set_position(new_x, new_y)
                new_board[new_y][new_x] = new_player_horse.get_value()

                # Recurse
                _, eval = self.minimax(
                    new_board, depth - 1, True, ai_horse, new_player_horse
                )

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

            return best_move, min_eval

    def play_the_ia(self):
        self.refesh_panel("La ia esta pensando")

        depth = 2
        if self.difficulty == "Amateur":
            depth = 4
        elif self.difficulty == "Expert":
            depth = 6

        # We need to pass copies to not mutate the actual game state during search
        # But wait, the root of minimax uses the current state.
        # The recursive calls use copies.
        # We pass the CURRENT board and horses to start.
        # The minimax function will clone them for its children.

        best_move, _ = self.minimax(
            self.board, depth, True, self.ai_horse, self.player_horse
        )

        # If best_move is None (no moves possible), we should probably handle it.
        # But calculate_player_valid_moves() check in play_turn handles the skip turn logic?
        # Actually, play_the_ia is only called if current_player == ai_horse.
        # And play_turn checks game over.
        # If AI has no moves, play_the_ia might fail if we don't handle None.

        if best_move is None:
            # This happens if AI has no moves.
            # In the game loop, we should have checked if game is over.
            # If game is not over, but AI has no moves, we just toggle player?
            # But apply_penalty_if_needed checks if valid moves exist.
            # If apply_penalty_if_needed returns True, it means no moves.
            # So play_the_ia shouldn't be called if no moves?
            # Let's check play_turn.
            pass
        else:
            calculate_best_move = best_move
            pygame.time.wait(1000)  # simulate the time the AI takes to think

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

        self.toggle_current_player()

    # GAME OVER
    def apply_penalty_if_needed(self):
        if not self.calculate_player_valid_moves(self.current_player):
            self.current_player.add_to_current_score(-4)
            self.refesh_panel(f"{self.current_player.get_name()} -4 point")
            return True
        return False

    def calculate_winner(self):
        ai_score = self.ai_horse.get_score()
        player_score = self.player_horse.get_score()

        if ai_score == player_score:
            self.ended_in_draw = True
            texto = "Empate"
        elif ai_score > player_score:
            self.winner = self.ai_horse
            self.loser = self.player_horse
            texto = "Caballo Blanco (IA) gana"
        else:
            self.winner = self.player_horse
            self.loser = self.ai_horse
            texto = "Caballo Negro (Jugador) gana"

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

    def get_clicked_coordinates(self):
        clicked_pos = pygame.mouse.get_pos()
        x, y = clicked_pos[0] // MATRIX_CELL_SIZE, clicked_pos[1] // MATRIX_CELL_SIZE

        return x, y

    def is_coordinate_valid(self, x, y):
        def is_range_valid(value):
            return 0 <= value < MATRIX_SIZE

        if not (is_range_valid(x) and is_range_valid(y)):
            return False

        return True

    def play_turn(self):
        self.draw_score_panel()
        pygame.display.flip()

        if (
            len(self.get_valid_moves(self.board, self.ai_horse)) == 0
            and len(self.get_valid_moves(self.board, self.player_horse)) == 0
        ):
            print("game ends")
            self.calculate_winner()
            pygame.time.wait(2000)
            return False
        print(f"AI: {len(self.get_valid_moves(self.board, self.ai_horse))}")
        print(f"AI: {self.get_valid_moves(self.board, self.ai_horse)}")
        print(f"Human: {len(self.get_valid_moves(self.board, self.player_horse))}")

        if self.apply_penalty_if_needed():
            self.toggle_current_player()
            print("stuck")
            return True

        # if self.apply_penalty_if_needed():
        #     return False
        # if self.check_game_over():
        #     return False

        if self.current_player == self.ai_horse:
            if self.apply_penalty_if_needed():
                print("exited")
                return
            self.play_the_ia()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = self.get_clicked_coordinates()
                if self.is_coordinate_valid(x_pos, y_pos):
                    self.move_horse(x_pos, y_pos)
                    self.toggle_current_player()

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
