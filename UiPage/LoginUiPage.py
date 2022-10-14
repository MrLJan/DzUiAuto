# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG, ColorEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, ControlTimeOut


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
            elif self.mulcolor_check(ColorEnumG.LOGIN_MAIN) or self.air_loop_find(ImgEnumG.LOGIN_FLAG, False):
                self.air_touch((524, 390), duration=GlobalEnumG.TouchDurationTime)  # 点击空白区域登录
            elif self.mulcolor_check(ColorEnumG.LOGIN_START, clicked=True, touch_wait=10):
                pass
            elif self.crop_image_find(ImgEnumG.START_GAME, touch_wait=10):
                pass
            elif self.air_loop_find(ImgEnumG.INGAME_FLAG, False) or self.air_loop_find(ImgEnumG.INGAME_FLAG2, False):
                self.sn.log_tab.emit(self.mnq_name, r"登录成功")
                select_queue.task_over('Login')
                return -1
            else:
                self.air_loop_find(ImgEnumG.CZ_FUHUO)
                self.crop_image_find(ImgEnumG.LOGIN_TIPS)
                self.mulcolor_check(ColorEnumG.LOGIN_CLOSE,True)
                self.mulcolor_check(ColorEnumG.QD_HD_BJBS,True, touch_wait=2)
                self.crop_image_find(ImgEnumG.QD_LQ, touch_wait=2)
                self.air_loop_find(ImgEnumG.UI_QR, touch_wait=2)
                self.crop_image_find(ImgEnumG.QD, touch_wait=2)
                self.mulcolor_check(ColorEnumG.QD_HD_BJBS_CLOSE, touch_wait=1)

        return 0

    def check_ingame(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        if self.crop_image_find(ImgEnumG.MR_BAT_EXIT):
            self.ocr_find(ImgEnumG.MR_YDZXD, True)
            self.ocr_find([(810, 519, 872, 548), '结'], True)
            self.get_rgb(734, 549, 'EE7046', True)
        elif self.air_loop_find(ImgEnumG.GAME_ICON):
            self.sn.log_tab.emit(self.mnq_name, r"检查到掉线")
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
            self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
            select_queue.task_over('Check')
            select_queue.put_queue('FuHuo')
            return -1
        elif self.check_allpic([ImgEnumG.INGAME_FLAG, ImgEnumG.INGAME_FLAG2], False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在游戏中")
            # if kwargs['角色信息']['等级'] == 0:
            #     select_queue.put_queue('CheckRole')
            select_queue.task_over('Check')
            return -1
        elif self.mulcolor_check(ColorEnumG.LOGIN_MAIN) or self.mulcolor_check(ColorEnumG.LOGIN_START):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在登录相关界面")
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
        else:
            if self.crop_image_find(ImgEnumG.TASK_CLOSE, False) and kwargs['任务id'] == '1':
                self.sn.log_tab.emit(self.mnq_name, r"检查到任务界面")
                while not self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    if self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=0):pass
                    elif self.air_loop_find(ImgEnumG.TASK_OVER, timeout=0.5, touch_wait=1):pass
                    elif self.air_loop_find(ImgEnumG.TASK_START, timeout=0.5, touch_wait=1):pass
                    elif self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=1):pass
                    elif self.crop_image_find(ImgEnumG.TASK_TAKE, touch_wait=0):pass
                    elif self.crop_image_find(ImgEnumG.TASK_REWARD, touch_wait=0):pass
                    elif self.ocr_find(ImgEnumG.SKIP_OCR, True):pass
                    else:
                        self.close_all()
                select_queue.task_over('Check')
                return -1
            self.close_all()
        return 0

    def check_ui(self):
        CLOSE_LIST = [
            ColorEnumG.LOGIN_CLOSE, ColorEnumG.LOGIN_START, ColorEnumG.BAG_MAIN, ColorEnumG.BAT_RES,
            ColorEnumG.MENU_MAIN, ColorEnumG.PET_TIME_END, ColorEnumG.QD_HD_BJBS, ColorEnumG.HB_ENUM,
            ColorEnumG.QD_HD_BJBS_CLOSE, ColorEnumG.QD_MY, ColorEnumG.HD_LB, ColorEnumG.BAG_MAIN, ColorEnumG.BAG_SELL,
            ColorEnumG.BAG_GOLD, ColorEnumG.BAG_SX, ColorEnumG.TASK_CLOSE, ColorEnumG.MR_KSDY, ColorEnumG.WL_MAIN,
            ColorEnumG.WL_JR, ColorEnumG.JZT_MAIN, ColorEnumG.JZT_JR, ColorEnumG.MRDC_MAIN, ColorEnumG.MRDC_JR,
            ColorEnumG.JHXT_MAIN, ColorEnumG.JHXT_JR, ColorEnumG.YZD_MAIN, ColorEnumG.GWSLT_MAIN, ColorEnumG.TBB_MAIN,
            ColorEnumG.TBB_JR, ColorEnumG.JYDC_END, ColorEnumG.JZT_END, ColorEnumG.CYRQ_END_F, ColorEnumG.SKIP_NEW,
            ColorEnumG.TBB_ZCJR, ColorEnumG.XLZC_MAIN, ColorEnumG.CYRQ_MAIN, ColorEnumG.MNDC_MAIN, ColorEnumG.MNDC_JR,
            ColorEnumG.XGT_MAIN, ColorEnumG.EXIT_TEAM, ColorEnumG.HDYZD_MAIN, ColorEnumG.GH_MAIN, ColorEnumG.GH_WXDC,
            ColorEnumG.MAIL_MAIN, ColorEnumG.KT_MAIN, ColorEnumG.PET_MAIN, ColorEnumG.JN_MAIN, ColorEnumG.YS_LOGIN,
            ColorEnumG.YS_SHOP, ColorEnumG.YS_XQ, ColorEnumG.YS_GM_QR, ColorEnumG.EXIT_GAME, ColorEnumG.ROLE_INFO,
            ColorEnumG.HD_CZZY, ColorEnumG.MAP_MAIN,
        ]
        for _c in CLOSE_LIST:
            if self.mulcolor_check(_c, True):
                return True
        return False

    def close_all(self, **kwargs):
        s_time=time.time()
        while time.time()-s_time<GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                break
            elif self.crop_image_find(ImgEnumG.GAME_ICON, False):
                self.sn.log_tab.emit(self.mnq_name, r"掉线")
                raise NotInGameErr
            elif self.mulcolor_check(ColorEnumG.EXIT_GAME, True):
                break
            elif self.ocr_find(ImgEnumG.MNDC_JG):
                self.get_rgb(564, 593, 'EE7046', True)
                break
            else:
                self.key_event(self.serialno, 'BACK')
                if self.get_rgb(394, 403, 'EE7046'):
                    self.air_touch((710, 211))
        return False

    def close_game(self):
        self.stop_game(self.serialno)

    def fuhuo_check(self, **kwargs):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"复活检查")
        select_queue = kwargs['状态队列']['选择器']
        exec_queue=kwargs['状态队列']['执行器']
        task_id=kwargs['任务id']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.INGAME_FLAG2, False):
                if self.ocr_find(ImgEnumG.BAG_FULL):
                    select_queue.put_queue('BagSell')
                elif self.ocr_find(ImgEnumG.HP_NULL_OCR):
                    select_queue.put_queue('BuyY')
                elif self.ocr_find(ImgEnumG.MP_NULL_OCR) and use_mp:
                    select_queue.put_queue('BuyY')
                select_queue.task_over('FuHuo')
                if task_id in ['3','4']:
                    exec_queue.task_over('AutoBat')
                return -1
            elif self.crop_image_find(ImgEnumG.CZ_FUHUO):
                pass
            else:
                self.key_event(self.serialno, 'BACK')
        raise ControlTimeOut('复活检查-超时异常')
