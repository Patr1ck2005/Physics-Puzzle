from pygame import Rect

from scripts.utils import Round, Poly

import pygame

from settings import WHITE


class BaseUI:
    def __init__(self,
                 name='Default', position=None, size=None, text=None, ico_path=None, ico_color=(100, 100, 100)):
        self.name = name
        self.font = pygame.font.Font(None, 36)
        self.text = text if text else name
        self.ico = None
        self.click_region = None
        self.ico_color = ico_color
        self._color = ico_color

        self.position = position
        self.size = size
        self.set_click_region()

        self.is_selected = False

    @staticmethod
    def highlight(color):
        return [min(int(50 + c), 255) for c in color]

    @staticmethod
    def mark_selection(color):
        return [int(255 - c) for c in color]

    # 获取一些基本信息, 然后更新. 在子类中续写
    def update(self, m_pos):
        self.is_mouse_over(m_pos)

    # 需在子类中重写
    def set_click_region(self):
        pass

    # 在草图的基础上画出图片
    def draw(self, screen):
        self.draw_mark(screen)
        self.draw_draft(screen)
        if self.ico is not None:
            screen.blit(self.ico, self.position)

    # 通过pygame原生图形作图, 需要在子类中重写
    def draw_draft(self, screen):
        pass

    def draw_mark(self, screen):
        pass

    def draw_icon(self, screen):
        pass

    # 显示调用
    def draw_center2mouse(self, screen, m_pos):
        pygame.draw.line(screen, (255, 255, 255), self.ui_center, m_pos, 3)

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
        # print(f'pressing {self.name}')
        pass

    def load_icon(self, icon_path):
        self.ico = pygame.image.load(icon_path)


class BaseUIRect(BaseUI):
    def __init__(self,
                 name='de_Box', position=None, size=(60, 40), text=None, ico_path=None, ico_color=(100, 100, 100), ):
        super().__init__(name, position, size, text, ico_path, ico_color, )
        self.ico = pygame.transform.scale(pygame.image.load(ico_path),
                                          (int(size[0]), int(size[1]))) if ico_path is not None else None

    @property
    def ui_center(self):
        return self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2

    @ui_center.setter
    def ui_center(self, pos):
        self.position = pos[0] - self.size[0] / 2, pos[1] - self.size[1] / 2
        self.set_click_region()

    def set_click_region(self):
        # if self.position:
        #     self.click_region = pygame.Rect(*self.position, *self.size)
        # else:
        #     print(f'{self.name} has no position to set click region')
        self.click_region = pygame.Rect(*self.position, *self.size)

    def draw_draft(self, screen):
        pygame.draw.rect(screen, self._color, (*self.position, *self.size))
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.position[0] + 10, self.position[1] + 5))

    def draw_mark(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, (255, 255, 255), Rect(*self.position, *self.size).scale_by(1.1))


class BaseUICircle(BaseUI):
    def __init__(self,
                 name='de_Circle', center=None,
                 radius=30, text=None, ico_path=None, ico_color=(100, 100, 100), ):
        self._center = center
        super().__init__(name, center, radius, text, ico_path, ico_color, )
        self.ico = pygame.transform.scale(pygame.image.load(ico_path),
                                          (int(radius * 2), int(radius * 2))) if ico_path is not None else None

    @property
    def ui_center(self):
        return self._center

    @ui_center.setter
    def ui_center(self, pos):
        self._center = pos
        self.set_click_region()

    def set_click_region(self):
        self.click_region = Round(self._center, self.size)  # 这里的position是圆心, size是半径

    def draw_draft(self, screen):
        pygame.draw.circle(screen, self._color, self._center, self.size)
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self._center[0] - self.size, self._center[1] - 10))

    def draw_mark(self, screen):
        if self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255), self._center, self.size * 1.1+5, 3)


class BaseUILine(BaseUI):
    def __init__(self,
                 name='de_Line', position=None,
                 width=10, text=None, ico_path=None, ico_color=(100, 100, 100), ):
        super().__init__(name, position, width, text, ico_path, ico_color, )

    def update(self, m_pos):
        pass

    def draw_draft(self, screen):
        if self.position:
            pygame.draw.line(screen, self._color, self.position[0], self.position[1], self.size)


class BaseUIBox(BaseUI):
    def __init__(self,
                 name='de_Box', center=None, angle=0, size=(60, 40), text=None, ico_path=None,
                 ico_color=(100, 100, 100), ):
        self._center = center
        self._points = ((center[0] + size[0] // 2, center[1] + size[1] // 2),
                        (center[0] + size[0] // 2, center[1] - size[1] // 2),
                        (center[0] - size[0] // 2, center[1] - size[1] // 2),
                        (center[0] - size[0] // 2, center[1] + size[1] // 2))
        super().__init__(name, center, size, text, ico_path, ico_color, )
        self._angle = 0
        self.ico = pygame.transform.scale(pygame.image.load(ico_path),
                                          (int(size[0]), int(size[1]))) if ico_path is not None else None

    @property
    def ui_center(self):
        return self._center

    @ui_center.setter
    def ui_center(self, pos):
        self.click_region.move(pos[0]-self._center[0], pos[1]-self._center[1])
        self._center = pos

    @property
    def ui_angle(self):
        return self._angle

    def set_click_region(self):
        self.click_region = Poly(self._points)

    def set_ui_angle(self, angle, center):
        self.click_region.self_rotate_rad(angle - self._angle, center)
        self._angle = angle

    def draw_draft(self, screen):
        pygame.draw.polygon(screen, self._color, self.click_region.points)
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.ui_center[0] - self.size[0]//2, self.ui_center[1] - self.size[1]//2))

    def draw_mark(self, screen):
        if self.is_selected:
            pygame.draw.circle(screen, WHITE, self.ui_center,
                               max(self.click_region.rect_width, self.click_region.rect_height)//1.5, 3)


class BaseUIPoly(BaseUI):
    def __init__(self,
                 name='de_Poly', points=(), angle=0, text=None, ico_path=None, ico_color=(100, 100, 100), ):
        self._points = points
        super().__init__(name, None, None, text, ico_path, ico_color, )
        self._center = self.click_region.center
        self._angle = 0
        self.ico = pygame.transform.scale(pygame.image.load(ico_path),
                                          (int(self.click_region.rect_width),
                                           int(self.click_region.rect_height))) if ico_path is not None else None

    @property
    def ui_center(self):
        return self._center

    @ui_center.setter
    def ui_center(self, pos):
        self.click_region.move(pos[0] - self._center[0], pos[1] - self._center[1])
        self._center = pos

    @property
    def ui_angle(self):
        return self._angle

    @property
    def poly_size(self):
        return self.click_region.rect_width, self.click_region.rect_height

    def set_click_region(self):
        self.click_region = Poly(self._points)

    def set_ui_angle(self, angle, center):
        self.click_region.self_rotate_rad(angle - self._angle, center)
        self._angle = angle

    def draw_draft(self, screen):
        pygame.draw.polygon(screen, self._color, self.click_region.points)
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.ui_center[0] - self.poly_size[0]//2, self.ui_center[1] - self.poly_size[1]//2))

    def draw_mark(self, screen):
        if self.is_selected:
            pygame.draw.circle(screen, WHITE, self.ui_center,
                               max(self.click_region.rect_width, self.click_region.rect_height)//1.5, 3)
