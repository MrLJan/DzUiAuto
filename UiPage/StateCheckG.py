# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.LoadConfig import LoadConfig


class StateCheckG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn, ocr):
        super(StateCheckG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.cn_ocr = ocr

    def choose_task(self, **kwargs):
        exec_queue = kwargs['状态队列']['执行器']
        select_queue = kwargs['状态队列']['选择器']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        if select_queue.queue.empty():
            if not self.check_hp_mp(use_mp):
                select_queue.put_queue('BuyY')
            if self.ocr_find(ImgEnumG.BAG_FULL):
                select_queue.put_queue('BagSell')
        else:
            if not self.check_hp_mp(use_mp):
                select_queue.put_queue('BuyY')
            if self.ocr_find(ImgEnumG.BAG_FULL):
                select_queue.put_queue('BagSell')
            if self.check_team():
                select_queue.put_queue('ChooseTeam')
            if select_queue.queue.empty():
                return 1

    def check_hp_mp(self, use_mp):
        if self.ocr_find(ImgEnumG.HP_NULL_OCR):
            return False
        if self.ocr_find(ImgEnumG.MP_NULL_OCR) and use_mp:
            return False
        return True

    def check_team(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut / 2:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.TEAM_TAB)
                if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                    return True
                else:
                    return False
            else:
                self.check_close()
        return False

    def close_all(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                return True
            elif self.crop_image_find(ImgEnumG.GAME_ICON, False):
                self.sn.log_tab.emit(self.mnq_name, r"掉线")
                return True
            elif self.air_loop_find(ImgEnumG.MR_BAT_EXIT):
                self.ocr_find(ImgEnumG.MR_YDZXD, clicked=True)
            else:
                self.check_close()
        return False

    def check_roleinfo(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _C_OVER = False  # 检查是否完成
        RED_GOLD = 0  # 红币
        GOLD = 0  # 金币
        BAT_NUM = 0  # 战力
        LEVEL = 0  # 等级
        STAR = 0  # 星力
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _C_OVER:
                    kwargs['角色信息']['等级'] = LEVEL
                    kwargs['角色信息']['星力'] = STAR
                    kwargs['角色信息']['战力'] = BAT_NUM
                    kwargs['角色信息']['金币'] = GOLD
                    kwargs['角色信息']['红币'] = RED_GOLD
                    self.sn.table_value.emit(self.mnq_name, 3, f"{LEVEL}")
                    self.sn.table_value.emit(self.mnq_name, 4, f"{STAR}")
                    self.sn.table_value.emit(self.mnq_name, 5, f"{BAT_NUM}")
                    self.sn.table_value.emit(self.mnq_name, 6, f"{GOLD}")
                    self.sn.log_tab.emit(self.mnq_name, f"等级：{LEVEL}_星力{STAR}_战力{BAT_NUM}_金币{GOLD}")
                    select_queue.task_over('CheckRole')
                    return True
                self.air_touch((1170, 39), touch_wait=3)
            elif self.get_rgb(RgbEnumG.BAG_GOLD_QR):
                if _C_OVER:
                    self.get_rgb(RgbEnumG.BAG_GOLD_QR, True)
                else:
                    res = self.get_roleinfo([(694, 368, 927, 412), (398, 370, 630, 413)])
                    GOLD = res[0]
                    RED_GOLD = res[-1]
                    LoadConfig.writeconf(self.mnq_name, '金币', str(GOLD), ini_name=self.mnq_name)
                    LoadConfig.writeconf(self.mnq_name, '红币', str(RED_GOLD), ini_name=self.mnq_name)
                    _C_OVER = True
            elif self.get_rgb(RgbEnumG.BAG_M):
                self.time_sleep(1)
                if _C_OVER:
                    self.back(self.serialno)
                else:
                    _res = self.get_roleinfo([(225, 162, 326, 187), (253, 218, 307, 243), (315, 505, 469, 536)])
                    LEVEL = _res[0]
                    STAR = _res[1]
                    BAT_NUM = _res[-1]
                    if LEVEL > 0:
                        LoadConfig.writeconf(self.mnq_name, '等级', str(LEVEL), ini_name=self.mnq_name)
                        LoadConfig.writeconf(self.mnq_name, '星力', str(STAR), ini_name=self.mnq_name)
                        LoadConfig.writeconf(self.mnq_name, '战力', str(BAT_NUM), ini_name=self.mnq_name)
                        self.crop_image_find(ImgEnumG.BAG_GOLD, touch_wait=2)
            else:
                self.check_close()
