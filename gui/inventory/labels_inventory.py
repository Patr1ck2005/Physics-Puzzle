from gui.phy_obj_ui.tool_ui import FrictionToolUI, ElasticityToolUI
from gui.inventory.placeable_inventory import PlaceableInventory


class LabelsInventory(PlaceableInventory):
    def __init__(self):
        super().__init__()
        self.items = {}
        # 调整位置排列物品栏
        self._align_items()

    @property
    def labels(self):
        return self.items

    def add_item_dict(self, item_dict: dict):
        self.items = {**self.items, **item_dict.get('labels', {})}
        self._align_items()

    def _align_items(self):
        old_name = 'default'
        i = 0
        for item in self.items.values():
            if item.name[:6] == old_name[:6]:
                ui_position = ui_position[0]+5, ui_position[1]+5
            else:
                # 假设每个物体的图标为50x50，依次排开成1列
                ui_position = (200 + (i % 1) * 70, 500 + (i // 1) * 70)
                i += 1
            # 设置物体对象UI中心的坐标
            item.ui_center = ui_position
            old_name = item.name

