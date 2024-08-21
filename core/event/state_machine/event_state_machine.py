class EventStateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state_name, allowed_events):
        """
        添加一个状态及其允许的事件列表。

        :param state_name: 状态的名称
        :param allowed_events: 在此状态下允许触发的事件列表
        """
        self.states[state_name] = allowed_events

    def set_state(self, state_name):
        """
        设置当前状态。

        :param state_name: 要设置为当前状态的状态名称
        """
        if state_name in self.states:
            self.current_state = state_name
            print(f"State changed to '{state_name}'")

    def trigger_event(self, event_name):
        """
        触发事件，如果该事件在当前状态下被允许。

        :param event_name: 要触发的事件名称
        """
        if self.current_state and event_name in self.states[self.current_state]:
            print(f"Event '{event_name}' triggered in state '{self.current_state}'")
        else:
            print(f"Event '{event_name}' not allowed in state '{self.current_state}'")


if __name__ == '__main__':
    # 使用示例

    # 初始化状态机
    state_machine = EventStateMachine()

    # 定义状态和允许的事件
    state_machine.add_state("state_a", ["event_a"])
    state_machine.add_state("state_b", ["event_b"])
    state_machine.add_state("state_c", ["event_c"])

    # 设置当前状态
    state_machine.set_state("state_a")

    # 触发事件
    state_machine.trigger_event("event_a")  # 有效，输出事件触发消息
    state_machine.trigger_event("event_b")  # 无效，不允许在当前状态触发，输出事件未触发消息

    # 改变状态
    state_machine.set_state("state_b")
    state_machine.trigger_event("event_b")  # 有效，输出事件触发消息
    state_machine.trigger_event("event_a")  # 无效，不允许在当前状态触发
