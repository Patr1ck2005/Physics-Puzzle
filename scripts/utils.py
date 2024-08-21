import numpy as np
from pymunk import Vec2d


class Round:
    def __init__(self, center=None, radius=20, position=None):
        self.center = center
        self.position = position
        self.radius = radius

    def collidepoint(self, x, y):
        if (x - self.center[0]) ** 2 + (y - self.center[1]) ** 2 <= self.radius ** 2:
            return True
        return False


class Poly:
    def __init__(self, points):
        self.points = points

    @property
    def rect_width(self):
        xs = [p[0] for p in self.points]
        return max(xs) - min(xs)

    @property
    def rect_height(self):
        ys = [p[1] for p in self.points]
        return max(ys) - min(ys)

    @property
    def center(self):
        area = 0
        cx = 0
        cy = 0

        n = len(self.points)
        for i in range(n):
            x0, y0 = self.points[i]
            x1, y1 = self.points[(i + 1) % n]
            cross_product = x0 * y1 - x1 * y0
            area += cross_product
            cx += (x0 + x1) * cross_product
            cy += (y0 + y1) * cross_product

        area *= 0.5
        cx /= (6 * area)
        cy /= (6 * area)
        return Vec2d(cx, cy)

    @property
    def local_points(self):
        return [(x - self.center.x, y - self.center.y) for x, y in self.points]

    def move(self, dx, dy):
        self.points = [(x + dx, y + dy) for x, y in self.points]

    def self_rotate_rad(self, angle, center):
        self.points = rotate_polygon_vector(self.points, angle, center)

    def self_rotate_deg(self, angle, center):
        angle = np.deg2rad(angle)
        self.points = rotate_polygon_vector(self.points, angle, center)

    def collidepoint(self, x, y):
        polygon = self.points
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside


def interpolate_color(color1, color2, factor):
    return (
        color1[0] + (color2[0] - color1[0]) * factor,
        color1[1] + (color2[1] - color1[1]) * factor,
        color1[2] + (color2[2] - color1[2]) * factor
    )

# 旋转方法：使用 numpy 矢量化计算


def get_rotation_matrix(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])


def rotate_polygon_vector(points, angle, center):
    points = np.array(points) - center
    rotation_matrix = get_rotation_matrix(angle)
    rotated_points = points @ rotation_matrix.T
    return rotated_points + center
