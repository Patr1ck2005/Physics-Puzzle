import pygame

from settings import *


# HUD类定义
class HUD:
    def __init__(self, screen, initial_score=0, initial_lives=3):
        self.screen = screen

        self.font = pygame.font.Font(None, 36)
        self.selecting = None
        self.score = initial_score
        self.lives = initial_lives
        self.time_scale = 1
        self.default_color = (200, 200, 200)
        self.score_color = (255, 255, 255)
        self.lives_color = (255, 0, 0)

    def update_score(self, points):
        self.score += points

    def update_lives(self, change):
        self.lives += change

    def update_time_scale(self, time_scale):
        self.time_scale = time_scale

    def render(self):
        # 渲染得分
        score_text = self.font.render(f'Score: {self.score}', True, self.score_color)
        score_rect = score_text.get_rect(topleft=(300, 10))
        self.screen.blit(score_text, score_rect)

        # 渲染生命值
        lives_text = self.font.render(f'Lives: {self.lives}', True, self.lives_color)
        lives_rect = lives_text.get_rect(topleft=(300, 50))
        self.screen.blit(lives_text, lives_rect)

        # 渲染时间倍率
        time_scale_text = self.font.render(f'time rate: X{self.time_scale}', True, self.default_color)
        time_scale_rect = lives_text.get_rect(topleft=(300, 90))
        self.screen.blit(time_scale_text, time_scale_rect)

    def reset(self):
        self.score = 0
        self.lives = 3
