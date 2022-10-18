# -*- coding: utf-8 -*-

import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, ColorEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import ControlTimeOut
from Utils.LoadConfig import LoadConfig


class RewardG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn, ocr):
        super(RewardG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.cn_ocr = ocr

    def get_reward(self, **kwargs):
        self.sn.table_value.emit(self.mnq_name, 8, r"领取奖励")
        s_time = time.time()
        _HD = False
        _KT = False
        _MAIL = False
        select_queue = kwargs['状态队列']['选择器']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
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
        raise ControlTimeOut(r'领取奖励-异常超时')

    def level_reward(self, **kwargs):
        s_time = time.time()
        _GET = False
        _MAIL = False
        select_queue = kwargs['状态队列']['选择器']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if _GET and _MAIL:
                for i in range(3):
                    self.get_rgb([737, 395, '617A'], True)  # 穿戴装备
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
        raise ControlTimeOut(r'获取成长奖励-异常超时')

    def get_equip(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"穿戴装备")
        _WQ = False
        _FJ = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _WQ and _FJ:
                    self.back(self.serialno)
                    return True
                self.air_touch((1170, 39), touch_wait=1)
            elif self.get_rgb(RgbEnumG.ZB_XQ):
                self.get_rgb(RgbEnumG.ZB_JD, True)  # 鉴定
                self.get_rgb(RgbEnumG.ZB_JDQR, True)  # 鉴定确认
                self.get_rgb(RgbEnumG.ZB_CD, True)  # 穿戴
            elif self.get_rgb(RgbEnumG.QR, True):
                pass
            elif self.get_rgb(RgbEnumG.BAG_M):
                if not self.crop_image_find(ImgEnumG.ZB_TS):
                    if not _WQ:
                        self.air_touch((780, 127), touch_wait=1)
                        _WQ = True
                    elif not _FJ:
                        self.air_touch((868, 125), touch_wait=1)
                        _FJ = True
                    if _WQ and _FJ:
                        self.back(self.serialno)
            else:
                self.check_close()
        raise ControlTimeOut(r'穿戴装备-异常超时')

    def get_mail_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取邮件")
        _G = False  # 公共
        _O = False  # 个人
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.MAIL_RQ)
            elif self.get_rgb(RgbEnumG.MAIL_M):
                if _G and _O:
                    self.back(self.serialno)
                    return True
                self.air_loop_find(ImgEnumG.UI_QBLQ)
                self.get_rgb(RgbEnumG.MAIL_LQ, True)
                self.crop_image_find(ImgEnumG.UI_QR)
                if self.get_rgb(RgbEnumG.MAIL_LQ_F):
                    _G = True
                    if self.get_rgb(RgbEnumG.MAIL_GR):
                        if self.get_rgb(RgbEnumG.MAIL_LQ_F):
                            _O = True
                    else:
                        self.get_rgb(RgbEnumG.MAIL_GR_F, True)
                        self.air_touch((922, 160))
            elif self.air_loop_find(ImgEnumG.UI_QR):
                pass
            elif self.crop_image_find(ImgEnumG.UI_QBLQ):
                pass
            else:
                self.check_close()
        raise ControlTimeOut(r'领取邮件-异常超时')

    def get_keti_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取课题奖励")
        _C_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                self.crop_image_find(ImgEnumG.MR_MENU)
            elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.KT_MENU, True)
            elif self.get_rgb(RgbEnumG.KT_M):
                if _C_OVER:
                    self.back(self.serialno)
                    return True
                if self.get_rgb(RgbEnumG.KT_MRRW):  # 每日任务
                    if self.get_rgb(RgbEnumG.KT_F, False):
                        self.air_touch((48, 207), touch_wait=1)
                    else:
                        self.air_touch((1119, 650), touch_wait=1)
                        # self.ocr_find(ImgEnumG.KT_MZRW_OCR, True)
                elif self.get_rgb(RgbEnumG.KT_MZRW):  # 每周任务
                    if self.get_rgb(RgbEnumG.KT_F):
                        self.air_touch((169, 309))
                    else:
                        self.air_touch((1120, 652))
                        # self.ocr_find(ImgEnumG.KT_MRSL_OCR, True)
                elif self.get_rgb(RgbEnumG.KT_MRSL):  # 每日狩猎
                    if self.get_rgb(RgbEnumG.KT_F):
                        self.air_touch((155, 490))
                    else:
                        self.air_touch((1109, 641))
                        # self.ocr_find(ImgEnumG.KT_CJ_OCR, True)
                elif self.get_rgb(RgbEnumG.KT_CJ):  # 成就
                    if self.get_rgb(RgbEnumG.KT_F):
                        _C_OVER = True
                    else:
                        self.air_touch((1107, 644))
            elif self.air_loop_find(ImgEnumG.KT_QBLQ):
                self.air_loop_find(ImgEnumG.UI_QR)
            elif self.air_loop_find(ImgEnumG.UI_QR):
                pass
            elif self.get_rgb([687, 524,'EE7047']):pass
            else:
                self.check_close()
        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
            return True
        return False

    def get_hd_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取登录奖励")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.MR_MENU)
            elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.HD_MENU, True)
            elif self.get_rgb(RgbEnumG.HD_M):
                if self.ocr_find(ImgEnumG.HD_DR_OCR, True):
                    if not self.get_rgb(RgbEnumG.RE_LQJL, True):  # 领取奖励:
                        self.ocr_find(ImgEnumG.HD_XX_OCR, True)
                        if not self.get_rgb(RgbEnumG.RE_LQJL1, True):  # 领取奖励
                            self.back(self.serialno)
                            self.back(self.serialno)
                            break
                else:
                    self.air_swipe((112, 621), (112, 256), swipe_wait=1)
            elif self.air_loop_find(ImgEnumG.UI_QR):
                pass
            else:
                self.check_close()
        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
            return True
        return False

    def get_level_reward(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, f"领取成长奖励")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if not self.crop_image_find(ImgEnumG.CZZY):
                    self.air_touch((38, 149), touch_wait=1)
            elif self.get_rgb(RgbEnumG.HD_CZZY):
                if self.get_rgb([1238, 655, 'ADADAD']):
                    self.back(self.serialno)
                    return True
                else:
                    self.air_touch((1238, 655), touch_wait=1)
            elif self.get_rgb(RgbEnumG.HD_M):
                if not self.ocr_find([(29, 88, 181, 700), '全部的'], True):
                    self.air_swipe((105, 598), (105, 391))
            else:
                self.check_close()
        raise ControlTimeOut(r'领取奖励-异常超时')

    def bag_clear(self, **kwargs):
        s_time = time.time()
        _SWIP_TIMES = 0
        select_queue = kwargs['状态队列']['选择器']
        _C_FLAG = False
        _BS = False  # 宝石清理
        _SP = False  # 饰品
        _FJ = False  # 防具
        _WQ = False  # 武器
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _C_FLAG:
                    select_queue.task_over('BagClear')
                    return True
                self.air_touch((1170, 39), touch_wait=2)
            elif self.get_rgb(RgbEnumG.BAG_DQ, True):
                pass
            elif self.get_rgb(RgbEnumG.BAG_DQQR, True):
                pass
            elif self.get_rgb(RgbEnumG.BAG_M):
                if _BS and _SP and _FJ and _WQ:
                    _C_FLAG = True
                if _C_FLAG:
                    self.back(self.serialno)
                else:
                    if not _BS:
                        self.get_rgb(RgbEnumG.BAG_BS, True)
                        if not self.crop_image_find(ImgEnumG.RED_BS):
                            if _SWIP_TIMES > 1:
                                self.sn.log_tab.emit(self.mnq_name, f"宝石清理完成")
                                _BS = True
                                _SWIP_TIMES = 0
                            else:
                                self.air_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
                    elif not _SP:
                        self.get_rgb(RgbEnumG.BAG_SP, True)
                        if not self.crop_image_find(ImgEnumG.JZT_DJ, touch_wait=1):
                            if _SWIP_TIMES > 1:
                                self.sn.log_tab.emit(self.mnq_name, f"饰品清理完成")
                                _SP = True
                                _SWIP_TIMES = 0
                            else:
                                self.air_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
                    elif not _FJ:
                        self.get_rgb(RgbEnumG.BAG_FJ, True)
                        if not self.check_mulpic([ImgEnumG.FJ_HE1, ImgEnumG.FJ_HE2]):
                            if _SWIP_TIMES > 1:
                                self.sn.log_tab.emit(self.mnq_name, f"防具清理完成")
                                _FJ = True
                                _SWIP_TIMES = 0
                            else:
                                self.air_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
                    elif not _WQ:
                        self.get_rgb(RgbEnumG.BAG_WQ, True)
                        if not self.check_mulpic([ImgEnumG.WQ_HE1, ImgEnumG.WQ_HE2]):
                            if _SWIP_TIMES > 1:
                                self.sn.log_tab.emit(self.mnq_name, f"武器清理完成")
                                _WQ = True
                                _SWIP_TIMES = 0
                            else:
                                self.air_swipe((1052, 559), (1052, 353), swipe_wait=1)
                                _SWIP_TIMES += 1
        raise ControlTimeOut(r'清理背包-异常超时')

    def bagsell(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _SX_FLAG = False
        _FJSX_FLAG = False  # 分解筛选
        _OVER = False
        _FJ_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _OVER:
                    select_queue.task_over('BagSell')
                    return True
                self.air_touch((1170, 39), touch_wait=2)
            elif self.get_rgb(RgbEnumG.BAG_SX):
                self.get_rgb(RgbEnumG.SX_SP, True)  # 饰品
                self.get_rgb(RgbEnumG.SX_SP2, True)  # 饰品
                self.get_rgb(RgbEnumG.SX_SP3, True)  # 饰品
                if self.get_rgb(RgbEnumG.BAG_SX_TY, True):
                    _SX_FLAG = True
            elif self.get_rgb(RgbEnumG.BAG_FJSX):
                self.get_rgb(RgbEnumG.FJ_SX, True)  # 史诗
                self.get_rgb(RgbEnumG.FJ_SX2, True)  # 史诗
                if self.get_rgb(RgbEnumG.FJ_TY, True):
                    _FJSX_FLAG = True
            elif self.get_rgb(RgbEnumG.CSFJ_M):  # 出售界面
                if _OVER and _FJ_OVER:
                    self.back(self.serialno)
                else:
                    if not _OVER:
                        if not self.get_rgb(RgbEnumG.CS_NULL):
                            if not _SX_FLAG:
                                self.air_touch((68, 677), touch_wait=1)  # 打开筛选
                                # self.crop_image_find(ImgEnumG.BAG_SX)
                            else:
                                _OVER = True
                                self.crop_image_find(ImgEnumG.MR_TIP_CLOSE)
                        else:
                            self.get_rgb(RgbEnumG.CS_QR, True)
                            if self.get_rgb(RgbEnumG.QR, True, touch_wait=2):
                                _OVER = True
                    elif not _FJ_OVER:
                        if self.get_rgb(RgbEnumG.FJ_NULL):  # 分解栏空
                            if not _FJSX_FLAG:
                                self.air_touch((68, 677), touch_wait=1)
                            else:
                                _FJ_OVER = True
                        else:
                            self.get_rgb(RgbEnumG.CS_QR, True)
                            if self.get_rgb(RgbEnumG.QR, True, touch_wait=2):
                                _FJ_OVER = True
            elif self.get_rgb(RgbEnumG.FJ_END, True, touch_wait=5):
                _FJ_OVER = True
            elif self.get_rgb(RgbEnumG.BAG_M):
                if _OVER and _FJ_OVER:
                    self.back(self.serialno)
                else:
                    if not _OVER:
                        self.get_rgb(RgbEnumG.CS, True)
                    elif not _FJ_OVER:
                        self.get_rgb(RgbEnumG.FJ, True)
            else:
                self.check_close()
        raise ControlTimeOut(r'出售背包-异常超时')

    def calculationgold(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _GOLD_NUM = LoadConfig.getconf(self.mnq_name, '金币', ini_name=self.mnq_name)
        _T_GOLD = 0
        _C_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _C_OVER:
                    select_queue.task_over('CheckGold')
                    return True
                self.air_touch((1170, 39), touch_wait=2)
            elif self.get_rgb(RgbEnumG.BAG_GOLD_QR):
                if _C_OVER:
                    self.get_rgb(RgbEnumG.BAG_GOLD_QR, True)
                else:
                    _res = self.get_roleinfo([(694, 368, 927, 412), (398, 370, 630, 413)])
                    GOLD = _res[0]
                    RED_COIN = _res[-1]
                    _T_GOLD = GOLD - int(_GOLD_NUM)
                    self.sn.table_value.emit(self.mnq_name, 6, f"{GOLD}")
                    self.sn.table_value.emit(self.mnq_name, 7, f"{round(_T_GOLD / 10000, 2)}万")
                    LoadConfig.writeconf(self.mnq_name, '产金量', str(_T_GOLD), ini_name=self.mnq_name)
                    LoadConfig.writeconf(self.mnq_name, '金币', str(GOLD), ini_name=self.mnq_name)
                    LoadConfig.writeconf(self.mnq_name, '红币', str(RED_COIN), ini_name=self.mnq_name)
                    _C_OVER = True
            elif self.get_rgb(RgbEnumG.BAG_M):
                if _C_OVER:
                    self.back(self.serialno)
                else:
                    r = self.get_roleinfo([(225, 162, 326, 187), (253, 218, 307, 243), (315, 505, 469, 536)])
                    LEVEL = r[0]
                    STAR = r[1]
                    BAT_NUM = r[-1]
                    if LEVEL > 0:
                        self.sn.table_value.emit(self.mnq_name, 3, f"{LEVEL}")
                        self.sn.table_value.emit(self.mnq_name, 4, f"{STAR}")
                        self.sn.table_value.emit(self.mnq_name, 5, f"{BAT_NUM}")
                        LoadConfig.writeconf(self.mnq_name, '等级', str(LEVEL), ini_name=self.mnq_name)
                        LoadConfig.writeconf(self.mnq_name, '星力', str(STAR), ini_name=self.mnq_name)
                        LoadConfig.writeconf(self.mnq_name, '战力', str(BAT_NUM), ini_name=self.mnq_name)
                        self.crop_image_find(ImgEnumG.BAG_GOLD, touch_wait=2)
        raise ControlTimeOut(r'计算产出-异常超时')
