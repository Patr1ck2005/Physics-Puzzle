import time

import pygame_gui
from pygame import Rect
import pygame
from pygame_gui.elements import UIButton

from gui.layout.box_layout import HBoxLayout, VBoxLayout
from settings import *

from gui.phy_obj_ui.entity_ui import BlankEntityUI


class PropertyPanel:
    def __init__(self, manager, container_rect, title=None):
        """
        初始化属性面板基类。

        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        :param container_rect: 属性面板的矩形区域
        :param title: 属性面板的标题
        """
        self.manager = manager
        self.container_rect = container_rect
        self.title = title

        # 创建面板容器
        self.panel_container = pygame_gui.elements.UIPanel(
            relative_rect=self.container_rect,
            manager=self.manager
        )

        # 使用垂直布局作为主布局
        self.main_layout = VBoxLayout(self.panel_container, padding=10, spacing=5, mode='proportional', title=self.title,
                                      manager=self.manager)

        # 添加侧边栏
        self._add_side_btn()

    def show(self):
        """显示属性面板"""
        self.panel_container.show()
        self.fold_btn.set_text('>')
        self.fold_btn.set_position((self.container_rect.x-15, self.container_rect.h//2))

    def hide(self):
        """隐藏属性面板"""
        self.panel_container.hide()
        self.fold_btn.set_text('<')
        self.fold_btn.set_position((SCREEN_WIDTH-15, self.container_rect.h//2))

    def _add_side_btn(self):
        self.fold_btn = UIButton(
            relative_rect=Rect(self.container_rect.x-15, self.container_rect.h//2, 20, 50),
            text='>',
            manager=self.manager
        )


class EntityPropertyPanel(PropertyPanel):
    def __init__(self, manager, entity=None, title=None, container_rect=Rect(SCREEN_WIDTH-400, 50, 400, SCREEN_HEIGHT-100)):
        """
        初始化实体属性面板。

        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        :param container_rect: 属性面板的矩形区域
        :param entity: 要显示属性的 Entity 对象
        :param title: 属性面板的标题
        """
        super().__init__(manager, container_rect, title)
        self.entity = entity if entity else BlankEntityUI()

        self.last_refresh_time = 0

        # 创建标签和图标
        self._create_layouts()

        # 添加物体属性部分
        self._add_entity_properties()

        # 添加物体位置信息部分
        self._add_position_properties()

    def process_events(self, event):
        '''
        处理用户输入事件，包括按钮点击和滑动条移动事件。
        '''
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn = event.ui_element
            if btn == self.fold_btn:
                self.hide() if self.panel_container.visible else self.show()

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            slider = event.ui_element
            self.refresh_property_text()
            if self.entity.name != 'Blank':
                if slider.object_ids[-1] == "#property_slider_Mass":
                    self.entity.mass = slider.current_value
                elif slider.object_ids[-1] == "#property_slider_Friction":
                    self.entity.friction = slider.current_value
                elif slider.object_ids[-1] == "#property_slider_Elasticity":
                    self.entity.elasticity = slider.current_value
            else:
                print('请先选择物体')
            return True

    def update_entity(self, entity):
        """更新当前显示的实体"""
        self.entity = entity
        self.refresh_property()   # 每次更新实体时，刷新面板内容

    def remove_entity(self):
        """移除当前显示的实体"""
        self.entity = BlankEntityUI()
        self.refresh_property()  # 每次移除实体时，刷新面板内容

    def refresh(self):
        """更新面板内容以反映当前实体的状态"""
        self.name_label.set_text(f'Name: {self.entity.name}')
        self.type_label.set_text(f'Type: {self.entity.type}')
        self.mass_label.set_text(f'Mass: {self.entity.mass:.2f} kg')

        self.refresh_property_text()

        self.graph_x_label.set_text(f'Position X: {self.entity.center[0]:.2f}')
        self.graph_y_label.set_text(f'Position Y: {self.entity.center[1]:.2f}')
        self.graph_angle_label.set_text(f'Angle: {self.entity.angle:.2f}')

        # 如果有其他需要更新的内容，例如图表
        self.update_graphs()

    def refresh_property(self):
        self.refresh_property_text()
        self.refresh_sliders()

    def refresh_property_text(self):
        self.mass_value_label.set_text(f'{self.entity.mass:.2f}')
        self.fri_value_label.set_text(f'{self.entity.friction:.2f}')
        self.elast_value_label.set_text(f'{self.entity.elasticity:.2f}')

    def refresh_sliders(self):
        self.mass_slider.set_current_value(self.entity.mass)
        self.fri_slider.set_current_value(self.entity.friction)
        self.elast_slider.set_current_value(self.entity.elasticity)

    def update_graphs(self):
        """更新图表显示"""
        self.last_refresh_time = time.time()
        head_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.entity.draw_icon(head_surface)
        self.icon.set_image(head_surface)  # 用实体的颜色填充图标
        # 这里刷新位置的图表数据
        position_x_graph_surface = self._create_graph_surface(self.entity.history_x, (255, 0, 0))
        position_y_graph_surface = self._create_graph_surface(self.entity.history_y, (0, 255, 0))
        angle_graph_surface = self._create_graph_surface(self.entity.history_angle, (0, 0, 255))
        # 更新图表UI元素
        self.position_graph_x.set_image(position_x_graph_surface)
        self.position_graph_y.set_image(position_y_graph_surface)
        self.graph_angle.set_image(angle_graph_surface)

    def _create_layouts(self):
        """创建UI布局和基本元素"""
        # 创建水平布局用于显示物体的图形和属性信息
        self.head_container = pygame_gui.elements.UIPanel(
            relative_rect=Rect((0, 0), (0, 0)),
            manager=self.manager,
            container=self.panel_container
        )
        head_hlayout = HBoxLayout(self.head_container, padding=10, spacing=5, mode='proportional')
        self.main_layout.add_layout(head_hlayout, 1)

        head_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(head_surface, (255, 0, 0), (100, 100), 50)
        # 左侧的物体图形（简单的颜色矩形作为占位符）
        self.icon = pygame_gui.elements.UIImage(
            relative_rect=Rect((0, 0), (60, 60)),
            manager=self.manager,
            container=self.head_container,
            image_surface=head_surface,
            object_id="#entity_icon"
        )
        self.icon.image.fill(self.entity.ico_color)  # 用实体的颜色填充图标

        # 右侧的垂直布局，用于显示物体的名称、类型和质量
        self.name_container = pygame_gui.elements.UIPanel(
            relative_rect=Rect((10, 10), (10, 10)),
            manager=self.manager,
            container=self.head_container
        )
        name_vlayout = VBoxLayout(self.name_container, padding=5, spacing=5, mode='proportional')
        head_hlayout.add_widget(self.icon)
        head_hlayout.add_layout(name_vlayout)

        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=Rect((0, 0), (180, 20)),
            text=f'Name: {self.entity.name}',
            manager=self.manager,
            container=self.name_container
        )

        self.type_label = pygame_gui.elements.UILabel(
            relative_rect=Rect((0, 0), (180, 20)),
            text=f'Type: {self.entity.type}',
            manager=self.manager,
            container=self.name_container
        )

        self.mass_label = pygame_gui.elements.UILabel(
            relative_rect=Rect((0, 0), (180, 20)),
            text=f'Mass: {self.entity.mass:.2f} kg',
            manager=self.manager,
            container=self.name_container
        )

        name_vlayout.add_widget(self.name_label)
        name_vlayout.add_widget(self.type_label)
        name_vlayout.add_widget(self.mass_label)

    def _add_entity_properties(self):
        """
        添加物体属性部分，包括质量、摩擦力、弹性及其调整滑块。
        """
        # 创建一个垂直布局，标题为 "Entity Property"
        self.entity_property_container = pygame_gui.elements.UIPanel(
            relative_rect=Rect((0, 0), (0, 0)),
            manager=self.manager,
            container=self.panel_container
        )
        entity_property_layout = VBoxLayout(self.entity_property_container, padding=5, spacing=5, mode='simple',
                                            title="Physics", manager=self.manager)

        # 首先, 将实体属性的垂直布局添加到主布局
        self.main_layout.add_layout(entity_property_layout, 2)
        # 质量
        self.mass_slider_label, self.mass_value_label, self.mass_slider = (
            self._add_property_slider(entity_property_layout, "Mass", self.entity.mass, 0.1, 10.0, 0.1)
        )
        # 摩擦力
        self.fri_slider_label, self.fri_value_label, self.fri_slider = (
            self._add_property_slider(entity_property_layout, "Friction", self.entity.friction, 0.0, 1.0, 0.01)
        )
        # 弹性
        self.elast_slider_label, self.elast_value_label, self.elast_slider = (
            self._add_property_slider(entity_property_layout, "Elasticity", self.entity.elasticity, 0.0, 1.0,
                                  0.01)
        )

    def _add_property_slider(self, parent_layout, property_name, initial_value, min_value, max_value, step):
        """
        添加带滑块的属性设置。

        :param parent_layout: 父布局，用于容纳此属性设置
        :param property_name: 属性名称
        :param initial_value: 属性的初始值
        :param min_value: 滑块的最小值
        :param max_value: 滑块的最大值
        :param step: 滑块的步长
        """
        # 创建一个水平布局用于属性标题、值和滑块
        self.property_sub_container = pygame_gui.elements.UIPanel(
            relative_rect=Rect((0, 0), (300, 50)),
            manager=self.manager,
            container=self.entity_property_container,
        )
        property_layout = HBoxLayout(self.property_sub_container, padding=5, spacing=5, mode='proportional')

        # 属性名称标签
        property_label = pygame_gui.elements.UILabel(
            relative_rect=Rect((0, 0), (100, 30)),
            text=f'{property_name}:',
            manager=self.manager,
            container=self.property_sub_container
        )

        # 当前值标签
        value_label = pygame_gui.elements.UILabel(
            relative_rect=Rect((0, 0), (50, 30)),
            text=f'{initial_value:.2f}',
            manager=self.manager,
            container=self.property_sub_container
        )

        # 属性调整滑块
        slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=Rect((0, 0), (100, 30)),
            start_value=initial_value,
            value_range=(min_value, max_value),
            manager=self.manager,
            container=self.property_sub_container,
            object_id=f"#property_slider_{property_name}",
        )

        # 初始化滑块值
        slider.set_current_value(initial_value)

        # 将标签和滑块添加到水平布局
        property_layout.add_widget(property_label, 1)
        property_layout.add_widget(value_label, 1)
        property_layout.add_widget(slider, 3)

        # 将此属性布局添加到父布局中
        parent_layout.add_layout(property_layout)
        return property_label, value_label, slider

    def _add_position_properties(self):
        """
        添加物体位置相关的属性布局，包括位置坐标和角度。
        """
        # 创建一个垂直布局，标题为 "Position"
        self.position_container = pygame_gui.elements.UIPanel(
            relative_rect=Rect((0, 0), (300, 300)),
            manager=self.manager,
            container=self.panel_container
        )
        position_layout = VBoxLayout(self.position_container, padding=5, spacing=5, mode='proportional', title=None,
                                     manager=self.manager)

        # 将位置属性的垂直布局添加到主布局
        self.main_layout.add_layout(position_layout, 4)

        # 位置 X 标签与图表
        self.graph_x_label, self.position_graph_x = (
            self._add_position_graph(position_layout, "Position X", self.entity.history_x))

        # 位置 Y 标签与图表
        self.graph_y_label, self.position_graph_y = (
            self._add_position_graph(position_layout, "Position Y", self.entity.history_y))

        # 角度 标签与图表
        self.graph_angle_label, self.graph_angle = (
            self._add_position_graph(position_layout, "Angle", self.entity.history_angle))

    def _add_position_graph(self, parent_layout, property_name, data):
        """
        添加显示位置的曲线图。

        :param parent_layout: 父布局，用于容纳此属性设置
        :param property_name: 属性名称
        :param data: 显示的历史数据数组
        """
        # 创建一个垂直布局用于属性标题和值
        self.position_sub_container = pygame_gui.elements.UIPanel(
            relative_rect=Rect((0, 0), (300, 100)),
            manager=self.manager,
            container=self.position_container
        )
        position_layout = VBoxLayout(self.position_sub_container, padding=5, spacing=5, mode='proportional')

        # 属性名称和当前值标签
        property_label = pygame_gui.elements.UILabel(
            relative_rect=Rect((0, 0), (200, 30)),
            text=f'{property_name}: {data[-1]:.2f}',
            manager=self.manager,
            container=self.position_sub_container
        )

        # 曲线图显示器
        graph = pygame_gui.elements.UIImage(
            relative_rect=Rect((0, 0), (200, 100)),
            image_surface=self._create_graph_surface(data),
            manager=self.manager,
            container=self.position_sub_container
        )

        # 将标签和曲线图添加到垂直布局
        position_layout.add_widget(property_label, 1)
        position_layout.add_widget(graph, 3)

        # 将此布局添加到父布局中
        parent_layout.add_layout(position_layout)

        return property_label, graph

    def _create_graph_surface(self, data, line_color=(255, 255, 255)):
        """
        使用 Pygame 绘制曲线图的 Surface。

        :param data: 显示的历史数据数组
        :return: Pygame Surface 包含绘制的曲线图
        """
        width, height = 600, 200
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # 填充背景为灰色
        surface.fill((100, 100, 100))

        # 找到数据中的最小值和最大值以进行比例调整
        min_data = min(data)
        max_data = max(data)

        # 绘制曲线
        points = []
        for i in range(len(data)):
            x = int(i * width / len(data))
            y = int((data[i] - min_data + 1) / (max_data - min_data + 1) * (height - 10))  # 根据数据调整 y 位置
            y = height - y  # 将 y 值翻转，使得较大的值在图表顶部
            points.append((x, y))

        if len(points) > 1:
            pygame.draw.lines(surface, line_color, False, points, 4)  # 使用蓝色绘制曲线

        return surface

    # def _create_graph_surface(self, data):
    #     # 创建一个新的 OpenGL 纹理并绑定
    #     texture = glGenTextures(1)
    #     glBindTexture(GL_TEXTURE_2D, texture)
    #     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 200, 100, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    #     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    #     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #
    #     # 创建并绑定 FBO
    #     fbo = glGenFramebuffers(1)
    #     glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    #     glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)
    #
    #     if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
    #         print("Error: Framebuffer is not complete!")
    #         return None
    #
    #     # 设置视口并清除缓冲区
    #     glViewport(0, 0, 200, 100)
    #     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #
    #     # 设置投影和模型视图矩阵
    #     glMatrixMode(GL_PROJECTION)
    #     glLoadIdentity()
    #     gluOrtho2D(0, len(data) - 1, min(data), max(data))
    #
    #     glMatrixMode(GL_MODELVIEW)
    #     glLoadIdentity()
    #
    #     # 绘制曲线
    #     glColor3f(0.0, 0.0, 1.0)
    #     glBegin(GL_LINE_STRIP)
    #     for i in range(len(data)):
    #         glVertex2f(i, data[i])
    #     glEnd()
    #
    #     # 读取 FBO 内容到 Pygame Surface
    #     raw_data = glReadPixels(0, 0, 200, 100, GL_RGBA, GL_UNSIGNED_BYTE)
    #     surface = pygame.image.fromstring(raw_data, (200, 100), "RGBA")
    #
    #     # 清理
    #     glBindFramebuffer(GL_FRAMEBUFFER, 0)
    #     glDeleteFramebuffers(1, [fbo])
    #     glDeleteTextures([texture])
    #
    #     return surface

