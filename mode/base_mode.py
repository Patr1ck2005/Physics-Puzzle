import pygame

import json

import os

from gui.menu import main_menu, pause_menu, settings_menu
from core.engine import Engine

from gui.ui_manager import UIManager


def default_level(screen):
    # 初始化pygame
    clock = pygame.time.Clock()
    player_rect = pygame.Rect(300, 300, 50, 60)  # 玩家debug方块
    running = True
    # 初始化物理世界: 后续计算该世界
    engine = Engine(screen)
    engine.init_world()
    # 初始化UI管理器
    ui_manager = UIManager(screen, engine.space)
    # 加载并播放背景音乐
    pygame.mixer.music.load('Aerie.mp3')
    pygame.mixer.music.play(-1)  # 循环播放
    pygame.mixer.music.set_volume(0.1)  # 设置音量为 50%

    # 获取上级目录中的 levels 文件夹路径
    levels_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'levels')

    # 指定要读取的 JSON 文件名称
    file_name = 'level_example_usable.json'
    file_path = os.path.join(levels_dir, file_name)

    # 读取 JSON 文件，并指定编码为 UTF-8
    with open(file_path, 'r', encoding='utf-8') as file:
        items = json.load(file)

    # 遍历并处理每个物品
    for item in items:
        print(f"Type: {item['type']}")
        print(f"Is placed: {item['is_placed']}")
        print(f"Quantity: {item['quantity']}")
        properties = item['properties']

        # 打印物品的属性
        print(f"Material: {properties.get('material', 'N/A')}")
        print(f"Size dimension1: {properties.get('size', {}).get('dimension1', 'N/A')}")
        print(f"Size dimension2: {properties.get('size', {}).get('dimension2', 'N/A')}")
        print(f"Mass: {properties.get('mass', 'N/A')}")
        print(f"Density: {properties.get('density', 'N/A')}")
        print(
            f"Position: (x: {properties.get('position', {}).get('x', 'N/A')}, y: {properties.get('position', {}).get('y', 'N/A')})")
        print(
            f"Initial velocity: (vx: {properties.get('initial_velocity', {}).get('vx', 'N/A')}, vy: {properties.get('initial_velocity', {}).get('vy', 'N/A')})")
        print(
            f"Acceleration: (ax: {properties.get('acceleration', {}).get('ax', 'N/A')}, ay: {properties.get('acceleration', {}).get('ay', 'N/A')})")
        print(f"Magnitude: {properties.get('magnitude', 'N/A')}")
        print(f"Direction angle: {properties.get('direction', {}).get('angle', 'N/A')}")

        print("---")

    # 游戏主循环
    while running:
        # 更新ui管理器 (刷新鼠标坐标等等)
        ui_manager.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # 按下ESC键退出关卡
                elif event.key == pygame.K_p:
                    game_state = pause_menu(screen)  # 按下P键暂停
                    if game_state == 'main_menu':
                        return 'main_menu'
            # 处理鼠标点选物品
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ui_manager.on_click()

        # 示例游戏逻辑：简单的左右移动
        debug_player(player_rect)

        # 计算更新物理世界
        engine.update_world()

        # 渲染关卡
        screen.fill((0, 0, 0))  # 重置画面
        engine.render_world()  # 渲染底层物理对象

        # 渲染高级视觉对象
        pygame.draw.rect(screen, (255, 0, 0), player_rect)  # 绘制玩家

        # 渲染UI
        ui_manager.render_all_ui()

        # 所有渲染完成后,更新画面
        pygame.display.flip()

        clock.tick(60)

    return 'main_menu'


def debug_player(player_rect):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        player_rect.y += 5
