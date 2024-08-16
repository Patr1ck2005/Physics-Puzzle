from .object_ui import BoxObjectUI, CircleObjectUI


class InventoryManager:
    items: dict[str, BoxObjectUI | CircleObjectUI]

    def __init__(self, screen):
        # 先随便设置位置, 后续会调整位置
        center = (0, 0)
        self.items = {
            'ball_1': CircleObjectUI(screen, 'ball_1', 'static', center, color=(200, 0, 200)),
            'ball_2': CircleObjectUI(screen, 'ball_2', 'dynamic', center, color=(200, 0, 200)),
            'ball_3': CircleObjectUI(screen, 'ball_3', 'kinematic', center, color=(200, 0, 200)),
            'rect_1': BoxObjectUI(screen, 'rect_1', 'static', center, size=(20, 40), color=(200, 200, 200)),
            'rect_2': BoxObjectUI(screen, 'rect_2', 'dynamic', center, size=(30, 20), color=(200, 200, 200)),
            'rect_3': BoxObjectUI(screen, 'rect_3', 'kinematic', center, size=(30, 20), color=(200, 200, 200)),
        }
        # 调整位置排列物品栏
        self.align_items()

    def add_item(self, item):
        self.items[item.name] = item

    def remove_item_by_name(self, name):
        self.items.pop(name)

    def get_item_by_name(self, name):
        return self.items[name]

    def align_items(self):
        for i, item in enumerate(self.items.values()):
            # 假设每个物体的图标为50x50，依次排开成三列
            ui_position = (50 + (i % 3) * 70, 30 + (i // 3) * 70)
            # 设置物体对象UI中心的坐标
            item.center = ui_position

