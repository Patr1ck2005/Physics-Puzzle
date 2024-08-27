import pygame

from core.phy_object.bg_wall import BGWall
from gui.base_ui import BaseUICircle, BaseUIRect, BaseUI


class BGWallUIAddition(BGWall, BaseUI):
    @property
    def center(self):
        return self.ui_center

    @center.setter
    def center(self, pos):
        self.ui_center = pos
        self.set_click_region()

    def add_to_space(self, space, center_pos=None):
        space.add(self.body)
        self.center = center_pos if center_pos else self.ui_center


class CircleBGWallUI(BGWallUIAddition, BGWall, BaseUICircle):
    def __init__(self, name, center, radius, **kwargs):
        BGWall.__init__(self)
        BaseUICircle.__init__(self, name, center, radius)

    def draw_draft(self, screen):
        # 创建一个支持透明的Surface
        circle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        # 透明度 (0-255), 其中 0 是完全透明，255 是完全不透明
        alpha = 128
        # 绘制一个透明的圆形
        pygame.draw.circle(circle_surface, (*self._color, alpha), (self.size, self.size), self.size)
        # 将圆形Surface绘制到屏幕上
        screen.blit(circle_surface, (self._center[0] - self.size, self._center[1] - self.size))
        # 绘制文字
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self._center[0] - self.size, self._center[1] - 10))


class RectBGWallUI(BGWallUIAddition, BGWall, BaseUIRect):
    def __init__(self, name, position, size, **kwargs):
        BGWall.__init__(self)
        BaseUIRect.__init__(self, name, position, size)

    def draw_draft(self, screen):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        alpha = 128
        pygame.draw.rect(surface, (*self._color, alpha), (0, 0, *self.size))
        screen.blit(surface, self.position)
        # 绘制文字
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, self.position)


class PolyBGWallUI(BGWallUIAddition, BGWall, BaseUICircle):
    def __init__(self, name, points, **kwargs):
        BGWall.__init__(self)
        BaseUICircle.__init__(self, name, points)



