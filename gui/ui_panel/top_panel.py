import pygame
import pygame_gui
from pygame_gui.elements import UIButton

from settings import *
from gui.layout.box_layout import HBoxLayout


class TopPanel:
    def __init__(self, manager):
        """
        初始化底部面板。

        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        """
        self.manager = manager
        self.container_rect = pygame.Rect((SCREEN_WIDTH-200, 0), (200, 60))

        # 创建主面板容器
        self.panel_container = pygame_gui.elements.UIPanel(
            relative_rect=self.container_rect,
            manager=self.manager
        )

        # 创建主水平布局，用于将三个子布局放在一起
        self.main_layout = HBoxLayout(self.panel_container, padding=5, spacing=20, mode='proportional',
                                      manager=self.manager)

        # 添加时间管理部分
        self._create_setting_section()

        # # 添加第二部分
        # self._create_second_part_section()

        # # 添加第三部分
        # self._create_third_part_section()

    def _create_setting_section(self):
        """
        创建时间管理部分的布局，包含三个按钮。
        """
        self.setting_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (0, 0)),
            manager=self.manager,
            container=self.panel_container
        )
        self.setting_layout = HBoxLayout(self.setting_container, padding=5, spacing=10,
                                                 mode='proportional',
                                                 manager=self.manager)

        self.main_layout.add_layout(self.setting_layout, 1)

        self.slow_btn = UIButton(
            pygame.Rect(0, 0, 0, 0),
            text='slow',
            manager=self.manager,
            container=self.setting_container)

        self.pause_btn = UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='pause',
            manager=self.manager,
            container=self.setting_container
        )
        self.speed_btn = UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='speed',
            manager=self.manager,
            container=self.setting_container
        )

        self.setting_layout.add_widget(self.slow_btn)
        self.setting_layout.add_widget(self.pause_btn)
        self.setting_layout.add_widget(self.speed_btn)

    def _create_second_part_section(self):
        """
        创建第二部分的布局，包含三个按钮。
        """
        self.second_part_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (0, 0)),
            manager=self.manager,
            container=self.panel_container
        )
        self.second_part_layout = HBoxLayout(self.second_part_container, padding=5, spacing=10, mode='proportional',
                                             manager=self.manager)

        self.main_layout.add_layout(self.second_part_layout, 3)

        button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='Second Button 1',
            manager=self.manager,
            container=self.second_part_container
        )
        button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='Second Button 2',
            manager=self.manager,
            container=self.second_part_container
        )
        button3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='Second Button 3',
            manager=self.manager,
            container=self.second_part_container
        )

        self.second_part_layout.add_widget(button1)
        self.second_part_layout.add_widget(button2)
        self.second_part_layout.add_widget(button3)

    def _create_third_part_section(self):
        """
        创建第三部分的布局，包含三个按钮。
        """
        self.third_part_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (0, 0)),
            manager=self.manager,
            container=self.panel_container
        )
        self.third_part_layout = HBoxLayout(self.third_part_container, padding=5, spacing=10, mode='proportional',
                                            manager=self.manager)

        self.main_layout.add_layout(self.third_part_layout)

        self.gravity_setting = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='gravity setting',
            manager=self.manager,
            container=self.third_part_container
        )
        self.init_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='init world',
            manager=self.manager,
            container=self.third_part_container
        )
        self.property_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='hide property',
            manager=self.manager,
            container=self.third_part_container
        )

        self.third_part_layout.add_widget(self.gravity_setting)
        self.third_part_layout.add_widget(self.init_btn)
        self.third_part_layout.add_widget(self.property_btn)


# 示例用法
if __name__ == "__main__":
    pygame.init()
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(pygame.Color("#000000"))

    bottom_panel = TopPanel(manager)

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()

    pygame.quit()
