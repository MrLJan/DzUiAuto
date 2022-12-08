# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG, WorldEnumG, MulColorEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import ControlTimeOut, BagFullerr, FuHuoRoleErr
from Utils.LoadConfig import LoadConfig


class UpRoleG(BasePageG):
    def __init__(self, devinfo, sn):
        super(UpRoleG, self).__init__()
        self.dev, self.mnq_name = devinfo
        self.sn = sn

    def upequip(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _SX = False
        _GET_ZB = False  # 获取升级装备列表
        zb_list = []
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):  # 游戏界面
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.cmp_rgb(RgbEnumG.TJP_SJ_M):  # 进入铁匠铺
                if self.cmp_rgb(RgbEnumG.TJP_SJ_BTN_F, True):  # 升级按钮
                    if _SX:
                        self.back()
                        self.back()
                        self.sn.log_tab.emit(self.mnq_name, r"无升级材料或金币不足,升级结束")
                        select_queue.task_over('UpEquip')
                        return 1
                    if not _GET_ZB:
                        # if self.pic_find(ImgEnumG.EQ_WZB, False):  # 装备槽
                        zb_list = self.find_zbz()
                        if len(zb_list) == 0:
                            self.sn.log_tab.emit(self.mnq_name, r"无可升级装备")
                            select_queue.task_over('upequip')
                            return 1
                        else:
                            _GET_ZB = True
                    elif self.cmp_rgb(RgbEnumG.TJP_SJXZ_BTN, True):
                        pass
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"选择装备")
                        self.touch(zb_list[0], touch_wait=2)

                else:
                    self.cmp_rgb(RgbEnumG.TJP_SJ_BTN, True)
            elif self.cmp_rgb(RgbEnumG.TJP_SJ_XZ):
                if _SX:
                    self.cmp_rgb(RgbEnumG.TJP_SJ_XZ, True)
                elif self.word_find(WorldEnumG.SJ_SET):
                    self.sn.log_tab.emit(self.mnq_name, f"升级装备筛选")
                    self.cmp_rgb([375, 557, 'c3c6ca'], True)
                    self.cmp_rgb([739, 296, 'aeb8c3'], True)
                    self.cmp_rgb([478, 344, 'aeb8c3'], True)
                    self.cmp_rgb([572, 345, 'aeb8c3'], True)
                    self.cmp_rgb(RgbEnumG.TJP_SJ_XZ, True)
                    _SX = True
                else:
                    self.dm_swipe((912, 507), (912, 303), swipe_wait=2)
            elif self.cmp_rgb(RgbEnumG.TJP_SJ_BTN, True, touch_wait=5):
                if not self.pic_find(ImgEnumG.EQ_UP):
                    self.sn.log_tab.emit(self.mnq_name, r"无升级材料或金币不足,升级结束")
                    self.back()
                    self.back()
                    select_queue.task_over('UpEquip')
                    return 1
                if self.pic_find(ImgEnumG.EQ_UP_QR):
                    self.sn.log_tab.emit(self.mnq_name, f"升级")
            # elif self.ocr_find(ImgEnumG.EQ_UP_OCR):
            elif self.word_find(WorldEnumG.SET_BTN):  # 菜单界面
                # self.ocr_find(ImgEnumG.EQ_TJP_OCR, True)
                self.enum_find('铁匠铺', True)
            elif self.word_find(WorldEnumG.ZB_SJ):
                self.sn.log_tab.emit(self.mnq_name, f"进入装备升级")
                self.touch((84, 268), touch_wait=5)
            elif self.cmp_rgb(RgbEnumG.TJP_SJ_BTN, True, touch_wait=5):
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
            if self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                if self.pic_find(ImgEnumG.CZ_FUHUO):
                    raise FuHuoRoleErr
            if self.find_color(MulColorEnumG.IGAME):
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
                if self.pic_find(ImgEnumG.BAG_MAX_IMG):
                    self.sn.log_tab.emit(self.mnq_name, f"背包满了,清理背包")
                    raise BagFullerr
                if _HP:
                    self.touch((1148, 364), duration=2)
                    _YS_TYPE = 1
                elif _MP:
                    self.touch((1230, 356), duration=2)
                    _YS_TYPE = 2
                else:
                    select_queue.task_over('BuyY')
                    return -1
            elif self.cmp_rgb(RgbEnumG.YS_LOGIN):  # 登录药水界面
                if _RES:
                    if self.word_find(WorldEnumG.YS_DL, True):
                        _RES = False
                        if _YS_TYPE == 1 and _HP:
                            _HP = False
                        elif _YS_TYPE == 2 and _MP:
                            _MP = False
                    else:
                        raise BagFullerr  # 包满清理
                else:
                    if self.word_find(WorldEnumG.YS_DL, True):
                        _RES = False
                        if _YS_TYPE == 1 and _HP:
                            self.sn.log_tab.emit(self.mnq_name, f"装备HP")
                            _HP = False
                        elif _YS_TYPE == 2 and _MP:
                            self.sn.log_tab.emit(self.mnq_name, f"装备MP")
                            _MP = False
                    elif self.word_find(WorldEnumG.YS_LJQW, True):
                        self.sn.log_tab.emit(self.mnq_name, f"前往商店")
                        self.time_sleep(3)
                    else:
                        raise BagFullerr
            elif self.word_find(WorldEnumG.YS_LJQW, True):
                self.sn.log_tab.emit(self.mnq_name, f"前往商店")
                self.time_sleep(3)
            elif self.cmp_rgb(RgbEnumG.YS_GMQR):
                if self.cmp_rgb(RgbEnumG.YS_GMQR, True):
                    _RES = True
            elif self.cmp_rgb(RgbEnumG.YS_XQ):
                self.touch((940, 638), duration=2)
                if _YS_TYPE == 1:
                    # if self.ocr_find([(733, 631, 810, 658), _NUM_HP]):
                    _res_num = self.check_put_num(0)
                    if str(_NUM_HP) == _res_num:
                        self.cmp_rgb(RgbEnumG.YS_XQ, True)
                    else:
                        for _N in _NUM_HP:
                            self.touch(ImgEnumG.YS_NUM[_N], touch_wait=1)
                else:
                    # if self.ocr_find([(733, 631, 810, 658), _NUM_MP]):
                    _res_num = self.check_put_num(0)
                    if str(_NUM_MP) == _res_num:
                        self.cmp_rgb(RgbEnumG.YS_XQ, True)
                    else:
                        for _N in _NUM_MP:
                            self.touch(ImgEnumG.YS_NUM[_N], touch_wait=1)
            elif self.cmp_rgb(RgbEnumG.YS_SHOP):
                if _RES:
                    self.back()
                else:
                    if _HP:
                        self.touch(hp_level)
                    elif _MP:
                        self.touch(mp_level)
                    else:
                        self.back()
            else:
                if time.time() - s_time > 10:
                    s_time = time.time()
                    self.check_close()
        raise ControlTimeOut(r'买药异常超时')

    def useskill(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _ZB_JN = False  # 技能是否装备完成
        _ZB_JN_POS = [
            [1017, 253, '4c87b0'], [1017, 383, '4c87b0'],
            [1017, 513, '4c87b0'], [1017, 643, '4c87b0']
        ]
        _ZB_FLAG = 0
        _ZB_JN_NUM = 0
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                if self.pic_find(ImgEnumG.CZ_FUHUO):
                    raise FuHuoRoleErr
            if self.find_color(MulColorEnumG.IGAME):  # 游戏界面
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.enum_find('技能', True):
                pass
            elif self.cmp_rgb(RgbEnumG.SKILL_M):
                if self.cmp_rgb([491, 396, '4c87b0'], True):  # 自动分配
                    if self.cmp_rgb([723, 532, 'ee7046'], True):
                        self.back()
                # if self.cmp_rgb([486,397,'c3c3c3']):#无技能点
                #     pass
                if self.cmp_rgb([1144, 251, 'ee7046'], True):  # 有技能可以加
                    self.sn.log_tab.emit(self.mnq_name, r"加技能")
                elif self.cmp_rgb([1144, 377, 'ee7046'], True):
                    self.sn.log_tab.emit(self.mnq_name, r"加技能")
                elif self.cmp_rgb([1144, 517, 'ee7046'], True):
                    self.sn.log_tab.emit(self.mnq_name, r"加技能")
                elif self.cmp_rgb([1144, 640, 'ee7046'], True):
                    self.sn.log_tab.emit(self.mnq_name, r"加技能")
                else:
                    if _ZB_JN:
                        self.back()
                        self.back()
                        self.sn.log_tab.emit(self.mnq_name, r"技能装配-完成")
                        select_queue.task_over('UseSkill')
                        if 90 > kwargs['角色信息']['等级'] >= 60:
                            LoadConfig.writeconf(self.mnq_name, '60级', '1', ini_name=self.mnq_name)
                        elif kwargs['角色信息']['等级'] >= 100:
                            LoadConfig.writeconf(self.mnq_name, '100级', '1', ini_name=self.mnq_name)
                        elif kwargs['角色信息']['等级'] >= 90:
                            LoadConfig.writeconf(self.mnq_name, '90级', '1', ini_name=self.mnq_name)
                        return -1
                    else:
                        if self.cmp_rgb(RgbEnumG.SKILL_CJN):
                            self.touch((132, 399), touch_wait=1)
                        else:
                            if _ZB_JN_NUM == 0:
                                for _pos in _ZB_JN_POS:
                                    if self.cmp_rgb(_pos):
                                        _ZB_JN_NUM += 1
                            else:
                                if _ZB_FLAG == _ZB_JN_NUM:
                                    _ZB_JN = True
                                else:
                                    self.touch((_ZB_JN_POS[_ZB_FLAG][0], _ZB_JN_POS[_ZB_FLAG][1]), touch_wait=1)
                                    self.touch(GlobalEnumG.JN_POS[_ZB_FLAG], touch_wait=1)
                                    _ZB_FLAG += 1
            else:
                if self.cmp_rgb([723, 532, 'ee7046'], True):
                    pass
                else:
                    self.check_close()

        raise ControlTimeOut(r'装备技能-异常超时')

    def usepet(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _PET1 = False  # 宠物栏是否装备宠物
        _PET2 = False
        _PET3 = False
        _C_JN = False  # 装技能
        _JN_OVER = False  # 技能装备完成
        _JN_POS_LIST = [[349, 539, 'dcdee1'], [407, 540, 'dcdee1'],
                        [521, 545, 'dcdee1'], [618, 541, 'dcdee1']]  # 技能登录list
        _JN_FLAG = 0
        _PET_FLAG = 1  # 宠物栏位置顺序
        _PET_TYPE = None  # 确定宠物种类
        _PET_POS = ImgEnumG.PET_POS  # 宠物侧边栏是否被选中
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):  # 游戏界面
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.word_find(WorldEnumG.SET_BTN):  # 菜单界面
                self.enum_find('宠物', True)
            elif self.cmp_rgb(RgbEnumG.ZB_XQ):  # 宠物装备-详情
                if self.cmp_rgb([1143, 622, 'ee7046'], True):
                    if _PET_FLAG == 1:
                        _PET1 = True
                    elif _PET_FLAG == 2:
                        _PET2 = True
                    elif _PET_FLAG == 3:
                        _PET3 = True
                    _PET_FLAG += 1
                    if _PET_FLAG > 3:
                        _PET_FLAG = 1
                elif self.cmp_rgb([1143, 622, 'c3c3c3']):
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
            elif self.cmp_rgb(RgbEnumG.PET_JN):
                if _C_JN:
                    if self.cmp_rgb([821, 205, 'c3c3c3']):
                        _JN_OVER = True
                        _C_JN = False
                    if self.word_find(WorldEnumG.YS_DL,True):
                        _C_JN = False
                        _JN_FLAG += 1
                else:
                    self.back()
            elif self.cmp_rgb(RgbEnumG.PET_M):  # 宠物界面
                if _PET1 and _PET2 and _PET3 and _JN_OVER:
                    self.sn.log_tab.emit(self.mnq_name, r"穿戴宠物-完成")
                    self.back()
                    self.back()
                    select_queue.task_over('UsePet')
                    kwargs['角色信息']['宠物'] = '1'
                    LoadConfig.writeconf(self.mnq_name, '宠物', kwargs['角色信息']['宠物'], ini_name=self.mnq_name)
                    return 1
                if _PET1 and _PET2 and _PET3 and not _JN_OVER:
                    self.sn.log_tab.emit(self.mnq_name, r"宠物装备技能")
                    if not self.cmp_rgb(RgbEnumG.PET_FEVER_JN, True):  # 点开Ferver技能槽
                        if _JN_FLAG > 4:
                            self.sn.log_tab.emit(self.mnq_name, r"宠物装备技能-完成")
                            _JN_OVER = True
                        else:
                            for _ in _JN_POS_LIST:
                                if self.cmp_rgb(_, True):
                                    _C_JN = True
                            if not _C_JN:
                                _JN_FLAG += 1
                    else:
                        _C_JN = True
                else:
                    if _PET_TYPE:
                        self.cmp_rgb([_PET_POS[_PET_FLAG][0], _PET_POS[_PET_FLAG][1], _PET_POS[_PET_FLAG][2]], True)
                        if self.cmp_rgb([_PET_POS[_PET_FLAG][0], _PET_POS[_PET_FLAG][1], _PET_POS[_PET_FLAG][-1]]):
                            if self.cmp_rgb(RgbEnumG.PET_NULL) or self.check_mulpic([ImgEnumG.PET_1,
                                                                                     ImgEnumG.PET_2],
                                                                                    clicked=False):
                                self.pic_find(ImgEnumG.CW_TYPE[_PET_TYPE][_PET_FLAG - 1])
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
                        if self.pic_find(ImgEnumG.CW_TYPE['A'][0], False):
                            _PET_TYPE = 'A'
                        elif self.pic_find(ImgEnumG.CW_TYPE['A'][1], False):
                            _PET_TYPE = 'A'
                        elif self.pic_find(ImgEnumG.CW_TYPE['A'][-1], False):
                            _PET_TYPE = 'A'
                        elif self.pic_find(ImgEnumG.CW_TYPE['B'][0], False):
                            _PET_TYPE = 'B'
                        elif self.pic_find(ImgEnumG.CW_TYPE['B'][1], False):
                            _PET_TYPE = 'B'
                        elif self.pic_find(ImgEnumG.CW_TYPE['B'][-1], False):
                            _PET_TYPE = 'B'
                        elif self.pic_find(ImgEnumG.CW_TYPE['C'][0], False):
                            _PET_TYPE = 'C'
                        elif self.pic_find(ImgEnumG.CW_TYPE['C'][1], False):
                            _PET_TYPE = 'C'
                        elif self.pic_find(ImgEnumG.CW_TYPE['C'][-1], False):
                            _PET_TYPE = 'C'
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"无可穿戴宠物")
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
            if self.find_color(MulColorEnumG.IGAME):  # 游戏界面
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.cmp_rgb(RgbEnumG.QH_JG, True):  # 星力强化结果
                pass
            elif self.cmp_rgb(RgbEnumG.QH_BTN, True):  # 强化星
                pass
            elif self.cmp_rgb(RgbEnumG.TJP_QH_M):  # 进入铁匠铺
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
                if self.cmp_rgb(RgbEnumG.TJP_QH_BTN_F):
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
                        self.touch(_ZB_LIST[_POS])
                        _POS += 1
                else:
                    if not self.pic_find(ImgEnumG.EQ_UP_QR):  # 确认
                        now_level = self.check_num(5)
                        if int(now_level) < int(_QH_LEVEL):
                            if _USE_XY:
                                self.cmp_rgb(RgbEnumG.QH_XYJ, True)
                            if _USE_DP:
                                self.cmp_rgb(RgbEnumG.QH_DP, True)
                            if _USE_BH:
                                self.cmp_rgb(RgbEnumG.QH_BH, True)
                            if _USE_ZK:
                                self.touch((446, 552), touch_wait=1)
                            if self.cmp_rgb(RgbEnumG.TJP_QH_BTN, True):
                                self.sn.log_tab.emit(self.mnq_name, f"强化")
                                _QH_FLAG = True
                        else:
                            self.touch((453, 162), touch_wait=1)
            elif self.word_find(WorldEnumG.SET_BTN):  # 菜单界面
                if self.word_find(WorldEnumG.ZB_QH):
                    self.sn.log_tab.emit(self.mnq_name, f"进入星力强化")
                    self.touch((208, 259), touch_wait=2)
                else:
                    self.enum_find('铁匠铺', True)
            elif self.word_find(WorldEnumG.ZB_QH):
                self.sn.log_tab.emit(self.mnq_name, f"进入星力强化")
                self.touch((208, 259), touch_wait=2)
            else:
                if _WITE > 10:
                    self.check_close()
                    _WITE = 0
                _WITE += 1
                self.time_sleep(2)
        raise ControlTimeOut(r'强化装备-异常超时')
