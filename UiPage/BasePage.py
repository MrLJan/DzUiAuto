# -*- coding: utf-8 -*-
import time

from airtest.core.android import Android
from Enum.ResEnum import GlobalEnumG, ImgEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.OpencvG import OpenCvTools, AirImgTools, CnOcrTool


class BasePageG(OpenCvTools, AirImgTools, CnOcrTool):
    def __init__(self):
        super(OpenCvTools, self).__init__()
        self.dev = None
        self.serialno = None

    @staticmethod
    def time_sleep(sleep_time):
        time.sleep(sleep_time)

    @staticmethod
    def start_game(serialno):
        """启动游戏"""
        ad = Android(serialno=serialno)
        ad.start_app(GlobalEnumG.GamePackgeName)

    @staticmethod
    def key_event(serialno, key, wait_time=1):
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
            if self.crop_image_find(pic, clicked):
                return True
        return False

    def check_close(self):
        if self.crop_image_find(ImgEnumG.GAME_ICON, False):
            return False
        if self.ocr_find(ImgEnumG.NET_ERR):#掉线
            _TIMES = 0
            for i in range(10):
                if _TIMES > 5:
                    self.stop_game(self.serialno)
                    return False
                if self.ocr_find(ImgEnumG.NET_ERR):
                    _TIMES += 1
                    self.time_sleep(10)
        self.crop_image_find(ImgEnumG.CZ_FUHUO)
        self.crop_image_find(ImgEnumG.UI_LB)
        self.crop_image_find(ImgEnumG.UI_CLOSE)
        return True

    def close_window(self):
        for i in range(10):
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                return True
            self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
            self.air_loop_find(ImgEnumG.UI_CLOSE)
            self.air_loop_find(ImgEnumG.UI_LB)
            self.air_loop_find(ImgEnumG.QD_1)
            self.air_loop_find(ImgEnumG.LOGIN_TIPS)
        return False

    def get_num(self, area):
        """获取范围内的int"""
        try:
            res = self.get_ocrres(area)
            num = ''.join(filter(lambda x: x.isdigit(), res))
            return int(num)
        except (ValueError, TypeError):
            return 0


if __name__ == '__main__':
    DevicesConnect('emulator-5554').connect_device()
    android = Android()
    r = android.list_app(third_only=True)
    print(r, GlobalEnumG.GamePackgeName)
