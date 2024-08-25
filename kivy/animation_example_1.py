from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation

class AnimatedBoxLayout(BoxLayout):
    def animate_label(self, instance):
        anim = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)
        anim += Animation(pos=(self.width - instance.width, self.y), duration=1)
        anim.start(instance)

class MyApp(App):
    def build(self):
        layout = AnimatedBoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text="Cool UI Effect", font_size='20sp')
        button = Button(text="Click Me", size_hint=(1, 0.2))

        button.bind(on_press=lambda x: layout.animate_label(label))

        layout.add_widget(label)
        layout.add_widget(button)
        return layout

if __name__ == '__main__':
    MyApp().run()
