"""Entity 物理对象单元测试"""
import pymunk
import pytest
from pymunk import Vec2d

from core.phy_object.entity import BoxEntity, CircleEntity, PolyEntity


class TestBoxEntity:
    """BoxEntity 创建与物理属性"""

    def test_creation(self):
        box = BoxEntity("box1", "dynamic", Vec2d(100, 200), angle=0, size=(50, 50))
        assert box.name == "box1"
        assert box.body is not None
        assert box.body_shape is not None
        assert box.body.body_type == pymunk.Body.DYNAMIC

    def test_moment_of_inertia_uses_size(self):
        """验证 BoxEntity 的转动惯量使用 size 而非硬编码 30"""
        box = BoxEntity("box1", "dynamic", Vec2d(0, 0), size=(50, 50), mass=1)
        expected_moment = pymunk.moment_for_box(1, (50, 50))
        assert box.moment == pytest.approx(expected_moment)

    def test_static_type(self):
        box = BoxEntity("box1", "static", Vec2d(0, 0), size=(50, 50))
        assert box.body.body_type == pymunk.Body.STATIC

    def test_kinematic_type(self):
        box = BoxEntity("box1", "kinematic", Vec2d(0, 0), size=(50, 50))
        assert box.body.body_type == pymunk.Body.KINEMATIC

    def test_add_to_space(self):
        space = pymunk.Space()
        box = BoxEntity("box1", "dynamic", Vec2d(100, 100), size=(30, 30))
        box.add_to_space(space)
        assert box.body in space.bodies
        assert box.body_shape in space.shapes

    def test_remove_from_space(self):
        space = pymunk.Space()
        box = BoxEntity("box1", "dynamic", Vec2d(100, 100), size=(30, 30))
        box.add_to_space(space)
        box.remove_from_space(space)
        assert box.body not in space.bodies
        assert box.body_shape not in space.shapes


class TestCircleEntity:
    """CircleEntity 创建与物理属性"""

    def test_creation(self):
        circle = CircleEntity("c1", "dynamic", Vec2d(100, 200), radius=25)
        assert circle.name == "c1"
        assert circle.body.body_type == pymunk.Body.DYNAMIC

    def test_moment_of_inertia_uses_radius(self):
        """验证 CircleEntity 的转动惯量使用实际半径"""
        circle = CircleEntity("c1", "dynamic", Vec2d(0, 0), radius=25, mass=1)
        expected_moment = pymunk.moment_for_circle(1, 0, 25)
        assert circle.moment == pytest.approx(expected_moment)

    def test_radius_not_hardcoded(self):
        """不同半径应有不同转动惯量"""
        c1 = CircleEntity("c1", "dynamic", Vec2d(0, 0), radius=10, mass=1)
        c2 = CircleEntity("c2", "dynamic", Vec2d(0, 0), radius=30, mass=1)
        assert c1.moment != c2.moment


class TestPolyEntity:
    """PolyEntity 创建"""

    def test_creation(self):
        poly = PolyEntity("p1", "dynamic",
                          local_points=[(-30, -30), (30, -30), (0, 30)],
                          center=Vec2d(100, 100))
        assert poly.name == "p1"
        assert poly.body is not None


class TestEntityRecord:
    """Entity.record 历史记录"""

    def test_record_stores_position(self):
        box = BoxEntity("box1", "dynamic", Vec2d(100, 100), size=(30, 30))
        box.record()
        assert box.history_x[-1] == 100
        assert box.history_y[-1] == 100

    def test_record_appends_every_call(self):
        """record() 每次调用都应追加（用于右侧面板平滑曲线图）"""
        box = BoxEntity("box1", "dynamic", Vec2d(100, 100), size=(30, 30))
        box.record()
        first_len = len(box.history_x)
        box.record()
        assert len(box.history_x) == first_len + 1
