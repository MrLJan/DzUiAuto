# -*- encoding=utf8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG
from UiPage.BasePage import BasePageG


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
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):  # 游戏界面
                self.crop_image_find(ImgEnumG.MR_MENU)
            if self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.EQ_TJP_OCR, True)
            elif self.ocr_find(ImgEnumG.EQ_UP_OCR):
                self.air_touch((84, 268))
            elif self.ocr_find(ImgEnumG.TJP_UI_OCR):  # 进入铁匠铺
                if self.crop_image_find(ImgEnumG.EQ_WZB):  # 装备槽
                    zb_list = self.get_all_text(ImgEnumG.EQ_ZBZ_OCR)
                    if len(zb_list) == 0:
                        self.sn.log_tab.emit(self.mnq_name, r"无可升级装备")
                        select_queue.task_over('upequip')
                        return 1
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"选择装备")
                        self.air_touch(zb_list[0])
                if not self.crop_image_find(ImgEnumG.EQ_UP):  # 强化按钮
                    self.crop_image_find(ImgEnumG.EQ_ZDXZ)  # 自动选择
                    if self.ocr_find(ImgEnumG.EQ_ZDXZ_UI_OCR):
                        if self.ocr_find(ImgEnumG.EQ_ZDXZ_SD_OCR):
                            self.get_rgb(375, 557, 'C2C5CA', True)
                            self.get_rgb(739, 296, 'AEB8C2', True)
                            self.get_rgb(478, 344, 'AEB8C2', True)
                            self.get_rgb(572, 345, 'AEB8C2', True)
                            if self.crop_image_find(ImgEnumG.UI_QR):
                                if not self.crop_image_find(ImgEnumG.EQ_UP):
                                    self.sn.log_tab.emit(self.mnq_name, r"无升级材料或金币不足,升级结束")
                                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                                    select_queue.task_over('upequip')
                                    return 1
                                self.crop_image_find(ImgEnumG.EQ_UP_QR, timeout=20)
                        else:
                            self.air_swipe((912, 507), (912, 303))
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    if not self.close_window():
                        return 0
        return 0

    def buyyao(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        hp_level = ImgEnumG.YS_LEVEL[kwargs['商店设置']['HP等级']]
        mp_level = ImgEnumG.YS_LEVEL[kwargs['商店设置']['MP等级']]
        s_time = time.time()
        _HP = False  # 是否购买HP
        _MP = False
        _YS_TYPE = 0  # 区分HP,MP是否被装备
        _RES = False  # 是否购买成功
        _NUM_HP = ImgEnumG.YS_NUM[kwargs['商店设置']['HP数量']]  # 购买数量
        _NUM_MP = ImgEnumG.YS_NUM[kwargs['商店设置']['MP数量']]  # 购买数量
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if self.ocr_find(ImgEnumG.HP_NULL_OCR):
                    _HP = True
                if self.ocr_find(ImgEnumG.MP_NULL_OCR):
                    _MP = True
                if _HP:
                    self.air_touch((1148, 364), duration=2)
                    _YS_TYPE = 1
                elif _MP:
                    self.air_touch((1230, 356), duration=2)
                    _YS_TYPE = 2
                else:
                    select_queue.task_over('BuyY')
                    return -1
            elif self.ocr_find(ImgEnumG.BUY_MP_LOGIN):  # 登录药水界面
                if _RES:
                    if self.crop_image_find(ImgEnumG.BUY_YS_LOGIN):
                        _RES = False
                        if _YS_TYPE == 1 and _HP:
                            _HP = False
                        elif _YS_TYPE == 2 and _MP:
                            _MP = False
                else:
                    self.crop_image_find(ImgEnumG.BUY_NOW_MOVE)  # 立即前往
            elif self.ocr_find(ImgEnumG.YS_GM_QR):
                if self.get_rgb(718, 515, 'EE7047', True):
                    _RES = True
            elif self.ocr_find(ImgEnumG.YS_GM):
                self.air_touch((873, 650), duration=2)
                if _YS_TYPE == 1:
                    self.air_touch(_NUM_HP)
                else:
                    self.air_touch(_NUM_MP)
                if _YS_TYPE == 1:
                    if self.ocr_find(ImgEnumG.YS_NUM_OCR[kwargs['商店设置']['HP数量']]):
                        self.get_rgb(1044, 629, 'EE7047', True)
                else:
                    if self.ocr_find(ImgEnumG.YS_NUM_OCR[kwargs['商店设置']['MP数量']]):
                        self.get_rgb(1044, 629, 'EE7047', True)
            elif self.ocr_find(ImgEnumG.SD_UI_OCR):
                if _RES:
                    self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                else:
                    if _HP:
                        self.air_touch(hp_level)
                    elif _MP:
                        self.air_touch(mp_level)
                    else:
                        self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    if not self.close_window():
                        return -1
        return 0

    def useskill(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _ZB_JN = False  # 技能是否装备完成
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):  # 游戏界面
                self.crop_image_find(ImgEnumG.MR_MENU)
            elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.MENU_JN, True)
            elif self.ocr_find(ImgEnumG.JN_UI_OCR):
                if _ZB_JN:
                    self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                    self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                    select_queue.task_over('UseSkill')
                    return -1
                else:
                    if self.get_rgb(125, 491, 'EE7546'):
                        self.air_touch((132, 399), touch_wait=2)
                    else:
                        jn_num = self.get_all_text(ImgEnumG.JN_ZB_OCR)
                        if len(jn_num):
                            for i in range(len(jn_num)):
                                self.air_touch(jn_num[i], touch_wait=1)
                                self.air_touch(GlobalEnumG.JN_POS[i], touch_wait=1)
                        _jn = self.find_all_pos(ImgEnumG.JN_XZ)
                        if len(_jn[-1]) >= len(jn_num) and _jn[0]:
                            _ZB_JN = True
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    if not self.close_window():
                        return -1
        return 0

    def usepet(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _PET1 = False  # 宠物栏是否装备宠物
        _PET2 = False
        _PET3 = False
        _PET_FLAG = 1  # 宠物栏位置顺序
        _PET_TYPE = None  # 确定宠物种类
        _PET_POS = ImgEnumG.PET_POS  # 宠物侧边栏是否被选中
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):  # 游戏界面
                self.crop_image_find(ImgEnumG.MR_MENU)
            elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.MENU_CW, True)  # 宠物
            elif self.ocr_find(ImgEnumG.USE_CW):  # 宠物装备
                if self.ocr_find(ImgEnumG.USE_CW, True):
                    if _PET_FLAG == 1:
                        _PET1 = True
                    elif _PET_FLAG == 2:
                        _PET2 = True
                    elif _PET_FLAG == 3:
                        _PET3 = True
                    _PET_FLAG += 1
                    if _PET_FLAG > 3:
                        _PET_FLAG = 1
            elif self.ocr_find(ImgEnumG.CW_UI_OCR):  # 宠物界面
                if _PET1 and _PET2 and _PET3:
                    self.crop_image_find(ImgEnumG.MR_TIP_CLOSE)
                    self.crop_image_find(ImgEnumG.MR_TIP_CLOSE)
                    select_queue.task_over('UsePet')
                    return 1
                if _PET_TYPE:
                    self.get_rgb(_PET_POS[_PET_FLAG][0], _PET_POS[_PET_FLAG][1], _PET_POS[_PET_FLAG][2], True)
                    if self.get_rgb(_PET_POS[_PET_FLAG][0], _PET_POS[_PET_FLAG][1], _PET_POS[_PET_FLAG][-1]):
                        if self.ocr_find(ImgEnumG.CW_NULL):
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
                        select_queue.task_over('UsePet')
                        return 1  # 无宠物
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    if not self.close_window():
                        return 0
        return 0

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
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):  # 游戏界面
                self.crop_image_find(ImgEnumG.MR_MENU)
            elif self.ocr_find(ImgEnumG.EQ_QH_OCR):  # 星力强化
                self.air_touch((210, 263), touch_wait=1)
            elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.EQ_TJP_OCR, True)  # 铁匠铺
            elif self.ocr_find(ImgEnumG.TJP_UI_OCR):  # 进入铁匠铺
                if _QH_OVER:
                    self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                    self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                    select_queue.task_over('StrongEquip')
                    return 1
                if len(_ZB_LIST) == 0:
                    _ZB_LIST = self.get_all_text(ImgEnumG.EQ_ZBZ_OCR)
                    if len(_ZB_LIST) == 0:
                        _QH_OVER = True
                if self.ocr_find(ImgEnumG.EQ_QH_NULL):
                    if _QH_FLAG:
                        res = self.get_all_text(ImgEnumG.EQ_ZBZ_OCR)
                        if len(res) != len(_ZB_LIST):
                            _ZB_LIST = res
                            _POS = 0
                            _QH_FLAG = False
                    else:
                        if _POS == len(_ZB_LIST):
                            _QH_OVER = True
                        else:
                            self.air_touch(_ZB_LIST[_POS])
                            _POS += 1
                else:
                    if not self.air_loop_find(ImgEnumG.EQ_UP_QR):  # 确认
                        now_level = self.get_num((281, 280, 368, 329))
                        if now_level < _QH_LEVEL:
                            if _USE_XY:
                                self.get_rgb(206, 552, 'DEDFE3', True, 1)
                            if _USE_DP:
                                self.get_rgb(287, 553, 'DEDFE3', True, 1)
                            if _USE_BH:
                                self.get_rgb(369, 553, 'DEDFE3', True, 1)
                            if _USE_ZK:
                                self.air_touch((446, 552), touch_wait=1)
                            if self.get_rgb(605, 662, 'EE7047', True, 2):
                                _QH_FLAG = True
                        else:
                            self.air_touch((453, 162), touch_wait=1)
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    if not self.close_window():
                        return 0
        return 0
