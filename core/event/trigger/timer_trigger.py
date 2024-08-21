import time

from core.event.trigger.trigger import Trigger


class TimerTrigger(Trigger):
    def __init__(self, duration, event_names, event_manager, start_immediately=True):
        """
        :param duration: 定时器的时间长度（秒）
        :param start_immediately: 是否立即开始计时
        """
        super().__init__(self._time_condition, event_names, event_manager, once=False)
        self.duration = duration
        self.start_time = time.time() if start_immediately else None

    def _time_condition(self):
        if self.start_time is None:
            return False
        return time.time() - self.start_time >= self.duration

    def start(self):
        """开始计时"""
        self.start_time = time.time()

    def reset(self):
        """重置定时器"""
        self.start_time = time.time()
