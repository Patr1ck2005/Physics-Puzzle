import pygame
from scripts.utils import Round


class BaseUI:
    def __init__(self, screen,
                 name='Default', position=None, size=None, ico_color=(100, 100, 100)):
        self.name = name
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.text = name
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
        print(self.name, "released")

    def call_click(self):
        # 默认的点击事件处理方法，可以在子类中重写
        print(f'{self.name} was clicked')

    def call_press(self):
        # 默认的按住事件处理方法，可以在子类中重写
        print(f'pressing {self.name}')


class BaseUIBox(BaseUI):
    def __init__(self, screen,
                 name='de_Box', position=None, size=(60, 40), ico_color=(100, 100, 100), ):
        super().__init__(screen, name, position, size, ico_color, )

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
                 radius=30, ico_color=(100, 100, 100), ):
        super().__init__(screen, name, center, radius, ico_color, )

    @property
    def center(self):
        return self.position[0]+self.size, self.position[1]+self.size

    def set_click_region(self):
        self.click_region = Round(self.center, self.size)  # 这里的position是圆心, size是半径

    def draw(self, screen):
        pygame.draw.circle(screen, self._color, self.center, self.size)
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.position[0]+15, self.position[1]+10))
