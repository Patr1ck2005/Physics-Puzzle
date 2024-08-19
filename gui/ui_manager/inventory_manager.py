from gui.phy_obj_ui.entity_ui import *
from gui.inventory.placeable_inventory import PlaceableInventory
from gui.inventory.tools_inventory import ToolsInventory


class InventoryManager:
    def __init__(self, screen):
        self.screen = screen
        self.placeable_inventory = PlaceableInventory(screen)
        self.tools_inventory = ToolsInventory(screen)
        self.item_bg_uis = {}
        self.placed_item = None
        self.selected_item = None
        self.selected_tool = None
        self.m_pos = None
        self._create_bg_uis_for_items()

    def _create_bg_uis_for_items(self):
        for i, item in enumerate(self.placeable_inventory.items.values()):
            # 设置每个物体的背景图标位置等于物体位置 (需要转化参考系)
            bg_ui_position = item.center[0] - 25, item.center[1] - 25
            # 设置物体对象的图标, 颜色淡化
            ico_color = [max(c - 100, 0) for c in item.ico_color]
            item_bg_ui = BaseUIBox(self.screen, item.name, bg_ui_position, (50, 50), ico_color=ico_color)
            self.item_bg_uis[item.name] = item_bg_ui

    def update(self, m_pos):
        self.placed_item = None
        self.m_pos = m_pos
        for item in self.placeable_inventory.items.values():
            if item.update(m_pos):
                return True
        for item_ui in self.item_bg_uis.values():
            if item_ui.update(m_pos):
                return True
        for tool_ui in self.tools_inventory.tools.values():
            if tool_ui.update(m_pos):
                return True

    def remove_item_by_name(self, name):
        self.placeable_inventory.remove_item_by_name(name)

    def clear_selection(self):
        self.selected_item = None
        self.selected_tool = None

    def on_click(self):
        # 先处理实体栏物品点击事件
        for item_ui in self.placeable_inventory.items.values():
            if item_ui.on_click(self.m_pos) and self.selected_item is None:
                self.selected_item = item_ui
                return item_ui
            elif self.selected_item:
                self.placed_item = self.selected_item
                self.selected_item = None
                return
        # 再处理工具栏物品点击事件
        for tool_ui in self.tools_inventory.tools.values():
            if tool_ui.on_click(self.m_pos):
                self.selected_tool = tool_ui
                return tool_ui
        # 最后处理物品栏背景点击事件
        for item_bg_ui in self.item_bg_uis.values():
            if item_bg_ui.on_click(self.m_pos):
                return item_bg_ui
        self.selected_tool = None
        return

    def on_press(self, m_pos):
        for item_ui in self.placeable_inventory.items.values():
            item_ui.on_press(m_pos)

    def on_release(self, m_pos):
        for item_ui in self.placeable_inventory.items.values():
            item_ui.on_release(m_pos)

    def render(self):
        for item_bg_ui in list(self.item_bg_uis.values())[::-1]:
            item_bg_ui.draw(self.screen)
        for item in list(self.placeable_inventory.items.values())[::-1]:
            item.draw(self.screen)
        for tool in list(self.tools_inventory.tools.values())[::-1]:
            tool.draw(self.screen)
        if self.selected_item or self.selected_tool:
            self.draw_mouse_mark()

    def draw_mouse_mark(self):
        pygame.draw.circle(self.screen, (0, 255, 0), self.m_pos, 5)

