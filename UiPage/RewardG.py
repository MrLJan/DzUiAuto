import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG
from UiPage.BasePage import BasePageG


class RewardG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(RewardG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def get_reward(self):
        self.get_keti_reward()
        self.get_hd_reward()
        self.get_mail_reward()

    def get_mail_reward(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.crop_image_find(ImgEnumG.MAIL_RQ)
            if self.ocr_find(ImgEnumG.MAIL_UI_OCR):
                self.crop_image_find(ImgEnumG.UI_QBLQ)
                if self.air_loop_find(ImgEnumG.HD_QBLQ2, False):
                    self.ocr_find(ImgEnumG.MAIL_SOLO_OCR, True)
                    if self.air_loop_find(ImgEnumG.HD_QBLQ2, False):
                        self.air_loop_find(ImgEnumG.UI_CLOSE, touch_wait=2)
                        break
            self.crop_image_find(ImgEnumG.UI_QR)
        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
            return True
        return False

    def get_keti_reward(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.MR_MENU)
            self.crop_image_find(ImgEnumG.MR_TIP_CLOSE)
            if not self.ocr_find(ImgEnumG.KT_UI_OCR):
                self.ocr_find(ImgEnumG.KT_MENU, True)
            if self.air_loop_find(ImgEnumG.KT_QBLQ):
                self.air_loop_find(ImgEnumG.UI_QR)
            if self.get_rgb(175, 128, 'EE7546'):  # 每日任务
                if self.get_rgb(1148, 643, 'C3C3C3', False):
                    self.ocr_find(ImgEnumG.KT_MZRW_OCR, True)
            if self.get_rgb(48, 207, 'EE7546'):  # 每周任务
                if self.get_rgb(1148, 643, 'C3C3C3', False):
                    self.ocr_find(ImgEnumG.KT_MRSL_OCR, True)
            if self.get_rgb(169, 309, 'EE7546'):  # 每日狩猎
                if self.get_rgb(1148, 643, 'C3C3C3', False):
                    self.ocr_find(ImgEnumG.KT_CJ_OCR, True)
            if self.get_rgb(155, 490, 'EE7546'):  # 成就
                if self.get_rgb(1148, 643, 'C3C3C3', False):
                    self.air_loop_find(ImgEnumG.UI_CLOSE)
                    self.air_loop_find(ImgEnumG.UI_CLOSE)
                    break
            self.air_loop_find(ImgEnumG.UI_QR)
        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
            return True
        return False

    def get_hd_reward(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.MR_MENU)
            if self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.HD_MENU, True)
            if self.ocr_find(ImgEnumG.HD_UI_OCR):
                if self.ocr_find(ImgEnumG.HD_DR_OCR, True):
                    if not self.get_rgb(679, 634, 'EE7047', True):  # 领取奖励:
                        self.ocr_find(ImgEnumG.HD_XX_OCR, True)
                        if not self.get_rgb(518, 616, 'EE7047', True):  # 领取奖励
                            self.air_loop_find(ImgEnumG.UI_CLOSE, touch_wait=2)
                            self.air_loop_find(ImgEnumG.UI_CLOSE, touch_wait=2)
                            break
            self.air_loop_find(ImgEnumG.UI_QR)
        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
            return True
        return False

    def bagsell(self):
        s_time = time.time()
        _sx_flag = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.air_touch((1170, 39))
                self.time_sleep(2)
            if self.ocr_find(ImgEnumG.BAG_OCR):
                self.crop_image_find(ImgEnumG.BAG_SELL)
            if self.ocr_find(ImgEnumG.BAG_CS_OCR):  # 出售界面
                if not self.crop_image_find(ImgEnumG.BAG_CS_LIST, False):
                    if not _sx_flag:
                        self.crop_image_find(ImgEnumG.BAG_SX)
                    else:
                        return True
                else:
                    if self.get_rgb(1120, 671, 'EE7047', True):
                        self.crop_image_find(ImgEnumG.BAG_CS_QR1, timeout=10)
                    else:
                        return True
            if self.ocr_find(ImgEnumG.BAG_SX_OCR):
                self.get_rgb(782, 375, 'ADB7C1', True)  # 饰品
                self.get_rgb(698, 451, 'ADB7C1', True)  # 饰品
                self.get_rgb(586, 537, 'ADB7C1', True)  # 饰品
                if self.get_rgb(855,636, 'EE7047', True):
                    _sx_flag = True

        return False
