import pygame

from core.phy_object.force import AbstractForce
from gui.base_ui import BaseUICircle

from pymunk import Vec2d


class ForceUI(AbstractForce, BaseUICircle):
    def __init__(self, name, force=Vec2d(0, 0), loc=(0, 0), target=None):
        AbstractForce.__init__(self, force, loc, target)
        BaseUICircle.__init__(self, name, loc, radius=10, ico_color=(100, 100, 100))

    @property
    def center(self):
        return self.ui_center

    @center.setter
    def center(self, pos):
        self.ui_center = pos
        self.set_click_region()

    def update(self, m_pos):
        # 在这里可以更新力, 例如实现力的'圆周运动'
        # self.force = self.force.rotated(0.1)
        BaseUICircle.update(self, m_pos)
        AbstractForce.update(self)

    # 将UI的位置和受力物体位置关联在一起
    def sync_ui(self):
        # 将 UI 位置同步为 Pymunk 位置
        self.ui_center = self.target.center

    def draw_draft(self, screen):
        if self.target:
            self.sync_ui()
        super().draw_draft(screen)
        # 计算箭头的终点
        arrow_end = self.ui_center + self.force/5

        # 绘制力的箭头
        pygame.draw.line(screen, (255, 0, 0), self.ui_center, arrow_end, 3)  # 绘制主线段

        # 箭头的尺寸和角度
        arrow_size = 10
        angle = self.force.angle
        arrow_angle1 = angle + 0.3  # 箭头角度偏移
        arrow_angle2 = angle - 0.3

        # 计算箭头两边的点
        arrow_point1 = arrow_end - Vec2d(arrow_size, 0).rotated(arrow_angle1)
        arrow_point2 = arrow_end - Vec2d(arrow_size, 0).rotated(arrow_angle2)

        # 绘制箭头的两个边
        pygame.draw.line(screen, (255, 0, 0), arrow_end, arrow_point1, 3)
        pygame.draw.line(screen, (255, 0, 0), arrow_end, arrow_point2, 3)


