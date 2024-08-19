from core.phy_object.tool import Tool, FrictionTool, ElasticityTool
from gui.base_ui import BaseUI, BaseUIBox


class ToolUI(Tool, BaseUI):
    pass


class FrictionToolUI(FrictionTool, BaseUIBox):
    def __init__(self, screen, name, position, size=(30, 30), ico_path=None, color=(150, 150, 150), friction=0.5):
        FrictionTool.__init__(self, friction)
        BaseUIBox.__init__(self, screen, name, position, size, ico_path=ico_path, ico_color=color)


class ElasticityToolUI(ElasticityTool, BaseUIBox):
    def __init__(self, screen, name, position, size=(30, 30), ico_path=None, color=(150, 150, 150), elasticity=0.5):
        ElasticityTool.__init__(self, elasticity)
        BaseUIBox.__init__(self, screen, name, position, size, ico_path=ico_path, ico_color=color)
