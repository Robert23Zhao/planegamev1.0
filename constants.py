import os,pygame


# 项目的根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件的目录
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# 开始背景图片
BG_IMG = os.path.join(ASSETS_DIR, 'images/background.png')
# 游戏背景音乐
BG_MUSIC = os.path.join(ASSETS_DIR, 'sounds/game_bg_music.mp3')

# 结束背景图片
BG_IMG_OVER = os.path.join(ASSETS_DIR, 'images/game_over.png')
# 结束音乐
BG_SOUND_OVER = os.path.join(ASSETS_DIR, 'sounds/game_over.wav')

# 游戏标题的图片
IMG_GAME_TITLE = os.path.join(ASSETS_DIR, 'images/game_title.png')
# 游戏开始按钮的图片
IMG_GAME_START_BTN = os.path.join(ASSETS_DIR, 'images/game_start.png')

# 游戏分数颜色
TEXT_SOCRE_COLOR = pygame.Color(255, 255, 0)
# 击中小型飞机添加10分
SCORE_SHOOT_SMALL = 10
# 游戏结果文件存储的位置
PLAY_RESULT_STORE_FILE = os.path.join(BASE_DIR, 'store/rest.txt')

# 我方飞机的图片
OUR_PLANE_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/hero1.png'),
    os.path.join(ASSETS_DIR, 'images/hero2.png')
]
# 我方飞机坠毁的图片
OUR_DESTORY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/hero_broken_n1.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n2.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n3.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n4.png')
]

# 敌方小型飞机的图片
SMALL_ENEMY_IMG_LIST = [os.path.join(ASSETS_DIR, 'images/enemy1.png')]
# 敌方小型飞机坠毁的图片
SMALL_ENEMY_DESTORY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy1_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down4.png')
]
# 敌方小型飞机坠毁的音效
SMALL_ENEMY_PLANE_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy1_down.wav')

# 子弹的图片
BULLET_IMG = os.path.join(ASSETS_DIR, 'images/bullet1.png')
# 子弹的音效
BULLET_SHOOT_SOUND = os.path.join(ASSETS_DIR, 'sounds/bullet.wav')

# 字体
TEXT_FONT = os.path.join(ASSETS_DIR, 'simhei.ttf')