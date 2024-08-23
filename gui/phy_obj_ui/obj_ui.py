from gui.base_ui import BaseUI, BaseUIRect


class ObjUIAddition(BaseUI):
    labels: list[BaseUI]

    def __init__(self):
        self.labels = []

