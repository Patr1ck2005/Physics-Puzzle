from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty


class DraggableBall(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 0, 1)  # 红色
            self.ball = Ellipse(pos=self.center, size=(100, 100))
        self.bind(pos=self.update_ball)

    def on_touch_down(self, touch):
        if self.collide_with_ball(touch.pos):
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.ball.pos = (touch.x - self.ball.size[0] / 2,
                             touch.y - self.ball.size[1] / 2)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super().on_touch_up(touch)

    def update_ball(self, *args):
        self.ball.pos = (self.center_x - self.ball.size[0] / 2,
                         self.center_y - self.ball.size[1] / 2)

    def collide_with_ball(self, pos):
        x, y = pos
        ball_x, ball_y = self.ball.pos
        ball_radius = self.ball.size[0] / 2

        dist = ((x - (ball_x + ball_radius)) ** 2 + (y - (ball_y + ball_radius)) ** 2) ** 0.5
        return dist <= ball_radius


class BallApp(App):
    def build(self):
        root = FloatLayout()
        ball = DraggableBall()
        root.add_widget(ball)
        return root


if __name__ == '__main__':
    BallApp().run()
