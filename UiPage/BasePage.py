# -*- coding: utf-8 -*-
import time

from airtest.core.android import Android
from airtest.core.api import device

from Enum.ResEnum import GlobalEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.OpencvG import OpenCvTools, AirImgTools


class BasePageG(OpenCvTools, AirImgTools):

    @staticmethod
    def time_sleep(sleep_time):
        time.sleep(sleep_time)

    @staticmethod
    def start_game(self):
        """启动游戏"""
        ad = Android()
        ad.start_app(GlobalEnumG.GamePackgeName)

    @staticmethod
    def stop_game():
        """关闭游戏"""
        ad = Android()
        ad.stop_app(GlobalEnumG.GamePackgeName)

    @staticmethod
    def close_other_app():
        """关闭除游戏客户端外其他应用"""
        ad = Android()
        app_list = ad.list_app()
        for al in app_list:
            if al != GlobalEnumG.GamePackgeName:
                ad.stop_app(al)


if __name__ == '__main__':
    DevicesConnect('emulator-5554').connect_device()
    android = Android()
    r = android.list_app(third_only=True)
    print(r, GlobalEnumG.GamePackgeName)
