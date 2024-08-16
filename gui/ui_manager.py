from .hud import HUD
from .inventory_manager import ItemBar


class UIManager:
    def __init__(self, screen, space, obj_manager):
        self.screen = screen
        self.obj_manager = obj_manager(space)
        self.hud = HUD(screen)
        self.item_bar = ItemBar(screen)
        self.all_uis = [self.item_bar, self.obj_manager]
        self.clicked_ui = []
        self.selected_item = None
        self.m_pos = None

    # 依次检测鼠标是否放置到指定UI
    def update(self, m_pos):
        self.m_pos = m_pos
        for ui in self.all_uis:
            ui.is_mouse_over(self.m_pos)

    # 依次检测是否点击到指定UI
    def on_click(self):
        selected_item = self.item_bar.on_click(self.m_pos)
        if self.selected_item is None:
            self.selected_item = selected_item
        else:
            self.obj_manager.add_obj(self.selected_item)
            self.item_bar.inventory.remove_item(self.selected_item)
            self.selected_item = None

    # 依次渲染所有UI
    def render_all_ui(self):
        for ui in self.all_uis:
            ui.render()
        self.hud.render()


