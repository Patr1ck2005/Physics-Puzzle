from collections import deque

import pymunk


# # Body: 物体的物理状态。
# Dynamic (动态): 可以受力、重力影响的普通物体。
# Kinematic (运动学): 不受重力影响，但可以被编程移动的物体。
# Static (静态): 不移动的物体，通常用于地面、墙壁等。

# # Shape: 物体的形状，用来检测碰撞。
# pymunk.Circle (圆形): 用于表示圆形的物体。
# pymunk.Segment (线段): 用于表示线段，通常用于静态边界或墙壁。
# pymunk.Poly (多边形): 用于表示多边形，可以定义任意形状的物体。
# pymunk.Poly.create_box (盒子): 用于创建矩形的多边形，通常用作箱子或方块。
# pymunk.Plane (平面): 用于表示一个无限大的平面边界。

# Constraint: 连接两个物体的物理约束。
# Space: 物理世界，管理和模拟物体、形状和约束。
# Arbiter: 管理和处理碰撞事件。


class Entity:
    def __init__(self, name, phy_type, shape=None, center=None, angle=None, size=None, color=None):
        self.history_x = deque((0, 0), maxlen=100)
        self.history_y = deque((0, 0), maxlen=100)
        self.history_angle = deque((0, 0), maxlen=100)
        self.name = name
        self.type = phy_type
        self.body = None
        self.body_shape = None
        self.shape = shape
        self._center = center
        self._angle = angle
        self.size = size

        self.icon_rect = None

        self.body, self.body_shape = self._create_phys()

        self.color = color

    @property
    def center(self):
        return self.body.position

    @center.setter
    def center(self, value):
        self.body.position = value

    @property
    def angle(self):
        return self.body.angle

    @angle.setter
    def angle(self, value):
        self.body.angle = value

    @property
    def mass(self):
        return self.body.mass

    @mass.setter
    def mass(self, value):
        self.body.mass = value

    @property
    def moment(self):
        return self.body.moment

    @moment.setter
    def moment(self, value):
        self.body.moment = value

    @property
    def velocity(self):
        return self.body.velocity

    @velocity.setter
    def velocity(self, value):
        self.body.velocity = value

    @property
    def angular_velocity(self):
        return self.body.angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, value):
        self.body.angular_velocity = value

    @property
    def friction(self):
        return self.body_shape.friction

    @friction.setter
    def friction(self, value):
        self.body_shape.friction = value

    @property
    def elasticity(self):
        return self.body_shape.elasticity

    @elasticity.setter
    def elasticity(self, value):
        self.body_shape.elasticity = value

    def _create_phys(self):
        switch_shape = {
            "box": pymunk.Poly.create_box,
            "circle": pymunk.Circle,
            "segment": pymunk.Segment,
        }
        switch_type = {
            "dynamic": pymunk.Body.DYNAMIC,
            "static": pymunk.Body.STATIC,
            "kinematic": pymunk.Body.KINEMATIC
        }
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, 30)
        body = pymunk.Body(mass, moment, body_type=switch_type.get(self.type, pymunk.Body.DYNAMIC))
        body.position = self._center
        body.angle = self._angle
        body_shape = switch_shape.get(self.shape, pymunk.Circle)(body, self.size)
        body_shape.friction = 0.7
        body_shape.elasticity = 0.8
        return body, body_shape

    def record(self):
        self.history_x.append(self.body.position.x)
        self.history_y.append(self.body.position.y)
        self.history_angle.append(self.body.angle)

    def add_to_space(self, space, center_pos):
        self.body.position = center_pos
        space.add(self.body, self.body_shape)

    def remove_from_space(self, space):
        space.remove(self.body, self.body_shape)


class BoxEntity(Entity):
    def __init__(self, name, phy_type, center=(100, 100), angle=0, size=(30, 30), color=(150, 150, 150)):
        Entity.__init__(self, name, phy_type, "box", center, angle, size, color)


class CircleEntity(Entity):
    def __init__(self, name, phy_type, center=(100, 100), angle=0, radius=30, color=(150, 150, 150)):
        Entity.__init__(self, name, phy_type, "circle", center, angle, radius, color)


class BlankEntity(Entity):
    def __init__(self, name='Blank', phy_type='None', center=(0, 0), angle=0, size=(0, 0), color=(150, 150, 150)):
        self.name = name
        self.type = phy_type
        self.shape = None
        self.color = color
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
