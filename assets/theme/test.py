import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIScrollingContainer, UILabel

pygame.init()

# Screen setup
pygame.display.set_caption('Auto-Scrolling Menu Demo')
window_surface = pygame.display.set_mode((800, 600))
ui_manager = pygame_gui.UIManager((800, 600))

# Create a scrolling container
scrolling_container = UIScrollingContainer(
    relative_rect=pygame.Rect(50, 50, 300, 400),
    manager=ui_manager,
    object_id=ObjectID(object_id='#auto_scroll_menu')
)

# Add items to the scrolling container
for i in range(20):
    UILabel(
        relative_rect=pygame.Rect(0, i * 30, 280, 30),
        text=f"Item {i + 1}",
        container=scrolling_container,
        manager=ui_manager
    )

# Main loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check if the mouse is over the scrolling container
    if scrolling_container.get_container().get_abs_rect().collidepoint(mouse_x, mouse_y):
        container_rect = scrolling_container.get_container().get_abs_rect()
        scroll_speed = 5

        # If mouse is near the bottom of the container, scroll down
        if mouse_y > container_rect.bottom - 50:
            new_scroll_position = scrolling_container.vert_scroll_bar.scroll_position + scroll_speed
            scrolling_container.vert_scroll_bar.set_position((new_scroll_position, 1))

        # If mouse is near the top of the container, scroll up
        elif mouse_y < container_rect.top + 50:
            new_scroll_position = scrolling_container.vert_scroll_bar.scroll_position - scroll_speed
            scrolling_container.vert_scroll_bar.set_position((new_scroll_position, 1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        ui_manager.process_events(event)

    ui_manager.update(time_delta)
    window_surface.fill((255, 255, 255))
    ui_manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
