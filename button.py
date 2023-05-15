import pygame
from main import *
from assets import *

class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont(pygame.font.fontStyle[0], 76)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.hover_color if self.is_hovered else self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()