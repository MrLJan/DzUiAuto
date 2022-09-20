# -*- coding: utf-8 -*-
import time

from airtest.core.android import Android
from airtest.core.api import device

from Enum.ResEnum import GlobalEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.OpencvG import OpenCvTools, AirImgTools, CnOcrTool


class BasePageG(OpenCvTools, AirImgTools, CnOcrTool):
    def __init__(self):
        super(OpenCvTools, self).__init__()
        self.dev = None

    @staticmethod
    def time_sleep(sleep_time):
        time.sleep(sleep_time)

    @staticmethod
    def start_game(serialno):
        """启动游戏"""
        ad = Android(serialno=serialno)
        ad.start_app(GlobalEnumG.GamePackgeName)

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
    def check_mulpic(self, pic_list,clicked=True):
        """检查多个图，找到其中1个则返回True"""
        for pic in pic_list:
            if self.crop_image_find(pic,clicked):
                return True
        return False


if __name__ == '__main__':
    DevicesConnect('emulator-5554').connect_device()
    android = Android()
    r = android.list_app(third_only=True)
    print(r, GlobalEnumG.GamePackgeName)
