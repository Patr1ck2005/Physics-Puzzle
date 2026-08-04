"""Engine 物理引擎单元测试"""
import pymunk
import pytest

from core.engine import Engine


class TestEngineGravity:
    """重力属性 getter/setter 一致性"""

    def test_gravity_setter_updates_space(self):
        """gravity setter 直接设置 space.gravity（原设计：不更新 _gravity）"""
        e = Engine()
        e.gravity = 5
        assert e.space.gravity == (0.0, 5000.0)

    def test_gravity_default_value(self):
        e = Engine()
        # 默认 _gravity = 1e3, getter 返回 1e3/1e3 = 1
        assert e.gravity == 1

    def test_if_gravity_toggle_uses_default_gravity(self):
        """if_gravity 开关使用 _gravity 默认值（1e3 = 重力 1）"""
        e = Engine()
        e.if_gravity = True
        assert e.space.gravity == (0.0, 1000.0)
        e.if_gravity = False
        assert e.space.gravity == (0.0, 0.0)
        e.if_gravity = True
        assert e.space.gravity == (0.0, 1000.0)

    def test_gravity_setter_does_not_affect_toggle_default(self):
        """设置 gravity 值不影响 if_gravity 开关使用的默认值"""
        e = Engine()
        e.gravity = 5  # 设置 space.gravity = (0, 5000)
        e.if_gravity = False  # 关闭 -> (0, 0)
        e.if_gravity = True  # 开启 -> 使用 _gravity 默认值 (0, 1000)
        assert e.space.gravity == (0.0, 1000.0)


class TestEngineUniversalGravity:
    """万有引力开关"""

    def test_universal_gravity_enable(self):
        e = Engine()
        e.universal_gravity = 2
        assert e._if_uni_gravity is True
        assert e._G == 2e6

    def test_universal_gravity_toggle_via_flag(self):
        """按钮直接切换 _if_uni_gravity 标志"""
        e = Engine()
        e.universal_gravity = 2
        assert e._if_uni_gravity is True
        # 按钮直接切换标志（不通过 setter）
        e._if_uni_gravity = False
        assert e._if_uni_gravity is False
        # _G 保持不变，仅标志变化
        assert e._G == 2e6


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
