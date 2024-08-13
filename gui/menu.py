import pygame
import sys

# 初始化Pygame
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# 字体设置
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# 菜单选项
MAIN_MENU = ["Start Game", "Settings", "Quit"]
PAUSE_MENU = ["Resume", "Settings", "Quit"]
SETTINGS_MENU = ["Volume", "Back"]

# 当前菜单状态
menu_state = 'main_menu'

# 当前选项索引
selected_option = 0


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def main_menu():
    global selected_option
    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//4)

        for i, option in enumerate(MAIN_MENU):
            color = GRAY if i == selected_option else WHITE
            draw_text(option, small_font, color, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(MAIN_MENU)
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(MAIN_MENU)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Start Game
                        return 'start_game'
                    if selected_option == 1:  # Settings
                        return 'settings_menu'
                    if selected_option == 2:  # Quit
                        pygame.quit()
                        sys.exit()


def pause_menu():
    global selected_option
    while True:
        screen.fill(BLACK)
        draw_text('Pause Menu', font, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//4)

        for i, option in enumerate(PAUSE_MENU):
            color = GRAY if i == selected_option else WHITE
            draw_text(option, small_font, color, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(PAUSE_MENU)
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(PAUSE_MENU)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Resume
                        return 'resume_game'
                    if selected_option == 1:  # Settings
                        return 'settings_menu'
                    if selected_option == 2:  # Quit
                        pygame.quit()
                        sys.exit()

def settings_menu():
    global selected_option
    while True:
        screen.fill(BLACK)
        draw_text('Settings Menu', font, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//4)

        for i, option in enumerate(SETTINGS_MENU):
            color = GRAY if i == selected_option else WHITE
            draw_text(option, small_font, color, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(SETTINGS_MENU)
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(SETTINGS_MENU)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Volume
                        print("Volume setting not implemented yet.")
                    if selected_option == 1:  # Back
                        return 'back'

# 启动菜单
if __name__ == '__main__':
    while True:
        if menu_state == 'main_menu':
            menu_state = main_menu()
        elif menu_state == 'pause_menu':
            menu_state = pause_menu()
        elif menu_state == 'settings_menu':
            menu_state = settings_menu()
        elif menu_state == 'start_game':
            print("Game Started!")  # 在这里启动游戏循环
            break  # 退出主菜单循环，开始游戏
        elif menu_state == 'resume_game':
            print("Game Resumed!")  # 在这里恢复游戏循环
            break  # 退出暂停菜单，恢复游戏
