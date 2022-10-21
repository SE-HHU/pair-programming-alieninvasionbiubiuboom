import pygame
from setting import Settings
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船属性及行为的类"""

    def __init__(self, game):
        """初始化飞船并设置其位置"""
        super().__init__()
        self.screen = game.screen
        self.setting = game.game_setting
        self.screen_rect = game.screen.get_rect()

        # 加载飞船图像并且获取以飞船图像为中心的外接矩形
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()

        # 每个新的飞船都初始化在屏幕的中央底部
        self.rect.midbottom = self.screen_rect.midbottom

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += 1
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= 1

    def blitme(self):
        """在指定的位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕底端中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)