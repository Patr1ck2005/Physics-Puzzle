import pygame
import pygame_gui
from pygame import Rect, Color
from pygame_gui.core import ObjectID

from gui.layout.box_layout import HBoxLayout, VBoxLayout
from settings import *


class ChapterMenu:
    def __init__(self, manager):
        self.manager = manager
        self.animating_panel = None
        self.animation_progress = 0.0

        # 创建主容器面板
        self.main_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((50, 50), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)),
                                                      manager=manager)

        # 创建水平布局
        self.main_layout = HBoxLayout(container=self.main_panel, padding=20, spacing=20, manager=manager, mode='proportional')

        # 创建章节UI
        self.chapter1 = self.create_chapter_ui('Classical Mechanics',
                                               'assets/images/CM.png',
                                               'Understand the fundamental theories\n and applications of classical mechanics.')
        self.chapter2 = self.create_chapter_ui('Electrostatics and Magnetostatics',
                                               'assets/images/CEM.png',
                                               'Explore the fascinating world of electrostatics and magnetostatics.')
        self.chapter3 = self.create_chapter_ui('Electromagnetism',
                                               'assets/images/EM.png',
                                               'Delve into the study of electromagnetism and its modern applications.')

        # 将章节UI添加到主布局中
        self.main_layout.add_layout(self.chapter1['layout'])
        self.main_layout.add_layout(self.chapter2['layout'])
        self.main_layout.add_layout(self.chapter3['layout'])

    def create_chapter_ui(self, title, image_path, description):
        # 创建面板容器
        panel = pygame_gui.elements.UIPanel(relative_rect=Rect((0, 0), (200, 300)), manager=self.manager, container=self.main_panel)
        # 创建面板布局
        layout = VBoxLayout(container=panel, padding=10, spacing=10, manager=self.manager, mode='proportional')

        # 添加章节按钮并显示图片
        chapter_button = pygame_gui.elements.UIButton(relative_rect=Rect((0, 0), (200, 200)),
                                                      text='',
                                                      manager=self.manager,
                                                      container=panel,
                                                      object_id=ObjectID(f'#chapter_button_{title}'))

        # 描述面板（初始透明）
        description_panel = pygame_gui.elements.UIPanel(relative_rect=Rect((10, 200), (200, 300)),
                                                        manager=self.manager,
                                                        container=panel,
                                                        object_id="#description_panel")

        description_panel.background_colour = Color(0, 0, 0, 30)  # 初始全透明背景
        description_panel.rebuild()

        # 添加描述标签
        description_textbox = pygame_gui.elements.UITextBox(
            html_text=description,
            relative_rect=pygame.Rect((0, 10), (180, 200)),
            manager=self.manager,
            container=description_panel
        )

        # 设置按钮事件：鼠标悬停时开始动画
        chapter_button.set_text('')  # 隐藏按钮文本

        layout.add_widget(chapter_button)

        return {
            'panel': panel,
            'layout': layout,
            'button': chapter_button,
            'description_panel': description_panel,
            'description_textbox': description_textbox
        }

    def start_animation(self, panel):
        self.animating_panel = panel
        self.animation_progress = 0.0

    def update(self):
        # 更新动画
        if self.animating_panel:
            self.animation_progress += 0.1
            alpha_value = min(180, int(self.animation_progress * 180))  # 逐渐从0变为180
            self.animating_panel.background_colour = Color(0, 0, 0, alpha_value)
            if alpha_value >= 180:
                self.animating_panel = None  # 动画结束

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.chapter1['button']:
                return "chapter1"
            elif event.ui_element == self.chapter2['button']:
                return "chapter2"
            elif event.ui_element == self.chapter3['button']:
                return "chapter3"
        return None

    def draw(self, screen):
        pass
