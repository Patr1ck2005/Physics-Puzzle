"""scripts/utils.py 工具函数单元测试"""
import pytest

from scripts.utils import Round, Poly, interpolate_color, get_rotation_matrix, rotate_polygon_vector
import numpy as np


class TestRound:
    """Round 圆形碰撞区域"""

    def test_collidepoint_inside(self):
        r = Round(center=(100, 100), radius=50)
        assert r.collidepoint(100, 100) is True
        assert r.collidepoint(120, 120) is True

    def test_collidepoint_outside(self):
        r = Round(center=(100, 100), radius=50)
        assert r.collidepoint(200, 200) is False

    def test_collidepoint_on_edge(self):
        r = Round(center=(0, 0), radius=50)
        # 刚好在半径上
        assert r.collidepoint(50, 0) is True
        assert r.collidepoint(51, 0) is False


class TestPoly:
    """Poly 多边形工具"""

    def test_center_of_square(self):
        poly = Poly([(0, 0), (100, 0), (100, 100), (0, 100)])
        center = poly.center
        assert center.x == pytest.approx(50)
        assert center.y == pytest.approx(50)

    def test_center_of_triangle(self):
        poly = Poly([(0, 0), (60, 0), (30, 60)])
        center = poly.center
        assert center.x == pytest.approx(30)
        assert center.y == pytest.approx(20)

    def test_rect_width_height(self):
        poly = Poly([(0, 0), (100, 0), (100, 50), (0, 50)])
        assert poly.rect_width == 100
        assert poly.rect_height == 50

    def test_local_points_relative_to_center(self):
        poly = Poly([(100, 100), (200, 100), (200, 200), (100, 200)])
        local = poly.local_points
        center = poly.center
        # 本地坐标应为相对于中心的坐标
        for (lx, ly) in local:
            assert abs(lx + center.x - 100) < 1 or abs(lx + center.x - 200) < 1

    def test_collidepoint_inside(self):
        poly = Poly([(0, 0), (100, 0), (100, 100), (0, 100)])
        assert poly.collidepoint(50, 50) is True

    def test_collidepoint_outside(self):
        poly = Poly([(0, 0), (100, 0), (100, 100), (0, 100)])
        assert poly.collidepoint(200, 200) is False

    def test_move(self):
        poly = Poly([(0, 0), (100, 0), (100, 100), (0, 100)])
        poly.move(50, 50)
        assert poly.points[0] == (50, 50)
        assert poly.points[2] == (150, 150)

    def test_self_rotate_deg(self):
        poly = Poly([(0, 0), (100, 0), (100, 100), (0, 100)])
        center = (50, 50)
        poly.self_rotate_deg(90, center)
        # 旋转 90 度后，(0,0) 应接近 (100, 0) 或 (0, 100)
        # 旋转中心是 (50,50)
        x, y = poly.points[0]
        assert abs(x - 100) < 1 or abs(x - 0) < 1


class TestColorInterpolation:
    """颜色插值"""

    def test_interpolate_start(self):
        c = interpolate_color((0, 0, 0), (100, 100, 100), 0)
        assert c == (0, 0, 0)

    def test_interpolate_end(self):
        c = interpolate_color((0, 0, 0), (100, 100, 100), 1)
        assert c == (100, 100, 100)

    def test_interpolate_mid(self):
        c = interpolate_color((0, 0, 0), (100, 100, 100), 0.5)
        assert c == (50, 50, 50)


class TestRotationMatrix:
    """旋转矩阵"""

    def test_identity(self):
        m = get_rotation_matrix(0)
        assert np.allclose(m, np.eye(2))

    def test_90_degrees(self):
        m = get_rotation_matrix(np.pi / 2)
        # (1, 0) 旋转 90 度应为 (0, 1)
        v = np.array([1, 0])
        rotated = v @ m.T
        assert np.allclose(rotated, [0, 1])


class TestRotatePolygonVector:
    """多边形旋转"""

    def test_rotate_90_around_origin(self):
        points = [(1, 0), (2, 0)]
        rotated = rotate_polygon_vector(points, np.pi / 2, (0, 0))
        # (1,0) 旋转 90 度应为 (0,1)
        assert np.allclose(rotated[0], [0, 1])
        assert np.allclose(rotated[1], [0, 2])

    def test_rotate_around_center(self):
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        rotated = rotate_polygon_vector(points, np.pi / 2, (50, 50))
        # 旋转后仍是正方形，中心不变
        center = Poly(rotated).center
        assert abs(center.x - 50) < 1
        assert abs(center.y - 50) < 1
