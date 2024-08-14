import pygame


class BaseUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    @staticmethod
    def mark_underselection(color):
        return [min(int(50 + c), 255) for c in color]

    @staticmethod
    def mark_selection(color):
        return [int(0.6 * c) for c in color]