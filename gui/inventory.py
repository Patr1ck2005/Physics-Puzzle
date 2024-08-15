import pygame
import pymunk

from .base_ui import BaseUI
from core.object import GameObject


class Inventory(BaseUI):
    def __init__(self, screen):
        super().__init__(screen)
        self.items = {
            'ball_1': GameObject('ball_1', 'static', 'circle', color=(200, 0, 200)),
            'ball_2': GameObject('ball_2', 'dynamic', 'circle', color=(200, 0, 200)),
            'rect_1': GameObject('rect_1', 'static', 'box', size=(20, 60), color=(200, 200, 200)),
            'rect_2': GameObject('rect_2', 'dynamic', 'box', size=(60, 20), color=(200, 200, 200)),
        }
        self.selecting = None

    def add_item(self, item):
        self.items[item.name] = item

    def remove_item(self, name):
        self.items.pop(name)

    def get_item(self, name):
        return self.items[name]

    def draw(self):
        for i, item in enumerate(self.items.values()):
            # 假设每个物体的图标为50x50，依次排开成三列
            icon_rect = pygame.Rect(10+(i % 3)*90, 10+(i//3)*90, 60, 60)
            # 设置物体对象的图标
            item.icon_rect = icon_rect
            # 对于选择的图标变色处理
            if item == self.selecting:
                color = self.mark_underselection(item.color)
            else:
                color = item.color
            # 绘制
            pygame.draw.rect(self.screen, color, icon_rect)

    def select_inventory(self) -> (GameObject, tuple):
        self.selecting = None
        # 获取鼠标位置
        m_pos = pygame.mouse.get_pos()
        for item in self.items.values():
            if item.icon_rect and item.icon_rect.collidepoint(m_pos):
                self.selecting = item
        return self.selecting, m_pos

