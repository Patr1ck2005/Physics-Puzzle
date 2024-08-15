import pygame

from .base_ui import BaseUI
from core.object import GameObject, CircleObject, BoxObject


class Inventory(BaseUI):
    def __init__(self, screen):
        super().__init__(screen)
        self.items = {
            'ball_1': CircleObject(screen, 'ball_1', 'static', color=(200, 0, 200)),
            'ball_2': CircleObject(screen, 'ball_2', 'dynamic', color=(200, 0, 200)),
            'ball_3': CircleObject(screen, 'ball_3', 'kinematic', color=(200, 0, 200)),
            'rect_1': BoxObject(screen, 'rect_1', 'static', size=(20, 60), color=(200, 200, 200)),
            'rect_2': BoxObject(screen, 'rect_2', 'dynamic', size=(60, 20), color=(200, 200, 200)),
            'rect_3': BoxObject(screen, 'rect_3', 'kinematic', size=(60, 20), color=(200, 200, 200)),
        }
        self.selecting = None

    def add_item(self, item):
        self.items[item.name] = item

    def remove_item(self, name):
        self.items.pop(name)

    def get_item(self, name):
        return self.items[name]

    def select_inventory(self) -> (GameObject, tuple):
        self.selecting = None
        # 获取鼠标位置
        m_pos = pygame.mouse.get_pos()
        for item in self.items.values():
            if item.icon_rect and item.icon_rect.collidepoint(m_pos):
                self.selecting = item
        return self.selecting, m_pos

