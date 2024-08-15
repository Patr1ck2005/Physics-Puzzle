from .hud import HUD
from .item_bar import ItemBar

import pygame


class UIManager:
    def __init__(self, screen, space):
        self.screen = screen
        self.hud = HUD(screen)
        self.item_bar = ItemBar(screen, space)
        self.all_uis = [self.item_bar]
        self.clicked_ui = []
        self.m_pos = None

    def detect_m_pos(self):
        self.m_pos = pygame.mouse.get_pos()

    # 依次检测鼠标是否放置到指定UI
    def update(self):
        self.detect_m_pos()
        for ui in self.all_uis:
            ui.is_mouse_over(self.m_pos)

    # 依次检测是否点击到指定UI
    def on_click(self):
        for ui in self.all_uis:
            ui.on_click(self.m_pos)

    # 依次渲染所有UI
    def render_all_ui(self):
        for ui in self.all_uis:
            ui.render()
        self.hud.render()


