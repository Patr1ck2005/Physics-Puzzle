import pygame

from core.object import BoxObject, CircleObject
from .base_ui import BaseUIBox, BaseUICircle


class BoxObjectUI(BoxObject, BaseUIBox):
    def __init__(self, screen, position, name, phy_type, size=(30, 30), color=(150, 150, 150)):
        BoxObject.__init__(self, position, name, phy_type, size)
        BaseUIBox.__init__(self, screen, position, name, size, color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, *self.size))
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.position[0] + 10, self.position[1] + 5))


class CircleObjectUI(CircleObject, BaseUICircle):
    def __init__(self, screen, position, name, phy_type, r=30, color=(150, 150, 150)):
        CircleObject.__init__(self, position, name, phy_type, r)
        BaseUICircle.__init__(self, screen, position, name, r, color)

    def draw(self, screen):
        center_p = (self.position[0] + self.size, self.position[1] + self.size)
        pygame.draw.circle(screen, self.color, center_p, self.size)
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.position[0] + 10, self.position[1] + 5))