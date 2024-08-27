import pygame

from core.phy_object.constrain import *
from gui.base_ui import BaseUILine, BaseUICircle
from settings import *


class ConstrainUI(Constrain, BaseUICircle):
    @property
    def center(self):
        return self.ui_center

    @center.setter
    def center(self, pos):
        self.ui_center = pos

    def sync_ui(self):
        # 将 UI 位置同步为 Pymunk 位置
        if self.target_a is not None and self.target_b is not None:
            pass
            # self.ui_center = (self.target_a.center+self.target_b.center)//2
        self.set_click_region()

    def draw(self, screen):
        self.sync_ui()
        if self.target_a and self.target_b:  # 此时已经被添加到世界中
            pass
        else:  # 此时仍在物品栏中
            super().draw(screen)

    def draw_draft(self, screen):
        if self.target_a is None and self.target_b is None:  # ��时��在物品��中, ��制����线条
            super().draw_draft(screen)
        elif self.target_a and not self.target_b:
            pygame.draw.line(screen, WHITE, self.target_a.center+self.anchor_a, pygame.mouse.get_pos(), 3)


class PinJointUI(ConstrainUI, PinJoint, BaseUICircle):
    def __init__(self, name, position, width=20, color=(190, 120, 120),
                 target_a=None, target_b=None, anchor_a=(0, 0), anchor_b=(0, 0)):
        PinJoint.__init__(self, name, target_a, target_b, anchor_a, anchor_b)
        BaseUICircle.__init__(self, name, position, radius=width, ico_color=color)


class SlideJointUI(ConstrainUI, SlideJoint, BaseUICircle):
    def __init__(self, name, position, width=20, color=(190, 120, 120),
                 target_a=None, target_b=None, anchor_a=(0, 0), anchor_b=(0, 0)):
        SlideJoint.__init__(self, name, target_a, target_b, anchor_a, anchor_b)
        BaseUICircle.__init__(self, name, position, width, ico_color=color)


class SpringUI(ConstrainUI, Spring, BaseUICircle):
    def __init__(self, name, position, width=20, color=(190, 120, 120),
                 target_a=None, target_b=None, anchor_a=(0, 0), anchor_b=(0, 0)):
        Spring.__init__(self, name, target_a, target_b, anchor_a, anchor_b)
        BaseUICircle.__init__(self, name, position, radius=width, ico_color=color)

