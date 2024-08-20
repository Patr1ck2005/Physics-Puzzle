import pygame

from settings import *


# HUD类定义
class HUD:
    def __init__(self, initial_score=0):

        self.font = pygame.font.Font(None, 24)
        self.score = initial_score
        self.time_scale = 1
        self.current_selection = None

        self.default_color = (200, 200, 200)
        self.score_color = (255, 255, 255)

    def update_score(self, points):
        self.score += points

    def update_current_selection(self, current_selection):
        self.current_selection = current_selection

    def update_time_scale(self, time_scale):
        self.time_scale = time_scale

    def render(self, screen):
        # 渲染得分
        score_text = self.font.render(f'Score: {self.score}', True, self.score_color)
        score_rect = score_text.get_rect(topleft=(300, 10))
        screen.blit(score_text, score_rect)

        # 渲染当前选择
        selection_text = self.font.render(f'Current Selection: {self.current_selection}', True, self.default_color)
        selection_rect = selection_text.get_rect(topleft=(300, 50))
        screen.blit(selection_text, selection_rect)

        # 渲染时间倍率
        time_scale_text = self.font.render(f'time rate: X{self.time_scale}', True, self.default_color)
        time_scale_rect = time_scale_text.get_rect(topleft=(300, 90))
        screen.blit(time_scale_text, time_scale_rect)

    def reset(self):
        self.score = 0
        self.lives = 3
