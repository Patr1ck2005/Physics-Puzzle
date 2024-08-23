from gui.phy_obj_ui.check_label_ui import CheckLabelUI
from gui.phy_obj_ui.entity_ui import EntityUIAddition
from gui.phy_obj_ui.force_ui import ForceUI

import pygame


class AdditionManager:
    running_forces: dict[str, ForceUI]
    running_labels: dict[str, CheckLabelUI]

    def __init__(self, space):
        self.space = space
        self.running_forces = {}
        self.running_labels = {}
        self.pressed_obj = None
        self.m_pos = None
        self.m_d_pos = None

        self.selected_item = None
        self.pre_placed_item = None

    def on_click(self) -> EntityUIAddition | None:
        for item_ui in self.running_labels.values():
            if item_ui.on_click(self.m_pos) and self.selected_item is None:
                self.selected_item = item_ui
                return item_ui
            elif self.selected_item:
                self.pre_placed_item = self.selected_item
                self.selected_item = None
                return
        for item_ui in self.running_forces.values():
            if item_ui.on_click(self.m_pos) and self.selected_item is None:
                self.selected_item = item_ui
                return item_ui
            elif self.selected_item:
                self.pre_placed_item = self.selected_item
                self.selected_item = None
                return

    def clear_selection(self):
        self.selected_item = None

    def update(self, m_pos):
        self.m_pos = m_pos
        for force in self.running_forces.values():
            force.update(m_pos)
        for label in self.running_labels.values():
            label.update(m_pos)

    def render_running_additions(self, screen):
        for force in self.running_forces.values():
            force.draw(screen)
        for label in self.running_labels.values():
            label.draw(screen)
        self.draw_mouse_mark(screen)

    def add_force(self, force):
        self.running_forces[force.name] = force

    # 用于初始化关卡
    def add_force_dict(self, force_dict):
        self.running_forces = {**self.running_forces, **force_dict}

    def add_label(self, label):
        self.running_labels[label.name] = label

    def draw_mouse_mark(self, screen):
        if self.selected_item:
            pygame.draw.circle(screen, (0, 0, 255), self.m_pos, 5)


