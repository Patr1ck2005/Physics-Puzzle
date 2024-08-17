import pygame
import pygame_gui

# 初始化 Pygame
pygame.init()

# 创建屏幕
screen = pygame.display.set_mode((800, 600))

# 创建一个 GUI 管理器
manager = pygame_gui.UIManager((800, 600))

# 创建一个按钮
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                      text='Click Me',
                                      manager=manager)

clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 让 GUI 管理器处理事件
        manager.process_events(event)

    # 更新 GUI 元素
    manager.update(time_delta)

    # 绘制 GUI 到屏幕
    screen.fill((0, 0, 0))
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
