from scripts.utils import Round

import pygame
import pygame_gui
from pygame_gui.core.ui_element import UIElement
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements.ui_button import UIButton

import pygame
import pygame_gui
from pygame_gui.core.ui_element import UIElement
from pygame_gui.core.interfaces import IUIManagerInterface

import pygame
import pygame_gui
from pygame_gui.core.ui_element import UIElement
from pygame_gui.core.interfaces import IUIManagerInterface


class UICircleButton(UIElement):
    def __init__(self, relative_rect: pygame.Rect, text: str, manager: IUIManagerInterface, container=None,
                 starting_height: int = 1, layer_thickness: int = 1):
        super().__init__(relative_rect, manager, container, starting_height=starting_height,
                         layer_thickness=layer_thickness)

        self.text = text
        self.image = pygame.Surface(relative_rect.size, pygame.SRCALPHA)
        self.rect = relative_rect
        self.manager = manager
        self.pressed = False

        # 确保 object_ids 被初始化
        self.object_ids = self.object_ids if self.object_ids else ['default_button']

        self._create_image()

    def _create_image(self):
        # 绘制圆形按钮
        pygame.draw.circle(self.image, (0, 0, 255), (self.rect.width // 2, self.rect.height // 2), self.rect.width // 2)

        # 使用 Pygame 的字体渲染
        font = pygame.font.Font(None, 24)  # 使用默认字体，可以替换成需要的字体文件
        text_surface = font.render(self.text, True, pygame.Color('#FFFFFF'))
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surface, text_rect.topleft)

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                self.on_click()
                return True
        return False

    def update(self, time_delta: float):
        super().update(time_delta)

    def on_click(self):
        print(f"{self.text} Button Clicked")

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect.topleft)


class BaseUI:
    def __init__(self, screen,
                 name='Default', position=None, size=None, text='Default', ico_path=None, ico_color=(100, 100, 100)):
        self.name = name
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.text = text
        self.ico = None
        self.position = position
        self.size = size
        self.click_region = None
        self.ico_color = ico_color
        self._color = ico_color

        self.set_click_region()

    @staticmethod
    def highlight(color):
        return [min(int(50 + c), 255) for c in color]

    @staticmethod
    def mark_selection(color):
        return [int(255 - c) for c in color]

    # 需在子类中重写
    def set_click_region(self):
        pass

    # 需在子类中重写
    def draw(self, screen):
        pass

    def is_mouse_over(self, m_pos):
        if self.click_region.collidepoint(*m_pos):
            self._color = self.highlight(self.ico_color)
            return True
        else:
            self._color = self.ico_color

    def on_click(self, m_pos):
        if self.click_region.collidepoint(*m_pos):
            self._color = self.mark_selection(self.ico_color)
            self.call_click()
            return True
        else:
            self._color = self.ico_color

    def on_press(self, m_pos):
        if self.click_region.collidepoint(*m_pos):
            self._color = self.mark_selection(self.ico_color)
            self.call_press()
            return True
        else:
            self._color = self.ico_color

    def on_release(self, m_pos):
        if self.click_region.collidepoint(*m_pos):
            print(f'{self.name} was released')

    def call_click(self):
        # 默认的点击事件处理方法，可以在子类中重写
        print(f'{self.name} was clicked')

    def call_press(self):
        # 默认的按住事件处理方法，可以在子类中重写
        print(f'pressing {self.name}')

    def load_icon(self, icon_path):
        self.ico = pygame.image.load(icon_path)


class BaseUIBox(BaseUI):
    def __init__(self, screen,
                 name='de_Box', position=None, size=(60, 40), text='Default', ico_path=None, ico_color=(100, 100, 100), ):
        super().__init__(screen, name, position, size, text, ico_path, ico_color, )
        self.ico = pygame.transform.scale(pygame.image.load(ico_path),
                                          (int(size[0]), int(size[1]))) if ico_path is not None else None

    @property
    def center(self):
        return self.position[0]+self.size[0]/2, self.position[1]+self.size[1]/2

    def set_click_region(self):
        self.click_region = pygame.Rect(*self.position, *self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, (*self.position, *self.size))
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.position[0] + 10, self.position[1] + 5))


class BaseUICircle(BaseUI):
    def __init__(self, screen,
                 name='de_Circle', center=None,
                 radius=30, text='Default', ico_path=None, ico_color=(100, 100, 100), ):
        super().__init__(screen, name, center, radius, text, ico_path, ico_color, )
        self.ico = pygame.transform.scale(pygame.image.load(ico_path),
                                          (int(radius*2), int(radius*2))) if ico_path is not None else None

    @property
    def center(self):
        return self.position[0]+self.size, self.position[1]+self.size

    def set_click_region(self):
        self.click_region = Round(self.center, self.size)  # 这里的position是圆心, size是半径

    def draw(self, screen):
        pygame.draw.circle(screen, self._color, self.center, self.size)
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.center[0]-self.size, self.center[1]-10))
