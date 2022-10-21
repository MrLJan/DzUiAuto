# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, ControlTimeOut, FuHuoRoleErr


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
        _WAIT_GX = 0
        while time.time() - s_time < GlobalEnumG.LoginGameTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False, timeout=1):
                self.start_game(self.serialno)
            elif self.air_loop_find(ImgEnumG.LOGIN_FLAG, False):
                if not self.get_rgb(RgbEnumG.GX_XZ, True):
                    self.air_touch((875, 390))  # 点击空白区域登录
                    self.time_sleep(5)
            elif self.crop_image_find(ImgEnumG.START_GAME):
                self.time_sleep(10)
            elif self.air_loop_find(ImgEnumG.INGAME_FLAG2, False):
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
                        self.stop_game(self.serialno)
                    self.sn.log_tab.emit(self.mnq_name, r"等待更新")
                    self.time_sleep(10)
                    _WAIT_GX += 1
            else:
                if not self.check_err():
                    self.back(self.serialno)
        return 0

    def check_ingame(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在游戏中")
            # if kwargs['角色信息']['等级'] == 0:
            #     select_queue.put_queue('CheckRole')
            if self.crop_image_find(ImgEnumG.TIP, False):
                self.air_touch(1239, 34, touch_wait=2)
            if self.get_rgb(RgbEnumG.FUHUO_BTN):
                if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                    self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                    raise FuHuoRoleErr
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT):
                self.ocr_find(ImgEnumG.MR_YDZXD, True)
                self.ocr_find([(810, 519, 872, 548), '结'], True)
            select_queue.task_over('Check')
            return -1
        elif self.air_loop_find(ImgEnumG.GAME_ICON,False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到掉线")
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
            self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
            select_queue.task_over('Check')
            select_queue.put_queue('FuHuo')
            return -1
        elif self.crop_image_find(ImgEnumG.LOGIN_FLAG, False) or self.crop_image_find(ImgEnumG.START_GAME, False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在登录相关界面")
            self.get_rgb(RgbEnumG.GX_XZ, True)
            self.get_rgb(RgbEnumG.CLOSE_GAME, True)  # 退出游戏-否
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        else:
            if self.crop_image_find(ImgEnumG.TASK_CLOSE, False) and kwargs['任务id'] == '1':
                self.sn.log_tab.emit(self.mnq_name, r"检查到任务界面")
                while not self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    if self.crop_image_find(ImgEnumG.TASK_ARROW, touch_wait=1):
                        pass
                    elif self.air_loop_find(ImgEnumG.TASK_OVER, touch_wait=1):
                        pass
                    elif self.air_loop_find(ImgEnumG.TASK_START, touch_wait=1):
                        pass
                    elif self.crop_image_find(ImgEnumG.TASK_ARROW, touch_wait=1):
                        pass
                    elif self.crop_image_find(ImgEnumG.TASK_TAKE, touch_wait=1):
                        pass
                    elif self.crop_image_find(ImgEnumG.TASK_REWARD, touch_wait=1):
                        pass
                    elif self.ocr_find(ImgEnumG.SKIP_OCR, True):
                        pass
                    else:
                        self.close_all(**kwargs)
                select_queue.task_over('Check')
                return -1
            self.close_all(**kwargs)
        return 0

    # def check_ui(self):
    #     CLOSE_LIST = [
    #         ColorEnumG.LOGIN_CLOSE, ColorEnumG.LOGIN_START, ColorEnumG.BAG_MAIN, ColorEnumG.BAT_RES,
    #         ColorEnumG.MENU_MAIN, ColorEnumG.PET_TIME_END, ColorEnumG.QD_HD_BJBS, ColorEnumG.HB_ENUM,
    #         ColorEnumG.QD_HD_BJBS_CLOSE, ColorEnumG.QD_MY, ColorEnumG.HD_LB, ColorEnumG.BAG_MAIN, ColorEnumG.BAG_SELL,
    #         ColorEnumG.BAG_GOLD, ColorEnumG.BAG_SX, ColorEnumG.TASK_CLOSE, ColorEnumG.MR_KSDY, ColorEnumG.WL_MAIN,
    #         ColorEnumG.WL_JR, ColorEnumG.JZT_MAIN, ColorEnumG.JZT_JR, ColorEnumG.MRDC_MAIN, ColorEnumG.MRDC_JR,
    #         ColorEnumG.JHXT_MAIN, ColorEnumG.JHXT_JR, ColorEnumG.YZD_MAIN, ColorEnumG.GWSLT_MAIN, ColorEnumG.TBB_MAIN,
    #         ColorEnumG.TBB_JR, ColorEnumG.JYDC_END, ColorEnumG.JZT_END, ColorEnumG.CYRQ_END_F, ColorEnumG.SKIP_NEW,
    #         ColorEnumG.TBB_ZCJR, ColorEnumG.XLZC_MAIN, ColorEnumG.CYRQ_MAIN, ColorEnumG.MNDC_MAIN, ColorEnumG.MNDC_JR,
    #         ColorEnumG.XGT_MAIN, ColorEnumG.EXIT_TEAM, ColorEnumG.HDYZD_MAIN, ColorEnumG.GH_MAIN, ColorEnumG.GH_WXDC,
    #         ColorEnumG.MAIL_MAIN, ColorEnumG.KT_MAIN, ColorEnumG.PET_MAIN, ColorEnumG.JN_MAIN, ColorEnumG.YS_LOGIN,
    #         ColorEnumG.YS_SHOP, ColorEnumG.YS_XQ, ColorEnumG.YS_GM_QR, ColorEnumG.EXIT_GAME, ColorEnumG.ROLE_INFO,
    #         ColorEnumG.HD_CZZY, ColorEnumG.MAP_MAIN,
    #     ]
    #     for _c in CLOSE_LIST:
    #         if self.mulcolor_check(_c, True):
    #             return True
    #     return False

    def close_all(self, **kwargs):
        s_time = time.time()
        task_id = kwargs['任务id']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.get_rgb(RgbEnumG.EXIT_FOU, True) or self.get_rgb(RgbEnumG.CLOSE_GAME, True):  # 退出游戏-否
                if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                    if self.get_rgb(RgbEnumG.FUHUO_BTN):
                        if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                            self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                            raise FuHuoRoleErr
                    if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, touch_wait=3):
                        self.ocr_find(ImgEnumG.MR_YDZXD, True)
                        self.ocr_find([(810, 519, 872, 548), '结'], True)
                    if self.crop_image_find(ImgEnumG.TIP,False):
                        self.air_touch(1239,34,touch_wait=2)
                    self.get_rgb(RgbEnumG.TC_1, True)
                    break
                elif self.air_loop_find(ImgEnumG.GAME_ICON, False):
                    self.sn.log_tab.emit(self.mnq_name, r"掉线")
                    raise NotInGameErr
                elif self.crop_image_find(ImgEnumG.LOGIN_FLAG):
                    self.sn.log_tab.emit(self.mnq_name, r"在游戏登录主界面")
                    break
                elif self.get_rgb(RgbEnumG.FUHUO_BTN):
                    if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                        self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                        raise FuHuoRoleErr
                elif self.crop_image_find(ImgEnumG.TASK_ARROW):
                    pass
                elif self.get_rgb(RgbEnumG.PET_END):
                    self.air_touch((908, 97), touch_wait=1)

                # elif self.ocr_find(ImgEnumG.MNDC_JG):
                # elif self.get_rgb(564, 593, 'EE7047', True):
                #     pass
            elif self.get_rgb(RgbEnumG.GX_XZ_BACK, True):
                pass
            else:

                if task_id in ['1']:
                    if self.crop_image_find(ImgEnumG.TASK_ARROW):
                        for i in range(3):
                            self.crop_image_find(ImgEnumG.TASK_ARROW)
                    self.get_rgb([1033, 414, 'EE7047'], True)
                self.key_event(self.serialno, 'BACK')
                # if self.get_rgb(394, 403, 'EE7047'):
                #     self.air_touch((710, 211))

    def close_game(self):
        self.stop_game(self.serialno)

    def fuhuo_check(self, **kwargs):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"复活检查")
        select_queue = kwargs['状态队列']['选择器']
        exec_queue = kwargs['状态队列']['执行器']
        task_id = kwargs['任务id']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.INGAME_FLAG2, False):
                # if self.ocr_find(ImgEnumG.BAG_FULL):
                if self.ocr_find(ImgEnumG.HP_NULL_OCR):
                    select_queue.put_queue('BuyY')
                elif use_mp and self.ocr_find(ImgEnumG.MP_NULL_OCR):
                    select_queue.put_queue('BuyY')
                elif self.crop_image_find(ImgEnumG.BAG_MAX_IMG, False):
                    select_queue.put_queue('BagSell')
                select_queue.task_over('FuHuo')
                # if task_id in ['3', '4']:
                #     exec_queue.task_over('AutoBat')
                return -1
            elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
                pass
            else:
                self.close_all(**kwargs)
        raise ControlTimeOut('复活检查-超时异常')
