# -*- coding:utf-8 -*-
import time

from airtest.core.android import Android
from airtest.core.android.adb import ADB

from Enum.ResEnum import GlobalEnumG, ImgEnumG, ColorEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.ExceptionTools import NotInGameErr, FuHuoRoleErr
from Utils.OpencvG import OpenCvTools, AirImgTools, CnOcrTool


class BasePageG(OpenCvTools, AirImgTools, CnOcrTool):
    def __init__(self):
        super(OpenCvTools, self).__init__()
        self.dev = None
        self.serialno = None
        self.cn_ocr = None

    def snap(self):
        return ADB(self.serialno).snapshot()

    @staticmethod
    def time_sleep(sleep_time):
        time.sleep(sleep_time)

    @staticmethod
    def start_game(serialno):
        """启动游戏"""
        ad = Android(serialno=serialno)
        ad.start_app(GlobalEnumG.GamePackgeName)

    @staticmethod
    def key_event(serialno, key, wait_time=1.5):
        ad = Android(serialno=serialno)
        ad.keyevent(key)
        time.sleep(wait_time)

    @staticmethod
    def stop_game(serialno):
        """关闭游戏"""
        ad = Android(serialno=serialno)
        ad.stop_app(GlobalEnumG.GamePackgeName)

    @staticmethod
    def close_other_app(serialno):
        """关闭除游戏客户端外其他应用"""
        ad = Android(serialno=serialno)
        app_list = ad.list_app()
        for al in app_list:
            if al != GlobalEnumG.GamePackgeName:
                ad.stop_app(al)

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
        w_time=time.time()
        while True:
            if time.time()-w_time>GlobalEnumG.UiCheckTimeOut:
                self.stop_game(self.serialno)
            if self.crop_image_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                return True
            if self.ocr_find(ImgEnumG.NET_ERR):  # 网络异常掉线
                _TIMES = 0
                for i in range(10):
                    if _TIMES > 5:
                        self.stop_game(self.serialno)
                        raise NotInGameErr
                    if self.ocr_find(ImgEnumG.NET_ERR):
                        _TIMES += 1
                        self.time_sleep(10)
            if self.mulcolor_check(ColorEnumG.EXIT_GAME,True):
                pass
            else:
                self.crop_image_find(ImgEnumG.CZ_FUHUO)
                self.crop_image_find(ImgEnumG.UI_LB)
                self.crop_image_find(ImgEnumG.UI_CLOSE)
                self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                self.air_loop_find(ImgEnumG.UI_QR)
                self.key_event(self.serialno,'back')

    def check_err(self):
        if self.air_loop_find(ImgEnumG.GAME_ICON, False):
            raise NotInGameErr
        if self.crop_image_find(ImgEnumG.CZ_FUHUO):
            raise FuHuoRoleErr
        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
            return True
        self.mulcolor_check(ColorEnumG.BAT_MAIN, True)
        self.mulcolor_check(ColorEnumG.BAT_RES, True)
        self.mulcolor_check(ColorEnumG.HB_ENUM, True)
        return False
        # if self.ocr_find(ImgEnumG.AUTO_JG):
        #     self.air_loop_find(ImgEnumG.UI_QR)
        # self.crop_image_find(ImgEnumG.UI_LB)

    def close_window(self):
        for i in range(10):
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                return True
            self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
            self.air_loop_find(ImgEnumG.UI_CLOSE)
            self.air_loop_find(ImgEnumG.UI_LB)
            self.air_loop_find(ImgEnumG.QD_1)
            self.air_loop_find(ImgEnumG.UI_QR)
            self.air_loop_find(ImgEnumG.LOGIN_TIPS)
            if i > 5:
                while not self.crop_image_find(ImgEnumG.INGAME_FLAG2,False):
                    self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=0)
                    self.ocr_find(ImgEnumG.SKIP_OCR, True)
                    self.air_loop_find(ImgEnumG.TASK_OVER, timeout=0.5, touch_wait=1)
                    self.air_loop_find(ImgEnumG.TASK_START, timeout=0.5, touch_wait=1)
                    self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=1)
                    self.crop_image_find(ImgEnumG.TASK_TAKE, touch_wait=0)
                    self.crop_image_find(ImgEnumG.TASK_REWARD, touch_wait=0)
                    self.check_err()
                    self.key_event(self.serialno, 'BACK')
        return False

    def get_num(self, area):
        """获取范围内的int"""
        try:
            res = self.get_ocrres(area)
            num = ''.join(filter(lambda x: x.isdigit(), res))
            return int(num)
        except (ValueError, TypeError):
            return 0

    def check_is_stop(self):
        _COLOR = self.get_rgb(447, 699)
        if self.crop_image_find(ImgEnumG.MOVE_NOW, False):
            self.time_sleep(GlobalEnumG.TaskWaitTime)
        _COLOR_1 = self.get_rgb(447, 699)
        if _COLOR == _COLOR_1:
            self.time_sleep(2)
            _COLOR_1 = self.get_rgb(447, 699)
            if _COLOR_1 == _COLOR:
                return True
        return False

    def skip_fever_buff(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.air_touch((857, 645))
            elif self.ocr_find(ImgEnumG.SKIP_OCR, True):
                pass
            elif self.mulcolor_check(ColorEnumG.FEVER_BUFF) or self.get_rgb(582, 191, 'F2F2F2'):
                return True
            else:
                if time.time() - s_time > GlobalEnumG.SelectCtrTimeOut / 2:
                    self.check_err()
        return False

    def skip_new(self):
        s_time = time.time()
        _C_TIMES = 0
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if not self.crop_image_find(ImgEnumG.SKIP_NEW, timeout=3):
                    return True

            elif self.mulcolor_check(ColorEnumG.SKIP_NEW) or self.get_rgb(622, 213, 'FFE'):
                self.air_touch((328, 369))
                self.air_touch((469, 369))
                self.air_touch((625, 369))
                self.air_touch((773, 369))
                if not self.get_rgb(374, 528, '4C87', True):
                    if _C_TIMES > 10:
                        self.mulcolor_check(ColorEnumG.SKIP_NEW, True)
                    else:
                        _C_TIMES += 1
                else:
                    _C_TIMES = 0
            elif self.get_rgb(374, 528, '4C87', True):
                if _C_TIMES > 10:
                    self.mulcolor_check(ColorEnumG.SKIP_NEW, True)
                else:
                    _C_TIMES += 1
            else:
                if time.time() - s_time > GlobalEnumG.SelectCtrTimeOut / 2:
                    self.check_err()
        return False


if __name__ == '__main__':
    DevicesConnect('emulator-5554').connect_device()
    android = Android()
    r = android.list_app(third_only=True)
    print(r, GlobalEnumG.GamePackgeName)
