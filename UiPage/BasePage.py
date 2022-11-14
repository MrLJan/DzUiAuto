# -*- coding:utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG, BatEnumG
from Utils.ExceptionTools import NotInGameErr, FuHuoRoleErr
from Utils.LoadConfig import LoadConfig
from Utils.OpencvG import OpenCvTools, AirImgTools


class BasePageG(OpenCvTools, AirImgTools):
    def __init__(self):
        super(OpenCvTools, self).__init__()
        self.dev = None
        self.serialno = None
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
        self.dev.app_start(GlobalEnumG.GamePackgeName,use_monkey=True)
        # self.dev.start_app(GlobalEnumG.GamePackgeName)
        time.sleep(wait_time)

    def key_event(self, key, wait_time=2):
        self.dev.keyevent(key)
        time.sleep(wait_time)

    def back(self, wait_time=GlobalEnumG.BackWaitTime):
        self.sn.log_tab.emit(self.mnq_name, r"返回back")
        self.dev.keyevent('back')
        time.sleep(wait_time)

    def stop_game(self):
        """关闭游戏"""
        self.sn.log_tab.emit(self.mnq_name, r"关闭游戏")
        self.dev.app_stop(GlobalEnumG.GamePackgeName)
        # self.dev.stop_app(GlobalEnumG.GamePackgeName)

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
            if self.air_loop_find(pic, clicked):
                return True
        return False

    def check_allpic(self, pic_list, clicked=True):
        """检查多个图，未找到其中1个则返回Flase"""
        for pic in pic_list:
            if not self.crop_image_find(pic, clicked):
                return False
        return True

    def check_close(self):
        w_time = time.time()
        while True:
            if time.time() - w_time > GlobalEnumG.SelectCtrTimeOut:
                self.stop_game()
                w_time = time.time()
            elif self.crop_image_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            elif self.get_rgb(RgbEnumG.EXIT_FOU, True):
                return True
            # elif self.get_rgb(RgbEnumG.EXIT_FOU, True, touch_wait=GlobalEnumG.ExitBtnTime) or self.get_rgb(
            #         RgbEnumG.CLOSE_GAME, True, touch_wait=GlobalEnumG.ExitBtnTime):  # 退出游戏-否
            elif self.find_info('ingame_flag2'):
                return True
            elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
            elif self.crop_image_find(ImgEnumG.LOGIN_TIPS, False):
                raise NotInGameErr
            elif self.find_info('coin_enum', True):
                pass
            else:
                # self.get_rgb(RgbEnumG.HD_BJBS, True)
                # self.get_rgb(RgbEnumG.QR, True)
                # self.back_ksdy()
                # self.get_rgb(RgbEnumG.MNDC_JG_QR, True)
                # self.find_info('LB_close', True)
                self.back()

    def check_err(self):
        if self.air_loop_find(ImgEnumG.GAME_ICON, False):
            raise NotInGameErr
        if self.crop_image_find(ImgEnumG.CZ_FUHUO):
            raise FuHuoRoleErr
        if self.find_info('ingame_flag2'):
            return True
        if self.find_info('game_login', True):
            return True
        self.get_rgb(RgbEnumG.BAT_JG, True)
        return False

    def close_window(self):
        for i in range(10):
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
            if self.find_info('ingame_flag2'):
                return True
            self.air_loop_find(ImgEnumG.UI_CLOSE)
            self.find_info('task_close', True)
            self.find_info('LB_close', True)
            self.air_loop_find(ImgEnumG.QD_1)
            self.air_loop_find(ImgEnumG.UI_QR)
            self.air_loop_find(ImgEnumG.LOGIN_TIPS)
            if i > 5:
                while not self.find_info('ingame_flag2'):
                    if self.find_info('task_arrow', True):
                        pass
                    self.air_loop_find(ImgEnumG.TASK_OVER, touch_wait=0)
                    self.air_loop_find(ImgEnumG.TASK_START, touch_wait=0)
                    self.check_err()
                    self.back()
        return False

    def check_is_stop(self):
        _COLOR = self.rgb(427, 656)
        # if self.crop_image_find(ImgEnumG.MOVE_NOW, False):
        _COLOR_1 = self.rgb(427, 656)
        if _COLOR == _COLOR_1:
            self.time_sleep(2)
            _COLOR_1 = self.rgb(427, 656)
            if _COLOR_1 == _COLOR:
                return True
        return False

    def skip_fever_buff(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):
                self.air_touch((857, 645))
            elif self.get_rgb(RgbEnumG.FEVER_BUFF):
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
            if self.get_rgb(RgbEnumG.SKIP_NEW) or self.get_rgb(RgbEnumG.SKIP_NEW1):
                self.air_touch((328, 369), touch_wait=0)
                self.air_touch((469, 369), touch_wait=0)
                self.air_touch((456, 369), touch_wait=0)
                self.air_touch((625, 369), touch_wait=0)
                self.air_touch((773, 369), touch_wait=0)
                self.air_touch((655, 369), touch_wait=0)
                self.air_touch((788, 369), touch_wait=0)
                if not self.get_rgb(RgbEnumG.SKIP_BTN, True):
                    if _C_TIMES > 10:
                        self.get_rgb(RgbEnumG.SKIP_NEW, True)
                    else:
                        _C_TIMES += 1
                else:
                    _C_TIMES = 0
            elif self.get_rgb(RgbEnumG.SKIP_BTN, True):
                if _C_TIMES > 10:
                    self.get_rgb(RgbEnumG.SKIP_NEW, True)
                else:
                    _C_TIMES += 1
            elif self.find_info('ingame_flag2'):
                if not self.crop_image_find(ImgEnumG.SKIP_NEW):
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
