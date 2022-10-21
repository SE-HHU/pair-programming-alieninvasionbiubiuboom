import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船发射的子弹的类"""

    def __init__(self, game):
        """在飞船的顶部创建一个子弹"""
        super().__init__()
        self.screen = game.screen
        self.setting = game.game_setting
        self.color = self.setting.bullet_color

        # 在（0,0）处建立矩形子弹，之后定位到飞船的顶部
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.setting.bullet_speed
        # 更新子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
