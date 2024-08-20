import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import QUIT

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 1000))  # 大的窗口来容纳所有区域
clock = pygame.time.Clock()
running = True

# 初始化 pymunk 空间
space = pymunk.Space()
space.gravity = (0, 0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# 创建地面
def create_ground(space, x_start, x_end, y, thickness=5):
    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground = pymunk.Segment(static_body, (x_start, y), (x_end, y), thickness)
    ground.friction = 1.0
    space.add(static_body, ground)
    return ground

# 创建物体
def create_ball(space, pos, radius=30):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.9
    space.add(body, shape)
    return body

def create_box(space, pos, size=(60, 60)):
    body = pymunk.Body(1, pymunk.moment_for_box(1, size))
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 0.9
    space.add(body, shape)
    return body

# 每个区域的宽度和高度
region_width = screen.get_width() // 5
region_height = screen.get_height() // 2

# 创建每个区域的地面
for i in range(5):
    create_ground(space, i * region_width, (i + 1) * region_width, region_height - 20)
    create_ground(space, i * region_width, (i + 1) * region_width, screen.get_height() - 20)

# 1. 区域 1: PinJoint
ball_a = create_ball(space, (region_width // 2, region_height // 2))
ball_b = create_ball(space, (region_width // 2 + 100, region_height // 2))
ball_a.velocity = (10, 10)
pin_joint = pymunk.PinJoint(ball_a, ball_b)
space.add(pin_joint)

# 2. 区域 2: SlideJoint
ball_c = create_ball(space, (region_width // 2 + region_width, region_height // 2))
ball_d = create_ball(space, (region_width // 2 + region_width + 100, region_height // 2))
ball_c.velocity = (10, 10)
slide_joint = pymunk.SlideJoint(ball_c, ball_d, (0, 0), (0, 0), 50, 150)
space.add(slide_joint)

# 3. 区域 3: PivotJoint
box_a = create_box(space, (2 * region_width + region_width // 2, region_height // 2))
box_aa = create_box(space, (2 * region_width + region_width // 2 + 100, region_height // 2))
box_a.velocity = (10, 10)
pivot_joint = pymunk.PivotJoint(box_a, box_aa, (2 * region_width + region_width // 2 + 10, region_height // 2 + 10))
space.add(pivot_joint)

# 4. 区域 4: GrooveJoint
box_b = create_box(space, (3 * region_width + region_width // 2, region_height // 2))
groove_joint = pymunk.GrooveJoint(space.static_body, box_b, (3 * region_width + 100, region_height // 2),
                                  (3 * region_width + 200, region_height // 2), (0, 0))
box_b.velocity = (10, 10)
space.add(groove_joint)

# 5. 区域 5: DampedSpring
ball_e = create_ball(space, (4 * region_width + 50, region_height // 2))
ball_f = create_ball(space, (4 * region_width + 150, region_height // 2))
ball_e.velocity = (10, 10)
spring_joint = pymunk.DampedSpring(ball_e, ball_f, (0, 0), (0, 0), rest_length=100, stiffness=200, damping=0.5)
space.add(spring_joint)

# 6. 区域 6: DampedRotarySpring
box_c = create_box(space, (region_width // 2, screen.get_height() - region_height // 2))
box_c.angular_velocity = 10
rotary_spring = pymunk.DampedRotarySpring(box_c, space.static_body, rest_angle=0, stiffness=500, damping=0.3)
space.add(rotary_spring)

# 7. 区域 7: RotaryLimitJoint
box_d = create_box(space, (region_width + region_width // 2, screen.get_height() - region_height // 2))
box_d.angular_velocity = 10
rotary_limit = pymunk.RotaryLimitJoint(box_d, space.static_body, min=-0.5, max=0.5)
space.add(rotary_limit)

# 8. 区域 8: RatchetJoint
box_e = create_box(space, (2 * region_width + region_width // 2, screen.get_height() - region_height // 2))
box_e.angular_velocity = -10
ratchet_joint = pymunk.RatchetJoint(box_e, space.static_body, phase=0, ratchet=0.5)
space.add(ratchet_joint)

# 9. 区域 9: GearJoint
box_f = create_box(space, (3 * region_width + 50, screen.get_height() - region_height // 2))
box_g = create_box(space, (3 * region_width + 150, screen.get_height() - region_height // 2))
box_f.angular_velocity = 10
gear_joint = pymunk.GearJoint(box_f, box_g, phase=0, ratio=5)
space.add(gear_joint)

# 10. 区域 10: SimpleMotor
box_h = create_box(space, (4 * region_width + region_width // 2, screen.get_height() - region_height // 2))
motor = pymunk.SimpleMotor(box_h, space.static_body, rate=-3.0)
space.add(motor)

# 主循环
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # 更新物理模拟
    space.step(1/50.0)

    # 绘制
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
