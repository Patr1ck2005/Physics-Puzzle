# 定义消息类型的事件处理函数
import pygame
from pygame_gui.windows import UIMessageWindow


def show_message(manager, title, message):
    """
    触发后在屏幕上弹出一个消息框。

    :param manager: pygame_gui 的 UIManager 实例
    :param title: 消息框的标题
    :param message: 消息框的内容
    """
    UIMessageWindow(
        rect=pygame.Rect((250, 200), (300, 200)),
        html_message=message,
        manager=manager,
        window_title=title
    )