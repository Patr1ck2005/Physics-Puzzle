import pymunk
from pymunk import Vec2d


class BGWall:
    def __init__(self):
        self.type = 'static'
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.history_x = (0, 0)
        self.history_y = (0, 0)
        self.history_angle = (0, 0)

    @property
    def mass(self):
        return 0

    @property
    def moment(self):
        return 0

    @property
    def velocity(self):
        return Vec2d(0, 0)

    @property
    def angular_velocity(self):
        return 0

    @property
    def friction(self):
        return 0

    @property
    def elasticity(self):
        return 0

    @property
    def center(self):
        return 0

    @property
    def angle(self):
        return 0

    def add_to_space(self, space, center_pos=None):
        space.add(self.body)


class CircleBGWall(BGWall):
    def __init__(self, center, radius):
        super().__init__()


class RectBGWall(BGWall):
    def __init__(self, center, size):
        super().__init__()


