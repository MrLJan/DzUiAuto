# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr


class LoginUiPageG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn, ocr):
        super(LoginUiPageG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.cn_ocr = ocr

    def start_login(self, **kwargs):
        self.sn.log_tab.emit(self.mnq_name, r"开始登录")
        select_queue = kwargs['状态队列']['选择器']
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.LoginGameTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False, timeout=1):
                self.start_game(self.serialno)
            self.crop_image_find(ImgEnumG.LOGIN_TIPS)
            if self.ocr_find(ImgEnumG.GAME_XZ):
                self.air_loop_find(ImgEnumG.UI_QR)
            if self.crop_image_find(ImgEnumG.LOGIN_FLAG1, False) or self.air_loop_find(ImgEnumG.LOGIN_FLAG, False):
                self.air_touch((524, 390), duration=GlobalEnumG.TouchDurationTime)  # 点击空白区域登录
            self.crop_image_find(ImgEnumG.START_GAME, touch_wait=10)
            self.crop_image_find(ImgEnumG.QD, touch_wait=2)
            if self.crop_image_find(ImgEnumG.QD_LQ, touch_wait=2):
                self.air_loop_find(ImgEnumG.UI_QR, touch_wait=2)
                self.crop_image_find(ImgEnumG.QD, touch_wait=2)
            self.crop_image_find(ImgEnumG.QD_1, touch_wait=2)
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False) or self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.sn.log_tab.emit(self.mnq_name, r"登录成功")
                select_queue.task_over('Login')
                return -1
        return 0

    def check_ingame(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        self.air_loop_find(ImgEnumG.UI_CLOSE)
        self.air_loop_find(ImgEnumG.UI_QR)
        self.crop_image_find(ImgEnumG.TIP_ClOSE)
        if self.ocr_find(ImgEnumG.GAME_END):
            self.air_loop_find(ImgEnumG.UI_NO)
        elif self.ocr_find(ImgEnumG.GAME_XZ):
            self.air_loop_find(ImgEnumG.UI_QR)
        elif self.crop_image_find(ImgEnumG.MR_BAT_EXIT):
            self.ocr_find(ImgEnumG.MR_YDZXD, True)
            self.ocr_find([(810, 519, 872, 548), '结'], True)
            self.get_rgb(734, 549, 'EE7047', True)
        elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
            self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
            return 0
        elif self.check_allpic([ImgEnumG.INGAME_FLAG, ImgEnumG.INGAME_FLAG2], False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在游戏中")
            # if kwargs['角色信息']['等级'] == 0:
            #     select_queue.put_queue('CheckRole')
            select_queue.task_over('Check')
            return -1
        elif self.check_mulpic([ImgEnumG.GAME_ICON, ImgEnumG.START_GAME, ImgEnumG.LOGIN_FLAG,
                                ImgEnumG.INGAME_FLAG2, ImgEnumG.LOGIN_TIPS], False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在登录相关界面")
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        elif self.check_mulpic([ImgEnumG.TASK_CLOSE, ImgEnumG.TASK_ARROW, ImgEnumG.TASK_REWARD], False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到任务界面")
            while not self.crop_image_find(ImgEnumG.INGAME_FLAG2):
                self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=0)
                self.ocr_find(ImgEnumG.SKIP_OCR, True)
                self.air_loop_find(ImgEnumG.TASK_OVER, timeout=0.5, touch_wait=1)
                self.air_loop_find(ImgEnumG.TASK_START, timeout=0.5, touch_wait=1)
                self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=1)
                self.crop_image_find(ImgEnumG.TASK_TAKE, touch_wait=0)
                self.crop_image_find(ImgEnumG.TASK_REWARD, touch_wait=0)
                self.check_err()
            select_queue.task_over('Check')
            return -1
        else:
            self.close_all()
        return 0

    def close_all(self,**kwargs):
        for i in range(10):
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                return True
            elif self.crop_image_find(ImgEnumG.GAME_ICON, False):
                self.sn.log_tab.emit(self.mnq_name, r"掉线")
                raise NotInGameErr
            elif self.ocr_find(ImgEnumG.GAME_END):
                self.air_loop_find(ImgEnumG.UI_NO)
                return True
            elif self.ocr_find(ImgEnumG.MNDC_JG):
                self.get_rgb(564, 593, 'EE7047', True)
                return True
            else:
                self.check_close()
                self.key_event(self.serialno, 'BACK')
        return False

    def close_game(self):
        self.stop_game(self.serialno)
