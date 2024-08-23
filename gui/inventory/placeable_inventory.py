from gui.base_ui import BaseUI
from gui.phy_obj_ui.constrain_ui import *
from gui.phy_obj_ui.entity_ui import BoxEntityUI, CircleEntityUI
from gui.phy_obj_ui.force_ui import ForceUI
from pymunk import Vec2d

class PlaceableInventory:
    items: dict[str, BaseUI]

    def __init__(self):
        # self.items = {
        #     'ball_1': CircleEntityUI('ball_1', 'static', center, color=(200, 0, 200), ico_path='assets/images/g2.png'),
        #     'ball_11': CircleEntityUI('ball_11', 'static', center, color=(200, 0, 200), ico_path='assets/images/g2.png'),
        #     'ball_2': CircleEntityUI('ball_2', 'dynamic', center, color=(200, 0, 200), ico_path='assets/images/g2.png'),
        #     'ball_21': CircleEntityUI('ball_21', 'dynamic', center, color=(200, 0, 200), ico_path='assets/images/天生输家.png'),
        #     'ball_22': CircleEntityUI('ball_22', 'dynamic', center, color=(200, 0, 200), ico_path='assets/images/py.png'),
        #     'ball_3': CircleEntityUI('ball_3', 'kinematic', center, color=(200, 0, 200), ico_path='assets/images/py.png'),
        #     'rect_1': BoxEntityUI('rect_1', 'static', center, size=(20, 40), color=(200, 200, 200)),
        #     'rect_2': BoxEntityUI('rect_2', 'dynamic', center, size=(30, 20), color=(200, 200, 200), ico_path='assets/images/天生输家.png'),
        #     'rect_3': BoxEntityUI('rect_3', 'kinematic', center, size=(30, 20), color=(200, 200, 200)),
        #     'f_1': ForceUI('f_1', Vec2d(0, 0)),
        #     'f_2': ForceUI('f_2', Vec2d(100, 0)),
        #     'f_3': ForceUI('f_3', Vec2d(0, 100)),
        #     'f_4': ForceUI('f_4', Vec2d(100, 100)),
        #     'c_1': PinJointUI('c_1', Vec2d(100, 100)),
        #     'c_2': SlideJointUI('c_2', Vec2d(100, 100)),
        #     'c_3': SpringUI('c_3', Vec2d(100, 100)),
        # }
        self.items = {}
        # 调整位置排列物品栏
        self._align_items()

    def add_item(self, item):
        self.items[item.name] = item
        self._align_items()

    def add_item_dict(self, item_dict: dict):
        self.items = {**self.items, **item_dict['entities'], **item_dict['forces'], **item_dict['constraints']}
        self._align_items()

    def remove_item_by_name(self, name):
        self.items.pop(name, None)

    def get_item_by_name(self, name):
        return self.items[name]

    def _align_items(self):
        old_name = 'default'
        i = 0
        for item in self.items.values():
            if item.name[:6] == old_name[:6]:
                ui_position = ui_position[0]+5, ui_position[1]+5
            else:
                # 假设每个物体的图标为50x50，依次排开成三列
                ui_position = (50 + (i % 3) * 70, 30 + (i // 3) * 70)
                i += 1
            # 设置物体对象UI中心的坐标
            item.center = ui_position
            old_name = item.name

