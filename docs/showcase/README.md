# Headless original-renderer frame / 原渲染器无头画面

![Original sandbox rendered to its complete SDL surface](headless-sandbox-public-baseline.png)

- Public source / 公开源码: [`dec24a14bcfaca65aa32c9c7c0b4c3057d6989ad`](https://github.com/Patr1ck2005/Physics-Puzzle/tree/dec24a14bcfaca65aa32c9c7c0b4c3057d6989ad)
- Capture / 生成: 2026-10-17; original `GameScene`, unchanged `sand_box`, 60 update/draw/UI frames.
- Output / 输出: entire 1600 × 900 Pygame display surface, saved directly with `pygame.image.save`.
- Image SHA-256: `afdbe1489861bd03ff24b7a9ad5bdb477e7488980ba6bb5127602d3f00ff0e79`
- [Full capture metadata / 完整元数据](capture.json)

**Headless actual-renderer frame.** SDL video and audio use `dummy`; this is not a native desktop screenshot or human gameplay acceptance. The source was exported from the public revision to an isolated directory. The original renderer, GUI, physics and level JSON were not modified, and the image was not composited, annotated or edited.

**原渲染器无头画面。** SDL 视频和音频采用 `dummy`，不是原生桌面截图或人工玩法验收。源码从公开版本导出到隔离目录，原渲染器、GUI、物理及关卡 JSON 均未改动，画面没有拼接、标注或图像编辑。

The capture reused the existing project Python 3.11 environment. Runtime module: pygame-ce 2.5.1; installed distributions also include pygame 2.6.0, pygame_gui 0.6.12, pymunk 6.8.1, NumPy 2.0.1 and Matplotlib 3.9.2. These are recorded versions, not a claim that all possible combinations work. No existing environment dependencies were changed.

本次复用项目原有 Python 3.11 环境，实际加载 pygame-ce 2.5.1；同时记录 pygame 2.6.0、pygame_gui 0.6.12、pymunk 6.8.1、NumPy 2.0.1、Matplotlib 3.9.2 的发行包信息。版本记录不代表所有组合均兼容，原环境依赖没有改动。

The original prototype has overlapping debug labels in this scene and emits a horizontal-slider “value not in range” warning. Both are retained rather than concealed. They did not prevent this finite render from completing.

原型场景存在调试文字重叠，并发出滑杆“value not in range”警告，均保留，没有隐藏；有限帧渲染仍正常结束。

## Reproduce / 最短复现

Use the public revision above with its existing declared dependencies, then run the included finite harness from the repository root:

使用上方公开版本及其原声明依赖，在仓库根运行附带的有限帧辅助脚本：

```bash
python docs/showcase/render-headless.py --frames 60 --output sandbox-frame.png
```

[render-headless.py](render-headless.py) only imports and calls the original scene, physics and UI drawing methods. It saves the complete surface after 60 frames and closes Pygame. Fonts and old UI behavior may vary with environment; the recorded hash identifies this exact capture.

脚本仅导入并调用原场景、物理与 UI 绘制方法，60 帧后保存完整 surface 并退出 Pygame。字体及旧 UI 行为可能随环境变化；哈希用于识别本张原图。
