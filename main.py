import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Difficulty Menu")
font = pygame.font.Font(None, 36)

SECONDARY = (179, 45, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)


class Button:
    def __init__(self, text, pos):
        self.text = text
        self.rect = pygame.Rect(0, 0, 200, 60)
        self.rect.center = pos
        self.color = GRAY
        self.text_surf = font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=10)
        surf.blit(self.text_surf, self.text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


def main():
    buttons = [
        Button("Beginner", (250, 150)),
        Button("Amateur", (250, 230)),
        Button("Expert", (250, 310)),
    ]

    while True:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_hovered(mouse_pos):
                        print(f"Selected difficulty: {button.text}")

        for button in buttons:
            button.color = SECONDARY if button.is_hovered(mouse_pos) else GRAY
            button.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
