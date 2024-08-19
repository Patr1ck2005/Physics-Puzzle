import math

import pygame

from core.phy_object.entity import Entity, BoxEntity, CircleEntity
from gui.base_ui import BaseUI, BaseUIBox, BaseUICircle


class EntityUI(Entity, BaseUI):

    @property
    def position(self):
        return self.rect_pos

    @position.setter
    def position(self, pos):
        self.rect_pos = pos
        self.set_click_region()

    @property
    def angle(self):
        return self.body.angle

    @angle.setter
    def angle(self, angle):
        self.body.angle = angle

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, pos):
        self._center = pos
        self.set_click_region()
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

    def update(self, m_pos):
        Entity.record(self)
        BaseUI.update(self, m_pos)

    def draw(self, screen):
        # 目前简单对于图像覆盖处理
        self.sync_ui()
        self.draw_mark(screen)
        self.draw_draft(screen)
        if self.ico is not None:
            angle_degrees = math.degrees(self.angle)
            rotated_image = pygame.transform.rotate(self.ico, -angle_degrees)
            rotated_rect = rotated_image.get_rect(center=self._center)
            screen.blit(rotated_image, rotated_rect.topleft)


class BoxEntityUI(EntityUI, BoxEntity, BaseUIBox):
    def __init__(self, screen, name, phy_type, position, angle=0, size=(30, 30), ico_path=None, color=(150, 150, 150)):
        BoxEntity.__init__(self, name, phy_type, position, angle, size)
        BaseUIBox.__init__(self, screen, name, position, size, ico_path=ico_path, ico_color=color)

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


class CircleEntityUI(EntityUI, CircleEntity, BaseUICircle):
    def __init__(self, screen, name, phy_type, center, angle=0, r=20, ico_path=None, color=(150, 150, 150)):
        CircleEntity.__init__(self, name, phy_type, center, angle, r)
        BaseUICircle.__init__(self, screen, name, center, r, ico_path=ico_path, ico_color=color)

    @property
    def rect_pos(self):
        return self._center[0]-self.size, self._center[1]-self.size

    @rect_pos.setter
    def rect_pos(self, pos):
        self._center = pos[0]+self.size, pos[1]+self.size
        if self.body is not None:
            self.body.position = pos[0]+self.size, pos[1]+self.size

    def draw_icon(self, surface):
        pygame.draw.circle(surface, self.ico_color, (surface.get_width()//2, surface.get_height()//2), self.size)


class BlankEntityUI(Entity, BaseUI):
    def __init__(self, name='Blank', phy_type='None', center=(0, 0), angle=0, size=(0, 0), ico_color=(150, 150, 150)):
        self.name = name
        self.type = phy_type
        self.shape = None
        self.ico_color = ico_color
        self.history_x = (0, 0)
        self.history_y = (0, 0)
        self.history_angle = (0, 0)

    @property
    def center(self):
        return (0, 0)

    @property
    def angle(self):
        return 0

    @property
    def mass(self):
        return 0

    @property
    def moment(self):
        return 0

    @property
    def velocity(self):
        return (0, 0)

    @property
    def angular_velocity(self):
        return 0

    @property
    def friction(self):
        return 0

    @property
    def elasticity(self):
        return 0

    def draw_icon(self, surface):
        pygame.draw.circle(surface, self.ico_color, (surface.get_width()//2, surface.get_height()//2), 10)
