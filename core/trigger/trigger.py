from core.event.event_manager import EventManager


class Trigger:
    def __init__(self, condition, event_name, event_manager, once=True):
        """
        初始化触发器。

        :param condition: 检查触发条件的函数，返回布尔值
        :param event_name: 条件满足时要触发的事件名称
        :param event_manager: 用于触发事件的事件管理器实例
        :param once: 如果为 True，条件满足后触发一次事件；如果为 False，则每次条件满足都会触发事件
        """
        self.condition = condition
        self.event_name = event_name
        self.event_manager = event_manager
        self.once = once
        self.triggered = False

    def check_and_trigger(self):
        """
        检查条件并在条件满足时触发事件。
        """
        if self.condition():  # 条件函数返回 True 时，触发事件
            if not self.triggered or not self.once:
                self.event_manager.trigger_event(self.event_name)
                self.triggered = True
        else:
            if not self.once:
                self.triggered = False  # 重置触发状态以允许再次触发

# 示例用法
if __name__ == "__main__":
    # 假设我们有一个简单的游戏环境
    player = {"health": 100, "coins": 0}

    # 初始化事件管理器
    event_manager = EventManager()

    # 定义一些事件处理函数
    def on_low_health():
        print("Warning: Player health is low!")

    def on_coin_collected():
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
