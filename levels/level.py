import pygame

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
