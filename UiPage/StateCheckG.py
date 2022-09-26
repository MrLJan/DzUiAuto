# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG
from UiPage.BasePage import BasePageG


class StateCheckG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(StateCheckG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def choose_task(self, **kwargs):
        exec_queue = kwargs['状态队列']['执行器']
        select_queue = kwargs['状态队列']['选择器']
        if select_queue.queue.empty():
            if not self.check_hp_mp():
                select_queue.put_queue('BuyY')
            if self.ocr_find(ImgEnumG.BAG_FULL):
                select_queue.put_queue('BagSell')
        else:
            if not self.check_hp_mp():
                select_queue.put_queue('BuyY')
            if self.ocr_find(ImgEnumG.BAG_FULL):
                select_queue.put_queue('BagSell')
            map, pd = self.check_map_pd()
            if map:
                select_queue.put_queue('ChooseXTMap')
                select_queue.put_queue('ChooseYTMap')
            if pd:
                select_queue.put_queue('ChoosePD')
            if self.check_team():
                select_queue.put_queue('ChooseTeam')
            if select_queue.queue.empty():
                return 1

    def check_hp_mp(self):
        if self.ocr_find(ImgEnumG.HP_NULL_OCR) or self.ocr_find(ImgEnumG.MP_NULL_OCR):
            return False
        return True

    def check_map_pd(self,**kwargs):
        s_time = time.time()
        _PD_NUM=kwargs['地图名']
        _MAP = False
        _PD = False
        _FLAG=False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut / 2:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _FLAG:
                    return _MAP, _PD
                self.air_touch((99, 99), duration=2)
            elif self.ocr_find(ImgEnumG.MAP_UI_OCR):
                if _FLAG:
                    self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                else:
                    pd_num = self.get_num((874, 23, 1068, 63))
                    xt_num = self.get_num((932, 105, 1236, 141))
                    map_name = self.get_num((932, 105, 1236, 141))
                    _FLAG = False
        return _MAP, _PD

    def check_team(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut / 2:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.TEAM_TAB)
                if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                    return True
                else:
                    return False
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
            elif not self.ocr_find(ImgEnumG.GAME_END):
                self.check_close()
                self.key_event(self.serialno, 'BACK')
            elif self.air_loop_find(ImgEnumG.MR_BAT_EXIT):
                self.ocr_find(ImgEnumG.MR_YDZXD, clicked=True,use_re=True)
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    self.key_event(self.serialno, 'BACK')
        return False
