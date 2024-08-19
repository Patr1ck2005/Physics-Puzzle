import numpy as np
import pygame
import pygame_gui
from pygame import Rect

from gui.layout.box_layout import HBoxLayout, VBoxLayout
from settings import *

import matplotlib.pyplot as plt

from core.entity import BlankEntity

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


class EntityPropertyPanel(PropertyPanel):
    def __init__(self, manager, entity=None, title=None, container_rect=Rect(SCREEN_WIDTH-400, 0, 400, SCREEN_HEIGHT-100)):
        """
        初始化实体属性面板。

        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        :param container_rect: 属性面板的矩形区域
        :param entity: 要显示属性的 Entity 对象
        :param title: 属性面板的标题
        """
        super().__init__(manager, container_rect, title)
        self.entity = entity if entity else BlankEntity()

        # 创建水平布局用于显示物体的图形和属性信息
        self.head_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (0, 0)),
            manager=manager,
            container=self.panel_container
        )
        head_hlayout = HBoxLayout(self.head_container, padding=10, spacing=5, mode='proportional')
        # 首先，将水平布局添加到主垂直布局中
        self.main_layout.add_layout(head_hlayout)

        # 左侧的物体图形（简单的颜色矩形作为占位符）
        icon = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (60, 60)),
            text='',
            manager=manager,
            container=self.head_container,
            object_id="#entity_icon"
        )
        icon.image.fill(self.entity.color)  # 用实体的颜色填充图标

        # 右侧的垂直布局，用于显示物体的名称、类型和质量
        self.name_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (0, 0)),
            manager=manager,
            container=self.head_container
        )
        name_vlayout = VBoxLayout(self.name_container, padding=5, spacing=5, mode='proportional')

        # 将图标和右侧垂直布局加入水平布局
        head_hlayout.add_widget(icon)
        head_hlayout.add_layout(name_vlayout)  # 将垂直布局的容器作为一个整体添加

        name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (180, 20)),
            text=f'Name: {self.entity.name}',
            manager=manager,
            container=self.name_container
        )

        type_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (180, 20)),
            text=f'Type: {self.entity.type}',
            manager=manager,
            container=self.name_container
        )

        mass_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (180, 20)),
            text=f'Mass: {self.entity.mass:.2f} kg',
            manager=manager,
            container=self.name_container
        )


        # 将这些标签加入右侧的垂直布局
        name_vlayout.add_widget(name_label)
        name_vlayout.add_widget(type_label)
        name_vlayout.add_widget(mass_label)

        # 添加物体属性部分
        self._add_entity_properties()

        # 添加物体位置信息部分
        self._add_position_properties()

    def update_entity(self, entity):
        """
        更新显示的实体。

        :param entity: 要显示属性的 Entity 对象
        """
        self.entity = entity

    def _add_entity_properties(self):
        """
        添加物体属性部分，包括质量、摩擦力、弹性及其调整滑块。
        """
        # 创建一个垂直布局，标题为 "Entity Property"
        self.entity_property_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (0, 0)),
            manager=self.manager,
            container=self.panel_container
        )
        entity_property_layout = VBoxLayout(self.entity_property_container, padding=5, spacing=5, mode='simple',
                                            title="Entity Property", manager=self.manager)

        # 首先, 将实体属性的垂直布局添加到主布局
        self.main_layout.add_layout(entity_property_layout, 2)
        # 质量
        self._add_property_slider(entity_property_layout, "Mass", self.entity.mass, 0.1, 10.0, 0.1)

        # 摩擦力
        self._add_property_slider(entity_property_layout, "Friction", self.entity.friction, 0.0, 1.0, 0.01)

        # 弹性
        self._add_property_slider(entity_property_layout, "Elasticity", self.entity.elasticity, 0.0, 1.0,
                                  0.01)

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
            relative_rect=pygame.Rect((0, 0), (300, 50)),
            manager=self.manager,
            container=self.entity_property_container
        )
        property_layout = HBoxLayout(self.property_sub_container, padding=5, spacing=5, mode='proportional')

        # 属性名称标签
        property_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (100, 30)),
            text=f'{property_name}:',
            manager=self.manager,
            container=self.property_sub_container
        )

        # 当前值标签
        value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (50, 30)),
            text=f'{initial_value:.2f}',
            manager=self.manager,
            container=self.property_sub_container
        )

        # 属性调整滑块
        slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 0), (100, 30)),
            start_value=initial_value,
            value_range=(min_value, max_value),
            manager=self.manager,
            container=self.property_sub_container
        )

        # 绑定滑块的变化事件，更新值标签
        slider.set_current_value(initial_value)

        def update_value_label():
            value = slider.get_current_value()
            value_label.set_text(f'{value:.2f}')
            if property_name == "Mass":
                self.entity.mass = value
            elif property_name == "Friction":
                self.entity.friction = value
            elif property_name == "Elasticity":
                self.entity.elasticity = value
        #
        # slider.bind_on_value_changed(update_value_label)

        # 将标签和滑块添加到水平布局
        property_layout.add_widget(property_label)
        property_layout.add_widget(value_label)
        property_layout.add_widget(slider)

        # 将此属性布局添加到父布局中
        parent_layout.add_layout(property_layout)

    def _add_position_properties(self):
        """
        添加物体位置相关的属性布局，包括位置坐标和角度。
        """
        # 创建一个垂直布局，标题为 "Position"
        self.position_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (300, 300)),
            manager=self.manager,
            container=self.panel_container
        )
        position_layout = VBoxLayout(self.position_container, padding=5, spacing=5, mode='proportional', title="Position",
                                     manager=self.manager)

        # 将位置属性的垂直布局添加到主布局
        self.main_layout.add_layout(position_layout, 3)

        # 位置 X
        self._add_position_graph(position_layout, "Position X", self.entity.history_x)

        # 位置 Y
        self._add_position_graph(position_layout, "Position Y", self.entity.history_x)

        # 角度
        self._add_position_graph(position_layout, "Angle", self.entity.history_angle)

    def _add_position_graph(self, parent_layout, property_name, data):
        """
        添加显示位置的曲线图。

        :param parent_layout: 父布局，用于容纳此属性设置
        :param property_name: 属性名称
        :param data: 显示的历史数据数组
        """
        # 创建一个垂直布局用于属性标题和值
        self.position_sub_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (300, 100)),
            manager=self.manager,
            container=self.position_container
        )
        position_layout = VBoxLayout(self.position_sub_container, padding=5, spacing=5, mode='proportional')

        # 属性名称和当前值标签
        property_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (200, 30)),
            text=f'{property_name}: {data[-1]:.2f}',
            manager=self.manager,
            container=self.position_sub_container
        )

        # 曲线图显示器
        graph = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((0, 0), (200, 100)),
            image_surface=self._create_graph_surface(data),
            manager=self.manager,
            container=self.position_sub_container
        )

        # 将标签和曲线图添加到垂直布局
        position_layout.add_widget(property_label, 1)
        position_layout.add_widget(graph, 3)

        # 将此布局添加到父布局中
        parent_layout.add_layout(position_layout)

    def _create_graph_surface(self, data):
        """
        创建显示曲线图的Surface。

        :param data: 显示的历史数据数组
        :return: pygame.Surface 包含绘制的曲线图
        """
        fig, ax = plt.subplots(figsize=(2, 1))
        ax.plot(data, color='blue')
        ax.set_xlim([0, len(data) - 1])
        ax.set_ylim([min(data), max(data)])

        # 移除轴线
        ax.axis('off')

        # 绘制到Surface
        fig.canvas.draw()

        # 使用 buffer_rgba 代替 tostring_rgb
        graph_surface = pygame.Surface((200, 100))
        graph_surface.blit(
            pygame.image.frombuffer(fig.canvas.buffer_rgba(), fig.canvas.get_width_height(), "RGBA"),
            (0, 0)
        )

        plt.close(fig)  # 关闭matplotlib绘图

        return graph_surface

