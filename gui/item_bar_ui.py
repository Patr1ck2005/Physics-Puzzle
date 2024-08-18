from .entity_ui import *
from .inventory_manager import InventoryManager
from core.objects_manager import ObjectManager


class ItemBar:
    def __init__(self, screen):
        self.screen = screen
        self.inventory_manager = InventoryManager(screen)
        self.item_bg_uis = {}
        self.placed_item = None
        self.selected_item = None
        self.create_bg_uis_for_items()

    def create_bg_uis_for_items(self):
        for i, item in enumerate(self.inventory_manager.items.values()):
            # 设置每个物体的背景图标位置等于物体位置 (需要转化参考系)
            bg_ui_position = item.center[0] - 25, item.center[1] - 25
            # 设置物体对象的图标, 颜色淡化
            ico_color = [max(c - 100, 0) for c in item.ico_color]
            item_bg_ui = BaseUIBox(self.screen, item.name, bg_ui_position, (50, 50), ico_color=ico_color)
            self.item_bg_uis[item.name] = item_bg_ui

    def is_mouse_over(self, m_pos):
        self.placed_item = None
        for item in self.inventory_manager.items.values():
            if item.is_mouse_over(m_pos):
                return True
        for item_ui in self.item_bg_uis.values():
            if item_ui.is_mouse_over(m_pos):
                return True

    def on_click(self, m_pos):
        # 点击物体
        for item_ui in self.inventory_manager.items.values():
            if item_ui.on_click(m_pos) and self.selected_item is None:
                self.selected_item = self.inventory_manager.items[item_ui.name]
                return
            elif self.selected_item:
                self.placed_item = self.selected_item
                self.inventory_manager.remove_item_by_name(self.selected_item.name)
                self.selected_item = None
                return

    def get_selected_item(self):
        return self.selected_item

    def get_placed_item(self):
        return self.placed_item

    def on_press(self, m_pos):
        for item_ui in self.inventory_manager.items.values():
            item_ui.on_press(m_pos)

    def on_release(self, m_pos):
        for item_ui in self.inventory_manager.items.values():
            item_ui.on_release(m_pos)

    def render(self):
        for item_bg_ui in list(self.item_bg_uis.values())[::-1]:
            item_bg_ui.draw(self.screen)
        for item in list(self.inventory_manager.items.values())[::-1]:
            item.draw(self.screen)

