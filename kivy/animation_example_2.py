from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        btn = Button(text="Go to Second Screen")
        btn.bind(on_press=lambda x: self.manager.transition_to('second'))
        layout.add_widget(btn)
        self.add_widget(layout)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        btn = Button(text="Go back to First Screen")
        btn.bind(on_press=lambda x: self.manager.transition_to('first'))
        layout.add_widget(btn)
        self.add_widget(layout)

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(FirstScreen(name='first'))
        self.add_widget(SecondScreen(name='second'))

    def transition_to(self, screen_name):
        self.transition = SlideTransition(direction='left')
        self.current = screen_name

class MyApp(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    MyApp().run()
