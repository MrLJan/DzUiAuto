# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG
from UiPage.BasePage import BasePageG
from Utils.LoadConfig import LoadConfig
import random


class DailyTaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(DailyTaskAutoG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def dailytask_start(self):
        task_list = []
        task_name = ['武陵', '金字塔', '菁英地城', '每日地城', '进化系统', '次元入侵', '汤宝宝',
                     '迷你地城', '怪物狩猎团', '星光塔', '怪物公园']
        for i in task_name:
            r = LoadConfig.getconf("全局配置", i)
            if r == '1':
                index = (task_name.index(i) + 1)
                task_list.append(index)
        random.shuffle(task_list)
        if len(task_list) == 0:
            return True
        while True:
            pass

    def wulin_task(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
                self.time_sleep(15)
                print('bat')
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                if self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    self.ocr_find([ImgEnumG.MR_AREA, '武陵道'], True)
                if self.ocr_find(ImgEnumG.MR_WLDC_OCR):  # 道场界面
                    self.get_rgb((1068, 650), 'EE7047', True)
                if self.ocr_find(ImgEnumG.MR_WLDC_JR):  # 入场选择
                    self.crop_image_find(ImgEnumG.MR_MAX)
                    self.get_rgb((729, 629), 'EE7047', True)
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    return True
        return False

    def jinzita_task(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
                self.time_sleep(15)
                print('bat')
            else:
                if self.get_rgb(334, 348, 'FEFFFF') and self.get_rgb(434, 258, '0F0F0F'):
                    self.time_sleep(15)
                    print('组队中')
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                if self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    self.ocr_find([ImgEnumG.MR_AREA, '学塔'], True)
                if self.ocr_find(ImgEnumG.MR_JZT_OCR):  # 金字塔界面
                    self.get_rgb(1053, 666, 'EE7047', True)
                if self.ocr_find(ImgEnumG.MR_JZT_JR):
                    self.air_loop_find(ImgEnumG.MR_MAX)
                    if self.get_rgb(717, 531, 'EE7047', True):
                        self.time_sleep(10)
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    return True
        return False

    def jingying_task(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
                print('bat')
                self.time_sleep(5)
            else:
                if self.get_rgb(334, 348, 'FEFFFF') and self.get_rgb(434, 258, '0F0F0F'):
                    self.time_sleep(15)
                    print('组队中')
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    if not self.ocr_find(ImgEnumG.MR_MENU_KSNR, True):
                        self.crop_image_find(ImgEnumG.UI_CLOSE)
                    if self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                        self.ocr_find([ImgEnumG.MR_AREA, '菁英'], True)
                    if self.ocr_find(ImgEnumG.MR_JYDC_OCR):  # 菁英地城界面
                        self.get_rgb(1053, 666, 'EE7047', True)
                    if self.ocr_find(ImgEnumG.MR_JZT_JR):  # 进入界面 和金字塔一样
                        self.air_loop_find(ImgEnumG.MR_MAX)
                        if self.get_rgb(717, 531, 'EE7047', True):
                            self.time_sleep(10)
                    if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        return True
        return False
