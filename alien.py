import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, game):
        """初始化外星人及其初始位置"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.game_setting
        # 加载外星人图片并且设置其rect属性
        self.image = pygame.image.load('image/alien.bmp')
        self.rect = self.image.get_rect()

        # 最开始外星人都在屏幕左上角的位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 精确设置外星人的坐标
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
