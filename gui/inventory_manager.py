from .object_ui import *
from .inventory import Inventory
from core.objects_manager import ObjectsManager


class ItemBar:
    def __init__(self, screen):
        self.screen = screen
        self.inventory = Inventory(screen)
        self.item_bg_uis = {}
        self.selected_item = None
        self.create_bg_uis_for_items()

    def create_bg_uis_for_items(self):
        for i, item in enumerate(self.inventory.items.values()):
            # 设置每个物体的背景图标位置等于物体位置 (需要转化参考系)
            bg_ui_position = item.center[0] - 25, item.center[1] - 25
            # 设置物体对象的图标, 颜色淡化
            ico_color = [max(c - 100, 0) for c in item.ico_color]
            item_bg_ui = BaseUIBox(self.screen, item.name, bg_ui_position, (50, 50), ico_color=ico_color)
            self.item_bg_uis[item.name] = item_bg_ui

    def is_mouse_over(self, m_pos):
        for item in self.inventory.items.values():
            if item.is_mouse_over(m_pos):
                return True
        for item_ui in self.item_bg_uis.values():
            if item_ui.is_mouse_over(m_pos):
                return True

    def on_click(self, m_pos):
        # 点击物体
        for item_ui in self.inventory.items.values():
            if item_ui.on_click(m_pos) and self.selected_item is None:
                self.selected_item = self.inventory.items[item_ui.name]
                return
            elif self.selected_item:
                copy = self.selected_item
                self.inventory.remove_item_by_name(self.selected_item.name)
                self.selected_item = None
                return copy

    def render(self):
        for item_bg_ui in self.item_bg_uis.values():
            item_bg_ui.draw(self.screen)
        for item in self.inventory.items.values():
            item.draw(self.screen)

