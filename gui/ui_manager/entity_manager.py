import time

from pymunk import Vec2d

from gui.phy_obj_ui.entity_ui import EntityUIAddition
from gui.ui_panel.property_panel import EntityPropertyPanel

import pygame
import pygame_gui

from settings import *


class EntityManager:
    '''
    实体管理器类，负责管理游戏中的实体对象及其附带的力, 物理标签等. 还负责管理和实体有关的属性面板.
    处理用户输入事件，更新实体状态，并渲染实体及其附加物。
    '''
    def __init__(self, space):
        '''
        初始化实体管理器，创建实体属性面板。
        '''
        self.entity_property_panel = None
        self.space = space
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'gui/ui_panel/property_theme.json')
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

        # 用户操作限制
        self.click_to_move = True
        self.drag_to_move = True

    def add_entity(self, obj):
        '''
        添加单个实体对象到管理器中，并将其添加到空间中。
        '''
        self.running_objects[obj.name] = obj  # 以字典的形式储存obj对象, 例如: {'ball_1': CircleObjectUI(),}
        obj.add_to_space(self.space, self.m_pos)  # ObjectsManager管理的都是已添加进space中的UI元素

    def add_entities_dict(self, entities_dict):
        '''
        批量添加实体对象到管理器中，并将其添加到空间中。
        用于初始化关卡.
        '''
        new_obj = {**entities_dict["entities"], **entities_dict["constraints"]}
        self.running_objects = {**self.running_objects, **entities_dict["entities"]}
        for obj in new_obj.values():
            obj.add_to_space(self.space)

    def update(self, m_pos, m_d_pos):
        '''
        更新管理器中的所有实体对象状态，并按照一定时间间隔刷新属性面板的曲线图。
        '''
        self.m_pos = m_pos
        self.m_d_pos = m_d_pos
        for obj in self.running_objects.values():
            obj.update(self.m_pos)
        self.manager.update(pygame.time.get_ticks() / 1000.0)
        if time.time() - self.entity_property_panel.last_refresh_time > .01:
            self.entity_property_panel.update_graphs()

    def refresh_panel_property(self):
        '''
        刷新属性面板中的属性滑动条和对应的标签。
        '''
        self.entity_property_panel.refresh_property_text()
        self.entity_property_panel.refresh_sliders()

    def process_event(self, event):
        '''
        让各UI面板自行处理用户输入事件。
        '''
        self.entity_property_panel.process_events(event)

    # 处理点击事件的函数
    # 遍历当前运行的对象，检查是否有对象被点击
    # 如果点击的对象是静态物体，则提示不能移动
    # 否则，更新被点击对象的中心位置
    def on_click_left(self) -> EntityUIAddition | None:
        '''
        处理左键点击事件，更新被点击对象的中心位置或提示静态物体不能移动。
        '''
        for obj in self.running_objects.values():
            if obj.on_click(self.m_pos) and self.left_selection is None:
                self.left_selection = obj
                return self.left_selection
            elif self.left_selection:
                if self.left_selection.type == 'static':  # 静态物体不能移动
                    print('静态物体不能被移动')
                else:
                    if self.click_to_move:
                        self.left_selection.center = self.m_pos
                    else:
                        print('已禁用点击移动功能')
                self.left_selection = None
                return

    def on_click_right(self) -> EntityUIAddition | None:
        '''
        处理右键点击事件，更新选中对象并刷新属性面板。
        '''
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

    def on_press(self) -> EntityUIAddition | None:
        '''
        处理鼠标按下事件，允许拖动非静态物体。
        '''
        # 只要存在被按住的物体
        if self.pressed_obj:
            # 如果启用了拖动移动功能，则更新被按下对象的中心位置和速度
            if self.drag_to_move:
                self.pressed_obj.center = self.m_pos
                self.pressed_obj.body.velocity = Vec2d(*self.m_d_pos) * 40
                return
            else:
                print('已禁用拖动移动功能')
                return
        for obj in self.running_objects.values():
            # 按住鼠标可以拖动物体
            if obj.on_press(self.m_pos):
                if obj.type == 'static':  # 静态物体不能移动
                    print('静态物体不能被移动')
                    self.pressed_obj = None
                    return
                else:
                    self.pressed_obj = obj
                    return obj

    def on_release(self):
        '''
        处理鼠标释放事件，松开被按下的物体。
        '''
        # 仅在释放鼠标时松开物体
        self.pressed_obj = None
        for obj in self.running_objects.values():
            obj.on_release(self.m_pos)

    def clear_selection(self):
        '''
        清除当前的左键选择。
        '''
        self.left_selection = None

    def render_running_objs(self, screen):
        '''
        渲染所有运行中的实体对象和属性面板，并在有选中对象时绘制鼠标标记。
        '''
        for obj in self.running_objects.values():
            obj.draw(screen)
        self.manager.draw_ui(screen)
        # 如果有选中物品则绘制鼠标位置
        if self.left_selection:
            self.draw_mouse_mark(screen)

    def draw_mouse_mark(self, screen):
        '''
        在屏幕上绘制鼠标标记。
        '''
        pygame.draw.circle(screen, (255, 0, 0), self.m_pos, 5)

