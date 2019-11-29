import sys, pygame, constants
from plane import OurPlane, SmallEnemyPlane
from result import PlayResult


class PlaneWar(object):
    """飞机事件类"""
    # 游戏状态
    READY = 0      # 游戏准备中
    PLAYING = 1    # 游戏中
    OVER = 2       # 游戏结束
    status = READY

    # 我方飞机
    our_plane = None

    # 动画播放的帧数
    frame = 0

    # 一架飞机可以属于多个精灵组
    small_enemies = pygame.sprite.Group()   # 小型敌机
    enemies = pygame.sprite.Group()         # 所有敌机

    # 游戏结果
    rest = PlayResult()

    def __init__(self):
        """加载游戏对象"""
        # 初始化游戏
        pygame.init()
        # 屏幕宽度、高度
        self.width, self.height = 480, 852
        # 屏幕对象
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 设置窗口标题
        pygame.display.set_caption('飞机大战')

        # 加载背景图片
        self.bg = pygame.image.load(constants.BG_IMG)
        # 加载结束背景图片
        self.bg_over = pygame.image.load(constants.BG_IMG_OVER)
        # 加载游戏标题图片
        self.img_game_title = pygame.image.load(constants.IMG_GAME_TITLE)
        self.img_game_title_rect = self.img_game_title.get_rect()
        # 调整标题的位置
        t_width, t_height = self.img_game_title.get_size()
        # 调整标题位置的topleft属性
        self.img_game_title_rect.topleft = (int((self.width - t_width) / 2), int(self.height / 2 - t_height))

        # 加载开始按钮
        self.btn_start = pygame.image.load(constants.IMG_GAME_START_BTN)
        self.btn_start_rect = self.btn_start.get_rect()
        # 调整开始按钮的位置
        btn_width, btn_height = self.btn_start.get_size()
        self.btn_start_rect.topleft = (int((self.width - btn_width) / 2), int(self.height / 2 + btn_height))

        # 加载游戏文字字体
        self.score_font = pygame.font.Font(constants.TEXT_FONT, 32)

        # 加载游戏背景音乐
        pygame.mixer.music.load(constants.BG_MUSIC)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        # 我方飞机对象
        self.our_plane = OurPlane(self.screen, speed=3)

        # 加载游戏动画帧
        self.clock = pygame.time.Clock()

        # 上次按的键盘上的某一个键,用于控制飞机
        self.key_down = None

    def bind_event(self):
        """添加绑定事件"""
        # 监听事件
        for event in pygame.event.get():
            # 退出事件
            if event.type == pygame.QUIT:
                sys.exit()
            # 鼠标事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 游戏正在准备中,点击鼠标才能进入游戏
                if self.status == self.READY:
                    self.status = self.PLAYING
                # 游戏中,点击鼠标发射子弹
                elif self.status == self.PLAYING:
                    self.our_plane.shoot()
                # 游戏结束后,点击鼠标重新开始
                elif self.status == self.OVER:
                    self.status = self.READY
                    self.rest.score = 0
                    # 游戏开始,随机添加6架战机
                    self.add_small_enemies(6)
            # 键盘事件
            elif event.type == pygame.KEYDOWN:
                # 设置游戏键记忆功能
                self.key_down = event.key
                # 游戏正在进行中,我方飞机需要键盘控制方向
                if self.status == self.PLAYING:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        # 我方飞机向上移动
                        self.our_plane.move_up()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        # 我方飞机向下移动
                        self.our_plane.move_down()
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        # 我方飞机向左移动
                        self.our_plane.move_left()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        # 我方飞机向右移动
                        self.our_plane.move_right()
                    elif event.key == pygame.K_SPACE:
                        # 我方飞机发射子弹
                        self.our_plane.shoot()

    def add_small_enemies(self, num):
        """ 添加小型敌机 """
        # 随机产生num架小型敌机
        for i in range(num):
            plane = SmallEnemyPlane(self.screen, 4)
            plane.add(self.small_enemies, self.enemies)

    def run_game(self):
        """游戏主循环部分"""
        while True:
            # 1 设定帧速率
            self.clock.tick(60)
            self.frame += 1
            # 2 绑定事件
            self.bind_event()
            # 3 更新游戏状态
            # 游戏在准备状态下
            if self.status == self.READY:
                # 绘制背景图片
                self.screen.blit(self.bg,self.bg.get_rect())
                # 绘制标题
                self.screen.blit(self.img_game_title,self.img_game_title_rect)
                # 绘制开始按钮
                self.screen.blit(self.btn_start,self.btn_start_rect)
            # 游戏在玩的状态下
            elif self.status == self.PLAYING:
                # 绘制背景图片
                self.screen.blit(self.bg, self.bg.get_rect())
                # 绘制我方飞机
                self.our_plane.update(self)
                # 绘制子弹
                self.our_plane.bullets.update(self)
                # 绘制敌方飞机
                self.small_enemies.update()
                # 得到得分对象
                score_text = self.score_font.render('得分:{0}'.format(self.rest.score), False, constants.TEXT_SOCRE_COLOR)
                # 绘制得分
                self.screen.blit(score_text, score_text.get_rect())
            # 游戏在结束的状态下
            elif self.status == self.OVER:
                # 绘制背景图片
                self.screen.blit(self.bg_over, self.bg.get_rect())
                # 分数显示
                # 1 最终成绩
                # 最终成绩的位置
                score_text_rect = score_text.get_rect()
                text_w, text_h = score_text.get_size()
                score_text_rect.topleft = (int((self.width - text_w) / 2), int(self.height / 2))
                # 得到最终成绩对象
                score_text = self.score_font.render('{0}'.format(self.rest.score), False, constants.TEXT_SOCRE_COLOR)
                # 绘制最终成绩
                self.screen.blit(score_text, score_text_rect)
                # 2 最高分
                # 得到最高分对象
                score_history = self.score_font.render('{0}'.format(self.rest.get_max_score()), False, constants.TEXT_SOCRE_COLOR)
                # 绘制最高分
                self.screen.blit(score_history, (150, 40))

            # 游戏刷新
            pygame.display.flip()