from core.tool import Tool, FrictionTool
from .base_ui import BaseUI, BaseUIBox,


class ToolUI(Tool, BaseUI):
    pass


class FrictionToolUI(FrictionTool, BaseUIBox):
    def __init__(self, screen, name, position, size=(30, 30), ico_path=None, color=(150, 150, 150)):
        FrictionTool.__init__(self, name, 0)
        BaseUIBox.__init__(self, screen, name, position, size, ico_path=ico_path, ico_color=color)
