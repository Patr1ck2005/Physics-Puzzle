import time

import pygame

from core.event.trigger.trigger import Trigger
from settings import SCREEN_WIDTH


class TimerTrigger(Trigger):
    def __init__(self, duration, event_names, event_manager, start_immediately=True, once=False):
        """
        :param duration: 定时器的时间长度（秒）
        :param start_immediately: 是否立即开始计时
        """
        super().__init__(self._time_condition, event_names, event_manager, once=once)
        self.duration = duration
        self.start_time = time.time() if start_immediately else None

        self.remain_time = self.duration

    def _time_condition(self):
        if self.start_time is None:
            return False
        self.remain_time = self.duration - (time.time() - self.start_time)
        return self.remain_time <= 0

    def start(self):
        """开始计时"""
        self.start_time = time.time()

    def reset(self):
        """重置定时器"""
        self.start_time = time.time()

    def draw(self, screen):
        font = pygame.font.Font(None, 36)  # None表示使用默认字体，36是字体大小
        number = str(self.remain_time)  # 你要绘制的数字
        text_surface = font.render(str(number), True, (255, 255, 255))  # True表示启用抗锯齿，(255, 255, 255) 是字体颜色（白色）
        screen.blit(text_surface, (SCREEN_WIDTH // 2, 100))  # 将数字绘制到屏幕上 (100, 100) 位置


