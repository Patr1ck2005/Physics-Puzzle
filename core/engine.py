import math

import pygame
import pymunk
import pymunk.pygame_util

from settings import *


class Engine:
    def __init__(self):

        self.space = pymunk.Space()
        self.pause = False
        self.time_scale = 1
        self.universal_gravity = True

        self._if_uni_gravity = False
        self._if_gravity = False
        self._gravity = 1e3
        self._G = 1e6

    @property
    def gravity(self):
        return self._gravity/1e3

    @gravity.setter
    def gravity(self, value):
        self.space.gravity = (0.0, value*1e3)

    @property
    def if_gravity(self):
        return self._if_gravity

    @if_gravity.setter
    def if_gravity(self, value):
        self.space.gravity = (0.0, self._gravity) if value else (0.0, 0.0)
        self._if_gravity = value

    @property
    def G(self):
        return self._G/1e6

    @G.setter
    def G(self, value):
        self._G = value*1e6

    @property
    def universal_gravity(self):
        return self._G/1e6

    @universal_gravity.setter
    def universal_gravity(self, value):
        if value > 0:
            self._G = value*1e6
            self._if_uni_gravity = True

    def init_world(self):
        self.space.remove(*self.space.bodies, *self.space.shapes, *self.space.constraints)
        if self.if_gravity:
            self.space.gravity = (0.0, self._gravity)

        # 创建一个静态的 body，用于附加墙壁
        static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # 添加静态 body 到空间
        self.space.add(static_body)
        # # 创建地面
        # ground = pymunk.Segment(static_body, (SCREEN_WIDTH/10, 500), (9*SCREEN_WIDTH/10, 500), 5)
        # ground.friction = 1.0
        # ground.elasticity = 1
        # self.space.add(static_body, ground)
        # 在四周创建墙壁
        static_lines = [
            pymunk.Segment(static_body, (0, 0), (0, SCREEN_HEIGHT), 5),
            pymunk.Segment(static_body, (0, 0), (SCREEN_WIDTH, 0), 5),
            pymunk.Segment(static_body, (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), 5),
            pymunk.Segment(static_body, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 5),
        ]
        for line in static_lines:
            line.friction = 1.0
            line.elasticity = 1
            self.space.add(line)

    def update_world(self):
        if self.pause:
            return
        self.space.step(1/180*self.time_scale)
        self.space.step(1/180*self.time_scale)
        self.space.step(1/180*self.time_scale)
        if self._G != 0 and self._if_uni_gravity:
            self.apply_gravitational_force()
        for body in self.space.bodies:
            x, y = body.position
            if x > 8000 or x < -8000 or y > 8000 or y < -8000:
                self.space.remove(body, *body.shapes)
                print(f"remove {body}")

    def apply_gravitational_force(self):
        bodies = [body for body in self.space.bodies if body.body_type == pymunk.Body.DYNAMIC]
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                body1 = bodies[i]
                body2 = bodies[j]

                # 计算两个物体之间的距离向量
                distance_vector = body2.position - body1.position
                distance = distance_vector.length

                # 确保距离不为零
                if distance == 0:
                    continue

                # 计算万有引力的大小
                force_magnitude = self._G * (body1.mass * body2.mass) / (distance ** 2)

                # 计算作用力的方向
                force_direction = distance_vector.normalized()

                # 计算力在世界坐标中的坐标
                force = force_direction * force_magnitude

                # 施加力到两个物体上
                body1.apply_force_at_world_point(force, body1.position)
                body2.apply_force_at_world_point(-force, body2.position)

    def render_world(self, screen):
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(screen))
        # 绘制垂直线
        for x in range(0, SCREEN_WIDTH, 100):
            pygame.draw.line(screen, GREY, (x, 0), (x, SCREEN_HEIGHT), 1)

        # 绘制水平线
        for y in range(0, SCREEN_HEIGHT, 100):
            pygame.draw.line(screen, GREY, (0, y), (SCREEN_WIDTH, y), 1)

    def debug_add(self, selected_item, m_pos):
        # 创建一个球体
        mass = 1
        radius = 15
        moment = pymunk.moment_for_circle(mass, 0, radius)
        ball_body = pymunk.Body(mass, moment)
        ball_body.position = m_pos
        ball_shape = pymunk.Circle(ball_body, radius)
        ball_shape.friction = 0.7
        ball_shape.elasticity = 1
        self.space.add(ball_body, ball_shape)
