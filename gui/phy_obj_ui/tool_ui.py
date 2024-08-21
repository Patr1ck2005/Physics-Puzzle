from core.phy_object.tool import Tool, FrictionTool, ElasticityTool
from gui.base_ui import BaseUI, BaseUICircle


class ToolUI(Tool, BaseUI):
    @property
    def center(self):
        return self.ui_center

    @center.setter
    def center(self, pos):
        self.ui_center = pos
        self.set_click_region()


class FrictionToolUI(ToolUI, FrictionTool, BaseUICircle):
    def __init__(self, name, center, r=15, ico_path=None, color=(150, 150, 150), friction=0.5):
        FrictionTool.__init__(self, friction)
        BaseUICircle.__init__(self, name, center, r, ico_path=ico_path, ico_color=color)


class ElasticityToolUI(ToolUI, ElasticityTool, BaseUICircle):
    def __init__(self, name, center, r=15, ico_path=None, color=(150, 150, 150), elasticity=0.5):
        ElasticityTool.__init__(self, elasticity)
        BaseUICircle.__init__(self, name, center, r, ico_path=ico_path, ico_color=color)
