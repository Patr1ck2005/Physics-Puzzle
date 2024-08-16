import pygame
from base_ui import BaseUIBox, BaseUICircle


class ButtonManager:
    def __init__(self, name, position):
        self.position = position
        self.button_name = name

