from pymunk import Vec2d

from gui.phy_obj_ui.entity_ui import EntityUI

import pymunk


class Constrain:
    target_a: None | EntityUI
    target_b: None | EntityUI

    def __init__(self, name, target_a=None, target_b=None, anchor_a=Vec2d(0, 0), anchor_b=Vec2d(0, 0)):
        self.name = name
        self.target_a = target_a
        self.target_b = target_b
        self.anchor_a = anchor_a
        self.anchor_b = anchor_b

        self.constraint = None

    def set_target_a(self, target_a):
        self.target_a = target_a

    def set_target_b(self, target_b):
        self.target_b = target_b

    def add_to_space(self, space):
        pass
        space.add(self.constraint)


# 轻杠
class PinJoint(Constrain):
    def __init__(self, name, target_a, target_b, anchor_a, anchor_b):
        super().__init__(name, target_a, target_b, anchor_a, anchor_b)

    def add_to_space(self, space):
        self.constraint = pymunk.PinJoint(self.target_a.body, self.target_b.body,
                                          self.anchor_a, self.anchor_b)
        super().add_to_space(space)

    def remove_from_space(self):
        pass


# 轻绳
class SlideJoint(Constrain):
    def __init__(self, name, target_a, target_b, anchor_a, anchor_b):
        super().__init__(name, target_a, target_b, anchor_a, anchor_b)

    def add_to_space(self, space):
        init_length = (self.target_a.center+self.anchor_a - self.target_b.center-self.anchor_b).length
        self.constraint = pymunk.SlideJoint(self.target_a.body, self.target_b.body,
                                            self.anchor_a, self.anchor_b,
                                            min=0, max=init_length)
        super().add_to_space(space)


# 弹簧
class Spring(Constrain):
    def __init__(self, name, target_a, target_b, anchor_a, anchor_b):
        super().__init__(name, target_a, target_b, anchor_a, anchor_b)

    def add_to_space(self, space):
        init_length = (self.target_a.center+self.anchor_a - self.target_b.center-self.anchor_b).length
        self.constraint = pymunk.DampedSpring(self.target_a.body, self.target_b.body,
                                              self.anchor_a, self.anchor_b,
                                              rest_length=init_length, stiffness=10, damping=0)
        super().add_to_space(space)
