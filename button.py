import pygame
from colours import COLOURS


class Button:
    def __init__(self, text, pos):
        font = pygame.font.Font(None, 36)
        self.text = text
        self.rect = pygame.Rect(0, 0, 200, 60)
        self.rect.center = pos
        self.colour = COLOURS.get("SECONDARY")
        self.text_surf = font.render(text, True, COLOURS.get("BLACK"))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surf):
        pygame.draw.rect(surf, self.colour, self.rect, border_radius=10)
        surf.blit(self.text_surf, self.text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def toggle_colour_on_hover(self, pos):
        self.colour = (
            COLOURS.get("RED_WOOD") if self.is_hovered(pos) else COLOURS.get("WOOD")
        )
