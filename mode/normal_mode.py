import pygame

import json

import  os

from gui.menu import main_menu, pause_menu, settings_menu
from core.enginee import init_world, update_world, render_world

from gui.hud import HUD


def default_level(screen):
    clock = pygame.time.Clock()
    running = True

    player_rect = pygame.Rect(50, 50, 50, 50)  # 玩家方块

    # 初始化物理世界: 后续计算该世界
    space = init_world()
    # 初始化HUD
    hud = HUD(screen)

    # 获取上级目录中的 levels 文件夹路径
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本的目录
    levels_dir = os.path.join(base_dir, '..', 'levels')  # 上级目录中的 levels 文件夹

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

    while running:
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

        # 处理拖拽交互
        selecting, m_pos = hud.drag_interaction()
        print(selecting, m_pos)

        # 示例游戏逻辑：简单的左右移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player_rect.x += 5

        # 计算更新物理世界
        update_world(space)

        # 渲染关卡
        screen.fill((0, 0, 0))  # 重置画面
        render_world(space, screen)  # 渲染底层物理对象

        # 渲染高级视觉对象
        pygame.draw.rect(screen, (255, 0, 0), player_rect)  # 绘制玩家

        # 渲染HUD
        hud.render()

        # 所有渲染完成后,更新画面
        pygame.display.flip()

        clock.tick(60)

    return 'main_menu'
