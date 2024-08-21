# 定义消息类型的事件处理函数
import pygame
from pygame_gui.windows import UIMessageWindow

from settings import *


def show_message(manager, title, message, *args, **kwargs):
    """
    触发后在屏幕上弹出一个消息框。

    :param manager: pygame_gui 的 UIManager 实例
    :param title: 消息框的标题
    :param message: 消息框的内容
    """
    if pygame.display.get_surface() is not None:
        # 获取屏幕尺寸
        window_width, window_height = pygame.display.get_surface().get_size()
    else:
        window_width, window_height = SCREEN_WIDTH, SCREEN_HEIGHT

    # 创建消息窗口
    message_window = UIMessageWindow(
        rect=pygame.Rect((window_width // 2 - 150, window_height // 2 - 100), (300, 200)),
        manager=manager,
        window_title=title,
        html_message=message
    )
    return message_window


def show_console_message(message: str, *args, **kwargs):
    print(message.center(80, '='))
    return
