import pygame


# HUD类定义
class HUD:
    def __init__(self, screen, initial_score=0, initial_lives=3):
        self.screen = screen
        self.score = initial_score
        self.lives = initial_lives
        self.font = pygame.font.Font(None, 36)
        self.score_color = (255, 255, 255)
        self.lives_color = (255, 0, 0)

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

    def reset(self):
        self.score = 0
        self.lives = 3


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
