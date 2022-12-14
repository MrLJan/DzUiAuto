# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import ControlTimeOut, BagFullerr, FuHuoRoleErr
from Utils.LoadConfig import LoadConfig


class UpRoleG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(UpRoleG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def upequip(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _SX = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):  # 游戏界面
                self.find_info('ui_enum', True)
            elif self.get_rgb(RgbEnumG.TJP_SJ_M):  # 进入铁匠铺
                if self.get_rgb(RgbEnumG.TJP_SJ_BTN_F, True):  # 强化按钮
                    if _SX:
                        self.back()
                        self.back()
                        self.sn.log_tab.emit(self.mnq_name, r"无升级材料或金币不足,升级结束")
                        select_queue.task_over('UpEquip')
                        return 1
                    if self.crop_image_find(ImgEnumG.EQ_WZB, False):  # 装备槽
                        zb_list = self.find_zbz()
                        if len(zb_list) == 0:
                            self.sn.log_tab.emit(self.mnq_name, r"无可升级装备")
                            select_queue.task_over('upequip')
                            return 1
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"选择装备")
                            self.air_touch(zb_list[0])
                    elif self.get_rgb(RgbEnumG.TJP_SJXZ_BTN, True):
                        pass
                else:
                    self.get_rgb(RgbEnumG.TJP_SJ_BTN, True)
            elif self.get_rgb(RgbEnumG.TJP_SJ_XZ):
                if _SX:
                    self.get_rgb(RgbEnumG.TJP_SJ_XZ, True)
                elif self.find_info('zb_sjset'):
                    self.sn.log_tab.emit(self.mnq_name, f"升级装备筛选")
                    self.get_rgb([375, 557, 'C2C5CA'], True)
                    self.get_rgb([739, 296, 'AEB8C2'], True)
                    self.get_rgb([478, 344, 'AEB8C2'], True)
                    self.get_rgb([572, 345, 'AEB8C2'], True)
                    self.get_rgb(RgbEnumG.TJP_SJ_XZ, True)
                    _SX = True
                else:
                    self.air_swipe((912, 507), (912, 303), swipe_wait=2)
            elif self.get_rgb(RgbEnumG.TJP_SJ_BTN, True, touch_wait=5):
                if not self.crop_image_find(ImgEnumG.EQ_UP):
                    self.sn.log_tab.emit(self.mnq_name, r"无升级材料或金币不足,升级结束")
                    self.back()
                    self.back()
                    select_queue.task_over('UpEquip')
                    return 1
                if self.crop_image_find(ImgEnumG.EQ_UP_QR):
                    self.sn.log_tab.emit(self.mnq_name, f"升级")
            # elif self.ocr_find(ImgEnumG.EQ_UP_OCR):
            elif self.find_info('ui_set'):  # 菜单界面
                # self.ocr_find(ImgEnumG.EQ_TJP_OCR, True)
                self.enum_find('tjp', True)
            elif self.find_info('zb_sj'):
                self.sn.log_tab.emit(self.mnq_name, f"进入装备升级")
                self.air_touch((84, 268), touch_wait=5)
            elif self.get_rgb(RgbEnumG.TJP_SJ_BTN, True, touch_wait=5):
                pass
            else:
                self.check_close()
        return 0

    def buyyao(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        hp_level = ImgEnumG.YS_LEVEL[kwargs['商店设置']['HP等级']]
        mp_level = ImgEnumG.YS_LEVEL[kwargs['商店设置']['MP等级']]
        s_time = time.time()
        _HP = False  # 是否购买HP
        _MP = False
        _CHECK = False
        _YS_TYPE = 0  # 区分HP,MP是否被装备
        _RES = False  # 是否购买成功
        _USE_MP = kwargs['挂机设置']['无蓝窗口']
        _NUM_HP = kwargs['商店设置']['HP数量']  # 购买数量
        _NUM_MP = kwargs['商店设置']['MP数量']  # 购买数量
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.get_rgb(RgbEnumG.FUHUO_BTN):
                if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                    raise FuHuoRoleErr
            if self.find_info('ingame_flag2'):
                if not _CHECK:
                    _res = self.check_hp_mp()
                    if 'HP' in _res:
                        self.sn.log_tab.emit(self.mnq_name, f"需要购买HP")
                        _HP = True
                    if _USE_MP:
                        if 'MP' in _res:
                            self.sn.log_tab.emit(self.mnq_name, f"需要购买MP")
                            _MP = True
                    _CHECK = True
                if self.crop_image_find(ImgEnumG.BAG_MAX_IMG):
                    self.sn.log_tab.emit(self.mnq_name, f"背包满了,清理背包")
                    raise BagFullerr
                if _HP:
                    self.air_touch((1148, 364), duration=2)
                    _YS_TYPE = 1
                elif _MP:
                    self.air_touch((1230, 356), duration=2)
                    _YS_TYPE = 2
                else:
                    select_queue.task_over('BuyY')
                    return -1
            elif self.get_rgb(RgbEnumG.YS_LOGIN):  # 登录药水界面
                if _RES:
                    if self.ys_contrl('ys_dl'):
                        _RES = False
                        if _YS_TYPE == 1 and _HP:
                            _HP = False
                        elif _YS_TYPE == 2 and _MP:
                            _MP = False
                    else:
                        raise BagFullerr  # 包满清理
                else:
                    if self.ys_contrl('ys_dl'):
                        _RES = False
                        if _YS_TYPE == 1 and _HP:
                            self.sn.log_tab.emit(self.mnq_name, f"装备HP")
                            _HP = False
                        elif _YS_TYPE == 2 and _MP:
                            self.sn.log_tab.emit(self.mnq_name, f"装备MP")
                            _MP = False
                    elif self.ys_contrl('ys_ljqw'):
                        self.sn.log_tab.emit(self.mnq_name, f"前往商店")
                        self.time_sleep(3)
                    else:
                        raise BagFullerr
            elif self.ys_contrl('ys_ljqw'):
                self.sn.log_tab.emit(self.mnq_name, f"前往商店")
                self.time_sleep(3)
            elif self.get_rgb(RgbEnumG.YS_GMQR):
                if self.get_rgb(RgbEnumG.YS_GMQR, True):
                    _RES = True
            elif self.get_rgb(RgbEnumG.YS_XQ):
                self.air_touch((940, 638), duration=2)
                if _YS_TYPE == 1:
                    # if self.ocr_find([(733, 631, 810, 658), _NUM_HP]):
                    _res_num = self.check_put_num(0)
                    if str(_NUM_HP) == _res_num:
                        self.get_rgb(RgbEnumG.YS_XQ, True)
                    else:
                        for _N in _NUM_HP:
                            self.air_touch(ImgEnumG.YS_NUM[_N], touch_wait=1)
                else:
                    # if self.ocr_find([(733, 631, 810, 658), _NUM_MP]):
                    _res_num = self.check_put_num(0)
                    if str(_NUM_MP) == _res_num:
                        self.get_rgb(RgbEnumG.YS_XQ, True)
                    else:
                        for _N in _NUM_MP:
                            self.air_touch(ImgEnumG.YS_NUM[_N], touch_wait=1)
            elif self.get_rgb(RgbEnumG.YS_SHOP):
                if _RES:
                    self.back()
                else:
                    if _HP:
                        self.air_touch(hp_level)
                    elif _MP:
                        self.air_touch(mp_level)
                    else:
                        self.back()
            elif self.find_info('LB_close', True):
                pass
            else:
                if time.time() - s_time > 30:
                    s_time = time.time()
                    self.check_close()
        raise ControlTimeOut(r'买药异常超时')

    def useskill(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _ZB_JN = False  # 技能是否装备完成
        _ZB_JN_POS = [
            [1017, 253, '4C87AF'], [1017, 383, '4C87AF'],
            [1017, 513, '4C87AF'], [1017, 643, '4C87AF']
        ]
        _ZB_FLAG = 0
        _ZB_JN_NUM = 0
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.get_rgb(RgbEnumG.FUHUO_BTN):
                if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                    raise FuHuoRoleErr
            if self.find_info('ingame_flag2'):  # 游戏界面
                self.find_info('ui_enum', True)
            elif self.find_info('ui_set'):  # 菜单界面
                # self.ocr_find(ImgEnumG.MENU_JN, True)
                self.enum_find('skill', True)
            elif self.get_rgb(RgbEnumG.SKILL_M):
                if self.get_rgb([491, 396, '4C87AF'], True):
                    self.get_rgb([723, 532, 'EE7047'], True)
                if _ZB_JN:
                    self.back()
                    self.back()
                    select_queue.task_over('UseSkill')
                    if 90 > kwargs['角色信息']['等级'] >= 60:
                        LoadConfig.writeconf(self.mnq_name, '60级', '1', ini_name=self.mnq_name)
                    elif kwargs['角色信息']['等级'] >= 100:
                        LoadConfig.writeconf(self.mnq_name, '100级', '1', ini_name=self.mnq_name)
                    elif kwargs['角色信息']['等级'] >= 90:
                        LoadConfig.writeconf(self.mnq_name, '90级', '1', ini_name=self.mnq_name)
                    return -1
                else:
                    if self.get_rgb(RgbEnumG.SKILL_CJN):
                        self.air_touch((132, 399), touch_wait=1)
                    else:
                        if _ZB_JN_NUM == 0:
                            for _pos in _ZB_JN_POS:
                                if self.get_rgb(_pos):
                                    _ZB_JN_NUM += 1
                        else:
                            if _ZB_FLAG == _ZB_JN_NUM:
                                _ZB_JN = True
                            else:
                                self.air_touch((_ZB_JN_POS[_ZB_FLAG][0], _ZB_JN_POS[_ZB_FLAG][1]), touch_wait=1)
                                self.air_touch(GlobalEnumG.JN_POS[_ZB_FLAG], touch_wait=1)
                                _ZB_FLAG += 1
            else:
                if self.get_rgb([723, 532, 'EE7047'], True):
                    pass
                elif time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    if not self.check_close():
                        return -1
        raise ControlTimeOut(r'装备技能-异常超时')

    def usepet(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _PET1 = False  # 宠物栏是否装备宠物
        _PET2 = False
        _PET3 = False
        _C_JN = False  # 装技能
        _JN_OVER = False  # 技能装备完成
        _JN_POS_LIST = [[349, 539, 'DDDEE2'], [407, 540, 'DDDEE2'],
                        [521, 545, 'DDDEE2'], [618, 541, 'DDDEE2']]  # 技能登录list
        _JN_FLAG = 0
        _PET_FLAG = 1  # 宠物栏位置顺序
        _PET_TYPE = None  # 确定宠物种类
        _PET_POS = ImgEnumG.PET_POS  # 宠物侧边栏是否被选中
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):  # 游戏界面
                if self.find_info('ui_enum', True):
                    self.time_sleep(GlobalEnumG.TouchWaitTime)
            elif self.find_info('ui_set'):  # 菜单界面
                # self.ocr_find(ImgEnumG.MENU_CW, True)  # 宠物
                self.enum_find('pet', True)
            elif self.get_rgb(RgbEnumG.ZB_XQ):  # 宠物装备-详情
                if self.get_rgb([1143, 622, 'EB7245'], True):
                    if _PET_FLAG == 1:
                        _PET1 = True
                    elif _PET_FLAG == 2:
                        _PET2 = True
                    elif _PET_FLAG == 3:
                        _PET3 = True
                    _PET_FLAG += 1
                    if _PET_FLAG > 3:
                        _PET_FLAG = 1
                elif self.get_rgb([1143, 622, 'C3C3C3']):
                    if _PET_FLAG == 1:
                        _PET1 = True
                    elif _PET_FLAG == 2:
                        _PET2 = True
                    elif _PET_FLAG == 3:
                        _PET3 = True
                    _PET_FLAG += 1
                    if _PET_FLAG > 3:
                        _PET_FLAG = 1
                    self.back()

            elif self.get_rgb(RgbEnumG.PET_JN):
                if _C_JN:
                    if self.get_rgb([821, 205, 'C3C3C3']):
                        _JN_OVER = True
                    self.get_rgb(RgbEnumG.PET_JN_LOGIN1, True)
                    self.get_rgb(RgbEnumG.PET_JN_LOGIN2, True)
                    self.crop_image_find(ImgEnumG.BUY_YS_LOGIN)
                    self.crop_image_find(ImgEnumG.JN_LOGIN_2)
                    _C_JN = False
                    _JN_FLAG += 1
                else:
                    self.back()
            elif self.get_rgb(RgbEnumG.PET_M):  # 宠物界面
                if _PET1 and _PET2 and _PET3 and _JN_OVER:
                    self.back()
                    self.back()
                    select_queue.task_over('UsePet')
                    kwargs['角色信息']['宠物'] = '1'
                    LoadConfig.writeconf(self.mnq_name, '宠物', kwargs['角色信息']['宠物'], ini_name=self.mnq_name)
                    return 1
                if _PET1 and _PET2 and _PET3 and not _JN_OVER:
                    if not self.get_rgb(RgbEnumG.PET_FEVER_JN, True):  # 点开Ferver技能槽
                        if _JN_FLAG > 4:
                            _JN_OVER = True
                        else:
                            for _ in _JN_POS_LIST:
                                if self.get_rgb(_, True):
                                    _C_JN = True
                                else:
                                    _JN_FLAG += 1
                    else:
                        _C_JN = True
                else:
                    if _PET_TYPE:
                        self.get_rgb([_PET_POS[_PET_FLAG][0], _PET_POS[_PET_FLAG][1], _PET_POS[_PET_FLAG][2]], True)
                        if self.get_rgb([_PET_POS[_PET_FLAG][0], _PET_POS[_PET_FLAG][1], _PET_POS[_PET_FLAG][-1]]):
                            if self.get_rgb(RgbEnumG.PET_NULL) or self.check_mulpic([ImgEnumG.PET_1,
                                                                                     ImgEnumG.PET_2],
                                                                                    clicked=False):
                                self.crop_image_find(ImgEnumG.CW_TYPE[_PET_TYPE][_PET_FLAG - 1])
                            else:
                                if _PET_FLAG == 1:
                                    _PET1 = True
                                elif _PET_FLAG == 2:
                                    _PET2 = True
                                elif _PET_FLAG == 3:
                                    _PET3 = True
                                _PET_FLAG += 1
                                if _PET_FLAG > 3:
                                    _PET_FLAG = 1
                    else:
                        if self.crop_image_find(ImgEnumG.CW_TYPE['A'][0], False):
                            _PET_TYPE = 'A'
                        elif self.crop_image_find(ImgEnumG.CW_TYPE['B'][0], False):
                            _PET_TYPE = 'B'
                        elif self.crop_image_find(ImgEnumG.CW_TYPE['C'][0], False):
                            _PET_TYPE = 'C'
                        else:
                            _PET1 = _PET2 = _PET3 = True  # 无宠物
            else:
                self.check_close()
        raise ControlTimeOut(r'装备宠物-异常超时')

    def strongequip(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _QH_LEVEL = kwargs['强化设置']['目标等级']  # 强化目标等级
        _USE_BH = kwargs['强化设置']['保护卷轴']  # 使用道具
        _USE_DP = kwargs['强化设置']['盾牌卷轴']
        _USE_XY = kwargs['强化设置']['幸运卷轴']
        _USE_ZK = kwargs['强化设置']['强化优惠卷']
        _ZB_LIST = []  # 存放穿戴中装备坐标
        _POS = 0  # 装备序号
        _QH_OVER = False  # 是否强化完成
        _QH_FLAG = False  # 点击强化后
        _WITE = 0
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):  # 游戏界面
                self.find_info('ui_enum', True)
            elif self.get_rgb(RgbEnumG.QH_JG, True):  # 星力强化结果
                pass
            elif self.get_rgb(RgbEnumG.QH_BTN, True):  # 强化星
                pass
            elif self.get_rgb(RgbEnumG.TJP_QH_M):  # 进入铁匠铺
                if _QH_OVER:
                    self.sn.log_tab.emit(self.mnq_name, f"强化-完成")
                    self.back()
                    self.back()
                    select_queue.task_over('StrongEquip')
                    return 1
                if len(_ZB_LIST) == 0:
                    _ZB_LIST = self.find_zbz()
                    if len(_ZB_LIST) == 0:
                        _QH_OVER = True
                if self.get_rgb(RgbEnumG.TJP_QH_BTN_F):
                    if _QH_FLAG:
                        self.sn.log_tab.emit(self.mnq_name, f"检查装备中装备")
                        res = self.find_zbz()
                        if len(res) != len(_ZB_LIST):
                            _ZB_LIST = res
                            _POS = 0
                            _QH_FLAG = False
                    if _POS == len(_ZB_LIST):
                        _QH_OVER = True
                    else:
                        self.air_touch(_ZB_LIST[_POS])
                        _POS += 1
                else:
                    if not self.air_loop_find(ImgEnumG.EQ_UP_QR):  # 确认
                        now_level = self.check_time_num(1)
                        if int(now_level) < int(_QH_LEVEL):
                            if _USE_XY:
                                self.get_rgb(RgbEnumG.QH_XYJ, True)
                            if _USE_DP:
                                self.get_rgb(RgbEnumG.QH_DP, True)
                            if _USE_BH:
                                self.get_rgb(RgbEnumG.QH_BH, True)
                            if _USE_ZK:
                                self.air_touch((446, 552), touch_wait=1)
                            if self.get_rgb(RgbEnumG.TJP_QH_BTN, True):
                                self.sn.log_tab.emit(self.mnq_name, f"强化")
                                _QH_FLAG = True
                        else:
                            self.air_touch((453, 162), touch_wait=1)
            elif self.find_info('ui_set'):  # 菜单界面
                if self.find_info('zb_qh'):
                    self.sn.log_tab.emit(self.mnq_name, f"进入星力强化")
                    self.air_touch((208, 259), touch_wait=2)
                else:
                    self.enum_find('tjp', True)
            elif self.find_info('zb_qh'):
                self.sn.log_tab.emit(self.mnq_name, f"进入星力强化")
                self.air_touch((208, 259), touch_wait=2)
            else:
                if _WITE > 10:
                    self.check_close()
                    _WITE = 0
                _WITE += 1
                self.time_sleep(2)
        raise ControlTimeOut(r'强化装备-异常超时')
