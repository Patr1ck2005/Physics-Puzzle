import pygame
import pygame_gui


class BoxLayout:
    def __init__(self, container, padding=5, spacing=5, mode='simple', title=None, manager=None):
        """
        初始化 HBoxLayout。

        :param container: pygame_gui.elements.UIPanel 用于放置子元素的容器
        :param padding: 布局左右的填充（像素）
        :param spacing: 各子元素之间的间距（像素）
        :param mode: 布局模式 ('simple' 或 'proportional')
        :param title: 布局的标题文本（可选）
        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        """
        self.container = container
        self.padding = padding

        self.spacing = spacing
        self.mode = mode
        self.elements = []
        self.ratios = []
        self.title = title
        self.manager = manager
        self.title_element = None
        self.layouts = []

        self.sub_width = self.container.relative_rect.width - 2 * self.padding
        self.sub_height = self.container.relative_rect.height - 2 * self.padding

        if self.title:
            self.padding += 10  # 增加 padding 以避免覆盖标题

    def add_widget(self, widget, ratio=1):
        """
        将新组件按比例添加到布局中。

        :param widget: 要添加的 pygame_gui 元素
        :param ratio: 该组件所占用的比例（仅在比例模式下有效，默认为1）
        """
        self.elements.append(widget)
        self.ratios.append(ratio)
        self.update_layout()

    def add_layout(self, layout, ratio=1):
        """
        将另一个布局管理器添加到当前布局中。

        :param layout: 要添加的另一个布局管理器 (VBoxLayout, HBoxLayout等)
        :param ratio: 该布局所占用的比例（仅在比例模式下有效，默认为1）
        """
        self.layouts.append((layout, ratio))
        self.update_layout()

    def update_layout(self):
        """
        更新布局，重新排列所有子元素和子布局的位置。
        """
        if self.mode == 'proportional':
            self._update_proportional_layout()
        else:
            self._update_simple_layout()
        self.sub_width = self.container.relative_rect.width - 2 * self.padding
        self.sub_height = self.container.relative_rect.height - 2 * self.padding
        if self.title:
            self.title_element = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((self.padding, self.padding), (self.sub_width, 20)),
                text=self.title,
                manager=self.manager,
                container=self.container
            )
        for layout, _ in self.layouts:
            layout.update_layout()

    def _update_simple_layout(self):
        """
        更新简单模式布局，从左到右按间隔排列控件，不改变控件大小。
        """
        pass

    def _update_proportional_layout(self):
        """
        更新比例模式布局，按比例分配容器的宽度并调整控件大小。
        """
        pass

    def clear(self):
        """
        清空布局中的所有子元素和子布局。
        """
        self.elements = []
        self.ratios = []
        self.layouts = []
        self.update_layout()


class HBoxLayout(BoxLayout):
    def __init__(self, container, padding=5, spacing=5, mode='simple', title=None, manager=None):
        """
        初始化 HBoxLayout。

        :param container: pygame_gui.elements.UIPanel 用于放置子元素的容器
        :param padding: 布局左右的填充（像素）
        :param spacing: 各子元素之间的间距（像素）
        :param mode: 布局模式 ('simple' 或 'proportional')
        :param title: 布局的标题文本（可选）
        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        """
        super().__init__(container, padding, spacing, mode, title, manager)

    @property
    def total_width(self):
        """
        VBoxLayout布局的总宽度。
        """
        total_width = 0
        for element in self.elements:
            total_width += element.relative_rect.width + self.spacing
        for layout, _ in self.layouts:
            if isinstance(layout, HBoxLayout):
                total_width += layout.total_width + self.spacing
            else:
                total_width += layout.container.relative_rect.height
        return total_width

    def _update_simple_layout(self):
        """
        更新简单模式布局，从左到右按间隔排列控件，不改变控件大小。
        """
        x_offset = self.padding
        y_offset = self.padding if not self.title_element else self.padding + 30

        for element in self.elements:
            element.set_dimensions((element.relative_rect.width, self.sub_height))
            element.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            x_offset += element.relative_rect.width + self.spacing

        for layout, _ in self.layouts:
            layout_container = layout.container
            layout.container.set_dimensions((layout.container.relative_rect.width, self.sub_height))
            layout_container.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            layout.update_layout()
            x_offset += layout_container.relative_rect.width + self.spacing

    def _update_proportional_layout(self):
        """
        更新比例模式布局，按比例分配容器的宽度并调整控件大小。
        """
        total_width = self.container.relative_rect.width
        total_ratio = sum(self.ratios) + sum(ratio for _, ratio in self.layouts)
        available_width = total_width - 2 * self.padding - (len(self.elements) + len(self.layouts) - 1) * self.spacing

        x_offset = self.padding
        y_offset = self.padding if not self.title_element else self.padding + 30

        for element, ratio in zip(self.elements, self.ratios):
            widget_width = int((ratio / total_ratio) * available_width)
            element.set_dimensions((widget_width, self.sub_height))
            element.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            x_offset += widget_width + self.spacing

        for layout, ratio in self.layouts:
            layout_width = int((ratio / total_ratio) * available_width)
            layout.container.set_dimensions((layout_width, self.sub_height))
            layout.container.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            layout.update_layout()
            x_offset += layout_width + self.spacing


class VBoxLayout(BoxLayout):
    def __init__(self, container=None, parent=None, padding=5, spacing=5, mode='simple', title=None, manager=None):
        """
        初始化VBoxLayout。

        :param container: pygame_gui.elements.UIPanel 用于放置子元素的容器
        :param padding: 布局上下的填充（像素）
        :param spacing: 各子元素之间的间距（像素）
        :param mode: 布局模式 ('simple' 或 'proportional')
        :param title: 布局的标题文本（可选）
        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        """
        super().__init__(container, padding, spacing, mode, title, manager)

    @property
    def total_height(self):
        """
        布局的总高度（包含标题）。
        """
        total_height = 0
        for element in self.elements:
            total_height += element.relative_rect.height + self.spacing
        for layout, _ in self.layouts:
            if isinstance(layout, VBoxLayout):
                total_height += layout.total_height + self.spacing
            else:
                total_height += layout.container.relative_rect.height
        return total_height

    def _update_simple_layout(self):
        """
        更新简单模式布局，从上到下按间隔排列控件，不改变控件大小。
        """
        x_offset = self.padding
        y_offset = self.padding if not self.title_element else self.padding + 30

        for element in self.elements:
            element.set_dimensions((self.sub_width, element.relative_rect.height))
            element.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            y_offset += element.relative_rect.height + self.spacing

        for layout, _ in self.layouts:
            layout_container = layout.container
            layout.container.set_dimensions((self.sub_width, layout.container.relative_rect.height))
            layout_container.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            layout.update_layout()
            y_offset += layout_container.relative_rect.height + self.spacing

    def _update_proportional_layout(self):
        """
        更新比例模式布局，按比例分配容器的高度并调整控件大小。
        """
        total_height = self.container.relative_rect.height
        total_ratio = sum(self.ratios) + sum(ratio for _, ratio in self.layouts)
        available_height = total_height - 2 * self.padding - (len(self.elements) + len(self.layouts) - 1) * self.spacing

        x_offset = self.padding
        y_offset = self.padding if not self.title_element else self.padding + 30

        for element, ratio in zip(self.elements, self.ratios):
            widget_height = int((ratio / total_ratio) * available_height)
            element.set_dimensions((self.sub_width, widget_height))
            element.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            y_offset += widget_height + self.spacing

        for layout, ratio in self.layouts:
            layout_height = int((ratio / total_ratio) * available_height)
            layout.container.set_dimensions((self.sub_width, layout_height))
            layout.container.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            layout.update_layout()
            y_offset += layout_height + self.spacing

