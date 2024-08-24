import numpy as np
import pygame.draw

from gui.base_ui import BaseUIRect
from gui.phy_obj_ui.obj_ui import ObjUIAddition


class CheckLabelUI(BaseUIRect):
    placed_on_object: ObjUIAddition | None

    def __init__(self, name,
                 property_name, expected_value,
                 ico_path=None, color=(200, 200, 200), **kwargs):
        BaseUIRect.__init__(self, name, (0, 0), (50, 30), property_name, ico_path=ico_path, ico_color=color)
        self.name = name  # 标签的名字
        self.property_name = property_name  # 标签追踪的物理属性名，例如 "velocity" 或 "position"
        self.expected_value = expected_value  # 标签期望的物理属性值
        self.is_placed = False  # 判断标签是否已被放置
        self.target = None  # 记录放置的物体

    def set_target(self, game_object):
        self.is_placed = True
        self.target = game_object

    def check_correctness(self):
        actual_value = getattr(self.target, self.property_name)

        if isinstance(actual_value, (int, float)):
            return round(actual_value/10) == round(self.expected_value/10)
        else:
            for coord, expected_coord in zip(actual_value, self.expected_value):
                if round(coord/10) != round(expected_coord/10):
                    return False
            return True

    def update(self, m_pos):
        if self.target:
            if self.check_correctness():
                self._color = (0, 200, 0)  # ��确时��色为���色
            else:
                self._color = (200, 0, 0)
        else:
            self._color = self.ico_color
        super().update(m_pos)

    # 将UI的位置和受力物体位置关联在一起
    def sync_ui(self):
        # 将 UI 位置同步为 Pymunk 位置, 并设置偏离
        self.ui_center = self.target.center + (60, -40)

    def draw(self, screen):
        if self.target:
            self.sync_ui()
            mid_pos = (self.ui_center[0] - 15, self.ui_center[1] + 30)
            btm_pos = (self.ui_center[0], self.ui_center[1] + 15)
            pygame.draw.line(screen, (200, 200, 200), self.target.center, mid_pos, 3)
            pygame.draw.line(screen, (200, 200, 200), mid_pos, btm_pos, 3)
        super().draw(screen)


class RoughCheckLabelUI(CheckLabelUI):
    rough_range: tuple

    def __init__(self, name,
                 property_name, rough_range: tuple,
                 ico_path=None, color=(200, 200, 200), **kwargs):
        super().__init__(name, property_name, None, ico_path, color, **kwargs)
        self.rough_range = rough_range

    def check_correctness(self):
        actual_value = getattr(self.target, self.property_name)
        if isinstance(actual_value, (int, float)):
            return self.rough_range[0] <= actual_value <= self.rough_range[1]
        else:
            for coord in actual_value:
                if not (self.rough_range[0] <= coord <= self.rough_range[1]):
                    return False
            return True
