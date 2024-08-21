import json
import pymunk
from core.event.trigger_manager import TriggerManager, State
from core.event.event_manager import EventManager
from core.event.trigger.timer_trigger import TimerTrigger
from core.event.trigger.query_trigger import PointQueryTrigger
from core.event.events.events import show_console_message

class EventLoader:
    def __init__(self, events_json_file, entities, space=None):
        self.events_json_file = events_json_file
        self.entities = entities  # 从EntityLoader加载的实体
        self.space = space or pymunk.Space()  # Pymunk space
        self.event_manager = EventManager()
        self.trigger_manager = TriggerManager(self.event_manager)
        self.event_mapping = {
            "transition_to_state_b": self.transition_to_state_b,
            "show_console_message": lambda *args, **kwargs: show_console_message("You are now in StateB"),
        }

    def transition_to_state_b(self, *args, **kwargs):
        print("Transitioning to StateB")
        self.trigger_manager.transition_to_state("StateB")

    def load_events(self):
        with open(self.events_json_file, 'r') as f:
            config = json.load(f)

        # 加载事件
        for event_name, event_handler in config['events'].items():
            if event_handler in self.event_mapping:
                self.event_manager.register_event(event_name, self.event_mapping[event_handler])

        # 加载状态和触发器
        for state_config in config['states']:
            state = State(state_config['name'])
            for trigger_config in state_config['triggers']:
                trigger = self.create_trigger(trigger_config)
                if trigger:
                    state.add_trigger(trigger)
            self.trigger_manager.add_state(state)

        # 设置初始状态为 JSON 中定义的第一个状态
        if config['states']:
            self.trigger_manager.set_initial_state(config['states'][0]['name'])

        return self.trigger_manager, self.event_manager

    def create_trigger(self, trigger_config):
        trigger_type = trigger_config.get("type", "Generic")

        if trigger_type == "TimerTrigger":
            return TimerTrigger(
                duration=trigger_config['duration'],
                event_names=trigger_config['events'],
                event_manager=self.event_manager,
                start_immediately=trigger_config.get("start_immediately", True)
            )
        elif trigger_type == "PointQueryTrigger":
            entity_name = trigger_config['entity_name']
            entity = self.entities.get(entity_name)
            if entity:
                return PointQueryTrigger(
                    entity=entity,
                    target_point=tuple(trigger_config['target_point']),
                    event_names=trigger_config['events'],
                    event_manager=self.event_manager,
                    space=self.space,
                    min_duration=trigger_config.get("min_duration", 0)
                )
        return None
