

class ObjectsManager:
    def __init__(self, space):
        self.space = space
        self.running_objects = {}
        self.selected_obj = None
        self.m_pos = None

    def add_object(self, obj):
        self.running_objects[obj.name] = obj
        self.space.add(obj.body, obj.shape)

    def is_mouse_over(self, m_pos):
        for obj in self.running_objects.values():
            obj.is_mouse_over(m_pos)

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

    def render(self):
        for obj in self.running_objects.values():
            obj.draw()


