# -*- coding:utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG, BatEnumG, MulColorEnumG, WorldEnumG
from Utils.ExceptionTools import NotInGameErr, FuHuoRoleErr
from Utils.LoadConfig import LoadConfig
from Utils.MnqTools import MnqTools
from Utils.OpencvG import ColorCvTools, DmImgTools


class BasePageG(ColorCvTools, DmImgTools):
    def __init__(self):
        super(ColorCvTools, self).__init__()
        self.dev = None
        self.sn = None
        self.mnq_name = None

    def snap(self):
        return self.dev.snapshot()

    @staticmethod
    def time_sleep(sleep_time):
        time.sleep(sleep_time)

    def start_game(self, wait_time=10):
        """启动游戏"""
        self.sn.log_tab.emit(self.mnq_name, r"启动游戏")
        MnqTools().start_mnq_app(self.mnq_name, GlobalEnumG.GamePackgeName)
        # self.dev.app_start(GlobalEnumG.GamePackgeName,use_monkey=True)
        time.sleep(wait_time)

    def back(self, wait_time=GlobalEnumG.BackWaitTime):
        self.sn.log_tab.emit(self.mnq_name, r"返回back")
        self.key_event('esc')
        time.sleep(wait_time)

    def stop_game(self):
        """关闭游戏"""
        self.sn.log_tab.emit(self.mnq_name, r"关闭游戏")
        MnqTools().stop_mnq_app(self.mnq_name, GlobalEnumG.GamePackgeName)

    def close_other_app(self):
        """关闭除游戏客户端外其他应用"""
        app_list = self.dev.app_list_running()
        for al in app_list:
            if al != GlobalEnumG.GamePackgeName:
                self.dev.app_stop(al)

    # @staticmethod
    def check_mulpic(self, pic_list, clicked=True):
        """检查多个图，找到其中1个则返回True"""
        for pic in pic_list:
            if self.pic_find(pic, clicked):
                return True
        return False

    def check_allpic(self, pic_list, clicked=True):
        """检查多个图，未找到其中1个则返回Flase"""
        for pic in pic_list:
            if not self.pic_find(pic, clicked):
                return False
        return True

    def check_close(self):
        w_time = time.time()
        while True:
            if time.time() - w_time > GlobalEnumG.SelectCtrTimeOut:
                self.stop_game()
                w_time = time.time()
            elif self.pic_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            elif self.cmp_rgb(RgbEnumG.EXIT_FOU, True):
                return True
            elif self.word_find(WorldEnumG.SKIP, True):
                pass
            elif self.find_color(MulColorEnumG.IGAME):
                return True
            elif self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                if self.pic_find(ImgEnumG.CZ_FUHUO):
                    raise FuHuoRoleErr
            elif self.pic_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
            elif self.pic_find(ImgEnumG.LOGIN_TIPS, False):
                raise NotInGameErr
            elif self.mul_color(MulColorEnumG.COIN_ENUM, True):
                pass
            elif self.mul_color(MulColorEnumG.GAME_START, True):
                pass
            elif self.net_err():
                self.time_sleep(5)
                pass
            else:
                self.back()

    def check_err(self):
        if self.pic_find(ImgEnumG.GAME_ICON, False):
            raise NotInGameErr
        if self.cmp_rgb(RgbEnumG.FUHUO_BTN):
            if self.pic_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
        if self.find_color(MulColorEnumG.IGAME):
            return True
        if self.mul_color(MulColorEnumG.GAME_START, True):
            return True
        self.cmp_rgb(RgbEnumG.BAT_JG, True)
        self.back()
        return False

    def close_window(self):
        for i in range(10):
            if self.pic_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            if self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                if self.pic_find(ImgEnumG.CZ_FUHUO):
                    raise FuHuoRoleErr
            if self.find_color(MulColorEnumG.IGAME):
                return True
            self.pic_find(ImgEnumG.UI_CLOSE)
            self.mul_color(MulColorEnumG.TASK_CLOSE, True)
            self.pic_find(ImgEnumG.QD_1)
            self.pic_find(ImgEnumG.UI_QR)
            self.pic_find(ImgEnumG.LOGIN_TIPS)
            if i > 5:
                while not self.find_color(MulColorEnumG.IGAME):
                    if self.word_find(WorldEnumG.TASK_ARROW, True, touch_wait=0):
                        pass
                    self.pic_find(ImgEnumG.TASK_OVER, touch_wait=0)
                    self.pic_find(ImgEnumG.TASK_START, touch_wait=0)
                    self.check_err()
        return False

    def check_now_app(self):
        now_app = MnqTools().check_now_runapp(self.mnq_name)
        if now_app in ['com.nexon.maplem.global', 'com.google.android.gms']:
            # self.sn.log_tab.emit(self.mnq_name, r"当前运行正常")
            pass
        else:
            MnqTools().stop_mnq_app(self.mnq_name, now_app)
            MnqTools().start_mnq_app(self.mnq_name, 'com.nexon.maplem.global')
        return True

    def check_is_stop(self):
        self.sn.log_tab.emit(self.mnq_name, r"检查界面是否卡住")
        res = self.dev.IsDisplayDead(322, 611, 454, 694, 5)
        res2 = self.dev.IsDisplayDead(384, 17, 608, 105, 5)
        if res == 1 and res2 == 1:
            return True
        return False

    def skip_fever_buff(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                self.touch((857, 645))
            elif self.cmp_rgb(RgbEnumG.FEVER_BUFF):
                return True
            # elif self.ocr_find(ImgEnumG.SKIP_OCR, True):
            #     pass
            else:
                self.check_close()
        return False

    def skip_new(self):
        s_time = time.time()
        _C_TIMES = 0
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.cmp_rgb(RgbEnumG.SKIP_NEW) or self.cmp_rgb(RgbEnumG.SKIP_NEW1):
                self.sn.log_tab.emit(self.mnq_name, r"关闭引导")
                self.touch((328, 369), touch_wait=0)
                self.touch((469, 369), touch_wait=0)
                self.touch((456, 369), touch_wait=0)
                self.touch((625, 369), touch_wait=0)
                self.touch((773, 369), touch_wait=0)
                self.touch((655, 369), touch_wait=0)
                self.touch((788, 369), touch_wait=0)
                if not self.cmp_rgb(RgbEnumG.SKIP_BTN, True):
                    if _C_TIMES > 10:
                        self.cmp_rgb(RgbEnumG.SKIP_NEW, True)
                    else:
                        _C_TIMES += 1
                else:
                    _C_TIMES = 0
            elif self.cmp_rgb(RgbEnumG.SKIP_BTN, True):
                if _C_TIMES > 10:
                    self.cmp_rgb(RgbEnumG.SKIP_NEW, True)
                else:
                    _C_TIMES += 1
            elif self.find_color(MulColorEnumG.IGAME):
                if not self.pic_find(ImgEnumG.SKIP_NEW):
                    return True
            else:
                self.check_close()
        return False

    def get_mapdata(self, **kwargs):
        star = kwargs['角色信息']['星力']
        XT_MAP = {
            147: '崎岖的峡谷',
            144: '灰烬之风高原',
            142: '武器库星图',
            136: '变形的森林',
            130: '偏僻泥沼',
            120: '忘却之路4',
            115: '时间漩涡',
            113: '机械室',
            110: '天空露台2',
            105: '奥斯塔入口',
            90: '爱奥斯塔入口',
            80: '龙蛋',
            95: '冰冷死亡战场',
            45: '西边森林',
            40: '研究所102',
        }
        for _s in XT_MAP.keys():
            if int(star) >= _s:
                kwargs['地图名'] = XT_MAP[_s]
                return self.change_mapdata('3', XT_MAP[_s], **kwargs)

    def change_mapdata(self, xt_yt, map_name, **kwargs):
        kwargs['任务id'] = xt_yt
        auto_choose = kwargs['托管模式']
        kwargs['地图名'] = map_name
        kwargs['战斗数据']['地图数据'] = BatEnumG.MAP_DATA[xt_yt][map_name]
        kwargs['战斗数据']['地图识别'] = BatEnumG.MAP_OCR[map_name]
        self.sn.table_value.emit(self.mnq_name, 2, map_name)
        if not auto_choose:
            LoadConfig.writeconf(self.mnq_name, '最近任务', map_name, ini_name=self.mnq_name)
        return kwargs

    def check_level_star(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut / 10:
            if self.find_color(MulColorEnumG.IGAME):
                _level = self.check_num(4)
                self.sn.table_value.emit(self.mnq_name, 3, f"{_level}")
                LoadConfig.writeconf(self.mnq_name, '等级', str(_level), ini_name=self.mnq_name)
                self.sn.log_tab.emit(self.mnq_name, f"等级:{_level}")
                return True
            else:
                self.check_close()

    def change_role_index(self, **kwargs):
        s_time = time.time()
        _C_ROLE = False  # 切换角色
        select_queue = kwargs['状态队列']['选择器']
        exec_queue = kwargs['状态队列']['执行器']
        self.sn.log_tab.emit(self.mnq_name, r"切换角色")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.word_find(WorldEnumG.SET_BTN):  # 菜单界面
                if not self.word_find(WorldEnumG.C_ROLE, True):
                    self.back()
            elif self.mul_color(MulColorEnumG.C_ROLE):
                self.cmp_rgb(RgbEnumG.BACK_ROLE, True, touch_wait=5)
            elif self.pic_find(ImgEnumG.CREAT_ROLE, False):
                if _C_ROLE:
                    if self.mul_color(MulColorEnumG.GAME_START, True):
                        select_queue.task_over('ChangeRole')
                        return True
                else:
                    now_index = self.check_role_now_index()
                    self.sn.log_tab.emit(self.mnq_name, f"当前{now_index}号角色")
                    self.choose_role_index(now_index + 1)
                    change_index = self.check_role_now_index()
                    if now_index == change_index:
                        self.sn.log_tab.emit(self.mnq_name, f"已经是最后1个角色,回到1号角色")
                        self.choose_role_index(1)  # 角色位置归1
                        self.mul_color(MulColorEnumG.GAME_START, True)
                        select_queue.task_over('ChangeRole')
                        select_queue.clear()
                        exec_queue.clear()
                        exec_queue.put_queue('Sleep')
                        return -1
                    else:
                        self.sn.log_tab.emit(self.mnq_name, f"选择{change_index}号角色")
                        _C_ROLE = True
            else:
                if time.time() - s_time > 60:
                    self.check_close()
                    s_time = time.time()
                self.time_sleep(2)

    def choose_role_index(self, role_index):
        role_pos = {
            1: (185, 293),
            2: (385, 293),
            3: (585, 293),
            4: (85, 583),
            5: (285, 583),
            6: (485, 583),
            7: (685, 583),
            8: (685, 583),
        }
        return self.touch(role_pos[role_index], touch_wait=2)

    def check_role_now_index(self):
        """检查当前角色序号"""
        role_index = {
            '185': 1,
            '385': 2,
            '585': 3,
            '85': 4,
            '285': 5,
            '485': 6,
            '685': 7,
        }
        role_res = self.dev.FindColorE(46, 288, 852, 643, 'ffd81d-000000', 1, 0)
        role_res = role_res.split('|')
        if role_res[0] != '-1':
            for _index in role_index.keys():
                if role_res[0] == _index:
                    return role_index[role_res[0]]
        return 0
