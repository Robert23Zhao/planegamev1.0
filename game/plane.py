import random, pygame, constants
from bullet import Bullet


class Plane(pygame.sprite.Sprite):
    """ 飞机基类 """

    # 飞机的图片
    plane_images = []
    # 飞机爆炸的图片
    destroy_image = []
    # 飞机坠毁的音效地址
    down_sound_src = None
    # 飞机的状态  True代表存活  False代表坠毁
    active = True
    # 飞机发射子弹需要子弹精灵组
    bullets = pygame.sprite.Group()

    # 重新父类的构造方法
    def __init__(self, screen, speed=None):
        super().__init__()
        # 主视图
        self.screen = screen
        # 加载静态资源
        # 1 飞机的图片列表
        self.img_list = []
        # 2 飞机的坠毁图片列表
        self.destroy_list = []
        # 3 飞机坠毁的音效列表
        self.down_sound = []
        # 4 加载静态资源方法
        self.load_src()
        # 飞机的飞行速度
        self.speed = speed or 10
        # 飞机的位置
        self.rect = self.img_list[0].get_rect()
        # 飞机的宽度和高度
        self.plane_w, self.plane_h = self.img_list[0].get_size()
        # 游戏主屏幕窗口宽度和高度
        self.width, self.height = self.screen.get_size()
        # 调整飞机的初始位置
        self.rect.topleft = (int((self.width - self.plane_w) / 2), int(self.height / 2))

    def load_src(self):
        """ 加载静态资源 """
        # 加载飞机图片
        for img in self.plane_images:
            self.img_list.append(pygame.image.load(img))
        # 加载飞机坠毁图片
        for img in self.destroy_image:
            self.destroy_list.append(pygame.image.load(img))
        # 加载飞机坠毁音效
        # 判断音效目录是否存在
        if self.down_sound_src:
            self.down_sound = pygame.mixer.Sound(self.down_sound_src)

    @property
    def image(self):
        """ 返回飞机第一张图片 """
        return self.img_list[0]

    def blit_me(self):
        """ 绘制飞机 """
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        """ 飞机向上移动 """
        self.rect.top -= self.speed

    def move_down(self):
        """ 飞机向下移动 """
        self.rect.top += self.speed

    def move_left(self):
        """ 飞机向左移动 """
        self.rect.left -= self.speed

    def move_right(self):
        """ 飞机向右移动 """
        self.rect.left += self.speed

    def broken_down(self):
        """ 飞机坠毁的效果 """
        # 1 播放坠毁的音效
        if self.down_sound:
            self.down_sound.play()
        # 2 播放坠毁的动画
        for img in self.destroy_list:
            self.screen.blit(img, self.rect)
        # 3 坠毁后
        self.active = False

    def shoot(self):
        """ 飞机发射子弹 """
        bullet = Bullet(self.screen, self, 15)
        self.bullets.add(bullet)


class OurPlane(Plane):
    """ 我方飞机类,继承自飞机基类 """
    # 我方飞机的图片
    plane_images = constants.OUR_PLANE_IMG_LIST
    # 我方飞机爆炸的图片
    destroy_image = constants.OUR_DESTORY_IMG_LIST
    # 我方飞机音乐坠毁的地址
    down_sound_src = None

    def update(self, war):
        """ 更新飞机的动画效果 """
        self.move(war.key_down)
        # 1 切换飞机的动画效果
        if war.frame % 5 == 0:
            self.screen.blit(self.img_list[0], self.rect)
        else:
            self.screen.blit(self.img_list[1], self.rect)
        # 2 飞机撞击的检测
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        if rest:
            # 1 游戏结束
            war.status = war.OVER
            # 2 敌方飞机清除
            war.enemies.empty()
            war.small_enemies.empty()
            # 3 我方飞机坠毁效果
            self.broken_down()

    def move(self, key):
        """ 飞机移动自动控制 """
        if key == pygame.K_w or key == pygame.K_UP:
            # 我方飞机向上移动
            self.move_up()
        elif key == pygame.K_s or key == pygame.K_DOWN:
            # 我方飞机向下移动
            self.move_down()
        elif key == pygame.K_a or key == pygame.K_LEFT:
            # 我方飞机向左移动
            self.move_left()
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            # 我方飞机向右移动
            self.move_right()

    def move_up(self):
        """ 防止我方飞机向上移动超出范围 """
        super().move_up()
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        """ 防止我方飞机向下移动超出范围 """
        super().move_down()
        if self.rect.top >= self.height - self.plane_h:
            self.rect.top = self.height - self.plane_h

    def move_left(self):
        """ 防止我方飞机向左移动超出范围 """
        super().move_left()
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        """ 防止我方飞机向右移动超出范围 """
        super().move_right()
        if self.rect.left >= self.width - self.plane_w:
            self.rect.left = self.width - self.plane_w


class SmallEnemyPlane(Plane):
    """ 敌方小型飞机类 """
    # 敌方小飞机的图片
    plane_images = constants.SMALL_ENEMY_IMG_LIST
    # 敌方小飞机爆炸的图片
    destroy_image = constants.SMALL_ENEMY_DESTORY_IMG_LIST
    # 敌方小飞机音乐坠毁的地址
    down_sound_src = constants.SMALL_ENEMY_PLANE_DOWN_SOUND

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        # 每次出现一架小型敌机时,让其随机的出现在屏幕中
        self.init_pos()

    def init_pos(self):
        """ 改变小型敌机的飞行高度 """
        self.rect.left = random.randint(0, self.width - self.plane_w)
        # 屏幕之外的随机高度
        self.rect.top = random.randint(-5 * self.plane_h, -self.plane_h)

    def update(self, *args):
        """ 更新飞机的移动 """
        super().move_down()

        # 绘制敌方小型飞机
        self.blit_me()

        # 防止敌方小型飞机超出屏幕范围
        # 采用重用的方法
        if self.rect.top >= self.height:
            self.active = False
            self.reset()

    def reset(self):
        """ 重置飞机的状态,达到复用的效果 """
        self.active = True
        # 改变飞机的位置
        self.init_pos()

    def broken_down(self):
        """ 小型敌机爆炸 """
        super().broken_down()
        self.reset()