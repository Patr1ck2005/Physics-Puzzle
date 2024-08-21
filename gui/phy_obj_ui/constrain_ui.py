from core.phy_object.constrain import *
from gui.base_ui import BaseUILine, BaseUICircle


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
            self.ui_center = (self.target_a.center, self.target_b.center)
        self.set_click_region()

    def draw(self, m_pos):
        self.sync_ui()
        super().draw(m_pos)


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

