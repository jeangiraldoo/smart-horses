import pygame
import sys
from colours import COLOURS
from settings import *
import random

pygame.init()

GAME_MENU_TITLE_FONT = pygame.font.Font(None, 70)
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((SCREEN_DIMENSIONS, SCREEN_DIMENSIONS))

BUTTONS = [
    Button("Beginner", (SCREEN_MIDDLE_X_POS, 270)),
    Button("Amateur", (SCREEN_MIDDLE_X_POS, 350)),
    Button("Expert", (SCREEN_MIDDLE_X_POS, 430)),
]

class Game:
    def __init__(self, screen):
        self.difficulty = ""
        self.board =  [ 
            [0,   0,   0,   0,   0,   0,   997,  0],
            [0,   1,   1,   0,   0,   0,   0,    0],
            [0,   0,   997, 0,   1,   0, 0,    0],
            [0,   0,   0,   0,   0,   0,   0,    0],
            [997, 1,   998, 0,   0,   0,   1,    997],
            [0,   0,   0,   0,   1,   0,   0,    0],
            [0, 999,   1,   1,   0,   997, 0,    0],
            [0,   0,   0,   997, 0,   1,   1,    0],
        ]   #self.generate_random_matrix()
        self.turn =  "White"  # White starts first
        self.screen = screen



    def generate_random_matrix(self):
        chosen_positions = random.sample(POSSIBLE_POSITIONS, len(MATRIX_ELEMENTS))

        board = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]

        for i, (x, y) in enumerate(chosen_positions):
            board[x][y] = MATRIX_ELEMENTS[i]

        return board


    #parte monica
    def find_horse_positions(self):
        horse_positions = {'white': None, 'black': None}
        for y in range(MATRIX_SIZE):
            for x in range(MATRIX_SIZE):
                if self.board[y][x] == 999:
                    horse_positions['white'] = (x, y)
                elif self.board[y][x] == 998:
                    horse_positions['black'] = (x, y)
        return horse_positions
    


    def horse_possibilities(self):
        # Implement the logic to calculate horse movement possibilities
        valid_moves = []
        x, y = self.find_horse_positions()[ 'white' if self.turn == "White" else 'black']
        horse_moves = [
                (x - 2, y + 1), (x - 1, y + 2), (x + 1, y + 2), (x + 2, y + 1),
                (x + 2, y - 1), (x + 1, y - 2), (x - 1, y - 2), (x - 2, y - 1)
            ]
        for move in horse_moves:
            if 0 <= move[0] < MATRIX_SIZE and 0 <= move[1] < MATRIX_SIZE:
                if self.board[move[1]][move[0]] != 997 and self.board[move[1]][move[0]] != 998:
                    valid_moves.append(move)
                

        return valid_moves




    #metodos de dibujar el mapa
    def draw_map(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                image = CELLS.get(cell)
                screen.blit(
                    pygame.transform.scale(image, (MATRIX_CELL_SIZE, MATRIX_CELL_SIZE)),
                    (x * MATRIX_CELL_SIZE, y * MATRIX_CELL_SIZE),
                )



    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                print(f"{self.find_horse_positions()} : {self.horse_possibilities()}")

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_map()
            pygame.display.flip()


    def set_difficulty(self, difficulty):
        self.difficulty = difficulty



class GUI:
    def __init__(self):
        self.game = Game(screen)


    def display_game_title(self):
        global CURRENT_MENU_TITLE_COLOUR
        CURRENT_MENU_TITLE_COLOUR = (
            "RED_WOOD" if not CURRENT_MENU_TITLE_COLOUR == "RED_WOOD" else "WOOD"
        )
        text_surface = GAME_MENU_TITLE_FONT.render(
            GAME_NAME, True, COLOURS.get(CURRENT_MENU_TITLE_COLOUR)
        )
        text_rect = text_surface.get_rect(center=(SCREEN_MIDDLE_X_POS, 160))
        screen.blit(text_surface, text_rect)


    def run(self):
        while True:
            screen.fill(COLOURS.get("BEIGE"))
            self.display_game_title()

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
                            self.game.set_difficulty(button.text)
                            self.game.start_game()

            for button in BUTTONS:
                button.toggle_colour_on_hover(mouse_pos)
                button.draw(screen)

            pygame.display.flip()


if __name__ == "__main__":
    GUI().run()

