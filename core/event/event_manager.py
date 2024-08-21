import logging

class EventManager:
    def __init__(self):
        self.events = {}
        logging.basicConfig(level=logging.INFO)

    def register_event(self, event_name, callback, priority=0):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append((priority, callback))
        # 按优先级排序，优先级高的先执行
        self.events[event_name].sort(key=lambda x: x[0], reverse=True)

        logging.info(f"Event '{event_name}' registered.")

    def unregister_event(self, event_name, callback):
        if event_name in self.events:
            self.events[event_name].remove(callback)
            if not self.events[event_name]:
                del self.events[event_name]
            logging.info(f"Event '{event_name}' unregistered.")

    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self.events:
            logging.info(f"Event '{event_name}' triggered.")
            for callback in self.events[event_name]:
                callback(*args, **kwargs)
        else:
            logging.warning(f"Event '{event_name}' not found.")

    def clear_all_events(self):
        self.events.clear()
        logging.info("All events cleared.")
