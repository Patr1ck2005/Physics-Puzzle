import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from gui.layout.box_layout import VBoxLayout
from settings import *


class MainMenu:
    def __init__(self, manager):
        self.manager = manager

        # 创建主容器面板
        self.main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 400, 0), (800, SCREEN_HEIGHT)),
            manager=manager, )

        # 整个屏幕的垂直布局
        self.main_layout = VBoxLayout(container=self.main_panel,
                                      padding=10, spacing=10, manager=manager, mode='proportional')

        # 添加游戏标题
        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (800, 100)),
                                                 text='Physics GO',
                                                 manager=manager,
                                                 container=self.main_panel,
                                                 object_id=ObjectID('#main_menu_title', '@labels'))
        self.main_layout.add_widget(self.title)

        # 创建一个新的垂直布局和面板用于放置按钮
        self.button_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (0, 0)),
                                                        manager=manager, container=self.main_panel)
        self.button_layout = VBoxLayout(container=self.button_panel,
                                        padding=10, spacing=10, manager=manager, mode='proportional')

        # 将按钮布局添加到主布局中
        self.main_layout.add_layout(self.button_layout, 2)

        # 添加按钮
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (200, 50)),
                                                         text='Start Game',
                                                         manager=manager,
                                                         container=self.button_panel,
                                                         object_id=ObjectID('#main_menu_btn', '@labels'))
        self.button_layout.add_widget(self.start_button)

        self.options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (200, 50)),
                                                           text='Settings',
                                                           manager=manager,
                                                           container=self.button_panel,
                                                           object_id=ObjectID('#main_menu_btn', '@labels'))
        self.button_layout.add_widget(self.options_button)

        self.badges_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (200, 50)),
                                                          text='Badges',
                                                          manager=manager,
                                                          container=self.button_panel,
                                                          object_id=ObjectID('#main_menu_btn', '@labels'))
        self.button_layout.add_widget(self.badges_button)

        self.help_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (200, 50)),
                                                        text='Help',
                                                        manager=manager,
                                                        container=self.button_panel,
                                                        object_id=ObjectID('#main_menu_btn', '@labels'))
        self.button_layout.add_widget(self.help_button)

        self.support_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (200, 50)),
                                                           text='Support',
                                                           manager=manager,
                                                           container=self.button_panel,
                                                           object_id=ObjectID('#main_menu_btn', '@labels'))
        self.button_layout.add_widget(self.support_button)

        self.about_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (200, 50)),
                                                         text='About',
                                                         manager=manager,
                                                         container=self.button_panel,
                                                         object_id=ObjectID('#main_menu_btn', '@labels'))
        self.button_layout.add_widget(self.about_button)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                return "start_game"
            elif event.ui_element == self.options_button:
                return "settings"
            elif event.ui_element == self.badges_button:
                return "badges"
            elif event.ui_element == self.help_button:
                return "help"
            elif event.ui_element == self.support_button:
                return "support"
            elif event.ui_element == self.about_button:
                return "about"
        return None

    def update(self):
        pass

    def draw(self, screen):
        pass
