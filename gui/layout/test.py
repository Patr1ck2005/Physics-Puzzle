import pygame
import pygame_gui

from hbox_layout import HBoxLayout
from vbox_layout import VBoxLayout

# 示例用法
pygame.init()
pygame.display.set_caption('VBox and HBox Layout Demo')
window_surface = pygame.display.set_mode((600, 600))

background = pygame.Surface((600, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((600, 600))

main_container = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((50, 50), (500, 500)),
    manager=manager
)

# 主垂直布局
main_vbox = VBoxLayout(main_container, padding=10, spacing=10, mode='proportional', title="Main Vertical Layout", manager=manager)

# 子垂直布局
sub_vbox = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((0, 0), (300, 150)),
    manager=manager,
    container=main_container
)
sub_vbox_layout = VBoxLayout(sub_vbox, padding=5, spacing=5, mode='proportional', title="Sub Vertical Layout", manager=manager)

# 在子垂直布局中添加按钮
button_1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (100, 50)),
    text='SubV Button 1',
    manager=manager,
    container=sub_vbox
)

button_2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (100, 50)),
    text='SubV Button 2',
    manager=manager,
    container=sub_vbox
)

button_3 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (100, 50)),
    text='SubV Button 3',
    manager=manager,
    container=sub_vbox
)

sub_vbox_layout.add_widget(button_1, ratio=1)
sub_vbox_layout.add_widget(button_2, ratio=1)
sub_vbox_layout.add_widget(button_3, ratio=1)

# 子水平布局
sub_hbox = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((0, 0), (300, 100)),
    manager=manager,
    container=main_container
)
sub_hbox_layout = HBoxLayout(sub_hbox, padding=5, spacing=5, mode='proportional', title="Sub Horizontal Layout", manager=manager)

# 在子水平布局中添加按钮
button_4 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (50, 100)),
    text='SubH Button 1',
    manager=manager,
    container=sub_hbox
)

button_5 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (50, 100)),
    text='SubH Button 2',
    manager=manager,
    container=sub_hbox
)


sub_hbox_layout.add_widget(button_4, ratio=1)
sub_hbox_layout.add_widget(button_5, ratio=1)

# 将子布局添加到主布局中
main_vbox.add_layout(sub_vbox_layout, ratio=3)
main_vbox.add_layout(sub_hbox_layout, ratio=1)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
