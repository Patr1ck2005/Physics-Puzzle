class Round:
    def __init__(self, center=None, position=None, radius=10):
        self.center = center
        self.position = position
        self.radius = radius

    def collidepoint(self, point):
        if (point[0] - self.center[0]) ** 2 + (point[1] - self.center[1]) ** 2 <= self.radius ** 2:
            return True
        return False
