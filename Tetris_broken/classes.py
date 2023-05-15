from settings import *

class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 76)  # Assuming fontStyle is a string containing font file path and size

    def draw(self):
        pygame.draw.rect(window, self.hover_color if self.is_hovered else self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            print("Button pressed!")
