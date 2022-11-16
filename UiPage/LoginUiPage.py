# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, ControlTimeOut, FuHuoRoleErr


class LoginUiPageG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(LoginUiPageG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def start_login(self, **kwargs):
        self.sn.log_tab.emit(self.mnq_name, r"开始登录")
        select_queue = kwargs['状态队列']['选择器']
        s_time = time.time()
        _WAIT_GX = 0
        _WAIT_TIMES = 0
        while time.time() - s_time < GlobalEnumG.LoginGameTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                self.start_game()
            elif self.air_loop_find(ImgEnumG.LOGIN_FLAG, False):
                if not self.get_rgb(RgbEnumG.GX_XZ, True):
                    self.air_touch((875, 390))  # 点击空白区域登录
                    self.time_sleep(10)
            elif self.find_info('game_login', True):
                self.time_sleep(10)
            elif self.find_info('ingame_flag2'):
                self.sn.log_tab.emit(self.mnq_name, r"登录成功")
                select_queue.task_over('Login')
                return -1
            elif self.get_rgb(RgbEnumG.PET_END):
                self.air_touch((908, 97), touch_wait=1)
            elif self.get_rgb(RgbEnumG.HD_BJBS, True):
                pass
            elif self.get_rgb(RgbEnumG.HD_BJBS, True):
                pass
            elif self.get_rgb(RgbEnumG.EXIT_FOU, True):  # 退出游戏-否
                pass
            elif self.get_rgb(RgbEnumG.CLOSE_GAME, True):
                pass
            elif self.air_loop_find(ImgEnumG.GX_XZ_ING, False):
                if not self.get_rgb(RgbEnumG.GX_XZ_BACK, True):
                    if _WAIT_GX > 60:
                        self.sn.log_tab.emit(self.mnq_name, r"更新超10分钟,重启游戏")
                        self.stop_game()
                    self.sn.log_tab.emit(self.mnq_name, r"等待更新")
                    self.time_sleep(10)
                    _WAIT_GX += 1
            else:
                if _WAIT_TIMES > 2:
                    if not self.check_err():
                        self.back()
                        _WAIT_TIMES = 0
                _WAIT_TIMES += 1
        return 0

    def check_ingame(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        if self.find_info('ingame_flag2'):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在游戏中")
            # if kwargs['角色信息']['等级'] == 0:
            #     select_queue.put_queue('CheckRole')
            if self.crop_image_find(ImgEnumG.TIP, False):
                self.air_touch((1239, 34), touch_wait=2)
            if self.get_rgb(RgbEnumG.FUHUO_BTN):
                if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                    self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                    raise FuHuoRoleErr
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT):
                self.back_ksdy()
            select_queue.task_over('Check')
            return -1
        elif self.net_err():
            self.sn.log_tab.emit(self.mnq_name, r"网络断开_等待重连")
            self.time_sleep(10)
        elif self.air_loop_find(ImgEnumG.GAME_ICON, False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到掉线")
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
            self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
            select_queue.task_over('Check')
            select_queue.put_queue('FuHuo')
            return -1
        elif self.crop_image_find(ImgEnumG.LOGIN_FLAG, False) or self.find_info('game_login', True):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在登录相关界面")
            self.get_rgb(RgbEnumG.GX_XZ, True)
            self.get_rgb(RgbEnumG.CLOSE_GAME, True)  # 退出游戏-否
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        else:
            if self.find_info('task_close') and kwargs['任务id'] == '1':
                # self.sn.log_tab.emit(self.mnq_name, r"检查到任务界面")
                while not self.find_info('ingame_flag2'):
                    if self.find_info('task_point', True):
                        pass
                    elif self.air_loop_find(ImgEnumG.TASK_OVER, touch_wait=1):
                        pass
                    elif self.air_loop_find(ImgEnumG.TASK_START, touch_wait=1):
                        pass
                    elif self.crop_image_find(ImgEnumG.TASK_TAKE, touch_wait=1):
                        pass
                    elif self.crop_image_find(ImgEnumG.TASK_REWARD, touch_wait=1):
                        pass
                    else:
                        self.close_all(**kwargs)
                select_queue.task_over('Check')
                return -1
            self.close_all(**kwargs)
        return 0

    def close_all(self, **kwargs):
        s_time = time.time()
        task_id = kwargs['任务id']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.sn.log_tab.emit(self.mnq_name, r"检查界面")
            if self.get_rgb(RgbEnumG.EXIT_FOU, True) or self.get_rgb(RgbEnumG.CLOSE_GAME, True):  # 退出游戏-否
                pass
            elif self.find_info('ingame_flag2'):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                if self.get_rgb(RgbEnumG.FUHUO_BTN):
                    if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                        self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                        raise FuHuoRoleErr
                if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, touch_wait=3):
                    # self.ocr_find(ImgEnumG.MR_YDZXD, True)
                    self.back_ksdy()
                if self.crop_image_find(ImgEnumG.TIP, False):
                    self.air_touch((1239, 34), touch_wait=2)
                self.get_rgb(RgbEnumG.TC_1, True)
                break
            elif self.air_loop_find(ImgEnumG.GAME_ICON, False):
                self.sn.log_tab.emit(self.mnq_name, r"掉线")
                raise NotInGameErr
            elif self.crop_image_find(ImgEnumG.LOGIN_FLAG) or self.find_info('game_login', True):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏登录主界面")
                break
            elif self.get_rgb(RgbEnumG.FUHUO_BTN):
                if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                    self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                    raise FuHuoRoleErr
            elif self.find_info('task_point', True):
                pass
            elif self.find_info('LB_close', True):
                pass
            elif self.find_info('coin_enum', True):
                pass
            elif self.get_rgb(RgbEnumG.WL_QX, True):
                pass
            elif self.find_info('task_close', True):
                pass
            elif self.get_rgb(RgbEnumG.PET_END):
                self.air_touch((908, 97), touch_wait=1)
            elif self.get_rgb(RgbEnumG.GX_XZ_BACK, True):
                pass
            elif self.find_info('task_arrow', True):
                pass
            elif self.get_rgb([1033, 414, 'EE7047'], True):
                pass
            elif self.find_info('skip', True):
                pass
            else:
                if task_id in ['1']:
                    if self.find_info('task_close'):
                        for i in range(3):
                            if self.find_info('task_point', True):
                                self.time_sleep(2)
                    self.get_rgb([1033, 414, 'EE7047'], True)
                self.back()
                # if self.get_rgb(394, 403, 'EE7047'):
                #     self.air_touch((710, 211))

    def close_game(self):
        self.stop_game()

    def fuhuo_check(self, **kwargs):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"复活检查")
        select_queue = kwargs['状态队列']['选择器']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):
                self.time_sleep(2)
                _res_hp_mp = self.check_hp_mp()
                if _res_hp_mp != '':
                    if 'HP' in _res_hp_mp:
                        select_queue.put_queue('BuyY')
                    elif use_mp:
                        if 'MP' in _res_hp_mp:
                            select_queue.put_queue('BuyY')
                elif self.crop_image_find(ImgEnumG.BAG_MAX_IMG, False):
                    select_queue.put_queue('BagSell')
                select_queue.task_over('FuHuo')
                return -1
            elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
                pass
            else:
                self.close_all(**kwargs)
        raise ControlTimeOut('复活检查-超时异常')
