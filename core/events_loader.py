import json
import pymunk

from core.event.trigger.label_trigger import LabelTrigger
from core.event.trigger_manager import TriggerManager, State
from core.event.event_manager import EventManager
from core.event.trigger.timer_trigger import TimerTrigger
from core.event.trigger.query_trigger import PointQueryTrigger
from core.event.events.events import *


class EventLoader:
    def __init__(self, events_json_file, all_objs, space, ui_manager):
        self.events_json_file = events_json_file
        self.space = space  # Pymunk space
        self.ui_manager = ui_manager
        self.event_manager = EventManager()
        self.trigger_manager = TriggerManager(self.event_manager)
        self.triggers = {}

        self.entities = all_objs['entities']  # 从 ObjLoader 加载的实体
        self.labels = all_objs['labels']  # 从 ObjLoader 加载的实体

    def state_transition(self, state_name, *args, **kwargs):
        self.trigger_manager.transition_to_state(state_name)

    def load_events(self):
        with open(self.events_json_file, 'r') as f:
            config = json.load(f)

        # 加载事件
        for event_name, event_handler in config['events'].items():
            handler_name = event_handler.get("handler")
            handler_params = event_handler.get("params", {})
            # 定义自定义状态转换逻辑，并在事件触发时执行。
            if handler_name == "state_transition":
                self.event_manager.register_event(
                    event_name,
                    lambda params=handler_params, *args, **kwargs: self.state_transition(**params)
                )
            elif handler_name == "show_message":
                self.event_manager.register_event(
                    event_name,
                    lambda params=handler_params, *args, **kwargs: show_message(manager=self.ui_manager, **params)
                )
            elif handler_name == "show_console_message":
                self.event_manager.register_event(
                    event_name,
                    lambda params=handler_params, *args, **kwargs: show_console_message(**params)
                )
        # 加载触发器
        for trigger_name, trigger_config in config['triggers'].items():
            self.triggers[trigger_name] = self.create_trigger(trigger_config)

        # 加载状态和触发器
        for state_config in config['states']:
            state = State(state_config['name'])
            for trigger_name in state_config['trigger_names']:
                trigger = self.triggers[trigger_name]
                if trigger:
                    state.add_trigger(trigger)
            self.trigger_manager.add_state(state)

        # 设置初始状态为 JSON 中定义的第一个状态
        if config['states']:
            self.trigger_manager.set_initial_state(config['states'][0]['name'])

        return self.trigger_manager, self.event_manager

    def create_trigger(self, trigger_config):
        trigger_type = trigger_config.get("type", "Generic")
        trigger_params = trigger_config.get("params", {})

        if trigger_type == "TimerTrigger":
            return TimerTrigger(
                event_manager=self.event_manager,
                **trigger_params
            )
        elif trigger_type == "LabelTrigger":
            label_names = trigger_config['label_names']
            labels = [self.labels.get(label_name) for label_name in label_names]
            return LabelTrigger(
                labels=labels,
                event_manager=self.event_manager,
                **trigger_params
            )
        elif trigger_type == "PointQueryTrigger":
            entity_name = trigger_config['entity_name']
            entity = self.entities.get(entity_name)
            if entity:
                return PointQueryTrigger(
                    entity=entity,
                    event_manager=self.event_manager,
                    space=self.space,
                    **trigger_params
                )
        return None
