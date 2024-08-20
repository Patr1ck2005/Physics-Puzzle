import pygame
import pygame_gui
from pygame import Rect, Color
from gui.layout.box_layout import HBoxLayout
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
        self.chapter1 = self.create_chapter_ui('经典力学', 'assets/images/CM.png', '了解经典力学的基础理论和应用')
        self.chapter2 = self.create_chapter_ui('静电学与静磁学', 'assets/images/CEM.png', '探索静电学和静磁学的奇妙世界')
        self.chapter3 = self.create_chapter_ui('电磁学', 'assets/images/EM.png', '深入学习电磁学及其现代应用')

        # 将章节UI添加到主布局中
        self.main_layout.add_widget(self.chapter1['panel'])
        self.main_layout.add_widget(self.chapter2['panel'])
        self.main_layout.add_widget(self.chapter3['panel'])

    def create_chapter_ui(self, title, image_path, description):
        # 创建面板容器
        panel = pygame_gui.elements.UIPanel(relative_rect=Rect((0, 0), (200, 300)), manager=self.manager, container=self.main_panel)

        # 添加章节按钮并显示图片
        chapter_image = pygame.image.load(image_path).convert_alpha()
        chapter_button = pygame_gui.elements.UIButton(relative_rect=Rect((0, 0), (200, 200)),
                                                      text='',
                                                      manager=self.manager,
                                                      container=panel,
                                                      object_id=f'#chapter_button_{title}')
        chapter_button.set_image(chapter_image)

        # 描述面板（初始透明）
        description_panel = pygame_gui.elements.UIPanel(relative_rect=Rect((0, 200), (200, 100)),
                                                        manager=self.manager,
                                                        container=panel,
                                                        object_id="#description_panel")

        description_panel.background_colour = Color(0, 0, 0, 0)  # 初始全透明背景

        # 添加描述标签
        description_label = pygame_gui.elements.UILabel(relative_rect=Rect((10, 10), (180, 80)),
                                                        text=description,
                                                        manager=self.manager,
                                                        container=description_panel)

        # 设置按钮事件：鼠标悬停时开始动画
        chapter_button.set_hold_range((500, 500))  # 增加按钮点击范围（以防拖动失效）
        chapter_button.set_text('')  # 隐藏按钮文本

        def on_hover():
            self.start_animation(description_panel)

        chapter_button.hovered_over = on_hover

        return {
            'panel': panel,
            'button': chapter_button,
            'description_panel': description_panel,
            'description_label': description_label
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
