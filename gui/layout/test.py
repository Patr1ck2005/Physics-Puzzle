import numpy as np
import pygame_gui

from gui.layout.property_panel import EntityPropertyPanel
from settings import *

import pygame

if __name__ == '__main__':
    from gui.phy_obj_ui.entity_ui import BoxEntityUI
    # 初始化Pygame和窗口
    pygame.init()
    pygame.display.set_caption('Entity Property Panel Example')
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(pygame.Color('#000000'))

    # 创建UI管理器
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 创建一个实体对象并添加位置历史记录
    entity = BoxEntityUI(window_surface, name="Box1", phy_type="dynamic", position=(0, 0), size=(30, 30), color=(150, 0, 0))
    entity.position_history_x = np.random.rand(100) * 300  # 模拟随机位置数据
    entity.position_history_y = np.random.rand(100) * 300
    entity.angle_history = np.random.rand(100) * 360 - 180

    # 创建一个实体属性面板
    entity_property_panel = EntityPropertyPanel(
        manager=manager,
        entity=entity,
        title="Entity Properties"
    )

    # 主循环
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        # 更新并绘制UI
        print("Updating UI...")
        manager.update(time_delta)

        print("Drawing UI...")
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.update()

    pygame.quit()