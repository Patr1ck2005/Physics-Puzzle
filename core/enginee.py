import pymunk
import pymunk.pygame_util


def init_world():

    space = pymunk.Space()
    space.gravity = (0.0, 1000.0)

    # 创建地面
    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground = pymunk.Segment(static_body, (50, 550), (750, 550), 5)
    ground.friction = 1.0
    ground.elasticity = 1
    space.add(static_body, ground)

    # 创建一个球体
    mass = 1
    radius = 15
    moment = pymunk.moment_for_circle(mass, 0, radius)
    ball_body = pymunk.Body(mass, moment)
    ball_body.position = (400, 50)
    ball_shape = pymunk.Circle(ball_body, radius)
    ball_shape.friction = 0.7
    ball_shape.elasticity = 0.8
    space.add(ball_body, ball_shape)
    return space


def update_world(space):
    space.step(1/60)


def render_world(space, screen):
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    space.debug_draw(draw_options)
