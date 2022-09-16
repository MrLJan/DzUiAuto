# -*- coding: utf-8 -*-
from airtest.core.cv import Template

from Utils.OtherTools import OT


class GlobalEnumG:
    Ver = '2.0'
    GamePackgeName=r'com.nexon.maplem.global'
    FindImgTimeOut = 20  # 查找图片等待超时时间
    TouchDurationTime = 4  # 延时点击

    TasKId = {

    }


class ImgEnumG:
    """图片数据"""
    GAME_ICON = Template(OT.imgpath('游戏icon.bmp'))
    PERSON_POS = Template(OT.imgpath('人物坐标.bmp'))
    TEST = Template(OT.imgpath('21.bmp'))


class UiEnumG:
    BAG_UI = [(59, 11, '415066'), (645, 32, '415066'), (557, 123, 'ffffff'),
              (467, 124, '2b3646'), (997, 675, '4c87b0'), (1148, 686, '4c87b0'), (59, 120, 'ee7546')]  # 背包主界面
