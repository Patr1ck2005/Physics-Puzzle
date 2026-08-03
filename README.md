# PhyGame 物理解谜游戏

## 1. 项目概述

### 项目名称

PhyGame

### 游戏类型

物理解谜游戏

### 开发工具

- Python 3.11
- Pygame（渲染与输入）
- pygame_gui（UI 组件）
- Pymunk（物理引擎）
- NumPy / Matplotlib（辅助计算与可视化）

### 目标平台

PC（Windows, Mac, Linux）

### 项目概述

这是一款基于物理引擎的解谜游戏，玩家通过使用多种物理工具和力学原理来解决各种复杂的物理难题。游戏的目标是为玩家提供富有挑战性和娱乐性的解谜体验，同时学习和运用基本的物理知识。

## 2. 快速开始

### 环境安装

```bash
pip install -r requirements.txt
```

### 运行游戏

```bash
python main.py
```

### 运行测试

```bash
python -m pytest tests/
```

## 3. 项目结构

```text
PhyGame/
├── main.py                # 入口：主循环与界面切换
├── settings.py            # 全局常量（窗口尺寸、颜色、FPS）
├── requirements.txt       # 依赖列表
├── core/                  # 核心逻辑
│   ├── engine.py          # 物理引擎封装（Pymunk Space）
│   ├── level_loader.py    # 关卡加载器
│   ├── phy_obj_loader.py  # 物理对象 JSON 加载器
│   ├── events_loader.py   # 事件 JSON 加载器
│   ├── setting_loader.py  # 引擎参数 JSON 加载器
│   ├── phy_object/        # 物理对象定义
│   │   ├── entity.py      # 实体（Box/Circle/Poly）
│   │   ├── constrain.py   # 约束（PinJoint/SlideJoint/Spring）
│   │   ├── force.py       # 力
│   │   ├── tool.py        # 工具（摩擦力/弹性工具）
│   │   └── bg_wall.py     # 背景墙
│   └── event/             # 事件系统
│       ├── event_manager.py
│       ├── trigger_manager.py
│       ├── events/        # 事件处理函数
│       └── trigger/       # 触发器（Timer/Label/Query）
├── gui/                   # 图形界面
│   ├── base_ui.py         # UI 基类
│   ├── hud.py             # HUD 显示
│   ├── phy_obj_ui/        # 物理对象 UI 装饰
│   ├── ui_manager/        # UI 管理器
│   └── ui_panel/          # 面板（属性/顶部/底部）
├── menus/                 # 菜单与场景
│   ├── main_menu.py
│   ├── chapter_menu.py
│   ├── level_menu.py
│   ├── game_scene.py      # 游戏主场景
│   └── pause_menu.py
├── levels/                # 关卡数据
│   ├── level_1/           # 关卡 1（标签匹配）
│   ├── sand_box/          # 沙盒模式
│   └── CM/                # 经典力学章节
├── scripts/               # 工具函数
│   └── utils.py           # 几何工具（Poly/Round/旋转）
├── assets/                # 资源（图片/音乐/主题）
└── tests/                 # 单元测试
```

## 4. 游戏设计

### 游戏背景

游戏设定在一个逼真的物理世界中，玩家需要在这个世界中使用各种物理道具与环境进行交互。通过解密的方式，玩家将直观地体验和学习物理定律。

### 核心玩法

玩家通过探索场景、收集道具并使用它们来解决一系列基于物理学的谜题。谜题的设计将巧妙地展示各种物理定律，如重力、惯性、摩擦力、弹性碰撞等。玩家需要在这些场景中应用物理知识，利用道具的特性完成任务目标。

### 游戏目标

游戏的根本目的是通过互动的方式展示和传授物理定律，帮助玩家培养物理直觉。通过解密过程，玩家能够加深对物理现象的理解，享受解决难题带来的成就感。

### 关卡设计

游戏将分为多个关卡，每个关卡都聚焦于特定的物理定律或现象。难度将随着关卡的推进逐步增加，从基础的物理概念到更为复杂的应用。每个关卡都会提供一个独特的环境和一系列道具供玩家使用。

### 道具与互动

玩家可以使用多种物理道具，例如：

- **实体**: 木箱、金属球、多边形等刚体
- **力**: 施加在物体上的外力（矢量）
- **约束**: 轻杆（PinJoint）、轻绳（SlideJoint）、弹簧（Spring）
- **工具**: 摩擦力工具、弹性工具
- **标签**: 检查物体属性是否符合预期值

### 用户界面（UI/UX）

游戏的用户界面将简洁直观，主要包括：

- **道具栏**: 展示玩家当前拥有的物理道具。
- **场景交互提示**: 当玩家接近可互动物体时，显示相关提示。
- **物理反馈**: 实时显示物体受力和运动状态，以帮助玩家理解物理过程。

## 5. 关卡配置格式

每个关卡是一个目录，包含以下 JSON 文件：

- `setting.json` - 引擎参数（gravity, universal_gravity, pause）
- `scene.json` - 场景中的实体、力、约束
- `inventory.json` - 物品栏中的可放置物品
- `events.json` - 事件与触发器定义

详细配置教程见 [core/2024-8-26.event_system_json_config_help.md](core/2024-8-26.event_system_json_config_help.md)。
