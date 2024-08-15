import pygame


class BaseUI:
    def __init__(self, screen,
                 position=(100, 100), ico_color=(100, 100, 100), name='Default', size=(60, 40)):
        self.name = name
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.text = name
        self.position = position
        self.size = size
        self.click_rect = pygame.Rect(*self.position, *self.size)
        self.ico_color = ico_color
        self.color = ico_color

    @staticmethod
    def highlight(color):
        return [min(int(50 + c), 255) for c in color]

    @staticmethod
    def mark_selection(color):
        return [int(255 - c) for c in color]

    # 可在子类中重写
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.position, *self.size))
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.position[0] + 10, self.position[1] + 5))

    def is_mouse_over(self, m_pos):
        if self.click_rect.collidepoint(*m_pos):
            self.color = self.highlight(self.ico_color)
            return True
        else:
            self.color = self.ico_color

    def on_click(self, m_pos):
        if self.click_rect.collidepoint(*m_pos):
            self.color = self.mark_selection(self.ico_color)
            return True
        else:
            self.color = self.ico_color

    def on_release(self, m_pos):
        if self.click_rect.collidepoint(*m_pos):
            self.color = self.mark_selection(self.ico_color)
        else:
            self.color = self.ico_color

    def call_click(self):
        # 默认的点击事件处理方法，可以在子类中重写
        pass
