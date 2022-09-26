# -*- encoding=utf8 -*-
import time

from Enum.ResEnum import ImgEnumG
from UiPage.BasePage import BasePageG


class TaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(TaskAutoG, self).__init__()
        self.dev, self.serialno = devinfo
        self.sn = sn
        self.mnq_name = mnq_name

    def start_autotask(self,**kwargs):
        select_queue = kwargs['状态队列']['选择器']
        # s_time=time.time()
        while True:
            for i in range(3):
                self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=0)
            if self.air_loop_find(ImgEnumG.GAME_ICON,False):
                select_queue.put_queue('Login')
                return 0
            if self.ocr_find(ImgEnumG.BAG_FULL):
                select_queue.put_queue('BagSell')
                return 0
            if self.ocr_find(ImgEnumG.HP_NULL_OCR) or self.ocr_find(ImgEnumG.MP_NULL_OCR):
                select_queue.put_queue('BuyY')
                return 0
            if self.ocr_find(ImgEnumG.TASK_OCR):
                self.sn.log_tab.emit(self.mnq_name, r"任务进行中")
                if self.crop_image_find(ImgEnumG.MOVE_NOW, False):
                    try:
                        move_num = self.get_num((697, 139, 797, 170))
                        stone_num=self.get_num((685,189,721,218))
                        if int(move_num) > 3 and stone_num>5:
                            self.crop_image_find(ImgEnumG.MOVE_NOW)
                    except ValueError:
                        pass
                self.time_sleep(5)
            else:
                self.air_loop_find(ImgEnumG.TASK_TAB, touch_wait=0)
                self.crop_image_find(ImgEnumG.TASK_POINT, touch_wait=0)
                self.crop_image_find(ImgEnumG.MR_TIP_CLOSE)
                if self.air_loop_find(ImgEnumG.TASK_CLOSE, False):
                    self.air_loop_find(ImgEnumG.TASK_OVER, timeout=0.5, touch_wait=0)
                    self.air_loop_find(ImgEnumG.TASK_START, timeout=0.5, touch_wait=0)
                    self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5, touch_wait=0)
                    self.crop_image_find(ImgEnumG.TASK_TAKE, touch_wait=0)
                else:
                    self.air_loop_find(ImgEnumG.TASK_MR_QR, touch_wait=0)
                    self.crop_image_find(ImgEnumG.TASK_REWARD, touch_wait=0)
                    self.air_loop_find(ImgEnumG.TASK_TAB, touch_wait=0)

