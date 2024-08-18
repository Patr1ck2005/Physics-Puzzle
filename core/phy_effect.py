import pymunk


class PhyEffect:
    def __init__(self, name, target):
        self.name = name
        self.target = target

    def affect(self):
        pass


class ForceEffect(PhyEffect):
    def __init__(self, name, target: pymunk.Body, rel_pos=(0, 0), force=(1, 1)):
        super().__init__(name, target)
        self.force = force
        self.rel_pos = rel_pos

    def affect(self):
        self.target.apply_force_at_local_point(self.force, self.rel_pos)

