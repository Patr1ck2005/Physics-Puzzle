import pygame

from .base_ui import BaseUI


class Inventory(BaseUI):
    def __init__(self, screen):
        super().__init__(screen)
        self.items = {}
        self.selecting = None

    def add_item(self, item):
        self.items[item.name] = item

    def remove_item(self, item):
        self.items.pop(item.name)

    def get_item(self, name):
        return self.items[name]

    def draw(self):
        for i, item in enumerate(self.items):
            # 假设每个物体的图标为50x50，依次排开成两列
            icon_rect = pygame.Rect(10+(i % 2)*60, 10+(i//2)*60, 50, 50)
            # 对于选择的图标变色处理
            if item == self.selecting:
                color = self.mark_underselection(item["color"])
            else:
                color = item["color"]
            # 绘制
            pygame.draw.rect(self.screen, color, icon_rect)

    def select_inventory(self):
        self.selecting = None
        # 获取鼠标位置
        m_pos = pygame.mouse.get_pos()
        for item in self.items:
            if item["rect"].collidepoint(m_pos):
                self.selecting = item
        return self.selecting, m_pos

