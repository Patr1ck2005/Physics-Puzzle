import pygame
import sys

from mode.base_mode import default_level
from gui.menu import main_menu, pause_menu, settings_menu
from gui.hud import HUD

# 初始化Pygame
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Physics!')

# 设置帧率
clock = pygame.time.Clock()
FPS = 60

# 初始化HUD
hud = HUD(screen)

# 游戏状态管理
game_state = 'main_menu'  # 可能的状态有 'main_menu', 'playing', 'paused', 'settings_menu'


def start_game():
    global game_state
    game_state = default_level(screen)
    hud.reset()  # 开始新游戏时重置HUD


def pause_game():
    global game_state
    game_state = 'paused'


def resume_game():
    global game_state
    game_state = 'playing'


# 主游戏循环
running = True
while running:
    if game_state == 'main_menu':
        selected_menu = main_menu()
        if selected_menu == 'start_game':
            start_game()
        elif selected_menu == 'settings_menu':
            game_state = 'settings_menu'
    elif game_state == 'settings_menu':
        selected_menu = settings_menu(screen)
        if selected_menu == 'back':
            game_state = 'main_menu'

        # 游戏逻辑更新
        hud.update_score(1)  # 示例：每帧增加1分

        # 清屏
        screen.fill((0, 0, 0))

        # 渲染HUD
        hud.render()

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        clock.tick(FPS)
    elif game_state == 'paused':
        selected_menu = pause_menu(screen)
        if selected_menu == 'resume_game':
            resume_game()
        elif selected_menu == 'settings_menu':
            game_state = 'settings_menu'

    # 其他状态下的事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
