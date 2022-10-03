# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import ImgEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import RestartTask, NotInGameErr


class TaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn,ocr):
        super(TaskAutoG, self).__init__()
        self.dev, self.serialno = devinfo
        self.sn = sn
        self.mnq_name = mnq_name
        self.cn_ocr = ocr

    def start_autotask(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        mrtask_queue = kwargs['每日任务']['每日任务队列']
        _CW_FLAG = False if kwargs['角色信息']['宠物'] == '0' else True
        _L2_FLAG = False if kwargs['角色信息']['60级'] == '0' else True
        _L3_FLAG = False if kwargs['角色信息']['90级'] == '0' else True
        # s_time=time.time()
        level = kwargs['角色信息']['等级']
        while True:
            for i in range(3):
                self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=0)
                self.ocr_find(ImgEnumG.SKIP_OCR,True)
            self.check_err()
            if self.ocr_find(ImgEnumG.BAG_FULL):
                select_queue.put_queue('BagSell')
                return 0
            if self.ocr_find(ImgEnumG.HP_NULL_OCR):
                select_queue.put_queue('BuyY')
                return 0
            if self.ocr_find(ImgEnumG.MP_NULL_OCR) and use_mp:
                select_queue.put_queue('BuyY')
                return 0
            if self.ocr_find(ImgEnumG.TASK_OCR):
                self.sn.log_tab.emit(self.mnq_name, r"任务进行中")
                self.ocr_find(ImgEnumG.TASK_ZDFP, True)
                self.ocr_find(ImgEnumG.TASK_ZB,True)
                level = self.get_num((35, 5, 99, 31))
                bat_num = self.get_num((41, 66, 165, 87))
                kwargs['角色信息']['等级'] = level
                kwargs['角色信息']['战力'] = bat_num
                self.sn.table_value.emit(self.mnq_name, 3, f"{level}")
                self.sn.table_value.emit(self.mnq_name, 5, f"{bat_num}")
                if self.crop_image_find(ImgEnumG.MOVE_NOW, False):
                    try:
                        move_num = self.get_num((697, 139, 797, 170))
                        stone_num = self.get_num((685, 189, 721, 218))
                        if int(move_num) > 3 and stone_num > 5:
                            self.crop_image_find(ImgEnumG.MOVE_NOW)
                    except ValueError:
                        pass
                self.time_sleep(5)
            else:
                if self.ocr_find([(28, 0, 94, 33), 'LV']) and self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    if level >= 30 and not _CW_FLAG:
                        select_queue.put_queue('UseSkill')
                        select_queue.put_queue('UsePet')
                        select_queue.put_queue('GetLevelReard')
                        select_queue.put_queue('CheckRole')
                        _CW_FLAG = True
                        return 0
                    elif level >= 60 and not _L2_FLAG:
                        r = random.randint(1, 3)
                        mrtask_queue.put_queue(str(r))  # 武林
                        select_queue.put_queue('AutoMR')
                        select_queue.put_queue('UseSkill')
                        select_queue.put_queue('GetLevelReard')
                        select_queue.put_queue('CheckRole')
                        kwargs['角色信息']['60级'] = '1'
                        _L2_FLAG = True
                        return 0
                    elif level >= 90 and not _L3_FLAG:
                        r = random.randint(1, 3)
                        mrtask_queue.put_queue(str(r))  # 武林
                        select_queue.put_queue('AutoMR')
                        select_queue.put_queue('GetLevelReard')
                        select_queue.put_queue('CheckRole')
                        self.sn.table_value.emit(self.mnq_name, 2, '冰冷死亡战场')
                        kwargs['角色信息']['90级'] = True
                        _L3_FLAG = True
                        raise RestartTask
                self.air_loop_find(ImgEnumG.TASK_TAB, touch_wait=0)
                self.crop_image_find(ImgEnumG.TASK_POINT, touch_wait=0)
                # self.crop_image_find(ImgEnumG.MR_TIP_CLOSE)
                if self.air_loop_find(ImgEnumG.TASK_CLOSE, False):
                    self.air_loop_find(ImgEnumG.TASK_OVER, timeout=0.5, touch_wait=0)
                    self.air_loop_find(ImgEnumG.TASK_START, timeout=0.5, touch_wait=0)
                    self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=0)
                    self.crop_image_find(ImgEnumG.TASK_TAKE, touch_wait=0)
                else:
                    self.air_loop_find(ImgEnumG.TASK_MR_QR, touch_wait=0)
                    self.crop_image_find(ImgEnumG.TASK_REWARD, touch_wait=0)
                    self.air_loop_find(ImgEnumG.TASK_TAB, touch_wait=0)
                if not self.crop_image_find(ImgEnumG.INGAME_FLAG2,False):
                    if not self.check_close():
                        raise NotInGameErr

    def change_mapdata(self, **kwargs):
        map_data = kwargs['战斗数据']['地图数据']
        map_ocr = kwargs['战斗数据']['地图识别']
        map_name = kwargs['地图名']
