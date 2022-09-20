# -*- encoding=utf8 -*-
from Enum.ResEnum import ImgEnumG
from UiPage.BasePage import BasePageG


class TaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(TaskAutoG, self).__init__()
        self.dev, self.serialno = devinfo
        self.sn = sn
        self.mnq_name = mnq_name

    def start_autotask(self):
        for i in range(3):
            self.crop_image_find(ImgEnumG.TASK_ARROW,timeout=0.5)
        if self.ocr_find(ImgEnumG.TASK_OCR):
            self.sn.log_tab.emit(self.mnq_name, r"任务进行中")
            self.crop_image_find(ImgEnumG.MOVE_NOW)
            self.time_sleep(5)
            self.start_autotask()
        else:
            self.crop_image_find(ImgEnumG.TASK_TAB)
            self.crop_image_find(ImgEnumG.TASK_POINT)
        if self.crop_image_find(ImgEnumG.TASK_CLOSE,False):
            self.air_loop_find(ImgEnumG.TASK_OVER,timeout=0.5)
            self.air_loop_find(ImgEnumG.TASK_START,timeout=0.5)
            self.crop_image_find(ImgEnumG.TASK_ARROW, timeout=0.5)
            self.crop_image_find(ImgEnumG.TASK_TAKE)
        else:
            self.crop_image_find(ImgEnumG.TASK_REWARD)
            self.crop_image_find(ImgEnumG.TASK_TAB)
        return 0

