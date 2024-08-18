import pymunk


class Tool:
    target: pymunk.Body = None

    def __init__(self, name):
        self.name = name
        self.target = None

    def use(self, target):
        self.target = target
        self._make_change()

    def _make_change(self):
        pass


class FrictionTool(Tool):
    def __init__(self, name, friction):
        super().__init__(name)
        self.friction = friction

    def _make_change(self):
        self.target.friction = self.friction

