import time

import pygame
import pygame_gui

from .hud import HUD
from .item_bar_ui import ItemBar
from .button_manager import ButtonManager
from core.objects_manager import ObjectManager
from settings import *


class UIManager:
    def __init__(self, screen, engine):
        self.screen = screen
        self.engine = engine
        self.hud = HUD(screen)   # HUD
        self.obj_manager = ObjectManager(screen, engine.space)   # 物理对象UI管理器
        self.btn_manager = ButtonManager(screen, engine, self.hud)   # 按钮UI
        self.item_bar = ItemBar(screen)   # 物品栏UI

        self.m_pos = None
        self.m_d_pos = None
        self.pressing_start_time = None

    # 依次检测鼠标是否悬停于指定UI
    def update(self):
        self.obj_manager.update(self.m_pos, self.m_d_pos)
        self.btn_manager.update()
        # 始终同步鼠标位置
        self.m_pos = pygame.mouse.get_pos()
        self.m_d_pos = pygame.mouse.get_rel()
        self.is_mouse_over()
        # 检测鼠标是否长按
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # 左键
            if time.time() - self.pressing_start_time > 0.1:  # 按下超过0.1秒算长按
                self.on_press()
                self.obj_manager.on_press()
                # 触发长按的时候需要撤回点击事件 (例如, 双次点击放置和长按放置取其一即可)
                self.call_back_click()
                self.obj_manager.call_back_click()

    def process_event(self, event):
        self.btn_manager.process_event(event)
        self.obj_manager.process_event(event)
        # 当鼠标点击时, 处理鼠标点击和UI的交互
        if event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.pressing_start_time = time.time()
            self.on_click()
            self.obj_manager.on_click()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_release()
            self.obj_manager.on_release()

    def is_mouse_over(self):
        self.item_bar.is_mouse_over(self.m_pos)
        # self.btn_manager.is_mouse_over(self.m_pos)

    # 检测UI是否被点击
    def on_click(self):
        # 获取物品栏放置结果
        placed_item = self.item_bar.on_click(self.m_pos)
        # 更新HUD显示物品栏选择结果(由于选择机制, 必须放在后面)
        self.hud.current_selection = self.item_bar.get_selected_item()
        if placed_item is not None:
            self.obj_manager.add_obj(placed_item)
        # call_btn = self.btn_manager.on_click(self.m_pos)
        # self.match_btn_call(call_btn)

    # 若鼠标长按则撤回点击事件
    def call_back_click(self):
        pass

    def on_press(self):
        self.item_bar.on_press(self.m_pos)

    def on_release(self):
        self.item_bar.on_release(self.m_pos)

    # 依次渲染所有UI
    def render_all_ui(self):
        self.item_bar.render()
        self.btn_manager.render()
        self.obj_manager.render_running_objs()
        self.hud.render()


