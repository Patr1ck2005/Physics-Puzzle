import pygame
import pymunk


# HUD类定义
class HUD:
    def __init__(self, screen, initial_score=0, initial_lives=3):
        self.selecting = None
        self.screen = screen
        self.score = initial_score
        self.lives = initial_lives
        self.font = pygame.font.Font(None, 36)
        self.score_color = (255, 255, 255)
        self.lives_color = (255, 0, 0)

        # 设置按钮
        self.settings_button = pygame.Rect(700, 10, 80, 30)

        # 物品栏
        self.inventory = [
            {"name": "Box", "type": "object", "rect": pygame.Rect(10, 10, 60, 60)},
            {"name": "Force", "type": "abstract", "rect": pygame.Rect(80, 10, 60, 60)},
        ]

    def update_score(self, points):
        self.score += points

    def update_lives(self, change):
        self.lives += change

    def render(self):
        # 渲染得分
        score_text = self.font.render(f'Score: {self.score}', True, self.score_color)
        score_rect = score_text.get_rect(topleft=(10, 10))
        self.screen.blit(score_text, score_rect)

        # 渲染生命值
        lives_text = self.font.render(f'Lives: {self.lives}', True, self.lives_color)
        lives_rect = lives_text.get_rect(topleft=(10, 50))
        self.screen.blit(lives_text, lives_rect)

        # 绘制物品栏
        for item in self.inventory:
            pygame.draw.rect(self.screen, (0, 128, 0), item["rect"])

        # 绘制设置按钮
        pygame.draw.rect(self.screen, (0, 0, 128), self.settings_button)

    def reset(self):
        self.score = 0
        self.lives = 3

    def drag_interaction(self):
        self.selecting = None
        # 获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        for item in self.inventory:
            if item["rect"].collidepoint(mouse_pos):
                self.selecting = item

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.selecting, event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.selecting:
                    if self.selecting["type"] == "object":
                        # 将实体道具拖入世界中
                        return self.selecting, event.pos
                    elif self.selecting["type"] == "abstract":
                        # 拖动“力”时，设定施力点
                        return self.selecting, event.pos
        return None, None


# 示例用法
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    hud = HUD(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 示例：每帧增加1分
        hud.update_score(1)

        # 清屏
        screen.fill((0, 0, 0))

        # 渲染HUD
        hud.render()

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        clock.tick(60)

    pygame.quit()
