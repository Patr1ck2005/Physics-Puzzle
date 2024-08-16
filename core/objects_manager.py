from pymunk import Vec2d

class ObjectsManager:
    def __init__(self, screen, space):
        self.screen = screen
        self.space = space
        self.running_objects = {}
        self.selected_obj = None
        self.pressed_obj = None
        self.m_pos = None
        self.m_d_pos = None

    def add_obj(self, obj):
        self.running_objects[obj.name] = obj  # 以字典的形式储存obj对象, 例如: {'ball_1': CircleObjectUI(),}
        obj.add_to_space(self.space, self.m_pos)  # ObjectsManager管理的都是已添加进space中的UI元素

    def update(self, m_pos, m_d_pos):
        self.m_pos = m_pos
        self.m_d_pos = m_d_pos
        for obj in self.running_objects.values():
            obj.is_mouse_over(self.m_pos)

    def on_click(self):
        for obj in self.running_objects.values():
            if obj.on_click(self.m_pos) and self.selected_obj is None:
                self.selected_obj = obj
                return
            elif self.selected_obj:
                if self.selected_obj.type == 'static':  # 静态物体不能移动
                    print('静态物体不能被移动')
                    self.selected_obj = None
                else:
                    self.selected_obj.center = self.m_pos
                    self.selected_obj = None
                return

    def call_back_click(self):
        self.selected_obj = None

    def on_press(self):
        for obj in self.running_objects.values():
            # 按住鼠标可以拖动物体
            if obj.on_press(self.m_pos):
                if obj.type == 'static':  # 静态物体不能移动
                    print('静态物体不能被移动')
                    self.pressed_obj = None
                else:
                    self.pressed_obj = obj
        # 只要存在被按住的物体就移动
        if self.pressed_obj:
            self.pressed_obj.center = self.m_pos
            self.pressed_obj.body.velocity = Vec2d(*self.m_d_pos) * 20

    def on_release(self):
        # 仅在释放鼠标时松开物体
        self.pressed_obj = None
        for obj in self.running_objects.values():
            obj.on_release(self.m_pos)

    def render_running_objs(self):
        for obj in self.running_objects.values():
            obj.sync_ui()
            obj.draw(self.screen)


