import pygame
import pymunk


# HUD类定义
class HUD:
    def __init__(self, screen, initial_score=0, initial_lives=3):
        self.selecting = None
        self.screen = screen
        self.score = initial_score
        self.lives = initial_lives
        self.font = pygame.font.Font(None, 36)
        self.score_color = (255, 255, 255)
        self.lives_color = (255, 0, 0)

        # 设置按钮
        self.settings_button = pygame.Rect(750, 10, 30, 30)

        # 物品栏
        self.inventory = [
            {"name": "Box", "type": "object",
             "rect": pygame.Rect(10, 10, 60, 60), 'color': (128, 128, 128)},
            {"name": "Force", "type": "abstract",
             "rect": pygame.Rect(80, 10, 60, 60),
             'color': (0, 50, 0)},
        ]

    def update_score(self, points):
        self.score += points

    def update_lives(self, change):
        self.lives += change

    def render(self):
        # 渲染得分
        score_text = self.font.render(f'Score: {self.score}', True, self.score_color)
        score_rect = score_text.get_rect(topleft=(10, 10))
        self.screen.blit(score_text, score_rect)

        # 渲染生命值
        lives_text = self.font.render(f'Lives: {self.lives}', True, self.lives_color)
        lives_rect = lives_text.get_rect(topleft=(10, 50))
        self.screen.blit(lives_text, lives_rect)

        # 绘制物品栏
        for item in self.inventory:
            if item == self.selecting:
                color = self.mark_underselection(item["color"])
            else:
                color = item["color"]
            pygame.draw.rect(self.screen, color, item["rect"])

        # 绘制设置按钮
        pygame.draw.rect(self.screen, (150, 150, 150), self.settings_button)

    def reset(self):
        self.score = 0
        self.lives = 3

    def select_inventory(self):
        self.selecting = None
        # 获取鼠标位置
        m_pos = pygame.mouse.get_pos()
        for item in self.inventory:
            if item["rect"].collidepoint(m_pos):
                self.selecting = item
        return self.selecting, m_pos

    @staticmethod
    def mark_underselection(color):
        return [min(int(10 + c), 255) for c in color]

    @staticmethod
    def mark_selection(color):
        return [int(0.8 * c) for c in color]
