import pygame
import json
import os
from core.engine import Engine
from gui.ui_manager.ui_manager import UIManager
from settings import MAX_FPS


class GameScene:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True

        # 初始化物理世界和内部的UI管理器
        self.engine = Engine()
        self.engine.init_world()

        self.ui_manager = UIManager(self.engine)

        # 加载背景音乐
        pygame.mixer.music.load('assets/music/Aerie.mp3')
        pygame.mixer.music.play(-1)  # 循环播放
        pygame.mixer.music.set_volume(0.1)  # 设置音量为 50%

    @property
    def manager(self):
        return self.ui_manager

    def load_level(self, level):
        # 获取上级目录中的 levels 文件夹路径
        levels_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'levels')
        file_name = 'level_example_usable.json'
        file_path = os.path.join(levels_dir, file_name)

        # 读取 JSON 文件，并指定编码为 UTF-8
        with open(file_path, 'r', encoding='utf-8') as file:
            items = json.load(file)

        # # 处理物品数据 (这里可以直接交给Engine来处理)
        # for item in items:
        #     self.engine.process_item(item)  # 假设Engine有这个方法来处理物品

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

    def draw(self, screen):
        self.engine.render_world(screen)  # 渲染底层物理世界
        # self.ui_manager.draw_ui(screen)  # 渲染UI
