import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from gui.layout.box_layout import VBoxLayout, HBoxLayout
from settings import *


class LevelMenu:
    def __init__(self, manager):
        self.manager = manager

        self.chapter_1_level_descriptions = {
            '1': 'Time! History and future',
            '2': 'Where is it? O_o',
            '3': 'They are moving!',
            '4': 'Strange motion? O_o',
            '5': '#Position, #Velocity and #Acceleration',
            '6': 'Weight, or Mass? Here comes force',
            '7': 'Strong Man!',
            '8': '#Force and #Acceleration',
            '9': 'Too many force',
            '10': '*Magical Circle :O'
        }

        # 创建主容器面板
        self.main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 400, 0), (800, SCREEN_HEIGHT)),
            manager=manager,
            container=None, anchors={'left': 'left', 'right': 'right', 'top': 'top', 'bottom': 'bottom'}
        )

        # 创建可滚动的容器
        self.scroll_panel = pygame_gui.elements.ui_scrolling_container.UIScrollingContainer(
            relative_rect=pygame.Rect((0, 0), (800, SCREEN_HEIGHT)),
            manager=manager,
            container=self.main_panel,
            object_id=ObjectID(object_id='#custom_scroll_container'),
        )
        self.scroll_panel.vert_scroll_bar.set_dimensions((110, 110))
        self.scroll_panel.horiz_scroll_bar.hide()

        # 创建垂直布局
        self.main_layout = VBoxLayout(
            container=self.scroll_panel,
            padding=10, spacing=10, manager=manager, mode='simple'
        )

        # 添加章节标题
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (800, 100)),
            text='Select Level',
            manager=manager,
            container=self.scroll_panel
        )
        self.main_layout.add_widget(self.title)

        # 添加关卡项
        for i in range(10):  # 增加关卡数量，以确保内容超出屏幕高度
            # 创建水平布局面板
            level_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((0, 0), (0, 100)),
                manager=manager,
                container=self.scroll_panel
            )
            level_layout = HBoxLayout(
                container=level_panel,
                padding=10, spacing=10, manager=manager, mode='proportional'
            )

            # 添加关卡按钮
            level_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((0, 0), (200, 50)),
                text=f'Level {i + 1}',
                manager=manager,
                container=level_panel,
                object_id=ObjectID('#level_btn')
            )
            level_layout.add_widget(level_button)

            # 动态设置按钮属性，便于事件处理
            setattr(self, f'level_button_{i}', level_button)

            # 添加描述文本框
            level_description = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((0, 0), (600, 50)),  # 确保文本框占据足够的宽度
                text=self.chapter_1_level_descriptions[f'{i + 1}'],
                manager=manager,
                container=level_panel,
                object_id=ObjectID('#level_text')
            )
            level_layout.add_widget(level_description, ratio=3)

            # 将水平布局添加到主垂直布局
            self.main_layout.add_layout(level_layout, ratio=1)

        # 更新滚动面板的大小以适应内容
        self.scroll_panel.set_scrollable_area_dimensions(
            (800, self.main_layout.height)
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for i in range(10):  # 这里的范围应与关卡数量一致
                level_button = getattr(self, f'level_button_{i}', None)
                if event.ui_element == level_button:
                    print(f'Level {i + 1} selected')
                    return f'level_{i + 1}'
        return None

    def update(self):
        pass

    def draw(self, screen):
        pass
