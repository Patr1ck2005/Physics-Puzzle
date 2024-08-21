from core.event.event_manager import EventManager

import time


class Trigger:
    def __init__(self, condition, event_names, event_manager, once=True, debounce_time=0):
        """
        :param event_names: 可以是一个事件名称或一个事件名称列表
        """
        self.condition = condition
        self.event_names = event_names if isinstance(event_names, list) else [event_names]
        self.event_manager = event_manager
        self.once = once
        self.triggered = False
        self.debounce_time = debounce_time
        self.last_trigger_time = 0

    def check_and_trigger(self):
        current_time = time.time()
        if self.condition() and (current_time - self.last_trigger_time >= self.debounce_time):
            if not self.triggered or not self.once:
                for event_name in self.event_names:
                    # 例如将条件结果作为参数传递
                    self.event_manager.trigger_event(event_name, condition_met=True)
                self.triggered = True
        else:
            if not self.once:
                self.triggered = False

    # 可视化触发器
    def draw(self, screen):
        # 在子类中重写
        pass


class ComplexCondition:
    # # 使用方式
    # complex_condition = ComplexCondition([condition1, condition2])
    # complex_trigger = Trigger(complex_condition, "complex_event", event_manager)
    def __init__(self, conditions):
        self.conditions = conditions

    def __call__(self):
        return all(condition() for condition in self.conditions)


# 示例用法
if __name__ == "__main__":
    # 假设我们有一个简单的游戏环境
    player = {"health": 100, "coins": 0}

    # 初始化事件管理器
    event_manager = EventManager()

    # 定义一些事件处理函数
    def on_low_health(*args, **kwargs):
        print("Warning: Player health is low!")

    def on_coin_collected(*args, **kwargs):
        print(f"Coins collected: {player['coins']}")

    # 注册事件
    event_manager.register_event("low_health", on_low_health)
    event_manager.register_event("coin_collected", on_coin_collected)

    # 定义触发条件
    def low_health_condition():
        return player["health"] < 20

    def coin_collected_condition():
        return player["coins"] > 0

    # 创建触发器
    low_health_trigger = Trigger(low_health_condition, "low_health", event_manager)
    coin_collected_trigger = Trigger(coin_collected_condition, "coin_collected", event_manager, once=False)

    # 模拟游戏更新循环
    def game_update():
        # 假设游戏在不断循环更新
        low_health_trigger.check_and_trigger()
        coin_collected_trigger.check_and_trigger()

    # 模拟游戏中的状态变化
    print("Game Start")
    for i in range(10):
        player["coins"] += 1
        player["health"] -= 25
        game_update()

    # 输出示例:
    # Game Start
    # Coins collected: 1
    # Warning: Player health is low!
    # Coins collected: 2
    # Coins collected: 3
    # Coins collected: 4
    # Coins collected: 5
