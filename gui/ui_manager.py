from .hud import HUD
from .item_bar_ui import ItemBar
from .button_manager import ButtonManager
from core.objects_manager import ObjectsManager


class UIManager:
    def __init__(self, screen, engine, obj_manager: ObjectsManager):
        self.screen = screen
        self.engine = engine
        self.hud = HUD(screen)
        self.obj_manager = obj_manager
        self.btn_manager = ButtonManager(screen)
        self.item_bar = ItemBar(screen)
        self.all_uis = [self.item_bar, self.btn_manager.all_buttons]
        self.clicked_ui = []
        self.m_pos = None

    # 依次检测鼠标是否悬停于指定UI
    def update(self, m_pos):
        self.m_pos = m_pos
        self.item_bar.is_mouse_over(self.m_pos)
        self.btn_manager.is_mouse_over(self.m_pos)

    # 检测UI是否被点击
    def on_click(self):
        # 获取物品栏放置结果
        placed_item = self.item_bar.on_click(self.m_pos)
        # 更新HUD显示物品栏选择结果(由于选择机制, 必须放在后面)
        self.hud.current_selection = self.item_bar.get_selected_item()
        if placed_item is not None:
            self.obj_manager.add_obj(placed_item)
        call_btn = self.btn_manager.on_click(self.m_pos)
        self.match_btn_call(call_btn)

    # 若鼠标长按则撤回点击事件
    def call_back_click(self):
        pass

    def on_press(self):
        self.item_bar.on_press(self.m_pos)

    def on_release(self):
        self.item_bar.on_release(self.m_pos)

    # 依次渲染所有UI
    def render_all_ui(self):
        self.item_bar.render()
        self.btn_manager.render()
        self.hud.render()

    def match_btn_call(self, btn):
        if btn is None:
            return
        elif btn.name == 'pause/resume':
            self.engine.pause = not self.engine.pause
            btn.text = 'resume' if self.engine.pause else 'pause'
        elif btn.name == 'restart':
            self.engine.init_world()
        elif btn.name == 'speed':
            self.engine.time_scale *= 2.0
            self.hud.update_time_scale(self.engine.time_scale)
        elif btn.name == 'slow':
            self.engine.time_scale *= 0.5
            self.hud.update_time_scale(self.engine.time_scale)


