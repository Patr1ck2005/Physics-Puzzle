import pygame

from .base_ui import BaseUIBox
from .inventory import Inventory
from core.objects_manager import ObjectsManager


class ItemBar(BaseUIBox):
    def __init__(self, screen, space):
        super().__init__(screen)
        self.inventory = Inventory(screen)
        self.space = space
        self.item_uis = {}
        self.selected_item = None
        self.create_uis_for_items()

    def create_uis_for_items(self):
        for i, item in enumerate(self.inventory.items.values()):
            # 假设每个物体的图标为50x50，依次排开成三列
            ui_position = (10+(i % 3)*70, 10+(i//3)*70)
            # 设置物体对象的图标
            item_ui = BaseUI(self.screen, ui_position, item.color, item.name)
            # 设置物体对象的坐标在物品栏中
            item.position = ui_position
            self.item_uis[item.name] = item_ui

    def is_mouse_over(self, m_pos):
        for item_ui in self.item_uis.values():
            if item_ui.is_mouse_over(m_pos):
                return True
        for item in self.inventory.items.values():
            if item.is_mouse_over(m_pos):
                return True

    def on_click(self, m_pos):
        # for item in self.inventory.items.values():
        #     if item.on_click(m_pos):
        #         self.selected_item = item
        #         break
        for item_ui in self.item_uis.values():
            if item_ui.on_click(m_pos) and self.selected_item is None:
                self.selected_item = self.inventory.items[item_ui.name]
                break
            elif self.selected_item:
                self.selected_item.add_to_space(self.space, m_pos)
                self.selected_item = None
                break

    def render(self):
        for item_ui in self.item_uis.values():
            item_ui.draw(self.screen)
        for item in self.inventory.items.values():
            item.draw(self.screen)

