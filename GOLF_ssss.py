import random
import time

import pygame
import pymunk
import sys
import pymunk.pygame_util
import math
from pymunk.vec2d import Vec2d

WIDTH, HEIGHT = 1200, 600

FPS = 90
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RADIUS = 8
MASS = 10
DT = 1 / FPS
tick = FPS
score = False

# 初始化游戏
pygame.init()
pygame.mixer.init()
# sky_image = pygame.image.load("image/sky.png")
# 创建背景
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# 随机出地面

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)


def angle(p0, p1):
    return math.atan2(p1[1] - p0[1], p1[0] - p0[0])


# 创建高尔夫球
def golf_ball(space, radius, mass, mouse_pos):
    golf_body = pymunk.Body()
    golf_body.position = mouse_pos
    golf_body_shape = pymunk.Circle(golf_body, radius)
    golf_body_shape.mass = mass
    golf_body_shape.color = (150, 150, 150, 100)
    golf_body_shape.elasticity = 0.5
    golf_body_shape.friction = 0.5
    golf_body_shape.collision_type = 1
    space.add(golf_body, golf_body_shape)
    return golf_body_shape


def gound(space, width, height):
    # rect = [(width / 2, height - 50), (width, 100)]
    # gound = pymunk.Body(body_type=pymunk.Body.STATIC)
    # gound.position = rect[0]
    # gound_shape = pymunk.Poly.create_box(gound, rect[1])
    # gound_shape.color = (244, 164, 96, 100)
    # gound_shape.elasticity = 1

    # space.add(gound, gound_shape)

    # poly_dims = []
    # dim_top = []
    # dim_bottom = []
    # for i in range(5):
    #     dim_bottom.append(0 + i * width / 4)
    #     dim_top.append((1 - random.random() / 2) * height )
    #     print(dim_bottom)
    #     print(dim_top)
    gound_list = []
    N = 8
    poly_dims = []
    # poly_dims = [(0, height),(width, height)]
    poly_dims.append((0, height - random.random() * height / 3))
    poly_dims.append((width, height - random.random() * height / 3))
    hole_deepth = height - random.random() * height / 5 - 10
    hole_x = 0.1 + 0.9 * random.random() * width
    poly_dims.append((hole_x, hole_deepth))
    poly_dims.append((hole_x + 20, hole_deepth))
    poly_dims.append((hole_x - 3, hole_deepth - 50))
    poly_dims.append((hole_x + 23, hole_deepth - 50))
    for i in range(N):
        x = random.random() * width
        if not hole_x - 3 <= x <= hole_x + 23:
            poly_dims.append((x, height - random.random() * height / 3))
    poly_dims = sorted(poly_dims)
    for i in range(len(poly_dims) - 1):
        gound = pymunk.Body(body_type=pymunk.Body.STATIC)
        gound.position = (0, 0)
        gound_shape = pymunk.Segment(gound, poly_dims[i], poly_dims[i + 1], 2)
        gound_shape.color = (244, 164, 96, 100)
        gound_shape.elasticity = 0.5
        gound_shape.friction = 0.9
        gound_shape.collision_type = 2
        space.add(gound, gound_shape)
        gound_list.append(gound_shape)
    return hole_x, hole_deepth, poly_dims, gound_list


# def hole(space):
#


def wall(space, width, height):
    rect_left = [(0, height / 2), (10, height * 2)]
    rect_right = [(width, height / 2), (10, height * 2)]
    wall_left = pymunk.Body(body_type=pymunk.Body.STATIC)
    wall_left.position = rect_left[0]
    wall_left_shape = pymunk.Poly.create_box(wall_left, rect_left[1])
    wall_left_shape.color = (70, 130, 180, 100)
    wall_left_shape.elasticity = 1
    space.add(wall_left, wall_left_shape)
    wall_right = pymunk.Body(body_type=pymunk.Body.STATIC)
    wall_right.position = rect_right[0]
    wall_right_shape = pymunk.Poly.create_box(wall_right, rect_right[1])
    wall_right_shape.color = (70, 130, 180, 100)
    wall_right_shape.elasticity = 1
    space.add(wall_right, wall_right_shape)


def cloud(space, width, height):
    num = random.randint(5, 20)
    cloud_shape_list = []
    for i in range(num):
        rect = [(random.random() * width, random.random() * height / 3),
                ((0.5 + 0.5 * random.random()) * 120, (0.6 + 0.4 * random.random()) * 30)]
        cloud = pymunk.Body(body_type=pymunk.Body.STATIC)
        cloud_shape = pymunk.Poly.create_box(cloud, rect[1])
        cloud.position = rect[0]
        cloud_shape.density = 0.01
        cloud_shape.color = (240, 240, 240, 100)
        cloud_shape.friction = 0.1
        cloud_shape.collision_type = 3
        cloud_shape_list.append(cloud_shape)

        space.add(cloud, cloud_shape)
    return cloud_shape_list


def stone(space, stones_dim, mouseR_pos):
    stone = pymunk.Body()
    for i in range(10):
        stones_dim.append((mouseR_pos[0] + random.randint(-20, 20), mouseR_pos[1] + random.randint(-15, 15)))
    # stones_dim = [(10, 10)]
    stone_shape = pymunk.Poly(stone, stones_dim)
    stone_shape.density = 0.1
    # stone.center_of_gravity = get_gravity_point(stones_dim)

    color = (100, 100, 100, 100)
    stone_shape.color = color
    stone_shape.elasticity = 0.1
    stone_shape.friction = 0.5
    stone_shape.collision_type = 2
    space.add(stone, stone_shape)
    return stone_shape


def draw(space, screen, width, height, draw_options, line, mouse_pos, hole_pos, sun_pos, sun_color):
    screen.fill((135, 206, 250))
    # screen.blit(sky_image, (0, 0))

    global tick
    global score
    # print(tick)
    # print(score)
    pygame.draw.polygon(screen, (244, 164, 96), hole_pos[2])
    pygame.draw.circle(screen, sun_color, sun_pos, 30)
    # pygame.draw.polygon(screen, (0,0,0), [hole_pos, (hole_pos[0] - 8, hole_pos[1] - 80), (hole_pos[0] - 10, hole_pos[1] - 80)])
    pygame.draw.polygon(screen, (50, 100, 150),
                        [(hole_pos[0] + 10, hole_pos[1] - 30), (hole_pos[0] + 6, hole_pos[1] - 60),
                         (hole_pos[0] + 14, hole_pos[1] - 60)])
    gound_dim = hole_pos[2]
    gound_dim.insert(0, (0, height))
    gound_dim.append((width, height))
    space.debug_draw(draw_options)
    draw_helptext(screen)
    if score and tick > 0:
        # tick = FPS
        draw_award(screen, hole_pos)
        tick -= 1
    elif score and tick <= 0:
        tick = FPS
        score = False
    if line:
        pygame.draw.line(screen, (248, 248, 255), line[0], line[1], 2)


def draw_helptext(screen):
    font = pygame.font.Font(None, 16)
    text = [

    ]
    y = 5
    for line in text:
        text = font.render(line, 1, pygame.Color("black"))
        screen.blit(text, (10, y))
        y += 10


def draw_award(sceen, hole_pos):
    font = pygame.font.Font(None, 16)
    text = [
        "SCORE!"
    ]
    y = 5
    for line in text:
        text = font.render(line, 1, pygame.Color("black"))
        screen.blit(text, (hole_pos[0] - 8, hole_pos[1] - 80))
        y += 10


def collision_begin(arbiter, space, data):
    print("a")


def get_gravity_point(points):
    """
    @brief      获取多边形的重心点
    @param      points  The points
    @return     The center of gravity point.
    """
    if len(points) <= 2:
        return list()

    area = (0.0)
    x, y = (0.0), (0.0)
    for i in range(len(points)):
        lng = (points[i][0])
        lat = (points[i][1])
        nextlng = (points[i - 1][0])
        nextlat = (points[i - 1][1])

        tmp_area = (nextlng * lat - nextlat * lng) / (2.0)
        area += tmp_area
        x += tmp_area * (lng + nextlng) / (3.0)
        y += tmp_area * (lat + nextlat) / (3.0)
    x = x / area
    y = y / area
    return [float(x), float(y)]


def run(screen, width, height):
    clock = pygame.time.Clock()
    global score
    # 加载音乐
    pygame.mixer_music.load("Aerie.mp3")
    pygame.mixer_music.set_volume(1)
    pygame.mixer_music.play(-1)

    # 创建物理世界
    space = pymunk.Space()
    space.gravity = (0, 100)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    ball_shape = None
    mouse_pos = None
    stones_dim = []
    stone_list = []
    cloud_shape_list = cloud(space, WIDTH, HEIGHT)
    gound_factors = gound(space, WIDTH, HEIGHT)
    wall(space, WIDTH, HEIGHT)
    sun_pos = (100, 75)
    mass_scale = 1
    real_sun = False
    center_vector_list = []
    stone_dis = [(0, 0), (0, 0)]
    # def draw_collision(arbiter, space, data):
    #     for c in arbiter.contact_point_set.points:
    #         r = max(3, abs(c.distance * 5))
    #         r = int(r)
    #         p = tuple(map(int, c.point_a))
    #         pygame.draw.circle(data["surface"], pygame.Color("red"), p, r, 0)
    # ch = space.add_collision_handler(0, 0)
    # ch.data["surface"] = screen
    # ch.post_solve = draw_collision
    # 碰撞检测

    # collision = space.add_collision_handler(1, 3)
    # collision.data["surface"] = screen
    # collision.begin = collision_begin

    while True:
        if stone_list:
            for i in range(len(stone_list)):
                if len(stone_dis) <= len(stone_list):
                    stone_dis.append((0, 0))
                stone_dis[i] += stone_list[i].body.velocity * 2 * DT
        if real_sun == False:
            sun_color = (255, 165, 0)
        else:
            sun_color = (0, 0, 0)
        line = None

        if real_sun == True:
            for Cloud in cloud_shape_list:
                Cloud.body.apply_force_at_world_point((0, - 200 * Cloud.mass), Cloud.body.position)
            if stone_list:
                for i in range(len(stone_list)):
                    Angle_sun_stone = angle(sun_pos, (stone_list[i].center_of_gravity + stone_list[i].body.position))
                    Force_sun_stone = 100000 * stone_list[i].mass / distance(sun_pos,
                                                                            (stone_list[i].center_of_gravity + stone_list[i].body.position))

                    stone_center = stone_list[i].center_of_gravity + stone_dis[i]
                    print(Force_sun_stone)
                    stone_list[i].body.apply_force_at_world_point((- Force_sun_stone * math.cos(Angle_sun_stone),
                                                                   - Force_sun_stone * math.sin(Angle_sun_stone)), stone_center)
        if ball_shape and mouse_pos:
            line = [mouse_pos, pygame.mouse.get_pos()]
        if ball_shape:
            # ball_shape.body.apply_force_at_world_point((0, 500*ball_shape.mass), ball_shape.body.position)
            if gound_factors[1] - RADIUS + 2 >= ball_shape.body.position.y >= gound_factors[1] - RADIUS - 2 and abs(
                    ball_shape.body.velocity.y) <= 0.1:
                space.remove(ball_shape, ball_shape.body)
                ball_shape = None
                score = True
            # collision = pymunk.CollisionHandler(ball_shape, space)
            # if collision.begin(ball_shape, space):
            #     print(1)
            elif real_sun == True:
                # print(ball_shape.body.position)
                Angle_sun = angle(sun_pos, ball_shape.body.position)
                Force_sun = 50000 * ball_shape.mass / distance(sun_pos, ball_shape.body.position)
                ball_shape.body.apply_force_at_world_point(
                    (- Force_sun * math.cos(Angle_sun), - Force_sun * math.sin(Angle_sun)), ball_shape.body.position)
        # if stone_list:
        #     for stones in stone_list:
        #         stones.body.apply_force_at_world_point((0, 500*stones.mass), stones.body.center_of_gravity)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if distance(pygame.mouse.get_pos(), sun_pos) <= 10:
                        if real_sun == False and random.random() > 0.5:
                            # cloud(space, WIDTH, HEIGHT)
                            # hole_pos = gound(space, WIDTH, HEIGHT)
                            for i in range(len(cloud_shape_list)):
                                space.remove(cloud_shape_list[i], cloud_shape_list[i].body)
                            for i in range(len(gound_factors[3])):
                                space.remove(gound_factors[3][i], gound_factors[3][i].body)
                            gound_factors = gound(space, WIDTH, HEIGHT)
                            cloud_shape_list = cloud(space, WIDTH, HEIGHT)
                            if ball_shape:
                                space.remove(ball_shape, ball_shape.body)
                                ball_shape = None
                            if stone_list:
                                for Stone in stone_list:
                                    space.remove(Stone, Stone.body)
                                stone_list = []
                                stone_dis = [(0, 0), (0, 0)]

                        elif real_sun == False:
                            real_sun = True
                            for i in range(len(cloud_shape_list)):
                                cloud_shape_list[i].body.body_type = pymunk.Body.DYNAMIC
                        else:
                            real_sun = False


                    elif not ball_shape:
                        mouse_pos = pygame.mouse.get_pos()
                        ball_shape = golf_ball(space, RADIUS, MASS, mouse_pos)
                        mouse_pos = None


                    elif ball_shape and not mouse_pos:
                        mouse_pos = pygame.mouse.get_pos()
                        if distance(mouse_pos, ball_shape.body.position) <= RADIUS:
                            space.remove(ball_shape, ball_shape.body)
                            ball_shape = None
                            mouse_pos = None
                if event.button == 2:
                    mass_scale += 0.5
                if event.button == 3:
                    print(1)
                    mouseR_pos = pygame.mouse.get_pos()
                    stones_dim.append(pygame.mouse.get_pos())
                    stone_list.append(stone(space, stones_dim, mouseR_pos))
                    if stone_list:
                        for Stone in stone_list:
                            center_vector_list.append(Stone.body.position - Stone.body.center_of_gravity)
                    stones_dim = []
                    # elif ball_shape and mouse_pos:
                    #     # print("1")
                    #     Angle = angle(*line)
                    #     Force = distance(*line) * 10
                    #     ball_shape.body.apply_impulse_at_local_point((Force * math.cos(Angle), Force * math.sin(Angle)),(0, 0))
                    #     mouse_pos = None
            if mouse_pos and event.type == pygame.MOUSEBUTTONUP:
                Angle = angle(*line)
                Force = distance(*line) * 10
                ball_shape.body.apply_impulse_at_world_point((- Force * math.cos(Angle), - Force * math.sin(Angle)),
                                                             ball_shape.body.position)
                mouse_pos = None

        space.step(DT)
        # 绘制图像
        # global tick
        # tick -= 1
        draw(space, screen, WIDTH, HEIGHT, draw_options, line, mouse_pos, gound_factors, sun_pos, sun_color)
        if stone_list:
            print(stone_list[0].body.velocity)
            # print(stone_list[0].body.position)
            # print(stone_list[0].center_of_gravity)
            # stone_dis += stone_list[0].body.velocity * 2 * DT
            print(stone_dis[0])
            stone_center = stone_list[0].center_of_gravity + stone_dis[0]
            # print(stone_center)
            pygame.draw.circle(screen, "black", stone_list[0].center_of_gravity, 2)
            # print(stone_list[0].center_of_gravity + stone_list[0].body.position)
            pygame.draw.circle(screen, "red", stone_center, 2)
        pygame.display.update()
        space.step(DT)
        clock.tick(FPS)
        pygame.display.set_caption("Golf " + "(fps: " + str(int(clock.get_fps())) + ")")


if __name__ == "__main__":
    run(screen, WIDTH, HEIGHT)
