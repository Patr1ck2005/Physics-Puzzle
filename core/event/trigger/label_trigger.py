from core.event.trigger.trigger import QueryTrigger
from gui.phy_obj_ui.check_label_ui import CheckLabelUI


class LabelTrigger(QueryTrigger):
    def __init__(self, labels: list[CheckLabelUI], *args, **kwargs):
        super().__init__(targets=labels, *args, **kwargs)

    def _query_condition(self):
        rsl = True
        for label in self.targets:
            rsl &= label.check_correctness()
        return rsl



