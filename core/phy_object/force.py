from pymunk import Vec2d

from gui.phy_obj_ui.entity_ui import EntityUI


class AbstractForce:
    def __init__(self, force: Vec2d, loc):
        self.force = force
        self.loc = loc

        self.target = None

    @property
    def normalised_direction(self):
        return self.force.normalized()

    @property
    def magnitude(self):
        return self.force.magnitude()

    def set_target(self, target: EntityUI):
        self.target = target

    def add_to_space(self, *args, **kwargs):
        self.set_target(kwargs['target'])

    def update(self):
        if self.target:
            self.target.body.apply_force_at_world_point(self.force, self.target.body.position)


