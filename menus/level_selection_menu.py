import pygame
import pygame_gui


class LevelSelectionMenu:
    def __init__(self, manager):
        self.manager = manager
        self.level_buttons = []
        for i in range(0, 5):
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 100 + i * 60), (100, 50)),
                                                  text=f'Level {i}',
                                                  manager=manager)
            self.level_buttons.append(button)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for i, button in enumerate(self.level_buttons):
                if event.ui_element == button:
                    return f"level_{i}"
        return None

    def update(self):
        pass

    def draw(self, screen):
        pass
