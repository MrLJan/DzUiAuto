# -*- encoding=utf8 -*-
import configparser

from Utils.OtherTools import OT


class LoadConfig:
    @staticmethod
    def init_config():
        LoadConfig.writeconf("路径", "模拟器路径", 'D:/LDPlayer/LDPlayer9/ldconsole.exe')
        LoadConfig.writeconf("路径", "绑定模式", '模式三')
        # "全局配置", "启动模拟器序号"
        LoadConfig.writeconf("野图配置", "短按窗口", '')
        LoadConfig.writeconf("野图配置", "组队密码", '5475')
        LoadConfig.writeconf("全局配置", "扫地模式", '0')
        LoadConfig.writeconf("全局配置", "HP等级", '5')
        LoadConfig.writeconf("全局配置", "MP等级", '5')
        LoadConfig.writeconf("全局配置", "自定义一", '自动任务,自动每日')
        LoadConfig.writeconf("全局配置", "自定义二", '自动每日,死亡战场')
        LoadConfig.writeconf("全局配置", "无蓝窗口", '12,22,2,9')
        LoadConfig.writeconf("全局配置", "人少退组", '0')
        LoadConfig.writeconf("全局配置", "自动切换角色", '0')
        LoadConfig.writeconf("全局配置", "任务停止等级", '99')
        LoadConfig.writeconf("全局配置", "离线时长", '50')
        LoadConfig.writeconf("全局配置", "随机休息", '1')
        LoadConfig.writeconf("全局配置", "在线休息", '1')
        LoadConfig.writeconf("全局配置", "离线休息", '0')
        LoadConfig.writeconf("全局配置", "挂机卡时长", '20')
        LoadConfig.writeconf("全局配置", "随机使用石头", '0')
        LoadConfig.writeconf("全局配置", "强化等级", '14')
        LoadConfig.writeconf("全局配置", "混皮卡啾", '0')
        LoadConfig.writeconf("全局配置", "混女皇", '0')
        LoadConfig.writeconf("全局配置", "任务结束关闭游戏", '0')
        LoadConfig.writeconf("全局配置", "公会内容", '1')
        LoadConfig.writeconf("全局配置", "混王图", '1')
        LoadConfig.writeconf("全局配置", "混沌炎魔",'0')
        LoadConfig.writeconf("全局配置", "定时任务", '1')
        LoadConfig.writeconf("全局配置", "固定每日时间", str('21:19'))
        LoadConfig.writeconf("全局配置", "检查产出", '60')
        LoadConfig.writeconf("全局配置", "职业类型", '1')
        LoadConfig.writeconf("全局配置", "混合自动按键", '1')
        LoadConfig.writeconf("全局配置", "武陵", '1')
        LoadConfig.writeconf("全局配置", "金字塔", '1')
        LoadConfig.writeconf("全局配置", "每日地城", '1')
        LoadConfig.writeconf("全局配置", "菁英地城", '1')
        LoadConfig.writeconf("全局配置", "星光塔", '0')
        LoadConfig.writeconf("全局配置", "进化系统", '0')
        LoadConfig.writeconf("全局配置", "次元入侵", '0')
        LoadConfig.writeconf("全局配置", "怪物狩猎团", '1')
        LoadConfig.writeconf("全局配置", "汤宝宝", '1')
        LoadConfig.writeconf("全局配置", "怪物公园", '1')
        LoadConfig.writeconf("全局配置", "迷你地城", '0')
        LoadConfig.writeconf("全局配置", "强化优惠卷", '1')
        LoadConfig.writeconf("全局配置", "幸运卷轴", '1')
        LoadConfig.writeconf("全局配置", "盾牌卷轴", '1')
        LoadConfig.writeconf("全局配置", "保护卷轴", '1')
        LoadConfig.writeconf("全局配置", "离线使用挂机卡", '0')
        LoadConfig.writeconf("野图配置", "1队成员", '0,6,12')
        LoadConfig.writeconf("野图配置", "2队成员", '1,7,13')
        LoadConfig.writeconf("野图配置", "3队成员", '2,8,14')
        LoadConfig.writeconf("野图配置", "4队成员", '3,9,15')
        LoadConfig.writeconf("野图配置", "5队成员", '4,10,16')
        LoadConfig.writeconf("野图配置", "6队成员", '5,11,17')
        LoadConfig.writeconf("野图配置", "1队频道", '28')
        LoadConfig.writeconf("野图配置", "2队频道", '32')
        LoadConfig.writeconf("野图配置", "3队频道", '45')
        LoadConfig.writeconf("野图配置", "4队频道", '35')
        LoadConfig.writeconf("野图配置", "5队频道", '39')
        LoadConfig.writeconf("野图配置", "6队频道", '42')

    @staticmethod
    def readconf(ini_name='TestConfig'):
        try:
            config = configparser.ConfigParser()
            # config.read(DTools.abspath(f"/res/{ini_name}.ini"), encoding="gbk")
            config.read(f"c:/{ini_name}.ini", encoding="gbk")
            return config
        except Exception as e:
            print(f'获取配置异常{e}')

    @staticmethod
    def writeconf(section, key, value, ini_name='TestConfig'):
        try:
            cf = LoadConfig.readconf(ini_name=ini_name)
            cf.set(section, key, value)
            f = open(f"c:/{ini_name}.ini", "w+", encoding="gbk")
            # f = open(DTools.abspath(f"/res/{ini_name}.ini"), "w+", encoding="gbk")
            cf.write(f)
            f.close()
        except Exception:
            LoadConfig.addsection(section, key, value, ini_name=ini_name)

    @staticmethod
    def addsection(section, key, value, ini_name='TestConfig'):
        cf = LoadConfig.readconf(ini_name=ini_name)
        if not cf.has_section(section):
            cf.add_section(section)
        cf.set(section, key, value)
        f = open(f"c:/{ini_name}.ini", "w+", encoding="gbk")
        # f = open(DTools.abspath(f"/res/{ini_name}.ini"), "w+", encoding="gbk")
        cf.write(f)
        f.close()

    @staticmethod
    def getconf(section, key, ini_name='TestConfig'):
        try:
            cf = LoadConfig.readconf(ini_name=ini_name)
            value = cf.get(section, key)
            if key == '金币' and value == '':
                value = '0'
            return value
        except Exception:
            if key in ['最近任务', '自定义一', '自定义二']:
                LoadConfig.writeconf(section, key, '', ini_name=ini_name)
                return ''
            if key == '金币':
                LoadConfig.writeconf(section, key, '0', ini_name=ini_name)
                return '0'
            else:
                LoadConfig.writeconf(section, key, '0', ini_name=ini_name)
                return '0'
