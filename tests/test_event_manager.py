"""EventManager 事件系统单元测试"""
import pytest

from core.event.event_manager import EventManager


class TestEventManagerRegister:
    """事件注册"""

    def test_register_single_event(self):
        em = EventManager()
        em.register_event("test", lambda: None)
        assert "test" in em.events

    def test_register_multiple_callbacks(self):
        em = EventManager()
        em.register_event("test", lambda: None, priority=1)
        em.register_event("test", lambda: None, priority=2)
        assert len(em.events["test"]) == 2

    def test_priority_ordering(self):
        em = EventManager()
        results = []
        em.register_event("test", lambda: results.append("low"), priority=1)
        em.register_event("test", lambda: results.append("high"), priority=10)
        em.trigger_event("test")
        assert results == ["high", "low"]


class TestEventManagerTrigger:
    """事件触发"""

    def test_trigger_executes_callback(self):
        em = EventManager()
        called = [False]
        em.register_event("test", lambda: called.__setitem__(0, True))
        em.trigger_event("test")
        assert called[0] is True

    def test_trigger_passes_args(self):
        em = EventManager()
        received = []
        em.register_event("test", lambda *a, **kw: received.append((a, kw)))
        em.trigger_event("test", 1, 2, key="value")
        assert received == [((1, 2), {"key": "value"})]

    def test_trigger_nonexistent_event_does_not_raise(self):
        """缺失事件不应抛异常，仅记录警告"""
        em = EventManager()
        # 不应抛出异常
        em.trigger_event("nonexistent")

    def test_trigger_multiple_callbacks(self):
        em = EventManager()
        results = []
        em.register_event("test", lambda: results.append(1))
        em.register_event("test", lambda: results.append(2))
        em.trigger_event("test")
        assert len(results) == 2


class TestEventManagerUnregister:
    """事件注销"""

    def test_unregister_existing_callback(self):
        em = EventManager()
        callback = lambda: None
        em.register_event("test", callback)
        em.unregister_event("test", callback)
        assert "test" not in em.events

    def test_unregister_removes_correct_callback(self):
        em = EventManager()
        cb1 = lambda: None
        cb2 = lambda: None
        em.register_event("test", cb1)
        em.register_event("test", cb2)
        em.unregister_event("test", cb1)
        assert len(em.events["test"]) == 1
        # 确认剩下的是 cb2
        assert em.events["test"][0][1] == cb2

    def test_unregister_nonexistent_event_does_not_raise(self):
        em = EventManager()
        em.unregister_event("nonexistent", lambda: None)


class TestEventManagerClear:
    """清空所有事件"""

    def test_clear_all_events(self):
        em = EventManager()
        em.register_event("a", lambda: None)
        em.register_event("b", lambda: None)
        em.clear_all_events()
        assert len(em.events) == 0
