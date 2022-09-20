import time

from Enum.ResEnum import GlobalEnumG,ImgEnumG
from UiPage.BasePage import BasePageG


class RewardG(BasePageG):
    def __init__(self):
        super(RewardG, self).__init__()

    def get_reward(self):
        pass

    def get_mail_reward(self):
        s_time=time.time()
        while time.time()-s_time <GlobalEnumG.UiCheckTimeOut:
            self.crop_image_find(ImgEnumG.MAIL_RQ)
            if self.ocr_find(ImgEnumG.MAIL_UI_OCR):
                # if self.crop_image_find(ImgEnumG.HD)
                self.crop_image_find(ImgEnumG.UI_QBLQ)

    def get_keti_reward(self):
        pass
