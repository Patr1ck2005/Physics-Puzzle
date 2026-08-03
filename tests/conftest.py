"""
Pytest 配置文件：初始化 pygame 显示环境，避免无头测试报错。
"""
import os
import sys

# 将项目根目录加入 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

# 使用虚拟显示驱动，避免在没有显示器的环境下崩溃
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
pygame.init()
pygame.display.set_mode((1, 1))
