import pygame
from dearpygui.core import *
from dearpygui.simple import *

# 初始化 Pygame
pygame.init()

# 设置 Pygame 窗口尺寸
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame with Dear PyGui")

# 初始化 Dear PyGui
def setup_dpg():
    with window("Dear PyGui Window"):
        add_text("This is a Dear PyGui window inside a Pygame window!")
        add_button("Click Me", callback=lambda sender, data: print("Button Clicked"))
        add_slider_float("Slider", default_value=0.5, min_value=0.0, max_value=1.0)
    start_dearpygui(primary_window="Dear PyGui Window")

setup_dpg()

# Pygame 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏并设置背景色
    screen.fill((30, 30, 30))

    # 渲染 Dear PyGui UI
    render_dearpygui_frame()

    # 更新 Pygame 显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
