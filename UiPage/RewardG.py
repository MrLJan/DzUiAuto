# -*- coding: utf-8 -*-

import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG, MulColorEnumG, WorldEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import ControlTimeOut


class RewardG(BasePageG):
    def __init__(self, devinfo, sn):
        super(RewardG, self).__init__()
        self.dev, self.mnq_name = devinfo
        self.sn = sn

    def get_reward(self, **kwargs):
        self.sn.table_value.emit(self.mnq_name, 8, r"领取奖励")
        s_time = time.time()
        _HD = False
        _KT = False
        _MAIL = False
        select_queue = kwargs['状态队列']['选择器']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if _HD and _MAIL and _KT:
                select_queue.task_over('GetReward')
                return True
            elif not _HD:
                if self.get_hd_reward():
                    _HD = True
            elif not _KT:
                if self.get_keti_reward():
                    _KT = True
            elif not _MAIL:
                if self.get_mail_reward():
                    _MAIL = True
        self.sn.log_tab.emit(self.mnq_name, r'领取奖励-异常超时放弃')
        return True
        # raise ControlTimeOut(r'领取奖励-异常超时')

    def level_reward(self, **kwargs):
        s_time = time.time()
        _GET = False
        _MAIL = False
        select_queue = kwargs['状态队列']['选择器']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if _GET and _MAIL:
                for i in range(3):
                    self.cmp_rgb([737, 395, '617A'], True)  # 穿戴装备
                    # self.ocr_find(ImgEnumG.TASK_ZB, touch_wait=2)
                self.get_equip()
                select_queue.task_over('GetLevelReard')
                return True
            elif not _GET:
                if self.get_level_reward():
                    _GET = True
            elif not _MAIL:
                if self.get_mail_reward():
                    _MAIL = True
            else:
                self.check_close()
        self.sn.log_tab.emit(self.mnq_name, r'获取成长奖励-异常超时放弃')
        return True
        # raise ControlTimeOut(r'获取成长奖励-异常超时')

    def get_equip(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"穿戴装备")
        _WQ = False
        _FJ = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _WQ and _FJ:
                    self.back()
                    return True
                elif self.cmp_rgb([720, 395, '617'], True):
                    pass
                else:
                    self.touch((1170, 39), touch_wait=2)
            elif self.mul_color(MulColorEnumG.COIN_ENUM, True):
                pass
            elif self.cmp_rgb(RgbEnumG.ZB_XQ):
                self.cmp_rgb(RgbEnumG.ZB_JD, True)  # 鉴定
                self.cmp_rgb(RgbEnumG.ZB_JDQR, True)  # 鉴定确认
                self.cmp_rgb(RgbEnumG.ZB_CD, True)  # 穿戴
            elif self.cmp_rgb(RgbEnumG.QR, True):
                pass
            elif self.cmp_rgb(RgbEnumG.ZB_JDQR, True):  # 鉴定确认
                pass
            elif self.mul_color(MulColorEnumG.ZB_TS, True, touch_wait=2):
                pass
            elif self.cmp_rgb(RgbEnumG.BAG_M):
                self.time_sleep(2)
                if not self.mul_color(MulColorEnumG.ZB_TS, True, touch_wait=2):
                    if not _WQ:
                        self.touch((780, 127), touch_wait=2)
                        self.sn.log_tab.emit(self.mnq_name, f"穿戴装备-武器")
                        _WQ = True
                    elif not _FJ:
                        self.touch((868, 125), touch_wait=2)
                        self.sn.log_tab.emit(self.mnq_name, f"穿戴装备-防具")
                        _FJ = True
                    elif _WQ and _FJ:
                        self.back()

            else:
                self.check_close()
        self.sn.log_tab.emit(self.mnq_name, r'穿戴装备-异常超时放弃')
        return True
        # raise ControlTimeOut(r'穿戴装备-异常超时')

    def get_mail_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取邮件")
        _G = False  # 公共
        _O = False  # 个人
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                self.touch((995, 41), touch_wait=3)
                # self.pic_find(ImgEnumG.MAIL_RQ)
            elif self.cmp_rgb(RgbEnumG.MAIL_M):
                if _G and _O:
                    self.sn.log_tab.emit(self.mnq_name, f"邮件领取-完成")
                    self.back()
                    return True
                self.pic_find(ImgEnumG.UI_QBLQ)
                self.cmp_rgb(RgbEnumG.MAIL_LQ, True)
                self.pic_find(ImgEnumG.UI_QR)
                if self.cmp_rgb(RgbEnumG.MAIL_LQ_F):
                    _G = True
                    if self.cmp_rgb(RgbEnumG.MAIL_GR):
                        if self.cmp_rgb(RgbEnumG.MAIL_LQ_F):
                            _O = True
                    else:
                        self.cmp_rgb(RgbEnumG.MAIL_GR_F, True)
                        self.touch((922, 160))
            elif self.pic_find(ImgEnumG.UI_QR):
                pass
            elif self.pic_find(ImgEnumG.UI_QBLQ):
                pass
            elif self.qr_tip():
                self.time_sleep(2)
            else:
                self.check_err()
        self.sn.log_tab.emit(self.mnq_name, r'领取邮件-异常超时放弃')
        return True
        # raise ControlTimeOut(r'领取邮件-异常超时')

    def get_keti_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取课题奖励")
        _C_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.word_find(WorldEnumG.SET_BTN):  # 菜单界面
                # self.ocr_find(ImgEnumG.KT_MENU, True)
                self.enum_find('课题', True)
            elif self.cmp_rgb(RgbEnumG.KT_M):
                if _C_OVER:
                    self.sn.log_tab.emit(self.mnq_name, f"领取课题奖励-完成")
                    self.back()
                    return True
                if self.cmp_rgb(RgbEnumG.KT_MRRW):  # 每日任务
                    self.sn.log_tab.emit(self.mnq_name, f"领取-每日任务奖励")
                    if self.cmp_rgb(RgbEnumG.KT_F, False):
                        self.touch((48, 207), touch_wait=3)
                    else:
                        self.touch((1119, 650), touch_wait=3)
                        # self.ocr_find(ImgEnumG.KT_MZRW_OCR, True)
                elif self.cmp_rgb(RgbEnumG.KT_MZRW):  # 每周任务
                    self.sn.log_tab.emit(self.mnq_name, f"领取-每周任务奖励")
                    if self.cmp_rgb(RgbEnumG.KT_F):
                        self.touch((169, 309), touch_wait=3)
                    else:
                        self.touch((1120, 652), touch_wait=3)
                        # self.ocr_find(ImgEnumG.KT_MRSL_OCR, True)
                elif self.cmp_rgb(RgbEnumG.KT_MRSL):  # 每日狩猎
                    self.sn.log_tab.emit(self.mnq_name, f"领取-每日狩猎奖励")
                    if self.cmp_rgb(RgbEnumG.KT_F):
                        self.touch((155, 490), touch_wait=3)
                    else:
                        self.touch((1109, 641), touch_wait=3)
                        # self.ocr_find(ImgEnumG.KT_CJ_OCR, True)
                elif self.cmp_rgb(RgbEnumG.KT_CJ):  # 成就
                    self.sn.log_tab.emit(self.mnq_name, f"领取-成就奖励")
                    if self.cmp_rgb(RgbEnumG.KT_F):
                        _C_OVER = True
                    else:
                        self.touch((1107, 644), touch_wait=3)
            elif self.pic_find(ImgEnumG.KT_QBLQ):
                self.pic_find(ImgEnumG.UI_QR)
            elif self.pic_find(ImgEnumG.UI_QR):
                pass
            elif self.cmp_rgb([687, 524, 'ee7046'],True):
                pass
            elif self.cmp_rgb([695,546,'ee7046'],True):
                pass
            elif self.qr_tip():
                self.time_sleep(2)
            else:
                self.check_err()
        if self.find_color(MulColorEnumG.IGAME):
            return True
        return False

    def get_hd_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取奖励")
        _LOGIN = False
        _IN_DLJL = False
        _IN_XX = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.word_find(WorldEnumG.SET_BTN):
                self.enum_find('活动', True)  # 菜单界面
            elif self.cmp_rgb(RgbEnumG.HD_M):
                self.time_sleep(GlobalEnumG.TouchWaitTime)
                if not _LOGIN:
                    if self.word_find(WorldEnumG.LOGIN_REWARD, True):
                        self.sn.log_tab.emit(self.mnq_name, f"领取登录奖励")
                        _IN_DLJL = True
                        self.time_sleep(GlobalEnumG.TouchWaitTime)
                if _IN_DLJL:
                    if not self.cmp_rgb(RgbEnumG.RE_LQJL, True):  # 领取奖励:
                        if self.word_find(WorldEnumG.SLEEP_REWARD, True):
                            self.sn.log_tab.emit(self.mnq_name, f"领取休息奖励")
                            _IN_XX = True
                            _IN_DLJL = False
                            _LOGIN = True
                if _IN_XX:
                    self.time_sleep(GlobalEnumG.TouchWaitTime)
                    if not self.cmp_rgb(RgbEnumG.RE_LQJL1, True):  # 领取奖励
                        self.back()
                        self.back()
                        break
                else:
                    self.dm_swipe((112, 621), (112, 256), swipe_wait=1)
            elif self.qr_tip():
                pass
            else:
                self.time_sleep(GlobalEnumG.TouchWaitTime)
                self.check_err()
        if self.find_color(MulColorEnumG.IGAME):
            return True
        return False

    def get_level_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取成长奖励")
        _FIND_TIMES = 0
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _FIND_TIMES > 3:
                    return True
                # if not self.find_info('czjl',True):
                if not self.pic_find(ImgEnumG.CZJL_ICON, touch_wait=3):
                    self.touch((38, 149), touch_wait=1)
                    _FIND_TIMES += 1
            elif self.cmp_rgb(RgbEnumG.HD_CZZY):
                if self.cmp_rgb(RgbEnumG.HC_CZZY_LQ):
                    self.sn.log_tab.emit(self.mnq_name, r"领取成长奖励-完成")
                    self.back()
                    return True
                else:
                    self.touch((1238, 655), touch_wait=2)
            elif self.cmp_rgb(RgbEnumG.HD_M):
                # if not self.ocr_find([(29, 88, 181, 700), '全部的'], True):
                if not self.word_find(WorldEnumG.HD_CZZY, True):
                    self.dm_swipe((105, 598), (105, 391))
            else:
                self.check_err()
        self.sn.log_tab.emit(self.mnq_name, r'领取奖励-异常超时放弃')
        return True

    def bag_clear(self, **kwargs):
        s_time = time.time()
        _SWIP_TIMES = 0
        select_queue = kwargs['状态队列']['选择器']
        dis_list = kwargs['挂机设置']['清理道具']
        _C_FLAG = False
        _BS = False  # 宝石清理
        _SP = False  # 饰品
        _FJ = False  # 防具
        _WQ = False  # 武器
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _C_FLAG:
                    select_queue.task_over('BagClear')
                    return True
                self.touch((1170, 39), touch_wait=2)
            elif self.mul_color(MulColorEnumG.COIN_ENUM, True):
                pass
            elif self.cmp_rgb(RgbEnumG.BAG_DQ, True, touch_wait=1):
                pass
            elif self.cmp_rgb(RgbEnumG.BAG_DQQR, True, touch_wait=1):
                pass
            elif self.cmp_rgb(RgbEnumG.BAG_M):
                if _BS and _SP and _FJ and _WQ:
                    _C_FLAG = True
                if _C_FLAG:
                    self.back()
                else:
                    if not _BS:
                        self.cmp_rgb(RgbEnumG.BAG_BS, True)
                        if '0' in dis_list and self.mul_color(MulColorEnumG.BS_RED, True, touch_wait=1):
                            pass
                        elif '1' in dis_list and self.mul_color(MulColorEnumG.BS_BLUE, True, touch_wait=1):
                            pass
                        elif '2' in dis_list and self.mul_color(MulColorEnumG.BS_GREE, True, touch_wait=1):
                            pass
                        elif '3' in dis_list and self.mul_color(MulColorEnumG.BS_Z, True, touch_wait=1):
                            pass
                        elif '4' in dis_list and self.mul_color(MulColorEnumG.BS_H, True, touch_wait=1):
                            pass
                        elif '5' in dis_list and self.mul_color(MulColorEnumG.WQ_DZ, True, touch_wait=1):
                            pass
                        elif '6' in dis_list and self.mul_color(MulColorEnumG.FJ_DZ, True, touch_wait=1):
                            pass
                        elif '7' in dis_list and self.mul_color(MulColorEnumG.FJ_DZ, True, touch_wait=1):
                            pass
                        elif '8' in dis_list and self.mul_color(MulColorEnumG.JH_COIN, True, touch_wait=1):
                            pass
                        else:
                            if self.pic_find(ImgEnumG.BAG_NULL, False) or _SWIP_TIMES > 15:
                                self.sn.log_tab.emit(self.mnq_name, f"消耗栏清理完成")
                                _BS = True
                                _SWIP_TIMES = 0
                            else:
                                self.dm_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
                    elif not _SP:
                        self.cmp_rgb(RgbEnumG.BAG_SP, True)
                        if '8' in dis_list and self.mul_color(MulColorEnumG.JZT_BMFLJZ, True, touch_wait=1):
                            pass
                        elif '9' in dis_list and self.pic_find(ImgEnumG.PKJ_FLAG, touch_wait=1):
                            pass
                        else:
                            if self.pic_find(ImgEnumG.BAG_NULL, False) or _SWIP_TIMES > 15:
                                self.sn.log_tab.emit(self.mnq_name, f"饰品清理完成")
                                _SP = True
                                _SWIP_TIMES = 0
                            else:
                                self.dm_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
                    elif not _FJ:
                        self.cmp_rgb(RgbEnumG.BAG_FJ, True)
                        # if not self.check_mulpic([ImgEnumG.FJ_HE1, ImgEnumG.FJ_HE2]):
                        if '10' in dis_list and self.pic_find(ImgEnumG.YM_YD, touch_wait=1):
                            pass
                        else:
                            if self.pic_find(ImgEnumG.BAG_NULL, False) or _SWIP_TIMES > 15:
                                self.sn.log_tab.emit(self.mnq_name, f"防具清理完成")
                                _FJ = True
                                _SWIP_TIMES = 0
                            else:
                                self.dm_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
                    elif not _WQ:
                        self.cmp_rgb(RgbEnumG.BAG_WQ, True)
                        if not self.check_mulpic([ImgEnumG.WQ_HE1, ImgEnumG.WQ_HE2]):
                            if self.pic_find(ImgEnumG.BAG_NULL, False) or _SWIP_TIMES > 15:
                                self.sn.log_tab.emit(self.mnq_name, f"武器清理完成")
                                _WQ = True
                                _SWIP_TIMES = 0
                            else:
                                self.dm_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
        select_queue.task_over('BagClear')
        raise ControlTimeOut(r'清理背包-异常超时')

    def bagsell(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _SX_FLAG = False
        _FJSX_FLAG = False  # 分解筛选
        _OVER = False
        _FJ_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _OVER and _FJ_OVER:
                    select_queue.task_over('BagSell')
                    return True
                self.touch((1170, 39), touch_wait=2)
            elif self.mul_color(MulColorEnumG.COIN_ENUM, True):
                pass
            elif self.cmp_rgb(RgbEnumG.CSFJ_M):  # 出售界面
                if _OVER or _FJ_OVER:
                    if _FJ_OVER:
                        if self.check_ui('分解'):
                            self.back()
                    if _OVER:
                        if self.check_ui('贩售'):
                            self.back()
                if not _FJ_OVER:
                    if self.cmp_rgb(RgbEnumG.FJ_NULL):  # 分解栏空
                        if not _FJSX_FLAG:
                            # self.touch((68, 677), touch_wait=2)
                            self.cmp_rgb(RgbEnumG.SX_BTN, True)
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"分解完成")
                            _FJ_OVER = True
                    else:
                        self.cmp_rgb(RgbEnumG.CS_QR, True, touch_wait=2)
                        if self.cmp_rgb(RgbEnumG.FJ_END, True, touch_wait=2):
                            self.sn.log_tab.emit(self.mnq_name, r"分解确认")
                            _FJ_OVER = True
                elif not _OVER:
                    if not self.cmp_rgb(RgbEnumG.CS_NULL):
                        if not _SX_FLAG:
                            self.cmp_rgb(RgbEnumG.SX_BTN, True)
                            # self.touch((68, 677), touch_wait=2)  # 打开筛选
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"出售完成")
                            _OVER = True
                            self.mul_color(MulColorEnumG.TASK_CLOSE, True)
                    else:
                        self.cmp_rgb(RgbEnumG.CS_QR, True)
                        if self.cmp_rgb(RgbEnumG.QR, True, touch_wait=2):
                            self.sn.log_tab.emit(self.mnq_name, r"出售完成")
                            _OVER = True
            elif self.cmp_rgb(RgbEnumG.BAG_M):
                if _OVER and _FJ_OVER:
                    self.back()
                else:
                    if not _FJ_OVER:
                        self.cmp_rgb(RgbEnumG.FJ, True)  # 分解
                    elif not _OVER:
                        self.cmp_rgb(RgbEnumG.CS, True)  # 出售
            elif self.cmp_rgb(RgbEnumG.BAG_SX):
                if _SX_FLAG:
                    self.cmp_rgb(RgbEnumG.BAG_SX_TY, True)
                else:
                    self.cmp_rgb(RgbEnumG.SX_SP, True)  # 饰品
                    self.cmp_rgb(RgbEnumG.SX_SP2, True)  # 饰品
                    self.cmp_rgb(RgbEnumG.SX_SP3, True)  # 饰品
                    if self.cmp_rgb(RgbEnumG.BAG_SX_TY, True):
                        self.sn.log_tab.emit(self.mnq_name, r"出售筛选设置-完成")
                        _SX_FLAG = True
            elif self.cmp_rgb(RgbEnumG.BAG_FJSX):
                if _FJSX_FLAG:
                    self.cmp_rgb(RgbEnumG.FJ_TY, True)
                else:
                    self.cmp_rgb(RgbEnumG.FJ_SX, True)  # 史诗
                    self.cmp_rgb(RgbEnumG.FJ_SX2, True)  # 史诗
                    if self.cmp_rgb(RgbEnumG.FJ_TY, True):
                        self.sn.log_tab.emit(self.mnq_name, r"分解筛选设置-完成")
                        _FJSX_FLAG = True
            elif self.cmp_rgb(RgbEnumG.FJ_END):
                self.cmp_rgb(RgbEnumG.FJ_END, True, touch_wait=5)
                self.sn.log_tab.emit(self.mnq_name, r"分解完成")
                _FJ_OVER = True
            else:
                self.check_err()
            self.time_sleep(GlobalEnumG.WaitTime)
        select_queue.task_over('BagSell')
        raise ControlTimeOut(r'出售背包-异常超时')
