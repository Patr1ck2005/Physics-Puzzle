import pygame
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
class GameObject:
    def __init__(self, name, phy_type, shape="circle", size=30, color=(150, 150, 150)):
        self.name = name
        self.type = phy_type
        self.body = None
        self.body_shape = None
        self.shape = shape
        self.size = size

        self.color = color
        self.icon_rect = None

        self.body, self.body_shape = self.create_phys()

    def create_phys(self):
        switch_shape = {
            "circle": pymunk.Circle,
            "box": pymunk.Poly.create_box,
            "segment": pymunk.Segment,
        }
        switch_type = {
            "dynamic": pymunk.Body.DYNAMIC,
            "static": pymunk.Body.STATIC,
        }
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, 30)
        body = pymunk.Body(mass, moment, body_type=switch_type.get(self.type, pymunk.Body.DYNAMIC))
        body_shape = switch_shape.get(self.shape, pymunk.Circle)(body, self.size)
        body_shape.friction = 0.7
        body_shape.elasticity = 0.8
        return body, body_shape

    def add_to_space(self, space, loc):
        new_body, new_body_shape = self.create_phys()
        new_body.position = loc
        space.add(new_body, new_body_shape)

    def remove_from_space(self, space):
        space.remove(self.body, self.shape)

    def draw(self, screen):
        # 这里可以定义绘制这个物体的方法
        pass
