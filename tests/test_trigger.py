"""Trigger 触发器单元测试"""
import time

import pytest

from core.event.event_manager import EventManager
from core.event.trigger.trigger import Trigger, ComplexCondition
from core.event.trigger.timer_trigger import TimerTrigger


class TestTriggerBasic:
    """基础 Trigger 行为"""

    def test_once_trigger_fires_once(self):
        em = EventManager()
        call_count = [0]
        em.register_event("test", lambda *a, **kw: call_count.__setitem__(0, call_count[0] + 1))

        condition = lambda: True
        trigger = Trigger(condition, "test", em, once=True)
        trigger.check_and_trigger()
        trigger.check_and_trigger()  # 第二次不应触发
        assert call_count[0] == 1

    def test_repeated_trigger_fires_multiple_times(self):
        em = EventManager()
        call_count = [0]
        em.register_event("test", lambda *a, **kw: call_count.__setitem__(0, call_count[0] + 1))

        condition = lambda: True
        trigger = Trigger(condition, "test", em, once=False)
        trigger.check_and_trigger()
        trigger.check_and_trigger()
        assert call_count[0] == 2

    def test_condition_false_does_not_fire(self):
        em = EventManager()
        call_count = [0]
        em.register_event("test", lambda *a, **kw: call_count.__setitem__(0, call_count[0] + 1))

        condition = lambda: False
        trigger = Trigger(condition, "test", em, once=True)
        trigger.check_and_trigger()
        assert call_count[0] == 0

    def test_multiple_event_names(self):
        em = EventManager()
        results = []
        em.register_event("a", lambda *a, **kw: results.append("a"))
        em.register_event("b", lambda *a, **kw: results.append("b"))

        condition = lambda: True
        trigger = Trigger(condition, ["a", "b"], em, once=True)
        trigger.check_and_trigger()
        assert set(results) == {"a", "b"}


class TestTriggerDebounce:
    """debounce_time 防抖"""

    def test_debounce_prevents_rapid_fire(self):
        em = EventManager()
        call_count = [0]
        em.register_event("test", lambda *a, **kw: call_count.__setitem__(0, call_count[0] + 1))

        condition = lambda: True
        trigger = Trigger(condition, "test", em, once=False, debounce_time=10)
        trigger.check_and_trigger()
        assert call_count[0] == 1
        # 立即再次检查，不应触发（debbounce 未过）
        trigger.check_and_trigger()
        assert call_count[0] == 1

    def test_debounce_allows_fire_after_wait(self):
        em = EventManager()
        call_count = [0]
        em.register_event("test", lambda *a, **kw: call_count.__setitem__(0, call_count[0] + 1))

        condition = lambda: True
        trigger = Trigger(condition, "test", em, once=False, debounce_time=0.1)
        trigger.check_and_trigger()
        assert call_count[0] == 1
        time.sleep(0.15)
        trigger.check_and_trigger()
        assert call_count[0] == 2


class TestTimerTrigger:
    """TimerTrigger 定时触发器"""

    def test_timer_fires_after_duration(self):
        em = EventManager()
        call_count = [0]
        em.register_event("timer_done", lambda *a, **kw: call_count.__setitem__(0, call_count[0] + 1))

        trigger = TimerTrigger(duration=0.1, event_names="timer_done",
                               event_manager=em, start_immediately=True, once=True)
        time.sleep(0.15)
        trigger.check_and_trigger()
        assert call_count[0] == 1

    def test_timer_not_fired_before_duration(self):
        em = EventManager()
        call_count = [0]
        em.register_event("timer_done", lambda *a, **kw: call_count.__setitem__(0, call_count[0] + 1))

        trigger = TimerTrigger(duration=10, event_names="timer_done",
                               event_manager=em, start_immediately=True, once=True)
        trigger.check_and_trigger()
        assert call_count[0] == 0

    def test_timer_not_started_returns_false(self):
        em = EventManager()
        trigger = TimerTrigger(duration=1, event_names="test",
                               event_manager=em, start_immediately=False, once=True)
        assert trigger._time_condition() is False


class TestComplexCondition:
    """ComplexCondition 组合条件"""

    def test_all_true(self):
        cond = ComplexCondition([lambda: True, lambda: True])
        assert cond() is True

    def test_any_false(self):
        cond = ComplexCondition([lambda: True, lambda: False])
        assert cond() is False
