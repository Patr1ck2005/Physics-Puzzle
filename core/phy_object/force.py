from pymunk import Vec2d

from gui.phy_obj_ui.entity_ui import EntityUI


class AbstractForce:
    def __init__(self, force: Vec2d, loc):
        self.force = force
        self.loc = loc

        self.target = None

    def set_target(self, target: EntityUI):
        self.target = target
