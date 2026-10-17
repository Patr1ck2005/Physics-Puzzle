"""Save a finite frame from the original PhyGame renderer using SDL dummy.

Run this helper with the repository's existing dependencies, from any directory.
It creates no native desktop window and does not alter game/UI source code.
"""
from pathlib import Path
import argparse
import os
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--frames', type=int, default=60)
args = parser.parse_args()
if not 1 <= args.frames <= 600:
    parser.error('--frames must be between 1 and 600')
output = args.output.resolve()
repo = Path(__file__).resolve().parents[2]
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.chdir(repo)
sys.path.insert(0, str(repo))

import pygame
from menus.game_scene import GameScene
from settings import WINDOW_SIZE

pygame.init()
try:
    screen = pygame.display.set_mode(WINDOW_SIZE)
    scene = GameScene()
    scene.load_level('sand_box')
    for _ in range(args.frames):
        for event in pygame.event.get():
            scene.manager.process_events(event)
            scene.handle_event(event)
        scene.update()
        scene.manager.update(1 / 60)
        screen.fill((0, 0, 0))
        scene.draw(screen)
        scene.manager.draw_ui(screen)
        pygame.display.flip()
    output.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(screen, str(output))
    print(f'Saved complete {screen.get_width()}x{screen.get_height()} surface to {output}')
finally:
    pygame.quit()
