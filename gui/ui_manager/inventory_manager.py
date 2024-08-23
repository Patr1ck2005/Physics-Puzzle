from gui.base_ui import BaseUIRect
from gui.phy_obj_ui.entity_ui import *
from gui.inventory.placeable_inventory import PlaceableInventory
from gui.inventory.tools_inventory import ToolsInventory


class InventoryManager:
    '''
    库存管理器类，负责管理可放置物品和工具的库存，以及它们的用户界面。
    '''
    def __init__(self):
        '''
        初始化库存管理器，创建可放置物品和工具的库存实例，并初始化相关变量。
        '''
        self.placeable_inventory = PlaceableInventory()
        self.tools_inventory = ToolsInventory()
        self.labels = {}
        self.item_bg_uis = {}
        self.pre_placed_item = None
        self.selected_item = None
        self.selected_tool = None
        self.m_pos = None
        self._create_bg_uis_for_items()

    def _create_bg_uis_for_items(self):
        '''
        为可放置物品创建背景界面。
        '''
        for i, item in enumerate(self.placeable_inventory.items.values()):
            # 设置每个物体的背景图标位置等于物体位置 (需要转化参考系)
            bg_ui_position = item.center[0] - 25, item.center[1] - 25
            # 设置物体对象的图标, 颜色淡化
            ico_color = [max(c - 100, 0) for c in item.ico_color]
            item_bg_ui = BaseUIRect(item.name, bg_ui_position, (50, 50), ico_color=ico_color)
            self.item_bg_uis[item.name] = item_bg_ui

    def update(self, m_pos):
        '''
        更新库存管理器的状态，包括鼠标位置和物品、工具的状态。
        '''
        self.pre_placed_item = None
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

    def add_item_dict(self, item_dict: dict):
        '''
        向库存中添加物品字典，并重新创建物品的背景用户界面。
        '''
        self.placeable_inventory.add_item_dict(item_dict)
        self.tools_inventory.add_item_dict(item_dict)
        self._create_bg_uis_for_items()

    def remove_item_by_name(self, name):
        '''
        根据名称从库存中移除物品。
        '''
        self.placeable_inventory.remove_item_by_name(name)

    def clear_selection(self):
        '''
        清除当前选中的物品和工具。
        '''
        self.selected_item = None
        self.selected_tool = None

    def on_click(self):
        '''
        处理鼠标点击事件，更新选中的物品或工具。
        '''
        for item_ui in self.placeable_inventory.items.values():
            if item_ui.on_click(self.m_pos) and self.selected_item is None:
                self.selected_item = item_ui
                return item_ui
            elif self.selected_item:
                self.pre_placed_item = self.selected_item
                self.selected_item = None
                return
        for tool_ui in self.tools_inventory.tools.values():
            if tool_ui.on_click(self.m_pos):
                self.selected_tool = tool_ui
                return tool_ui
        for item_bg_ui in self.item_bg_uis.values():
            if item_bg_ui.on_click(self.m_pos):
                return item_bg_ui
        self.selected_tool = None
        return

    def on_press(self, m_pos):
        '''
        处理鼠标按下事件，更新物品的状态。
        '''
        for item_ui in self.placeable_inventory.items.values():
            item_ui.on_press(m_pos)

    def on_release(self, m_pos):
        '''
        处理鼠标释放事件，更新物品的状态。
        '''
        for item_ui in self.placeable_inventory.items.values():
            item_ui.on_release(m_pos)

    def render(self, screen):
        '''
        渲染库存中的物品和工具到屏幕上。
        '''
        for item_bg_ui in list(self.item_bg_uis.values())[::-1]:
            item_bg_ui.draw(screen)
        for item in list(self.placeable_inventory.items.values())[::-1]:
            item.draw(screen)
        for tool in list(self.tools_inventory.tools.values())[::-1]:
            tool.draw(screen)
        if self.selected_item or self.selected_tool:
            self.draw_mouse_mark(screen)

    def draw_mouse_mark(self, screen):
        '''
        在鼠标位置绘制标记。
        '''
        pygame.draw.circle(screen, (0, 255, 0), self.m_pos, 5)
