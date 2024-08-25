# 游戏事件系统详细文档

## 目录
1. [概述](#概述)
2. [事件系统组成](#事件系统组成)
   - [EventManager](#eventmanager)
   - [TriggerManager](#triggermanager)
   - [Trigger](#trigger)
   - [State](#state)
   - [EventLoader](#eventloader)
3. [事件系统的运行原理](#事件系统的运行原理)
4. [关卡事件的JSON配置方法](#关卡事件的json配置方法)
   - [JSON配置示例](#json配置示例)
   - [配置详解](#配置详解)

## 概述

游戏的事件系统是一个模块化、灵活且高度可配置的系统，旨在管理和处理游戏中各种复杂的交互事件。通过使用事件管理器（EventManager）、触发器管理器（TriggerManager）、状态（State）、触发器（Trigger）以及事件加载器（EventLoader），游戏能够根据特定条件触发事件，并执行相应的处理逻辑。

## 事件系统组成

### EventManager

`EventManager` 是事件系统的核心组件，负责管理事件的注册、注销和触发。其主要功能包括：

- **注册事件**：允许其他系统或模块注册事件及其对应的处理函数，支持优先级排序。
  
  使用方法：

  ```python
  event_manager = EventManager()

  # 注册一个事件
  event_manager.register_event('show_message', show_message_event_handler, priority=10)
  ```
  

- **注销事件**：可以移除已注册的事件处理函数，确保事件管理器的灵活性。
  
  使用方法：

  ```python
  # 注销一个事件
  event_manager.unregister_event('show_message', show_message_event_handler)
  ```

- **触发事件**：当某个事件被触发时，`EventManager` 会调用所有与该事件关联的处理函数，并传递相关参数。
  
  使用方法：

  ```python
  # 触发一个事件
  event_manager.trigger_event('show_message', message='Hello, World!')
  ```

- **清除所有事件**：清除事件管理器中所有已注册的事件。

  使用方法：

  ```python
  # 清除所有事件
  event_manager.clear_all_events()
  ```

### TriggerManager

`TriggerManager` 管理游戏中的所有触发器，并通过状态（'State'）来组织这些触发器。其主要功能包括：

- **管理状态**：`TriggerManager` 可以管理多个状态，每个状态包含不同的触发器。

  使用方法：

  ```python
  trigger_manager = TriggerManager(event_state_machine)

  # 添加状态
  state_a = State('StateA')
  trigger_manager.add_state(state_a)
  ```

- **设置初始状态**：设置触发器管理器的初始状态。

  使用方法：

  ```python
  # 设置初始状态
  trigger_manager.set_initial_state('StateA')
  ```

- **切换状态**：游戏可以通过 `TriggerManager` 在不同状态之间切换，从而激活或停用某些触发器。

  使用方法：

  ```python
  # 切换到另一个状态
  trigger_manager.transition_to_state('StateB')
  ```

- **检查当前状态的触发器**：当状态激活时，`TriggerManager` 会定期检查与该状态关联的所有触发器，并根据条件决定是否触发事件。

  使用方法：

  ```python
  # 检查当前状态的触发器
  trigger_manager.check_triggers()
  ```

### Trigger

`Trigger` 是所有触发器类的基类，用于检测游戏中的特定条件是否满足。一旦条件满足，触发器会通知 `EventManager` 触发相应的事件。`Trigger` 支持以下功能：

- **条件检查**：通过 `check_and_trigger` 方法，触发器会定期检查条件是否满足，并决定是否触发事件。

  使用方法：

  ```python
  # 定义一个简单的触发器
  trigger = Trigger(
      condition=lambda: player_health < 50,
      event_names='low_health_warning',
      event_manager=event_manager
  )

  # 在游戏循环中定期检查触发器
  trigger.check_and_trigger()
  ```

- **去抖动**：支持 `debounce_time` 参数，防止在短时间内重复触发事件。

  使用方法：

  ```python
  # 定义一个带有去抖动的触发器
  trigger = Trigger(condition=lambda: player_health < 50, event_names=['low_health'], event_manager=event_manager, debounce_time=5.0)
  ```

- **单次触发**：支持 `once` 参数，控制触发器是否只触发一次。

  使用方法：

  ```python
  # 定义一个只触发一次的触发器
  trigger = Trigger(condition=lambda: player_health < 50, event_names=['low_health'], event_manager=event_manager, once=True)
  ```

- **复杂条件**：使用 `ComplexCondition` 类定义组合条件。

  使用方法：

  ```python
  complex_condition = ComplexCondition([condition1, condition2])
  complex_trigger = Trigger(complex_condition, "complex_event", event_manager)
  ```

- **扩展**: 在触发器的基类上可以扩展出其他较复杂的触发器. 这主要通过在子类触发器中定义较为复杂的`condition`并传入触发器基类的初始化函数. 例如, 计时触发器`TimerTrigger`. 还有一些一些触发器创建时需要传入具体游戏物理对象, 然后它们的触发条件通常于该游戏物理对象的状态有关, 例如游戏物理对象的位置, 速度等等. 例如`PointQueryTrigger`当对象与目标点重合时触发.

### State

`State` 类表示游戏中的一个状态，包含该状态下所具有的一组触发器。每个状态都可以独立管理这些触发器，并在状态激活时检查其触发条件。状态的主要功能包括：

- **添加触发器**：可以将触发器添加到某一个状态中，以便在该状态激活时进行检查。

  使用方法：

  ```python
  state_a = State('StateA')

  # 添加触发器到状态
  state_a.add_trigger(trigger)
  ```

- **检查触发器**：当状态激活时，`State` 会遍历所有触发器，并调用它们的 `check_and_trigger` 方法。

  使用方法：

  ```python
  # 检查状态中的所有触发器
  state_a.check_triggers()
  ```

### EventLoader

`EventLoader` 类负责从外部JSON配置文件中加载事件和触发器。这种设计使得游戏事件系统可以在不修改代码的情况下，通过配置文件来调整或扩展事件逻辑。其主要功能包括：

- **加载事件**：从JSON文件中解析事件配置，并将事件处理函数注册到 'EventManager' 中。

  使用方法：

  ```python
  event_loader = EventLoader(events_json_file='events.json', entities=entities, space=space)

  # 加载事件和触发器
  event_loader.load_events()
  ```

- **注册事件处理函数**：根据配置文件中的 `handler` 名称注册事件处理函数。

  使用方法：

  ```python
  # 注册 "show_console_message" 事件
  self.event_manager.register_event(
      event_name,
      lambda params=handler_params, *args, **kwargs: show_console_message(**params)
  )
  ```

- **在状态中加载触发器**：触发器会被加载到相应的状态中。

  使用方法：

  ```python
  # 处理定时器触发器
  if trigger_type == "TimerTrigger":
      trigger = TimerTrigger(
          duration=trigger_config["duration"],
          events=trigger_config["events"],
          event_manager=self.event_manager,
          start_immediately=trigger_config.get("start_immediately", False),
          once=trigger_config.get("once", True)
      )

  # 处理点查询触发器
  elif trigger_type == "PointQueryTrigger":
      trigger = PointQueryTrigger(
          entity_name=trigger_config["entity_name"],
          target_point=tuple(trigger_config["target_point"]),
          events=trigger_config["events"],
          space=self.space,
          min_duration=trigger_config.get("min_duration", 0)
      )
  ```

- **状态转换**：定义自定义状态转换逻辑，并在事件触发时执行。

  使用方法：

  ```python
  def trans_to_state_b(self, *args, **kwargs):
      self.trigger_manager.transition_to_state("StateB")
  ```

## 事件系统的运行原理

1. **初始化**：当游戏启动时，`EventLoader` 从配置文件中加载事件和触发器。事件被注册到 `EventManager`，触发器被分配到不同的状态，并由 `TriggerManager` 进行管理。
  
2. **状态管理**：游戏中的不同场景或阶段可以通过状态（State）来表示。每个状态包含一组触发器，这些触发器会在状态激活时进行条件检查。

3. **条件检查与事件触发**：`TriggerManager` 会定期检查当前状态下的所有触发器。如果某个触发器的条件满足，`EventManager` 会触发相应的事件，并执行预先注册的处理函数。

4. **状态切换**：当某些事件触发时，游戏可以通过 `TriggerManager` 切换状态，从而改变当前激活的触发器集。例如，当玩家完成某个任务时，游戏可能会切换到一个新的状态，以启动新的事件和触发器。

## 关卡事件的JSON配置方法

### JSON配置示例

  ```json
    {
      "events": {
        "state_transition_to_b": {
          "handler": "transition_to_state_b"
        },
        "show_message_event": {
          "handler": "show_console_message",
          "params": {
            "message": "Hello, this is a custom message!"
          }
        },
        "message_running_out_of_time": {
          "handler": "show_console_message",
          "params": {
            "message": "You are running out of time!"
          }
        }
      },
      "states": [
        {
          "name": "StateA",
          "triggers": [
            {
              "type": "PointQueryTrigger",
              "entity_name": "ball_2",
              "target_point": [300, 300],
              "events": ["show_message_event"],
              "space": "pymunk_space",
              "min_duration": 1
            },
            {
              "type": "TimerTrigger",
              "duration": 3,
              "events": ["message_running_out_of_time"],
              "start_immediately": true,
              "once": true
            }
          ]
        },
        {
          "name": "StateB",
          "triggers": [
            {
              "type": "TimerTrigger",
              "duration": 2,
              "events": ["show_message_event"],
              "start_immediately": true
            }
          ]
        }
      ]
    }
  ```

### 配置详解

- **`events` 部分**: 定义了所有可以触发的事件以及它们的处理函数（handler）。
  - `state_transition_to_b`: 当事件被触发时，调用 `transition_to_state_b` 函数来处理状态转换。
  - `show_message_event`: 调用 `show_console_message` 函数，并传递参数 `message` 来显示自定义消息。
  - `message_running_out_of_time`: 类似地，调用 `show_console_message` 显示 "You are running out of time!" 的消息。

- **`states` 部分**: 定义了游戏中的各个状态以及与这些状态关联的触发器。
  - `StateA`: 
    - `PointQueryTrigger`: 触发器会检测名为 `ball_2` 的实体是否在指定的 `target_point`（[300, 300]）处停留至少 `min_duration` 秒。如果条件满足，则触发 `show_message_event` 事件。
    - `TimerTrigger`: 计时触发器，在3秒后触发 `message_running_out_of_time` 事件，并且只触发一次。
  - `StateB`: 
    - `TimerTrigger`: 计时触发器，在2秒后触发 `show_message_event` 事件，并且会立即开始计时。

### 使用方法
1. 将JSON文件放置在合适的配置目录中，并在游戏启动时通过 `EventLoader` 加载该文件。
2. 在游戏运行过程中，`TriggerManager` 将会根据当前的状态，管理触发器的检查和事件的触发。
3. 根据需要，通过修改JSON文件，可以轻松调整触发条件和事件逻辑，而无需更改游戏代码。

---

通过上述系统设计，游戏可以灵活地管理复杂的事件交互，并且易于扩展和维护。JSON配置文件的使用进一步增强了系统的可配置性，适用于不同的游戏场景和关卡设计。
