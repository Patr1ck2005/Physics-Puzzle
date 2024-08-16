

class ObjectsManager:
    def __init__(self, screen, space):
        self.screen = screen
        self.space = space
        self.running_objects = {}
        self.selected_obj = None
        self.m_pos = None

    def add_obj(self, obj):
        self.running_objects[obj.name] = obj  # 以字典的形式储存obj对象, 例如: {'ball_1': CircleObjectUI(),}
        obj.add_to_space(self.space, self.m_pos)  # ObjectsManager管理的都是已添加进space中的UI元素

    def update(self, m_pos):
        self.m_pos = m_pos
        for obj in self.running_objects.values():
            obj.is_mouse_over(self.m_pos)

    def on_click(self):
        for obj in self.running_objects.values():
            if obj.on_click(self.m_pos) and self.selected_obj is None:
                self.selected_obj = obj
                return
            elif self.selected_obj:
                if obj.name in self.running_objects:
                    print("已经有这个物体了")
                else:
                    self.selected_obj.add_to_space(self.space, self.m_pos)
                self.selected_obj = None
                return

    def render_running_objs(self):
        for obj in self.running_objects.values():
            obj.sync_ui()
            obj.draw(self.screen)


