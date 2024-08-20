class Round:
    def __init__(self, center=None, radius=20, position=None):
        self.center = center
        self.position = position
        self.radius = radius

    def collidepoint(self, x, y):
        if (x - self.center[0]) ** 2 + (y - self.center[1]) ** 2 <= self.radius ** 2:
            return True
        return False


def interpolate_color(color1, color2, factor):
    return (
        color1[0] + (color2[0] - color1[0]) * factor,
        color1[1] + (color2[1] - color1[1]) * factor,
        color1[2] + (color2[2] - color1[2]) * factor
    )
