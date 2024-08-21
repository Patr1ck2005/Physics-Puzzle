import time
from collections import deque

import pymunk
from pymunk import Vec2d


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
    def __init__(self, name, phy_type, center: Vec2d = None, angle=None, size=None, color=None):
        self.history_x = deque((0, 0), maxlen=256)
        self.history_y = deque((0, 0), maxlen=256)
        self.history_angle = deque((0, 0), maxlen=256)
        self.record_delta = 0.5
        self.last_record_time = 0

        self.name = name
        self.type = phy_type
        self.body = None
        self.body_shape = None
        self._center = center
        self._angle = angle
        self._size = size

        self.icon_rect = None

        self.body, self.body_shape = self._create_phys()

        self.color = color

    @property
    def phy_center(self):
        return self.body.position

    @phy_center.setter
    def phy_center(self, value):
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
        pass

    def record(self):
        # if time.time() - self.last_record_time > self.record_delta:
        #     self.history_x.append(self.body.position.x)
        #     self.history_y.append(self.body.position.y)
        #     self.history_angle.append(self.body.angle)
        #     self.last_record_time = time.time()
        # else:
        #     return
        self.history_x.append(self.body.position.x)
        self.history_y.append(self.body.position.y)
        self.history_angle.append(self.body.angle)

    def add_to_space(self, space, center_pos=None):
        if center_pos:
            self.body.position = center_pos
        space.add(self.body, self.body_shape)

    def remove_from_space(self, space):
        space.remove(self.body, self.body_shape)


class BoxEntity(Entity):
    def __init__(self, name, phy_type, center, angle=0, size=(30, 30), color=(150, 150, 150)):
        Entity.__init__(self, name, phy_type, center, angle, size, color)

    def _create_phys(self):
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
        body_shape = pymunk.Poly.create_box(body, self._size)
        body_shape.friction = 0.7
        body_shape.elasticity = 0.8
        return body, body_shape


class CircleEntity(Entity):
    def __init__(self, name, phy_type, center, angle=0, radius=30, color=(150, 150, 150)):
        Entity.__init__(self, name, phy_type, center, angle, radius, color)

    def _create_phys(self):
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
        body_shape = pymunk.Circle(body, self._size)
        body_shape.friction = 0.7
        body_shape.elasticity = 0.8
        return body, body_shape


class PolyEntity(Entity):
    def __init__(self, name, phy_type, local_points, center, angle=0, color=(150, 150, 150)):
        self._center = center
        self._local_points = local_points
        Entity.__init__(self, name, phy_type, center, angle, None, color)

    @property
    def points(self):
        return 0

    def _create_phys(self):
        switch_type = {
            "dynamic": pymunk.Body.DYNAMIC,
            "static": pymunk.Body.STATIC,
            "kinematic": pymunk.Body.KINEMATIC
        }
        mass = 10
        moment = pymunk.moment_for_poly(mass, self._local_points)
        body = pymunk.Body(mass, moment, body_type=switch_type.get(self.type, pymunk.Body.DYNAMIC))
        body_shape = pymunk.Poly(body, self._local_points)

        body.position = self._center
        body.angle = self._angle
        body_shape.friction = 0.7
        body_shape.elasticity = 0.8
        return body, body_shape
