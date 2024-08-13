import pygame


def default_level(screen):
    clock = pygame.time.Clock()
    running = True

    player_rect = pygame.Rect(50, 50, 50, 50)  # 玩家方块

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # 按下ESC键退出关卡

        # 示例游戏逻辑：简单的左右移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player_rect.x += 5

        # 渲染关卡
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), player_rect)  # 绘制玩家
        pygame.display.flip()

        clock.tick(60)

    return 'main_menu'
