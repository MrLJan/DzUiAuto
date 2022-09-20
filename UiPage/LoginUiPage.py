# -*- encoding=utf8 -*-
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG
from UiPage.BasePage import BasePageG


class LoginUiPageG(BasePageG):
    def __init__(self, devinfo,mnq_name,sn):
        super(LoginUiPageG,self).__init__()
        self.dev= devinfo[0]
        self.serialno=devinfo[-1]
        self.sn=sn
        self.mnq_name=mnq_name

    def start_login(self):
        self.sn.log_tab.emit(self.mnq_name, r"开始登录")
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.LoginGameTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False,1):
                self.start_game(self.serialno)
            self.crop_image_find(ImgEnumG.LOGIN_TIPS)
            if self.crop_image_find(ImgEnumG.LOGIN_FLAG1,False) or self.air_loop_find(ImgEnumG.LOGIN_FLAG,False, 1):
                self.air_touch(524, 390, duration=GlobalEnumG.TouchDurationTime)  # 点击空白区域登录
            self.crop_image_find(ImgEnumG.START_GAME,1)
            self.crop_image_find(ImgEnumG.QD,2)
            self.crop_image_find(ImgEnumG.QD_1,2)
            if self.crop_image_find(ImgEnumG.INGAME_FLAG,False) or self.crop_image_find(ImgEnumG.INGAME_FLAG2,False):
                self.sn.log_tab.emit(self.mnq_name, r"登录成功")
                return 2
        return 1

    def check_ingame(self):
        if self.check_mulpic([ImgEnumG.INGAME_FLAG,ImgEnumG.INGAME_FLAG2],False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在游戏中")
            return 1
        if self.check_mulpic([ImgEnumG.GAME_ICON,ImgEnumG.START_GAME,ImgEnumG.LOGIN_FLAG,
                              ImgEnumG.INGAME_FLAG2,ImgEnumG.LOGIN_TIPS],False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在登录相关界面")
            return 2
        if self.check_mulpic([ImgEnumG.TASK_CLOSE,ImgEnumG.TASK_ARROW,ImgEnumG.TASK_REWARD],False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到任务界面")
            return 3
        return 0
