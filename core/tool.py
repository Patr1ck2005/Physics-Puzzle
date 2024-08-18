from gui.entity_ui import EntityUI


class Tool:
    target: EntityUI = None

    def __init__(self):
        self.target = None

    def affect(self, target):
        self.target = target
        self._make_change()

    def _make_change(self):
        pass


class FrictionTool(Tool):
    def __init__(self, friction):
        super().__init__()
        self.friction = friction

    def _make_change(self):
        self.target.body_shape.friction = self.friction
        print(f"change {self.target.name}'s friction to {self.friction}")


class ElasticityTool(Tool):
    def __init__(self, elasticity):
        super().__init__()
        self.elasticity = elasticity

    def _make_change(self):
        self.target.body_shape.elasticity = self.elasticity
        print(f"change {self.target.name}'s elasticity to {self.elasticity}")