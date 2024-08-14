import pymunk


class GameObject:
    def __init__(self, body, shape):
        self.body = body
        self.shape = shape

    def add_to_space(self, space):
        space.add(self.body, self.shape)

    def remove_from_space(self, space):
        space.remove(self.body, self.shape)

    def draw(self, screen):
        # 这里可以定义绘制这个物体的方法
        pass
