# -*- encoding=utf8 -*-
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG
from UiPage.BasePage import BasePageG


class LoginUiPageG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(LoginUiPageG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def start_login(self,**kwargs):
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
                self.air_loop_find(ImgEnumG.UI_QR,touch_wait=2)
                self.crop_image_find(ImgEnumG.QD, touch_wait=2)
            self.crop_image_find(ImgEnumG.QD_1, touch_wait=2)
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False) or self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.sn.log_tab.emit(self.mnq_name, r"登录成功")
                select_queue.task_over('Login')
                return -1
        return 0

    def check_ingame(self,**kwargs):
        select_queue=kwargs['状态队列']['选择器']
        self.air_loop_find(ImgEnumG.UI_CLOSE)
        if self.check_mulpic([ImgEnumG.INGAME_FLAG, ImgEnumG.INGAME_FLAG2], False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在游戏中")
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT):
                self.ocr_find(ImgEnumG.MR_YDZXD,True)
            select_queue.task_over('Check')
            return -1
        if self.check_mulpic([ImgEnumG.GAME_ICON, ImgEnumG.START_GAME, ImgEnumG.LOGIN_FLAG,
                              ImgEnumG.INGAME_FLAG2, ImgEnumG.LOGIN_TIPS], False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在登录相关界面")
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        if self.check_mulpic([ImgEnumG.TASK_CLOSE, ImgEnumG.TASK_ARROW, ImgEnumG.TASK_REWARD], False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到任务界面")
            select_queue.task_over('Check')
            return -1
        self.close_all()
        return 0

    def close_all(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                return True
            elif self.crop_image_find(ImgEnumG.GAME_ICON, False):
                self.sn.log_tab.emit(self.mnq_name, r"掉线")
                return True
            elif not self.ocr_find(ImgEnumG.GAME_END):
                self.check_close()
                self.key_event(self.serialno, 'BACK')
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    self.key_event(self.serialno, 'BACK')
        return False

