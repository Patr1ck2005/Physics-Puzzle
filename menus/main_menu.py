import pygame
import pygame_gui

class MainMenu:
    def __init__(self, manager):
        self.manager = manager
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 200), (100, 50)),
                                                         text='Start Game',
                                                         manager=manager)
        self.options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 300), (100, 50)),
                                                           text='Options',
                                                           manager=manager)
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (100, 50)),
                                                        text='Exit',
                                                        manager=manager)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                return "start_game"
            elif event.ui_element == self.options_button:
                return "options"
            elif event.ui_element == self.exit_button:
                return "exit"
        return None

    def update(self):
        pass

    def draw(self, screen):
        pass