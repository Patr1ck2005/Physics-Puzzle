import time

import pygame
import pygame_gui
from pymunk import Vec2d

from core.phy_object.bg_wall import BGWall
from core.phy_object.constrain import Constrain
from core.phy_object.tool import Tool
from gui.hud import HUD
from gui.phy_obj_ui.check_label_ui import CheckLabelUI
from gui.phy_obj_ui.force_ui import ForceUI
from gui.ui_manager.inventory_manager import InventoryManager
from gui.ui_manager.btn_manager import ButtonManager
from gui.ui_manager.entity_manager import EntityManager
from gui.ui_manager.addition_manager import AdditionManager

from core.phy_object.entity import Entity
from settings import *


class UIManager:
    def __init__(self, engine):
        self.engine = engine
        self.hud = HUD()   # HUD
        self.entity_manager = EntityManager(engine.space)   # 物理对象UI管理器
        self.addition_manager = AdditionManager(self.entity_manager)
        self.btn_manager = ButtonManager(engine, self.hud)   # 按钮UI
        self.inventory_manager = InventoryManager()   # 物品栏UI

        self.event_ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.m_pos = None
        self.m_d_pos = None
        self.pressing_start_time = None

        self.last_clicked_ui = None
        self.selected_item = None
        self.selected_tool = None
        self.pre_constraint_entity = None
        self.pre_placed_constrain = None
        self.ui_on_hovered = False

        self.check_labels = {}

    def update(self, t_delta):
        # 始终同步鼠标位置
        self.m_pos = pygame.mouse.get_pos()
        self.m_d_pos = pygame.mouse.get_rel()
        # 更新各种手搓UIManager, 依次检测鼠标是否悬停于指定UI
        self.entity_manager.update(self.m_pos, self.m_d_pos)
        self.addition_manager.update(self.m_pos)
        self.inventory_manager.update(self.m_pos)
        # 更新基于pygame_gui的UIManager
        time_delta = pygame.time.get_ticks() / 1000.0
        self.btn_manager.update(time_delta)
        self.event_ui_manager.update(time_delta)
        # 检测鼠标是否长按
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # 左键
            if time.time() - self.pressing_start_time > 0.3:  # 按下超过0.3秒算长按
                self._on_press()
                self.entity_manager.on_press()
                # 触发长按的时候需要撤回实体点击事件 (例如, 双次点击放置和长按放置取其一即可)
                self.entity_manager.clear_selection()

    def process_events(self, event):
        if self.btn_manager.process_event(event):
            # 这里很奇怪
            pass
        if self.event_ui_manager.process_events(event):
            pass
        if self.entity_manager.process_event(event):
            pass
        # 当鼠标点击时, 处理鼠标点击和UI的交互
        if event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.pressing_start_time = time.time()
                self._on_click_left()
            if event.button == 3:
                self._on_click_right()
        elif event.type == pygame.MOUSEBUTTONUP:
            self._on_release()

    def process_triggerd_events(self, event_name):
        if event_name == 'disable_click_to_move':
            self.entity_manager.click_to_move = False
        elif event_name == 'enable_click_to_move':
            self.entity_manager.click_to_move = True
        elif event_name == 'disable_drag_to_move':
            self.entity_manager.drag_to_move = False
        elif event_name == 'enable_drag_to_move':
            self.entity_manager.drag_to_move = True

    # 检测哪个UI被点击. 理论上仅可能有一个UI被点击
    def _on_click_left(self):

        # 简单储存物品栏左键选择结果
        selected = self.inventory_manager.on_click()
        if selected:
            return  # 只要选择到物品栏就直接跳过判断其他UI逻辑了(物品栏优先级最高)
        # 获取物品栏放置结果
        pre_placed_item = self.inventory_manager.pre_placed_item

        # 简单储存世界实体左键选择结果
        selected_addition = self.addition_manager.on_click()
        # 这部分逻辑丑陋
        if pre_placed_item:
            self.addition_manager.clear_selection()
        if selected_addition and pre_placed_item is None:
            return
        selected_entity = self.entity_manager.on_click_left()

        # 更新HUD显示物品栏选择结果
        self.hud.current_selection = selected or selected_entity or selected_addition

        # 判断各种可放置物体
        if isinstance(pre_placed_item, Entity):
            # 放置物品
            self.inventory_manager.remove_item_by_name(pre_placed_item.name)
            self.entity_manager.add_entity(pre_placed_item)
            self._clear_all_selection()  # 此时清除所有选择
            return
        elif isinstance(pre_placed_item, BGWall):
            # 放置背景墙
            self.inventory_manager.remove_item_by_name(pre_placed_item.name)
            self.entity_manager.add_entity(pre_placed_item)
            self._clear_all_selection()  # 此时清除所有选择
            return
        elif isinstance(pre_placed_item, ForceUI):
            # 放置力
            if selected_entity and selected_entity.type == 'dynamic':
                self.inventory_manager.remove_item_by_name(pre_placed_item.name)   # 从物品栏中移除力
                pre_placed_item.set_target(selected_entity)  # 绑定实体
                self.addition_manager.add_force(pre_placed_item)   # 添加力到附加物管理器
                self.entity_manager.clear_selection()    # 此时清除实体选择
                return
            else:
                print('please select a dynamic entity to apply FORCE')
        elif isinstance(pre_placed_item, CheckLabelUI):
            # 放置标签 (和放置力逻辑相似)
            if selected_entity and selected_entity.type == 'dynamic':
                self.inventory_manager.remove_item_by_name(pre_placed_item.name)   # 从物品栏中移除标签
                pre_placed_item.set_target(selected_entity)  # 绑定实体
                self.addition_manager.add_label(pre_placed_item)   # 添加标签到附加物管理器
                self.entity_manager.clear_selection()    # 此时清除实体选择
                return
            else:
                print('please select a dynamic entity to apply LABEL')
        elif isinstance(pre_placed_item, Tool):
            # 放置工具 (弃用)
            if selected_entity and selected_entity.type == 'dynamic':
                pre_placed_item.affect(target=selected_entity)   # 对选择的实体应用工具
                # self.inventory_manager.remove_item_by_name(pre_placed_item.name)   # 从物品栏中移除工具
                self.entity_manager.clear_selection()    # 此时清除实体选择
                self.entity_manager.refresh_panel_property()  # 更新实体面板属性
                self._clear_hud_selection()
                print('tool applied to entity')
            else:
                print('please select a entity to apply tool')
        elif isinstance(pre_placed_item, Constrain):
            # 想要放置约束
            self.pre_placed_constrain = pre_placed_item   # 储存约束对象
            if isinstance(selected_entity, BGWall):  # 如果约束在墙体上, 设置锚点坐标
                self.pre_placed_constrain.set_anchor_a(Vec2d(*self.m_pos))
            if selected_entity:
                self.pre_constraint_entity = selected_entity   # 储存约束作用的第一个实体
                self.pre_placed_constrain.set_target_a(self.pre_constraint_entity)
                self.entity_manager.clear_selection()   # 此时清除实体选择
                self._clear_hud_selection()
                return
            else:
                print('please select a entity to apply constrain')
        # 已经选择了约束并选择了第一个目标实体
        elif self.pre_constraint_entity:
            if selected_entity:  # 选择了第二个物体
                self.pre_placed_constrain.set_target_b(selected_entity)
                if isinstance(selected_entity, BGWall):  # 如果约束在墙体上.
                    self.pre_placed_constrain.set_anchor_b(self.m_pos)
                self.pre_placed_constrain.add_to_space(self.engine.space)

                self.inventory_manager.remove_item_by_name(self.pre_placed_constrain.name)
                self.pre_constraint_entity = None
                self.pre_placed_constrain = None
                self.entity_manager.clear_selection()
                self._clear_hud_selection()
                return
            else:
                print('select another entity to apply constrain to')

        # 获取附加物重新放置结果 优先级低于物品栏放置
        pre_placed_addition = self.addition_manager.pre_placed_item
        if isinstance(pre_placed_addition, CheckLabelUI):
            self.entity_manager.clear_selection()  # 此时清除实体选择
            self.addition_manager.pre_placed_item = None
            # 放置标签
            if selected_entity and selected_entity.type == 'dynamic':
                pre_placed_addition.set_target(selected_entity)  # 绑定实体
                return
            else:
                print('please select a dynamic entity to Re-apply LABEL')
                return
        elif isinstance(pre_placed_addition, ForceUI):
            self.entity_manager.clear_selection()  # 此时清除实体选择
            self.addition_manager.pre_placed_item = None
            # 放置力
            if selected_entity and selected_entity.type == 'dynamic':
                pre_placed_addition.set_target(selected_entity)  # 绑定实体
                self.addition_manager.pre_placed_item = None
                return
            else:
                print('please select a dynamic entity to Re-apply FORCE')
                return

    def _clear_all_selection(self):
        self.entity_manager.clear_selection()
        self.inventory_manager.clear_selection()
        self.addition_manager.clear_selection()
        self.pre_constraint_entity = None
        if self.pre_placed_constrain:
            self.pre_placed_constrain.reset()
            self.pre_placed_constrain = None
        self.hud.current_selection = None

    def _clear_hud_selection(self):
        self.hud.current_selection = None

    def _on_click_right(self):
        self._clear_all_selection()
        # 简单储存世界实体右键键选择结果
        selected_entity = self.entity_manager.on_click_right()

    # 检测哪个UI被按住
    def _on_press(self):
        self.inventory_manager.on_press(self.m_pos)

    # 检测哪个UI被松开
    def _on_release(self):
        self.inventory_manager.on_release(self.m_pos)
        self.entity_manager.on_release()

    # 依次渲染所有UI
    def draw_ui(self, screen):
        self.entity_manager.render_running_objs(screen)
        self.addition_manager.render_running_additions(screen)
        self.inventory_manager.render(screen)
        self.btn_manager.render(screen)
        self.event_ui_manager.draw_ui(screen)
        self.hud.render(screen)

    # 若鼠标长按则撤回点击事件
    def _call_back_click(self):
        pass

    def draw_mouse_mark(self):
        pass



