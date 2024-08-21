from gui.phy_obj_ui.tool_ui import FrictionToolUI, ElasticityToolUI
from gui.inventory.placeable_inventory import PlaceableInventory


class ToolsInventory(PlaceableInventory):
    def __init__(self):
        super().__init__()
        # 先随便设置位置, 后续会调整位置
        center = (0, 0)
        self.items = {
            'frictionless': FrictionToolUI('frictionless', center, color=(200, 0, 200), ico_path='assets/images/g2.png', friction=0),
            'elastic': ElasticityToolUI('elastic', center, color=(200, 0, 200), ico_path='assets/images/g2.png', elasticity=1),
        }
        # 调整位置排列物品栏
        self._align_items()

    @property
    def tools(self):
        return self.items

    def _align_items(self):
        old_name = 'default'
        i = 0
        for item in self.items.values():
            if item.name[:6] == old_name[:6]:
                ui_position = ui_position[0]+5, ui_position[1]+5
            else:
                # 假设每个物体的图标为50x50，依次排开成1列
                ui_position = (50 + (i % 1) * 70, 500 + (i // 1) * 70)
                i += 1
            # 设置物体对象UI中心的坐标
            item.center = ui_position
            old_name = item.name

