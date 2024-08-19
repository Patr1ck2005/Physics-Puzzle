import time

from pymunk import Vec2d
from gui.ui_panel.property_panel import EntityPropertyPanel

import pygame
import pygame_gui

from settings import *


class EntityManager:
    def __init__(self, screen, space):
        self.entity_property_panel = None
        self.screen = screen
        self.space = space
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running_objects = {}
        self.left_selection = None
        self.right_selection = None
        self.pressed_obj = None
        self.m_pos = None
        self.m_d_pos = None

        # 创建一个实体属性面板
        self.entity_property_panel = EntityPropertyPanel(
            manager=self.manager,
            title="Selected Entity Properties"
        )

    def add_entity(self, obj):
        self.running_objects[obj.name] = obj  # 以字典的形式储存obj对象, 例如: {'ball_1': CircleObjectUI(),}
        obj.add_to_space(self.space, self.m_pos)  # ObjectsManager管理的都是已添加进space中的UI元素

    def update(self, m_pos, m_d_pos):
        self.m_pos = m_pos
        self.m_d_pos = m_d_pos
        for obj in self.running_objects.values():
            obj.update(self.m_pos)
        self.manager.update(pygame.time.get_ticks() / 1000.0)
        if time.time() - self.entity_property_panel.last_refresh_time > .01:
            self.entity_property_panel.refresh()

    def refresh_panel_sliders(self):
        self.entity_property_panel.refresh_sliders()

    def process_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn = event.ui_element
            if btn.text == 'show property':
                self.entity_property_panel.show()
                btn.set_text('hide property')
            elif btn.text == 'hide property':
                self.entity_property_panel.hide()
                btn.set_text('show property')

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            slider = event.ui_element
            if slider.object_ids[-1] == "#property_slider_Mass":
                self.entity_property_panel.entity.mass = slider.current_value
            elif slider.object_ids[-1] == "#property_slider_Friction":
                self.entity_property_panel.entity.friction = slider.current_value
            elif slider.object_ids[-1] == "#property_slider_Elasticity":
                self.entity_property_panel.entity.elasticity = slider.current_value
            return True

    # 处理点击事件的函数
    # 遍历当前运行的对象，检查是否有对象被点击
    # 如果点击的对象是静态物体，则提示不能移动
    # 否则，更新被点击对象的中心位置
    def on_click_left(self):
        for obj in self.running_objects.values():
            if obj.on_click(self.m_pos) and self.left_selection is None:
                self.left_selection = obj
                return self.left_selection
            elif self.left_selection:
                if self.left_selection.type == 'static':  # 静态物体不能移动
                    print('静态物体不能被移动')
                else:
                    print(2)
                    self.left_selection.center = self.m_pos
                self.left_selection = None
                return

    def on_click_right(self):
        for obj in self.running_objects.values():
            if obj.on_click(self.m_pos):
                if self.right_selection != obj:
                    if self.right_selection:
                        self.right_selection.is_selected = False
                    obj.is_selected = True
                    self.entity_property_panel.update_entity(obj)
                else:
                    obj.is_selected = not obj.is_selected
                    self.entity_property_panel.update_entity(obj)
                    if not obj.is_selected:
                        self.entity_property_panel.remove_entity()
                self.right_selection = obj
                return

    def clear_selection(self):
        self.left_selection = None

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
            obj.draw(self.screen)
        self.manager.draw_ui(self.screen)
        # 如果有选中物品则绘制鼠标位置
        if self.left_selection:
            self.draw_mouse_mark()

    def draw_mouse_mark(self):
        pygame.draw.circle(self.screen, (255, 0, 0), self.m_pos, 5)
