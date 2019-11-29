from war import PlaneWar


def main():
    """游戏入口,main方法"""
    # 实例化wars事件
    war = PlaneWar()
    # 添加小型敌机
    war.add_small_enemies(6)
    # 运行游戏
    war.run_game()


if __name__ == '__main__':
    main()