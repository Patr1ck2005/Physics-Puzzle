import pygame
import pygame_gui

from gui.layout.box_layout import BoxLayout


class GridLayout(BoxLayout):
    def __init__(self, container, padding=5, spacing=5, title=None, manager=None, rows=None, columns=None):
        """
        初始化 GridLayout。

        :param container: pygame_gui.elements.UIPanel 用于放置子元素的容器
        :param padding: 布局的填充（像素）
        :param spacing: 各子元素之间的间距（像素）
        :param title: 布局的标题文本（可选）
        :param manager: pygame_gui 的 UIManager，用于管理UI元素
        :param rows: 网格的行数（可选，如果未指定，将自动调整）
        :param columns: 网格的列数（可选，如果未指定，将自动调整）
        """
        super().__init__(container, padding, spacing, title=title, manager=manager)
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.column_ratios = []
        self.row_ratios = []

    def add_widget(self, widget, row, col, row_span=1, col_span=1):
        """
        将新组件添加到指定的网格位置。

        :param widget: 要添加的 pygame_gui 元素
        :param row: 添加到的行索引
        :param col: 添加到的列索引
        :param row_span: 跨越的行数
        :param col_span: 跨越的列数
        """
        self.elements.append((widget, row, col, row_span, col_span))
        self.update_layout()

    def add_layout(self, layout, row, col, row_span=1, col_span=1):
        """
        将另一个布局管理器添加到指定的网格位置。

        :param layout: 要添加的另一个布局管理器 (VBoxLayout, HBoxLayout等)
        :param row: 添加到的行索引
        :param col: 添加到的列索引
        :param row_span: 跨越的行数
        :param col_span: 跨越的列数
        """
        self.layouts.append((layout, row, col, row_span, col_span))
        self.update_layout()

    def update_layout(self):
        """
        更新网格布局，重新排列所有子元素和子布局的位置。
        """
        if not self.elements+self.layouts:
            return  # 如果没有元素，就不用更新布局了

        self.sub_width = self.container.relative_rect.width - 2 * self.padding
        self.sub_height = self.container.relative_rect.height - 2 * self.padding

        # 计算网格的行和列数
        self.rows = max(row for _, row, _, _, _ in self.elements+self.layouts) + 1
        self.columns = max(col for _, _, col, _, _ in self.elements+self.layouts) + 1

        # 计算行和列的宽度
        available_width = self.sub_width - (self.columns - 1) * self.spacing
        available_height = self.sub_height - (self.rows - 1) * self.spacing

        column_widths = [available_width // self.columns] * self.columns
        row_heights = [available_height // self.rows] * self.rows

        # 布置控件
        for widget, row, col, row_span, col_span in self.elements:
            x_offset = self.padding + sum(column_widths[:col]) + col * self.spacing
            y_offset = self.padding + sum(row_heights[:row]) + row * self.spacing

            widget_width = sum(column_widths[col:col + col_span]) + (col_span - 1) * self.spacing
            widget_height = sum(row_heights[row:row + row_span]) + (row_span - 1) * self.spacing

            widget.set_dimensions((widget_width, widget_height))
            widget.set_relative_position(pygame.math.Vector2(x_offset, y_offset))

        # 布置子布局
        for layout, row, col, row_span, col_span in self.layouts:
            x_offset = self.padding + sum(column_widths[:col]) + col * self.spacing
            y_offset = self.padding + sum(row_heights[:row]) + row * self.spacing

            layout_width = sum(column_widths[col:col + col_span]) + (col_span - 1) * self.spacing
            layout_height = sum(row_heights[row:row + row_span]) + (row_span - 1) * self.spacing

            layout.container.set_dimensions((layout_width, layout_height))
            layout.container.set_relative_position(pygame.math.Vector2(x_offset, y_offset))
            layout.update_layout()

    def clear(self):
        """
        清空布局中的所有子元素和子布局。
        """
        self.elements = []
        self.layouts = []
        self.update_layout()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    manager = pygame_gui.UIManager((800, 600))

    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((50, 50), (400, 300)),
        manager=manager
    )

    # 创建 GridLayout 布局
    grid_layout = GridLayout(panel, padding=10, spacing=5, manager=manager)

    # 添加一些按钮到 GridLayout
    button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (0, 0)),
                                           text="Button 1",
                                           manager=manager,
                                           container=panel)
    button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (0, 0)),
                                           text="Button 2",
                                           manager=manager,
                                           container=panel)
    button3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (0, 0)),
                                           text="Button 3",
                                           manager=manager,
                                           container=panel)

    grid_layout.add_widget(button1, row=0, col=0)
    grid_layout.add_widget(button2, row=0, col=1)
    grid_layout.add_widget(button3, row=1, col=0)

    sub_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((50, 50), (200, 200)),
        manager=manager,
        container=panel
    )

    sub_layout = GridLayout(sub_panel, padding=10, spacing=5, manager=manager)

    grid_layout.add_layout(sub_layout, row=1, col=1)
    sub_button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (0, 0)),
                                               text="Sub 1",
                                               manager=manager,
                                               container=sub_panel)
    sub_button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (0, 0)),
                                               text="Sub 2",
                                               manager=manager,
                                               container=sub_panel)
    sub_layout.add_widget(sub_button1, row=0, col=0)
    sub_layout.add_widget(sub_button2, row=0, col=1)

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)

        manager.update(time_delta)
        screen.fill((0, 0, 0))
        manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()

