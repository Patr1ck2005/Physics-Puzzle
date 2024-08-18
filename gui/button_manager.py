import pygame
from pygame import Rect, Surface, Color, Vector2, Vector3
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel, UIImage, UIProgressBar

from settings import *


class ButtonManager:
    def __init__(self, screen, engine, hud):
        self.screen = screen
        self.engine = engine
        self.hud = hud

        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))  # 外置UI管理器
        self.default_size = (50, 30)
        self.all_buttons = {
            "setting": UIButton(pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 50, *self.default_size), text='Setting',
                                manager=self.manager),
            "rewind": UIButton(pygame.Rect(50, SCREEN_HEIGHT - 50, *self.default_size), text='rewind',
                               manager=self.manager),
            "slow": UIButton(pygame.Rect(200, SCREEN_HEIGHT - 50, *self.default_size), text='slow',
                             manager=self.manager),
            "pause/resume": UIButton(pygame.Rect(250, SCREEN_HEIGHT - 50, *self.default_size), text='pause',
                                     manager=self.manager),
            "speed": UIButton(pygame.Rect(300, SCREEN_HEIGHT - 50, *self.default_size), text='speed',
                              manager=self.manager),
        }
        self.toggle_gravity_window = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 50, *self.default_size),
            text='Toggle Menu',
            manager=self.manager
        )
        self._create_gravity_setting()

    def update(self):
        self.manager.update(pygame.time.get_ticks() / 1000.0)

    def process_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn = event.ui_element
            if btn == self.all_buttons.get('setting', None):
                print("settings clicked!")
            elif btn == self.all_buttons.get('pause/resume', None):
                self.engine.pause = not self.engine.pause
                btn.set_text('resume' if self.engine.pause else 'pause')
            elif btn == self.all_buttons.get('restart', None):
                self.engine.init_world()
            elif btn == self.all_buttons.get('speed', None):
                self.engine.time_scale *= 2.0
                self.hud.update_time_scale(self.engine.time_scale)
            elif btn == self.all_buttons.get('slow', None):
                self.engine.time_scale *= 0.5
                self.hud.update_time_scale(self.engine.time_scale)

            elif btn == self.toggle_gravity_window:
                # 切换菜单窗口的显示状态
                self.gravity_window.visible = not self.gravity_window.visible
                if self.gravity_window is None or not self.gravity_window.alive():
                    # 创建一个新的窗口实例
                    self._create_gravity_setting(True)
                else:
                    if self.gravity_window.visible:
                        self.gravity_window.show()
                    else:
                        self.gravity_window.hide()
            elif btn == self.gravity_checkbox:
                self.engine.if_gravity = not self.engine.if_gravity
                btn.set_text('tune off' if self.engine.if_gravity else 'tune on')
            elif btn == self.universal_gravity_checkbox:
                self.engine.if_uni_gravity = not self.engine.if_uni_gravity
                btn.set_text('tune off' if self.engine.if_uni_gravity else 'tune on')

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.universal_gravity_slider:
                self.universal_gravity_value_label.set_text(f'universal gravity:{event.value:.2f}')
                self.engine.G = event.value
            elif event.ui_element == self.gravity_slider:
                self.gravity_value_label.set_text(f'earth gravity:{event.value:.2f}')
                self.engine.gravity = event.value

    def render(self):
        self.manager.draw_ui(self.screen)

    def _create_gravity_setting(self, visible=False):
        # 创建一个 UI 窗口
        self.gravity_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((350, 150), (300, 200)),  # 窗口位置和大小
            manager=self.manager,
            window_display_title='Gravity Control',
            object_id='#gravity_window',
            visible=visible,
        )
        # # 创建一个标签，显示 "Gravity"
        # self.gravity_label = pygame_gui.elements.UILabel(
        #     relative_rect=pygame.Rect((120, 10), (120, 30)),
        #     text='Gravity',
        #     manager=self.manager,
        #     container=self.gravity_window
        # )

        # 创建一个滑块，用于调节万有引力
        self.universal_gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((100, 50), (150, 30)),
            start_value=1.0,
            value_range=(0.0, 10.0),
            manager=self.manager,
            container=self.gravity_window
        )

        # 创建一个标签，实时显示滑块值
        self.universal_gravity_value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 20), (120, 30)),
            text=f'universal gravity:{self.universal_gravity_slider.get_current_value():.2f}',
            manager=self.manager,
            container=self.gravity_window
        )

        # 创建一个滑块，用于调节重力大小系数
        self.gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((100, 120), (150, 30)),
            start_value=1.0,
            value_range=(0.0, 10.0),
            manager=self.manager,
            container=self.gravity_window
        )

        # 创建一个标签，实时显示滑块值
        self.gravity_value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 90), (120, 30)),
            text=f'earth gravity:{self.gravity_slider.get_current_value():.2f}',
            manager=self.manager,
            container=self.gravity_window
        )

        # 创建一个复选框，用于控制万有引力的开关
        self.universal_gravity_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 50), (60, 30)),
            text='tune on',
            manager=self.manager,
            container=self.gravity_window
        )

        # 创建一个复选框，用于控制地球重力的开关
        self.gravity_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 120), (60, 30)),
            text='tune on',
            manager=self.manager,
            container=self.gravity_window
        )
