from gui.base_ui import BaseUI


class ObjUIAddition(BaseUI):
    labels: list[BaseUI]

    def __init__(self):
        self.labels = []

    def add_label(self, label: BaseUI):
        self.labels.append(label)

    def clear_labels(self):
        self.labels.clear()

    def draw_labels(self, screen):
        for label in self.labels:
            label.draw(screen)


class PhysicsLabel:
    def __init__(self, name, expected_value):
        self.name = name  # 标签的名字，例如 "速度" 或 "位置"
        self.expected_value = expected_value  # 标签期望的物理属性值
        self.is_placed = False  # 判断标签是否已被放置
        self.placed_on_object = None  # 记录放置的物体

    def place_on_object(self, game_object):
        self.is_placed = True
        self.placed_on_object = game_object

    def check_correctness(self):
        if self.placed_on_object:
            actual_value = getattr(self.placed_on_object, self.name, None)
            return actual_value == self.expected_value
        return False
