import pygame

from core.object import GameObject, BoxObject, CircleObject
from .base_ui import BaseUI, BaseUIBox, BaseUICircle


class ObjectUI(GameObject, BaseUI):

    @property
    def position(self):
        return self.rect_pos

    @position.setter
    def position(self, pos):
        self.rect_pos = pos

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, pos):
        self._center = pos
        if self.body is not None:
            self.body.position = pos

    @property
    def rect_pos(self):
        return 0

    @rect_pos.setter
    def rect_pos(self, pos):
        pass

    # 将UI的位置和pymunk位置关联在一起
    def sync_ui(self):
        # 将 UI 位置同步为 Pymunk 位置
        self.set_click_region()
        self.center = self.body.position


class BoxObjectUI(ObjectUI, BoxObject, BaseUIBox):
    def __init__(self, screen, name, phy_type, position, angle=0, size=(30, 30), color=(150, 150, 150)):
        BoxObject.__init__(self, name, phy_type, position, angle, size)
        BaseUIBox.__init__(self, screen, name, position, size, color)

    # 将UI的位置和pymunk位置关联在一起
    def sync_ui(self):
        # 将 UI 位置同步为 Pymunk 位置
        self.set_click_region()
        self.center = self.body.position

    @property
    def rect_pos(self):
        return self._center[0]-self.size[0]/2, self._center[1]-self.size[1]/2

    @rect_pos.setter
    def rect_pos(self, pos):
        self._center = pos[0]+self.size[0]/2, pos[1]+self.size[1]/2
        if self.body is not None:
            self.body.position = pos[0]+self.size[0]/2, pos[1]+self.size[1]/2


class CircleObjectUI(ObjectUI, CircleObject, BaseUICircle):
    def __init__(self, screen, name, phy_type, center, angle=0, r=20, color=(150, 150, 150)):
        CircleObject.__init__(self, name, phy_type, center, angle, r)
        BaseUICircle.__init__(self, screen, name, center, r, color)

    @property
    def rect_pos(self):
        return self._center[0]-self.size, self._center[1]-self.size

    @rect_pos.setter
    def rect_pos(self, pos):
        self._center = pos[0]+self.size, pos[1]+self.size
        if self.body is not None:
            self.body.position = pos[0]+self.size, pos[1]+self.size

