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

    def upequip(self):
        s_time = time.time()

        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):  # 游戏界面
                self.crop_image_find(ImgEnumG.MR_MENU)
            if self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.EQ_TJP_OCR, True)
            if self.ocr_find(ImgEnumG.TJP_UI_OCR):  # 进入铁匠铺
                if self.crop_image_find(ImgEnumG.EQ_WZB):  # 装备槽
                    zb_list = self.get_all_text(ImgEnumG.EQ_ZBZ_OCR)
                    if len(zb_list) == 0:
                        self.sn.log_tab.emit(self.mnq_name, r"无可升级装备")
                        return True
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
                                    return True
                                self.crop_image_find(ImgEnumG.EQ_UP_QR, timeout=20)
                        else:
                            self.air_swipe((912, 507), (912, 303))
            else:
                if self.ocr_find(ImgEnumG.EQ_UP_OCR):
                    self.air_touch((84, 268))
        return False
