import pymunk
import pymunk.pygame_util

from core.event.event_manager import EventManager
from core.phy_object.entity import CircleEntity
from core.trigger.trigger import Trigger


class PointQueryTrigger(Trigger):
    def __init__(self, entity, target_point, event_name, event_manager, space):
        """
        初始化点查询触发器。

        :param entity: 要检测的物体
        :param target_point: 目标点 (x, y)
        :param event_name: 触发的事件名称
        :param event_manager: 用于触发事件的事件管理器实例
        :param space: Pymunk 空间
        """
        super().__init__(self._point_condition, event_name, event_manager)
        self.entity = entity
        self.target_point = target_point
        self.space = space

    def _point_condition(self):
        shapes = self.space.point_query(self.target_point, max_distance=0, shape_filter=pymunk.ShapeFilter())
        return any(shape.shape == self.entity.body_shape for shape in shapes)


class SegmentQueryTrigger(Trigger):
    def __init__(self, entity, segment_start, segment_end, event_name, event_manager, space):
        """
        初始化线段查询触发器。

        :param entity: 要检测的物体
        :param segment_start: 线段的起点 (x1, y1)
        :param segment_end: 线段的终点 (x2, y2)
        :param event_name: 触发的事件名称
        :param event_manager: 用于触发事件的事件管理器实例
        :param space: Pymunk 空间
        """
        super().__init__(self._segment_condition, event_name, event_manager)
        self.entity = entity
        self.segment_start = segment_start
        self.segment_end = segment_end
        self.space = space

    def _segment_condition(self):
        shapes = self.space.segment_query(self.segment_start, self.segment_end, radius=0, shape_filter=pymunk.ShapeFilter())
        return any(shape.shape == self.entity.body_shape for shape in shapes)


class BBQueryTrigger(Trigger):
    def __init__(self, entity, target_bb, event_name, event_manager, space):
        """
        初始化 BB 查询触发器。

        :param entity: 要检测的物体
        :param target_bb: 目标区域 (pymunk.BB 对象)
        :param event_name: 触发的事件名称
        :param event_manager: 用于触发事件的事件管理器实例
        :param space: Pymunk 空间
        """
        super().__init__(self._bb_condition, event_name, event_manager)
        self.entity = entity
        self.target_bb = target_bb
        self.space = space

    def _bb_condition(self):
        shapes = self.space.bb_query(self.target_bb, shape_filter=pymunk.ShapeFilter())
        return self.entity.body_shape in shapes


if __name__ == "__main__":
    # 初始化 Pygame 和 Pymunk 空间
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = (0, -900)

    # 初始化事件管理器
    event_manager = EventManager()

    # 创建一个物体
    player = CircleEntity("player", "dynamic", center=(100, 500), radius=30)
    player.add_to_space(space, (100, 500))

    # 定义查询参数
    target_point = (300, 300)
    segment_start = (100, 100)
    segment_end = (500, 100)
    target_bb = pymunk.BB(400, 400, 500, 500)

    # 注册事件处理函数
    def on_point_reached(*args, **kwargs):
        print("Player reached the target point!")

    def on_segment_crossed(*args, **kwargs):
        print("Player crossed the target segment!")

    def on_area_entered(*args, **kwargs):
        print("Player entered the target bounding box area!")

    event_manager.register_event("point_reached", on_point_reached)
    event_manager.register_event("segment_crossed", on_segment_crossed)
    event_manager.register_event("bb_area_entered", on_area_entered)

    # 创建触发器
    point_trigger = PointQueryTrigger(player, target_point, "point_reached", event_manager, space)
    segment_trigger = SegmentQueryTrigger(player, segment_start, segment_end, "segment_crossed", event_manager, space)
    bb_trigger = BBQueryTrigger(player, target_bb, "bb_area_entered", event_manager, space)

    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        space.step(1 / 50.0)
        space.debug_draw(draw_options)

        # 检查触发器
        point_trigger.check_and_trigger()
        segment_trigger.check_and_trigger()
        bb_trigger.check_and_trigger()

        pygame.display.flip()
        clock.tick(50)

    pygame.quit()
