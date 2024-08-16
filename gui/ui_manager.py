from .hud import HUD
from .inventory_manager import ItemBar
from core.objects_manager import ObjectsManager


class UIManager:
    def __init__(self, screen, obj_manager: ObjectsManager):
        self.screen = screen
        self.obj_manager = obj_manager
        self.hud = HUD(screen)
        self.item_bar = ItemBar(screen)
        self.all_uis = [self.item_bar]
        self.clicked_ui = []
        self.m_pos = None

    # 依次检测鼠标是否放置到指定UI
    def update(self, m_pos):
        self.m_pos = m_pos
        for ui in self.all_uis:
            ui.is_mouse_over(self.m_pos)

    # 检测UI是否被点击
    def on_click(self):
        selected_item = self.item_bar.on_click(self.m_pos)
        if selected_item is not None:
            self.obj_manager.add_obj(selected_item)

    # 依次渲染所有UI
    def render_all_ui(self):
        for ui in self.all_uis:
            ui.render()
        self.hud.render()


