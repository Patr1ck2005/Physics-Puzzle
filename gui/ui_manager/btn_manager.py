import pygame
from pygame import Rect, Surface, Color, Vector2, Vector3
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel, UIImage, UIProgressBar

from gui.ui_panel.bottom_panel import BottomPanel
from settings import *


class ButtonManager:
    def __init__(self, engine, hud):
        self.engine = engine
        self.hud = hud

        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))  # 外置UI管理器
        self.default_size = (50, 30)
        self.toggle_gravity_window = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 50, *self.default_size),
            text='Toggle Menu',
            manager=self.manager
        )
        self._create_gravity_setting()
        self.button_panel = BottomPanel(self.manager)

    def update(self):
        self.manager.update(pygame.time.get_ticks() / 1000.0)

    # 处理事件的方法，根据事件类型执行相应的操作
    def process_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn = event.ui_element
            if btn == self.button_panel:
                print("settings clicked!")
            elif btn == self.button_panel.pause_btn:
                self.engine.pause = not self.engine.pause
                btn.set_text('resume' if self.engine.pause else 'pause')
            elif btn == self.button_panel.init_btn:
                self.engine.init_world()
            elif btn == self.button_panel.speed_btn:
                self.engine.time_scale *= 2.0
                self.hud.update_time_scale(self.engine.time_scale)
            elif btn == self.button_panel.slow_btn:
                self.engine.time_scale *= 0.5
                self.hud.update_time_scale(self.engine.time_scale)

            elif btn == self.button_panel.gravity_setting:
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
            return True

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.universal_gravity_slider:
                self.universal_gravity_value_label.set_text(f'universal gravity:{event.value:.2f}')
                self.engine.G = event.value
            elif event.ui_element == self.gravity_slider:
                self.gravity_value_label.set_text(f'earth gravity:{event.value:.2f}')
                self.engine.gravity = event.value
            return True

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                return True
        return False

    def render(self, screen):
        self.manager.draw_ui(screen)

    def _create_gravity_setting(self, visible=False):
        # 创建一个 UI 窗口
        self.gravity_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((SCREEN_WIDTH-600, SCREEN_HEIGHT-300), (300, 200)),  # 窗口位置和大小
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
            relative_rect=pygame.Rect((10, 20), (150, 30)),
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
            relative_rect=pygame.Rect((10, 90), (150, 30)),
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
