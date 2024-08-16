import pygame

from core.object import GameObject, BoxObject, CircleObject
from .base_ui import BaseUI, BaseUIBox, BaseUICircle


class ObjectUI(GameObject, BaseUI):

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        if self.body is not None:
            self.body.position = value

    @property
    def center(self):
        return 0

    @center.setter
    def center(self, pos):
        pass

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
        self.position = self.body.position

    def add_to_space(self, space, loc):
        self.body.position = loc
        space.add(self.body, self.body_shape)


class BoxObjectUI(ObjectUI, BoxObject, BaseUIBox):
    def __init__(self, screen, name, phy_type, position, size=(30, 30), color=(150, 150, 150)):
        BoxObject.__init__(self, name, phy_type, position, size)
        BaseUIBox.__init__(self, screen, name, position, size, color)

    @property
    def center(self):
        return self.position[0]+self.size[0]/2, self.position[1]+self.size[1]/2

    @center.setter
    def center(self, pos):
        self.position = pos[0]-self.size[0]/2, pos[1]-self.size[1]/2

    @property
    def rect_pos(self):
        return self.position

    @rect_pos.setter
    def rect_pos(self, pos):
        self.position = pos


class CircleObjectUI(ObjectUI, CircleObject, BaseUICircle):
    def __init__(self, screen, name, phy_type, center, r=20, color=(150, 150, 150)):
        CircleObject.__init__(self, name, phy_type, center, r)
        BaseUICircle.__init__(self, screen, name, center, r, color)

    @property
    def center(self):
        return self.position

    @center.setter
    def center(self, pos):
        self.position = pos

    @property
    def rect_pos(self):
        return self.position[0]-self.size, self.position[1]-self.size

    @rect_pos.setter
    def rect_pos(self, pos):
        self.position = pos[0]-self.size, pos[1]-self.size

