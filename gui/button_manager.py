import pygame
from .base_ui import BaseUIBox, BaseUICircle
from settings import *


class ButtonManager:
    def __init__(self, screen):
        self.screen = screen
        self.all_buttons = {
            "setting": BaseUICircle(screen, "setting", (SCREEN_WIDTH - 100, 30), 30,
                                    text='setting', ico_color=(170, 170, 170)),
            "rewind ": BaseUICircle(screen, "rewind", (50, SCREEN_HEIGHT-50), 20,
                                 text='rewind', ico_color=(80, 80, 80)),
            "slow": BaseUICircle(screen, "slow", (200, SCREEN_HEIGHT - 50), 20,
                                 text='slow', ico_color=(80, 80, 80)),
            "pause/resume": BaseUICircle(screen, "pause/resume", (250, SCREEN_HEIGHT - 50), 20,
                                         text='pause', ico_color=(80, 80, 80)),
            "speed": BaseUICircle(screen, "speed", (300, SCREEN_HEIGHT - 50), 20,
                                  text='speed', ico_color=(80, 80, 80)),
        }

    def is_mouse_over(self, m_pos):
        for btn in self.all_buttons.values():
            btn.is_mouse_over(m_pos)

    def on_click(self, m_pos):
        for btn in self.all_buttons.values():
            if btn.on_click(m_pos):
                return btn

    def render(self):
        for btn in self.all_buttons.values():
            btn.draw(self.screen)
