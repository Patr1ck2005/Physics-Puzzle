import pygame
from pygame import Rect, Surface, Color, Vector2, Vector3
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel, UIImage, UIProgressBar
from .base_ui import UICircleButton

from settings import *


class ButtonManager:
    def __init__(self, screen, engine, hud):
        self.screen = screen
        self.engine = engine
        self.hud = hud

        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))  # 外置UI管理器
        default_size = (50, 30)
        self.all_buttons = {
            # "setting": UICircleButton(pygame.Rect(SCREEN_WIDTH-50, SCREEN_HEIGHT-50, 30, 30), text='Setting', manager=self.manager),
            "setting": UIButton(pygame.Rect(SCREEN_WIDTH-80, SCREEN_HEIGHT-50, *default_size), text='Setting', manager=self.manager),
            "rewind": UIButton(pygame.Rect(50, SCREEN_HEIGHT-50, *default_size), text='rewind', manager=self.manager),
            "slow": UIButton(pygame.Rect(200, SCREEN_HEIGHT - 50, *default_size), text='slow', manager=self.manager),
            "pause/resume": UIButton(pygame.Rect(250, SCREEN_HEIGHT - 50, *default_size), text='pause', manager=self.manager),
            "speed": UIButton(pygame.Rect(300, SCREEN_HEIGHT - 50, *default_size), text='speed', manager=self.manager),
        }

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

    def is_mouse_over(self, m_pos):
        pass

    def on_click(self, m_pos):
        pass

    def render(self):
        self.manager.draw_ui(self.screen)
