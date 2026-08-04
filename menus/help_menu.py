import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from settings import *


class HelpMenu:
    def __init__(self, manager):
        self.manager = manager

        # 主容器面板
        self.main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((100, 50), (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100)),
            manager=manager,
        )

        # 标题
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH - 200, 60)),
            text='Help',
            manager=manager,
            container=self.main_panel,
            object_id=ObjectID('#main_menu_title', '@labels'),
        )

        # 帮助内容 (HTML 格式, 供 UITextBox 渲染)
        # 注意: pygame_gui 不支持 <h1>/<h2> 等标签, 用 <b> + <font> 替代
        help_html = (
            '<b><font size="24">控制方式</font></b><br><br>'
            '本游戏主要使用鼠标进行操作：<br><br>'

            '<b>左键点击</b><br>'
            '• <b>选择物品</b>：在沙盒模式中，左键点击游戏世界中的物体即可选择该物体。<br>'
            '• <b>移动物体</b>：选择物体后，再次左键点击可以将物体瞬间移动到鼠标指定的位置。<br>'
            '• <b>拖动物体</b>：左键长按物体可将其拖动，松开左键后可放置物体，快速甩动鼠标可以将物体甩出。<br><br>'

            '<b>右键点击</b><br>'
            '• <b>选中物体</b>：右键点击物体可以将其选中到右侧属性面板，'
            '面板会实时显示物体的物理状态（位置、角度、速度等曲线图）。<br>'
            '• 再次右键点击同一物体会取消选中。<br><br>'

            '<b><font size="24">物品栏与物品放置</font></b><br><br>'
            '游戏界面左上角的物品栏包含所有可互动的对象，分为以下四类：'
            '物理实体、力、约束、工具。<br><br>'

            '<b>物理实体</b><br>'
            '• 点击物品栏中的实体后，再次点击可将其放置到鼠标所在的位置。<br><br>'

            '<b>力</b><br>'
            '• 选择力后，需要将其点击放置在游戏世界中的动态物体上。<br><br>'

            '<b>约束</b><br>'
            '• 选择约束后，需依次点击指定两个物体，从而建立它们之间的约束。<br>'
            '• 约束代表物理世界中的轻杆（PinJoint）、轻绳（SlideJoint）、弹簧（Spring）等。<br><br>'

            '<b>工具</b><br>'
            '• 选择工具后，需要点击将其作用于动态物体上。<br>'
            '• 工具会修改物体的摩擦力或弹性等物理属性。<br><br>'

            '<b><font size="24">设置按钮</font></b><br><br>'
            '游戏界面下方的设置按钮用于调整物理引擎的模拟参数：<br><br>'

            '• <b>模拟速度</b>：调整物理模拟的速度，可以选择快速或慢速运行模拟。<br>'
            '• <b>模拟设置</b>：开启或关闭重力、万有引力等物理属性，以定制模拟环境。<br>'
            '• <b>重力滑块</b>：调节重力大小（0-10）。<br>'
            '• <b>万有引力滑块</b>：调节万有引力系数（0-10）。<br><br>'

            '<b><font size="24">快捷键</font></b><br><br>'
            '• <b>ESC</b>：退出当前关卡<br>'
            '• <b>P</b>：暂停游戏<br>'
            '• <b>Q</b>：返回关卡选择菜单<br>'
        )

        # 可滚动的文本框
        self.text_box = pygame_gui.elements.UITextBox(
            html_text=help_html,
            relative_rect=pygame.Rect((20, 80), (SCREEN_WIDTH - 240, SCREEN_HEIGHT - 220)),
            manager=manager,
            container=self.main_panel,
            object_id=ObjectID('#help_text_box'),
        )

        # 返回按钮
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 130), (300, 50)),
            text='Back to Main Menu',
            manager=manager,
            container=self.main_panel,
            object_id=ObjectID('#main_menu_btn', '@labels'),
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                return 'back_to_menu'
        return None

    def update(self):
        pass

    def draw(self, screen):
        pass
