"""Engine 物理引擎单元测试"""
import pymunk
import pytest

from core.engine import Engine


class TestEngineGravity:
    """重力属性 getter/setter 一致性"""

    def test_gravity_setter_updates_getter(self):
        e = Engine()
        e.gravity = 5
        assert e.gravity == 5

    def test_gravity_default_value(self):
        e = Engine()
        # 默认 _gravity = 1e3, getter 返回 1e3/1e3 = 1
        assert e.gravity == 1

    def test_gravity_setter_updates_space_when_enabled(self):
        e = Engine()
        e.if_gravity = True
        e.gravity = 3
        assert e.space.gravity == (0.0, 3000.0)

    def test_if_gravity_toggle(self):
        e = Engine()
        e.gravity = 5
        e.if_gravity = True
        assert e.space.gravity == (0.0, 5000.0)
        e.if_gravity = False
        assert e.space.gravity == (0.0, 0.0)
        # 再次开启应恢复之前设置的 gravity
        e.if_gravity = True
        assert e.space.gravity == (0.0, 5000.0)


class TestEngineUniversalGravity:
    """万有引力开关"""

    def test_universal_gravity_enable(self):
        e = Engine()
        e.universal_gravity = 2
        assert e._if_uni_gravity is True
        assert e._G == 2e6

    def test_universal_gravity_disable(self):
        e = Engine()
        e.universal_gravity = 2
        e.universal_gravity = 0
        assert e._if_uni_gravity is False
        assert e._G == 0


class TestEngineInitWorld:
    """init_world 创建边界墙壁"""

    def test_init_world_creates_static_walls(self):
        e = Engine()
        e.init_world()
        # 四面墙 + 静态 body
        static_shapes = [s for s in e.space.shapes if s.body.body_type == pymunk.Body.STATIC]
        assert len(static_shapes) >= 4

    def test_init_world_clears_existing(self):
        e = Engine()
        e.init_world()
        # 添加一个动态物体
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, 10)
        body = pymunk.Body(mass, moment)
        body.position = (100, 100)
        shape = pymunk.Circle(body, 10)
        e.space.add(body, shape)
        assert len(e.space.bodies) > 0

        # 重新 init 应清空
        e.init_world()
        dynamic_bodies = [b for b in e.space.bodies if b.body_type == pymunk.Body.DYNAMIC]
        assert len(dynamic_bodies) == 0


class TestEngineUpdateWorld:
    """update_world 物理步进"""

    def test_update_world_advances_physics(self):
        e = Engine()
        e.init_world()
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, 10)
        body = pymunk.Body(mass, moment)
        body.position = (100, 100)
        shape = pymunk.Circle(body, 10)
        e.space.add(body, shape)

        initial_y = body.position.y
        e.if_gravity = True
        e.update_world()
        assert body.position.y != initial_y

    def test_update_world_paused(self):
        e = Engine()
        e.init_world()
        e.pause = True
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, 10)
        body = pymunk.Body(mass, moment)
        body.position = (100, 100)
        shape = pymunk.Circle(body, 10)
        e.space.add(body, shape)

        initial_pos = (body.position.x, body.position.y)
        e.update_world()
        assert (body.position.x, body.position.y) == initial_pos

    def test_update_world_removes_far_objects(self):
        e = Engine()
        e.init_world()
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, 10)
        body = pymunk.Body(mass, moment)
        body.position = (10000, 10000)  # 超出边界
        shape = pymunk.Circle(body, 10)
        e.space.add(body, shape)

        e.update_world()
        assert body not in e.space.bodies
