import pygame
import pygame_gui

from menus.chapter_menu import ChapterMenu
from menus.main_menu import MainMenu
from menus.level_menu import LevelMenu
from menus.game_scene import GameScene
from menus.pause_menu import PauseMenu

from settings import *

pygame.init()

# 设置窗口大小和标题
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('My Game')

clock = pygame.time.Clock()
is_running = True

# 当前界面和管理器
current_screen = None
current_manager = None

# 创建持久的游戏场景实例
game_scene = None


# 初始化界面的工厂函数
def load_main_menu():
    global current_manager, current_screen
    current_manager = pygame_gui.UIManager(WINDOW_SIZE, 'assets/theme/theme.json')
    current_screen = MainMenu(current_manager)


def load_chapter_menu():
    global current_manager, current_screen
    current_manager = pygame_gui.UIManager(WINDOW_SIZE, 'assets/theme/theme.json')
    current_screen = ChapterMenu(current_manager)


def load_level_selection_menu():
    global current_manager, current_screen
    current_manager = pygame_gui.UIManager(WINDOW_SIZE, 'assets/theme/theme.json')
    current_screen = LevelMenu(current_manager)


def load_game_scene():
    global current_manager, current_screen, game_scene
    if game_scene is None:  # 仅在首次加载时创建
        game_scene = GameScene()
        current_manager = game_scene.manager  # 这里有所不同, game_scene自带UIManager
    current_manager = game_scene.manager  # 切换回游戏场景的UIManager
    current_screen = game_scene


def load_pause_menu():
    global current_manager, current_screen
    current_manager = pygame_gui.UIManager(WINDOW_SIZE)
    current_screen = PauseMenu(current_manager)


# 加载初始界面
load_main_menu()

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # 处理当前屏幕的事件
        screen_result = current_screen.handle_event(event)

        # 根据处理结果切换不同的屏幕
        if screen_result == "start_game":
            load_chapter_menu()
        elif (screen_result and screen_result.startswith("chapter")) or screen_result == "level_menu":
            game_scene = None  # 如果返回关卡，销毁当前游戏场景实例
            load_level_selection_menu()
        elif screen_result and screen_result.startswith("level_"):
            load_game_scene()
            current_screen.load_level(screen_result)  # 加载选定的关卡
        elif screen_result == "pause":
            load_pause_menu()
        elif screen_result == "resume_game":
            load_game_scene()  # 切换回游戏场景
        elif screen_result == "back_to_menu":
            game_scene = None  # 如果返回主菜单，销毁当前游戏场景实例
            load_main_menu()
        elif screen_result == "exit":
            is_running = False

        current_manager.process_events(event)

    current_screen.update()  # 更新窗口, 涉及到物理引擎的更新
    current_manager.update(time_delta)  # 更新UIManager

    screen.fill((0, 0, 0))
    current_screen.draw(screen)  # 窗口类中的渲染不可交互图形
    current_manager.draw_ui(screen)  # UIManager中渲染UI
    pygame.display.flip()

pygame.quit()
