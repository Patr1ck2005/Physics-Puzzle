from core.phy_object.constrain import *
from gui.base_ui import BaseUILine, BaseUICircle


class ConstrainUI(Constrain, BaseUICircle):
    def sync_ui(self):
        # 将 UI 位置同步为 Pymunk 位置
        self.set_click_region()
        if self.target_a is not None and self.target_b is not None:
            self.position = (self.target_a.center, self.target_b.center)

    def draw(self, m_pos):
        self.sync_ui()
        super().draw(m_pos)


class PinJointUI(PinJoint, BaseUICircle):
    def __init__(self, screen, name, position, width=20, color=(190, 120, 120)):
        PinJoint.__init__(self, name)
        BaseUICircle.__init__(self, screen, name, position, radius=width, ico_color=color)


class SlideJointUI(SlideJoint, BaseUICircle):
    def __init__(self, screen, name, position, width=20, color=(190, 120, 120)):
        SlideJoint.__init__(self, name)
        BaseUICircle.__init__(self, screen, name, position, width, ico_color=color)


class SpringUI(Spring, BaseUICircle):
    def __init__(self, screen, name, position, width=20, color=(190, 120, 120)):
        Spring.__init__(self, name)
        BaseUICircle.__init__(self, screen, name, position, width, ico_color=color)

