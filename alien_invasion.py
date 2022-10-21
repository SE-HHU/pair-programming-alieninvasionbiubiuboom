import sys
from time import sleep

import alien
import pygame
from setting import Settings
from game_stats import GameStsts
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """用于管理游戏总体的资源和操作"""

    def __init__(self):
        """用于初始化游戏以及加载游戏资源"""
        pygame.init()  # 用于初始化背景
        self.game_setting = Settings()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 创建全屏显示窗口
        self.screen = pygame.display.set_mode((self.game_setting.screen_width, self.game_setting.screen_hegiht))#窗口化显示游戏
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("飞船大战外星人")

        # 创建存贮游戏信息的实例

        # 创建一个存储游戏统计信息的实例
        self.stats = GameStsts(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._creat_fleet()

        # 创建play按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.ships_left == 0:
                self.stats.game_active = False

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.game_setting.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并且新建一群外星人
            self.bullets.empty()
            self._creat_fleet()
            self.game_setting.increase_speed()

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕低端
        self._check_aliens_bottom()

    def _update_screen(self):
        """更新屏幕的图像并且切换到新屏幕"""
        self.screen.fill(self.game_setting.bg_color)  # 重新绘制屏幕R
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # 让每一次绘制的屏幕都显示出来

    def _check_events(self):
        """用于检测按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 若点击右上角×号就退出游戏
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家点击play时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.play_button.rect.collidepoint(mouse_pos):
            # 重置游戏设置
            self.game_setting.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._creat_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """按下按键的检测"""
        if event.key == pygame.K_ESCAPE:  # 按ESE退出游戏
            sys.exit()
        elif event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """松开按键的检测"""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.game_setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _creat_fleet(self):
        """创建外星人群组"""
        alien = Alien(self)

        # 创建一个外星人并且计算一行能容纳的外星人数量
        # 每个外星人间距为一个外星人的宽度
        alien_width, alien_height = alien.rect.size
        available_space_x = self.game_setting.screen_width - 2 * alien_width
        num_alien_x = available_space_x // (alien_width * 2)

        # 计算屏幕能容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = self.game_setting.screen_hegiht - 3 * alien_height - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # 创建一群外星人
        for row_num in range(number_rows):
            for alien_number in range(num_alien_x):
                self._creat_alien(alien_number, row_num)

    def _creat_alien(self, alien_num, row_num):
        """创建一个外星人并且放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_num
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.game_setting.fleet_drop_speed
        self.game_setting.fleet_direction *= -1

    def _ship_hit(self):
        """相应飞船被外星人撞倒"""
        if self.stats.ships_left > 0:
            # 将ship_left 减一
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕低端中央
            self._creat_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船呗撞倒一样处理
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建游戏示例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
