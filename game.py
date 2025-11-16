import random
import pygame
import sys
from settings import *
from enum import Enum



class Turno(Enum):
    WHITE = 999
    BLACK = 998

print(Turno.WHITE.value)
print(Turno.BLACK.value)



class Game:
    def __init__(self, screen):
        self.difficulty = ""
        self.board =  [ 
            [0,   0,   0,   0,   0,   0,   997,  0],
            [0,   1,   1,   0,   0,   0,   0,    0],
            [0,   0,   997, 0,   1,   0, 0,    0],
            [0,   0,   997,   0,   997,   0,   0,    0],
            [-1, 1,   998, 0,   0,   997,   1,    997],
            [0,   0,   0,   0,   1,   0,   0,    0],
            [0, 999,   1,   1,   0,   997, 0,    0],
            [0,   0,   997,   997, 997,   1,   1,    0],
        ]   #self.generate_random_matrix()
        self.turn =  Turno.WHITE  # white starts first
        self.screen = screen

        self.ai_score = 0
        self.player_score = 0

        self.alert = ""
        self.winner = ""



    def generate_random_matrix(self):
        chosen_positions = random.sample(POSSIBLE_POSITIONS, len(MATRIX_ELEMENTS))

        board = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

        for i, (x, y) in enumerate(chosen_positions):
            board[x][y] = MATRIX_ELEMENTS[i]

        return board



    #parte monica
    def find_horse_positions(self):
        for y in range(MATRIX_SIZE):
            for x in range(MATRIX_SIZE):
                if self.board[y][x] == self.turn.value:
                    return (x, y)
        return None
    

    def horse_possibilities(self):
        valid_moves = []
        x, y = self.find_horse_positions()
        horse_moves = [
                (x - 2, y + 1), (x - 1, y + 2), (x + 1, y + 2), (x + 2, y + 1),
                (x + 2, y - 1), (x + 1, y - 2), (x - 1, y - 2), (x - 2, y - 1)
            ]

        for move in horse_moves:
            if 0 <= move[0] < MATRIX_SIZE and 0 <= move[1] < MATRIX_SIZE:
                if self.board[move[1]][move[0]] != 997 and self.board[move[1]][move[0]] != 998:
                    valid_moves.append(move)
                

        return valid_moves


    def move_horse(self, x, y):
        horse_positions = self.find_horse_positions()

        if (x, y) not in self.horse_possibilities():
            self.alert = "Movimiento inválido"
            return

        if self.turn == Turno.WHITE:
            self.board[horse_positions[1]][horse_positions[0]] = 997
            self.board[y][x] = 999
        else:
            self.board[horse_positions[1]][horse_positions[0]] = 997
            self.board[y][x] = 998

        self.turn = Turno.BLACK if self.turn == Turno.WHITE else Turno.WHITE
        self.alert = ""



    def check_game_over(self):
        if self.apply_penalty_if_needed():
            self.calculate_winner()
            return True
        return False


    #metodos del juego
    def apply_penalty_if_needed(self):
        print("evalaudno si hay penalizacion")
        print(self.horse_possibilities(Turno.WHITE))
        print(self.horse_possibilities(Turno.BLACK))

        if not self.horse_possibilities(Turno.WHITE) or self.find_horse_positions(Turno.BLACK) == None:
            self.ai_score -= 4 if self.turn == Turno.WHITE else 0
            self.player_score -= 4 if self.turn == Turno.BLACK else 0
            print(f"{self.turn} no tiene movimientos. Penalización -4 puntos.")
            return True
        return False



    def calculate_winner(self):
        if self.ai_score > self.player_score:
            self.alert = "Caballo Blanco (IA) gana"
            self.winner = "White"
        elif self.ai_score < self.player_score:
            self.alert = "Caballo Negro (Jugador) gana"
            self.winner = "Black"
        else:
            self.alert = "Empate"
            self.winner = "Draw"



    #metodos de dibujar el mapa
    def draw_map(self):
        for y, row in enumerate[list[int]](self.board):
            for x, cell in enumerate[int](row):
                image = CELLS.get(cell)

                calculate_cells_available = self.horse_possibilities()

                if (x, y) in calculate_cells_available:
                    image = pygame.transform.scale(pygame.transform.scale(pygame.image.load("assets/resalt.png"), IMAGE_SCALE), (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE))
                    self.screen.blit(image, (x * MATRIX_CELL_SIZE, y * MATRIX_CELL_SIZE))

                else:
                    self.screen.blit(
                        pygame.transform.scale(image, (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE)),
                        (x * MATRIX_CELL_SIZE, y * MATRIX_CELL_SIZE),
                    )   



    def start_game(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    casilla = pygame.mouse.get_pos()
                    x, y = casilla[0] // MATRIX_CELL_SIZE, casilla[1] // MATRIX_CELL_SIZE
                    print(x, y)
                    if x < MATRIX_SIZE and y < MATRIX_SIZE:
                        self.move_horse(x, y)

            self.draw_map()
            self.draw_score_panel()
            pygame.display.flip()
            clock.tick(60)



    def draw_score_panel(self):
        panel_x = MATRIX_CELL_SIZE * MATRIX_SIZE + 10
        panel_width = SCREEN_WIDTH - MATRIX_CELL_SIZE * MATRIX_SIZE - 20
        panel_height = screen.get_height() - 20

        panel_rect = pygame.Rect(panel_x, 10, panel_width, panel_height)
        pygame.draw.rect(self.screen, (245, 240, 200), panel_rect, border_radius=10)

        title = PANEL_INFO_FONT.render("PUNTUACION", True, (0, 0, 0))
        self.screen.blit(title, (panel_x + 40, 30))
        
        ai_text = PANEL_INFO_FONT.render(f"Caballo Blanco (IA): {self.ai_score}", True, (0, 0, 128))
        player_text = PANEL_INFO_FONT.render(f"Caballo Negro (Jugador): {self.player_score}", True, (128, 0, 0))    

        self.screen.blit(ai_text, (panel_x + 20, 100))
        self.screen.blit(player_text, (panel_x + 20, 150))

        pygame.draw.line(
            self.screen, (120, 120, 120), (panel_x + 10, 200), (panel_x + panel_width - 10, 200), 2
        )

        status_text = PANEL_INFO_FONT.render("Estado: Jugando...", True, (60, 60, 60))
        self.screen.blit(status_text, (panel_x + 20, 230))

        turn_text = PANEL_INFO_FONT.render(f"Es turno de {self.turn}", True, (0, 0, 128) if self.turn == "White" else (128, 0, 0))
        self.screen.blit(turn_text, (panel_x + 20, 260))

        alert_test = PANEL_INFO_FONT.render(f"Alert: {self.alert}", True, (255, 0, 0))
        self.screen.blit(alert_test, (panel_x + 20, 300))


    def set_difficulty(self, difficulty):
        self.difficulty = difficulty