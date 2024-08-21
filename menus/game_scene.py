import pygame
import json
import os
from core.engine import Engine
from core.events_loader import EventLoader
from core.level_loader import LevelLoader
from core.phy_obj_loader import ObjsLoader
from core.setting_loader import EngineLoader
from gui.ui_manager.ui_manager import UIManager
from settings import MAX_FPS


class GameScene:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True

        # 初始化物理世界和内部的UI管理器
        self.engine = Engine()
        self.space = self.engine.space
        self.engine.init_world()

        self.ui_manager = UIManager(self.engine)

        # 加载背景音乐
        pygame.mixer.music.load('assets/music/Aerie.mp3')
        pygame.mixer.music.play(-1)  # 循环播放
        pygame.mixer.music.set_volume(0.1)  # 设置音量为 50%

        # 初始化加载器 (在这里还没有加载具体的关卡)
        self.game_loader = None
        self.trigger_manager = None
        self.event_manager = None

    @property
    def manager(self):
        return self.ui_manager

    def load_level(self, level):
        # 获取上级目录中的 levels 文件夹路径
        levels_dir = 'levels'

        # 加载物理引擎设置 JSON 文件
        setting_file = os.path.join(levels_dir, f'{level}', 'setting.json')
        # 设置物理引擎
        EngineLoader(self.engine).load_from_json(setting_file)
        # 加载物品栏, 场景和事件 JSON 文件
        inventory_file = os.path.join(levels_dir, f'{level}', 'inventory.json')
        scene_file = os.path.join(levels_dir, f'{level}', 'scene.json')
        events_file = os.path.join(levels_dir, f'{level}', 'events.json')

        # 载入物品栏入UIManager
        inventory = ObjsLoader(inventory_file).load_objs()
        self.ui_manager.inventory_manager.add_item_dict(inventory)
        # 载入场景入UIManage
        scene = ObjsLoader(scene_file).load_objs()
        self.ui_manager.entity_manager.add_entities_dict(scene)
        self.ui_manager.force_manager.add_force_dict(scene['forces'])

        # 设置关卡事件
        all_objs = {**inventory['entities'], **scene['entities']}
        self.trigger_manager, self.event_manager\
            = EventLoader(events_file, all_objs, self.space).load_events()  # 加载所有事件和触发器

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False  # 按下ESC键退出关卡
            elif event.key == pygame.K_p:  # 按下P键暂停
                return 'pause'
        return None

    def update(self):
        # 更新物理世界
        self.engine.update_world()
        # 检查并触发事件
        if self.trigger_manager:
            self.trigger_manager.check_triggers()

    def draw(self, screen):
        self.engine.render_world(screen)  # 渲染底层物理世界
        self.trigger_manager.draw_triggers(screen)  # 渲染触发器
        # self.ui_manager.draw_ui(screen)  # 渲染UI
