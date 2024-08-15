import pygame
from base_ui import BaseUI


class ButtonArea:
    def __init__(self, name, position):
        self.position = position
        self.button_name = name

    def draw(self, surface):
        pygame.draw.rect(surface, (150, 150, 150), (self.position[0], self.position[1], 100, 30))
        text = pygame.font.SysFont(None, 24).render(self.button_name, True, (255, 255, 255))
        surface.blit(text, (self.position[0] + 10, self.position[1] + 5))
