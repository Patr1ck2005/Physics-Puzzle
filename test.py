import pygame
import numpy as np


def draw_function_graph(surface, data, color=(0, 0, 255)):
    surface.fill((255, 255, 255))  # 清空背景

    max_value = max(data)
    min_value = min(data)
    range_value = max_value - min_value if max_value != min_value else 1
    width = surface.get_width()
    height = surface.get_height()

    for i in range(1, len(data)):
        x1 = int((i - 1) * width / len(data))
        y1 = int(height - (data[i - 1] - min_value) / range_value * height)
        x2 = int(i * width / len(data))
        y2 = int(height - (data[i] - min_value) / range_value * height)
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)


# 初始化Pygame
pygame.init()
window_size = (800, 600)
window_surface = pygame.display.set_mode(window_size)
pygame.display.set_caption('Function Graph Example')

# 创建一个图表表面
graph_surface = pygame.Surface((800, 400))

# 示例数据
data = np.sin(np.linspace(0, 2 * np.pi, 100)) * 100 + np.random.randn(100) * 5  # 生成一个正弦波

clock = pygame.time.Clock()
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # 示例数据
    data = np.sin(np.linspace(0, 2 * np.pi, 100)) * 100 + np.random.randn(100) * 5  # 生成一个正弦波

    # 绘制函数图
    draw_function_graph(graph_surface, data)

    # 更新窗口
    window_surface.fill((0, 0, 0))
    window_surface.blit(graph_surface, (0, 100))  # 将图表放在窗口中间
    pygame.display.update()

    clock.tick(60)

pygame.quit()
