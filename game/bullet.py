import pygame,constants


class Bullet(pygame.sprite.Sprite):
    """ 子弹类"""
    # 子弹的状态
    active = True

    def __init__(self, screen, plane, speed=None):
        super().__init__()
        self.screen = screen
        self.plane = plane
        self.speed = speed or 30
        # 加载子弹的图片
        self.image = pygame.image.load(constants.BULLET_IMG)
        # 改变子弹的位置
        self.rect = self.image.get_rect()
        self.rect.centerx = plane.rect.centerx
        self.rect.top = plane.rect.top
        # 子弹的音效
        self.shoot_sound = pygame.mixer.Sound(constants.BULLET_SHOOT_SOUND)
        self.shoot_sound.set_volume(0.3)
        self.shoot_sound.play()

    def update(self, war):
        """" 更新子弹的位置"""
        self.rect.top -= self.speed
        # 超出屏幕范围
        if self.rect.top < 0:
            self.remove(self.plane.bullets)
        # 绘制子弹
        self.screen.blit(self.image, self.rect)
        # 碰撞检测,检测是否碰撞到了敌机
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        for i in rest:
            # 1 子弹消失
            self.kill()
            # 2 飞机爆炸,坠毁
            i.broken_down()
            # 3 统计游戏结果
            war.rest.score += constants.SCORE_SHOOT_SMALL
            # 4 保存历史记录
            war.rest.set_history()

