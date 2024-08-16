class Round:
    def __init__(self, center=None, radius=20, position=None):
        self.center = center
        self.position = position
        self.radius = radius

    def collidepoint(self, x, y):
        if (x - self.center[0]) ** 2 + (y - self.center[1]) ** 2 <= self.radius ** 2:
            return True
        return False
