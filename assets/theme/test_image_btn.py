import pygame
import pygame_gui
from pygame_gui.elements import UIButton

pygame.init()

# Screen setup
window_surface = pygame.display.set_mode((800, 600))
ui_manager = pygame_gui.UIManager((800, 600), 'test_theme.json')

# Create a button
button = UIButton(relative_rect=pygame.Rect(100, 100, 200, 50),
                  text='',
                  manager=ui_manager)

# Main loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        ui_manager.process_events(event)

    ui_manager.update(time_delta)
    window_surface.fill((255, 255, 255))
    ui_manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
