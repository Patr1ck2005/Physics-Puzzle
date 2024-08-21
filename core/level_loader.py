import time

import pygame
import pymunk

from core.events_loader import EventLoader
from core.phy_obj_loader import ObjsLoader


class LevelLoader:
    def __init__(self, entities_json_file, events_json_file=None, space=None):
        self.entities_json_file = entities_json_file
        self.events_json_file = events_json_file
        self.entities = {}
        self.space = space

    def load_entities(self):
        entity_loader = ObjsLoader(self.entities_json_file)
        self.entities = entity_loader.load_entities()
        return self.entities

    def load_events(self):
        if not self.entities:  # 确保实体已经加载
            self.load_entities()
        event_loader = EventLoader(self.events_json_file, self.entities, self.space)
        trigger_manager, event_manager = event_loader.load_events()
        return trigger_manager, event_manager

    def load_all(self):
        self.load_entities()
        return self.load_events()


# 使用 GameLoader 类
if __name__ == '__main__':
    pygame.init()
    space = pymunk.Space()
    game_loader = LevelLoader('world_test.json', 'events_test.json', space)

    # 加载实体
    entities = game_loader.load_entities()
    print("Loaded entities:", entities)

    # 加载事件和触发器
    trigger_manager, event_manager = game_loader.load_events()

    # 模拟游戏循环
    for _ in range(10):
        trigger_manager.check_triggers()
        time.sleep(0.3)
        print(_)
