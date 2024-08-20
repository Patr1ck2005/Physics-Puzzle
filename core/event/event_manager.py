class EventManager:
    def __init__(self):
        # 存储事件和它们的处理函数
        self.events = {}

    def register_event(self, event_name, callback):
        """
        注册一个事件及其对应的处理函数。

        :param event_name: 事件名称，作为事件的标识符
        :param callback: 当事件触发时执行的函数
        """
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(callback)

    def unregister_event(self, event_name, callback):
        """
        注销一个事件及其对应的处理函数。

        :param event_name: 事件名称
        :param callback: 需要移除的处理函数
        """
        if event_name in self.events:
            self.events[event_name].remove(callback)
            if not self.events[event_name]:
                del self.events[event_name]

    def trigger_event(self, event_name, *args, **kwargs):
        """
        触发一个事件，调用所有注册的处理函数。

        :param event_name: 事件名称
        :param args: 传递给处理函数的位置参数
        :param kwargs: 传递给处理函数的关键字参数
        """
        if event_name in self.events:
            for callback in self.events[event_name]:
                callback(*args, **kwargs)

    def clear_all_events(self):
        """
        清除所有注册的事件和它们的处理函数。
        """
        self.events.clear()