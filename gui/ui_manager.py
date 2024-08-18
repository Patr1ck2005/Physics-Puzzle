import time

import pygame
import pygame_gui

from .hud import HUD
from .item_bar_ui import ItemBar
from .button_manager import ButtonManager
from core.entity_manager import EntityManager
from core.force_manager import ForceManager
from settings import *

from core.entity import Entity
from core.force import AbstractForce
from core.tool import Tool


class UIManager:
    def __init__(self, screen, engine):
        self.screen = screen
        self.engine = engine
        self.hud = HUD(screen)   # HUD
        self.entity_manager = EntityManager(screen, engine.space)   # 物理对象UI管理器
        self.force_manager = ForceManager(screen, self.entity_manager)
        self.btn_manager = ButtonManager(screen, engine, self.hud)   # 按钮UI
        self.item_bar = ItemBar(screen)   # 物品栏UI

        self.m_pos = None
        self.m_d_pos = None
        self.pressing_start_time = None
        self.selected_item = None
        self.selected_tool = None

    def update(self):
        # 始终同步鼠标位置
        self.m_pos = pygame.mouse.get_pos()
        self.m_d_pos = pygame.mouse.get_rel()
        # 更新各种ui_manager, 依次检测鼠标是否悬停于指定UI
        self.entity_manager.update(self.m_pos, self.m_d_pos)
        self.force_manager.update(self.m_pos)
        self.item_bar.update(self.m_pos)

        self.btn_manager.update()
        # 检测鼠标是否长按
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # 左键
            if time.time() - self.pressing_start_time > 0.3:  # 按下超过0.3秒算长按
                self._on_press()
                self.entity_manager.on_press()
                # 触发长按的时候需要撤回实体点击事件 (例如, 双次点击放置和长按放置取其一即可)
                self.entity_manager.call_back_click()

    def process_event(self, event):
        self.btn_manager.process_event(event)
        # self.entity_manager.process_event(event)
        # 当鼠标点击时, 处理鼠标点击和UI的交互
        if event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.pressing_start_time = time.time()
            self._on_click()
        elif event.type == pygame.MOUSEBUTTONUP:
            self._on_release()

    # 检测哪个UI被点击
    def _on_click(self):
        # 简单储存物品栏选择结果
        selected = self.item_bar.on_click()
        # 简单储存世界实体选择结果
        selected_entity = self.entity_manager.on_click()
        # 获取物品栏放置结果
        placed_item = self.item_bar.placed_item
        if isinstance(placed_item, Entity):
            self.item_bar.remove_item_by_name(placed_item.name)
            self.entity_manager.add_entity(placed_item)
        else:
            if isinstance(placed_item, AbstractForce):
                if selected_entity and selected_entity.type == 'dynamic':
                    self.item_bar.remove_item_by_name(placed_item.name)
                    placed_item.set_target(selected_entity)
                    self.force_manager.add_force(placed_item)
                    # 若应用力则撤回实体点击事件
                    self.entity_manager.call_back_click()
                else:
                    print('force have to been apply to a certain dynamic entity')

        if self.selected_tool and selected_entity:
            # 应用工具 (先于获取工具选择结果)
            self.selected_tool.affect(target=selected_entity)
            # 若应用工具则撤回实体点击事件
            self.entity_manager.call_back_click()
        # 获取工具选择结果
        self.selected_tool = self.item_bar.selected_tool

        # 更新HUD显示物品栏选择结果
        self.hud.current_selection = selected or selected_entity

    # 检测哪个UI被按住
    def _on_press(self):
        self.item_bar.on_press(self.m_pos)

    # 检测哪个UI被松开
    def _on_release(self):
        self.item_bar.on_release(self.m_pos)
        self.entity_manager.on_release()

    # 依次渲染所有UI
    def render_all_ui(self):
        self.entity_manager.render_running_objs()
        self.force_manager.render_running_forces()
        self.item_bar.render()
        self.btn_manager.render()
        self.hud.render()

    # 若鼠标长按则撤回点击事件
    def _call_back_click(self):
        pass


