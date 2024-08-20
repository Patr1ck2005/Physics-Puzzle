import pygame
import pygame_gui


class PauseMenu:
    def __init__(self, manager):
        self.manager = manager
        self.resume_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 200), (100, 50)),
                                                          text='Resume',
                                                          manager=manager)
        self.main_menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 300), (100, 50)),
                                                             text='Main Menu',
                                                             manager=manager)
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (100, 50)),
                                                        text='Exit',
                                                        manager=manager)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.resume_button:
                return "resume_game"
            elif event.ui_element == self.main_menu_button:
                return "back_to_menu"
            elif event.ui_element == self.exit_button:
                return "exit"
        return None

    def update(self):
        pass

    def draw(self, screen):
        pass
