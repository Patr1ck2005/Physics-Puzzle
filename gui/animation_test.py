import pygame
import pygame_gui
import math

pygame.init()

# 设置窗口
pygame.display.set_caption('Animated Button with Info Box')
window_surface = pygame.display.set_mode((600, 400))

background = pygame.Surface((600, 400))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((600, 400))

clock = pygame.time.Clock()

# 创建一个大的正方形按钮
button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 50), (300, 300)),
    text='',
    manager=manager
)

# 自定义介绍栏
info_box = pygame.Surface((400, 300), pygame.SRCALPHA)
info_box.fill((0, 0, 0, 0))  # 透明背景
info_rect = info_box.get_rect(center=(300, 500))  # 初始位置

# 动画参数
showing_info = False
info_box_opacity = 0
info_box_y_offset = 0

# 主循环
running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED and event.ui_element == button:
                showing_info = True

            if event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED and event.ui_element == button:
                showing_info = False

    # 更新UI管理器
    manager.update(time_delta)

    # 处理介绍栏动画
    if showing_info:
        info_box_opacity = min(255, info_box_opacity + 10)  # 渐变出现
        info_box_y_offset = min(200, info_box_y_offset + 10)  # 向上移动
    else:
        info_box_opacity = max(0, info_box_opacity - 15)  # 渐变消失
        info_box_y_offset = max(0, info_box_y_offset - 5)  # 向下移动

    # 清空介绍栏背景
    info_box.fill((0, 0, 0, 0))

    # 绘制带有渐变效果的矩形
    for y in range(0, 200):
        alpha = int(info_box_opacity*((200 - y * 1) / 200)**0.3)
        pygame.draw.rect(info_box, (50, 50, 50, alpha), (0, y, 400, 1))

    # 在介绍栏上绘制文字并调整透明度
    font = pygame.font.SysFont('Time New Roman', 24)
    text_surface = font.render('Info about the buttonInfo about the button\nInfo about the button', True, (255, 255, 255))
    text_surface.set_alpha(info_box_opacity)
    text_rect = text_surface.get_rect(center=(200, 50))  # 文字在介绍栏中居中
    info_box.blit(text_surface, text_rect)

    # 绘制背景
    window_surface.blit(background, (0, 0))

    # 绘制UI元素
    manager.draw_ui(window_surface)

    # 显示介绍栏
    window_surface.blit(info_box, (info_rect.x, info_rect.y - info_box_y_offset))

    pygame.display.update()

pygame.quit()
