from core.event.trigger.trigger import Trigger


class PositionTrigger(Trigger):
    def __init__(self, entity, target_position, event_names, event_manager, tolerance=1.0):
        """
        :param entity: 要监控的物体
        :param target_position: 目标位置 (x, y)
        :param tolerance: 位置的容差
        """
        super().__init__(self._position_condition, event_names, event_manager)
        self.entity = entity
        self.target_position = target_position
        self.tolerance = tolerance

    def _position_condition(self):
        current_position = self.entity.center
        return abs(current_position.x - self.target_position[0]) <= self.tolerance and \
               abs(current_position.y - self.target_position[1]) <= self.tolerance


class SpeedTrigger(Trigger):
    def __init__(self, entity, min_speed, event_names, event_manager):
        """
        :param entity: 要监控的物体
        :param min_speed: 触发事件的最小速度
        """
        super().__init__(self._speed_condition, event_names, event_manager)
        self.entity = entity
        self.min_speed = min_speed

    def _speed_condition(self):
        return self.entity.velocity.length > self.min_speed


class AngularVelocityTrigger(Trigger):
    def __init__(self, entity, min_angular_velocity, event_names, event_manager):
        """
        :param entity: 要监控的物体
        :param min_angular_velocity: 触发事件的最小角速度
        """
        super().__init__(self._angular_velocity_condition, event_names, event_manager)
        self.entity = entity
        self.min_angular_velocity = min_angular_velocity

    def _angular_velocity_condition(self):
        return abs(self.entity.angular_velocity) > self.min_angular_velocity


class TrajectoryTrigger(Trigger):
    def __init__(self, entity, expected_trajectory, event_names, event_manager, tolerance=1.0):
        """
        :param entity: 要监控的物体
        :param expected_trajectory: 预期的轨迹，列表形式 [(x1, y1), (x2, y2), ...]
        :param tolerance: 位置的容差
        """
        super().__init__(self._trajectory_condition, event_names, event_manager)
        self.entity = entity
        self.expected_trajectory = expected_trajectory
        self.tolerance = tolerance

    def _trajectory_condition(self):
        history_positions = list(zip(self.entity.history_x, self.entity.history_y))
        if len(history_positions) < len(self.expected_trajectory):
            return False

        for hist_pos, exp_pos in zip(history_positions[-len(self.expected_trajectory):], self.expected_trajectory):
            if abs(hist_pos[0] - exp_pos[0]) > self.tolerance or abs(hist_pos[1] - exp_pos[1]) > self.tolerance:
                return False
        return True


class ContactTrigger(Trigger):
    def __init__(self, entity, other_entity, event_names, event_manager):
        """
        :param entity: 物体 A
        :param other_entity: 物体 B
        """
        super().__init__(self._contact_condition, event_names, event_manager)
        self.entity = entity
        self.other_entity = other_entity

    def _contact_condition(self):
        for arbiter in self.entity.body_shape.space.arbiters:
            if (arbiter.shapes[0] == self.entity.body_shape and arbiter.shapes[1] == self.other_entity.body_shape) or \
               (arbiter.shapes[1] == self.entity.body_shape and arbiter.shapes[0] == self.other_entity.body_shape):
                return True
        return False


class CollisionTrigger(Trigger):
    def __init__(self, entity, other_entity, event_names, event_manager, space):
        """
        初始化碰撞触发器。

        :param entity: 物体 A
        :param other_entity: 物体 B
        :param event_manager: 用于触发事件的事件管理器实例
        :param space: Pymunk 空间
        """
        super().__init__(self._collision_condition, event_names, event_manager)
        self.entity = entity
        self.other_entity = other_entity

        # 注册碰撞处理器
        handler = space.add_collision_handler(self.entity.body_shape.collision_type,
                                              self.other_entity.body_shape.collision_type)
        handler.begin = self._begin_collision

    def _collision_condition(self):
        # 碰撞条件会在碰撞开始时由 Pymunk 调用
        return True

    def _begin_collision(self, arbiter, space, data):
        # 在碰撞开始时触发事件
        print("Collision detected!")
        return True
