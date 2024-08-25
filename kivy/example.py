import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color
import pymunk
from pymunk import Vec2d


class PhysicsBall(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.space = pymunk.Space()
        self.space.gravity = (0, -300)

        self.body = pymunk.Body(1, 1, pymunk.Body.DYNAMIC)
        self.body.position = 300, 500
        self.shape = pymunk.Circle(self.body, 50)
        self.shape.elasticity = 0.95
        self.space.add(self.body, self.shape)

        with self.canvas:
            Color(1, 0, 0)
            self.ball = Ellipse(pos=self.body.position, size=(100, 100))

        self.dragged_body = None
        self.last_touch_pos = None
        self.rel_touch_v = None

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_touch_down(self, touch):
        if self.collide_with_ball(touch.pos):
            self.dragged_body = self.body
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.last_touch_pos:
            print(touch, 'current')
            print(self.last_touch_pos, 'last')
            self.rel_touch_v = Vec2d(touch.x - self.last_touch_pos[0], touch.y - self.last_touch_pos[1])
            print(self.rel_touch_v)
        self.last_touch_pos = touch.x, touch.y
        if self.dragged_body:
            self.dragged_body.position = touch.x, touch.y
            self.dragged_body.velocity = (0, 0)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.dragged_body:
            self.dragged_body.velocity = self.rel_touch_v*100
            self.dragged_body = None
            return True
        return super().on_touch_up(touch)

    def update(self, dt):
        self.space.step(dt)
        if self.dragged_body:
            self.dragged_body.velocity = (0, 0)
        self.ball.pos = (self.body.position.x - 50, self.body.position.y - 50)

    def collide_with_ball(self, pos):
        """ Check if the touch position is inside the ball """
        x, y = pos
        ball_x, ball_y = self.body.position
        ball_radius = self.shape.radius

        # Calculate the distance between the touch point and the ball's center
        dist = ((x - ball_x) ** 2 + (y - ball_y) ** 2) ** 0.5
        return dist <= ball_radius


class MyApp(App):
    def build(self):
        return PhysicsBall()


if __name__ == '__main__':
    MyApp().run()
