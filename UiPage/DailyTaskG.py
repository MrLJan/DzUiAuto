# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, ControlTimeOut
import random

from Utils.OpencvG import AirImgTools


class DailyTaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn,ocr):
        super(DailyTaskAutoG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.cn_ocr=ocr

    def dailytask_start(self, **kwargs):
        task_list = kwargs['每日任务']['任务列表']
        select_queue = kwargs['状态队列']['选择器']
        mrtask_queue = kwargs['每日任务']['每日任务队列']
        level = kwargs['角色信息']['等级']
        if len(task_list) == 0:
            select_queue.task_over('AutoMR')
            select_queue.put_queue('GetReward')
            select_queue.put_queue('BagClear')
            select_queue.put_queue('BagSell')
            return 1
        if mrtask_queue.queue.empty():
            for _task in task_list:
                mrtask_queue.put_queue(_task)
        do_task = {
            '1': self.wulin_task,
            '2': self.jinzita_task,
            '3': self.jingying_task,
            '4': self.meiri_task,
            '5': self.jinhua_task,
            '6': self.ciyuan_task,
            '7': self.tangbaobao_task,
            '8': self.minidc_task,
            '9': self.guaiwu_task,
            '10': self.star_tower_task,
            '11': self.gw_park_task
        }
        while not mrtask_queue.queue.empty():
            _id = mrtask_queue.get_task()
            if 100 <= level < 140 and _id == '11':
                mrtask_queue.task_over(_id)
            elif level < 100 and _id in ['5', '6', '10', '11']:
                mrtask_queue.task_over(_id)
            elif level < 60:
                mrtask_queue.task_over(_id)
            else:
                res = do_task[_id]()
                if res:
                    mrtask_queue.task_over(_id)
                else:
                    if not self.check_close():
                        select_queue.put_queue('Check')
                        return 0
                self.back_mr_main()
        select_queue.task_over('AutoMR')
        select_queue.put_queue('GetReward')
        select_queue.put_queue('BagClear')
        select_queue.put_queue('BagSell')
        return 1

    def back_mr_main(self):
        self.sn.log_tab.emit(self.mnq_name, r"返回")
        for i in range(10):
            self.crop_image_find(ImgEnumG.MR_BACK, timeout=1, touch_wait=3)
            if i > 3:
                self.crop_image_find(ImgEnumG.MR_BAT_EXIT)
            self.ocr_find(ImgEnumG.MR_YDZXD, True)
            if self.ocr_find(ImgEnumG.MR_UI_OCR):
                return True
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
        self.check_close()

    def wulin_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"武林道场")
        self.sn.table_value.emit(self.mnq_name, 8, r"武林道场")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"武林道场-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"武林道场战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.ocr_find(ImgEnumG.MR_WLDC_PM):  # 排名结算
                    self.air_loop_find(ImgEnumG.UI_QR)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '武陵道'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_WLDC_JR):  # 入场选择
                    self.ocr_find([(965, 233, 1043, 286), 'MAX'], clicked=True, touch_wait=1)
                    self.get_rgb(729, 629, 'EE7047', True)
                elif self.ocr_find(ImgEnumG.MR_WLDC_OCR):  # 道场界面
                    times = self.get_num((157, 516, 188, 543))  # 剩余次数
                    if times > 0:
                        self.get_rgb(1068, 650, 'EE7047', True)
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"武林道场-无次数")
                        return True
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"武林道场-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"武林道场-超时失败")

    def jinzita_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"金字塔")
        self.sn.table_value.emit(self.mnq_name, 8, r"金字塔")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"金字塔-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"金字塔战斗中")
                self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r'金字塔-组队中')
                    self.time_sleep(15)
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, r'塔'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_JZT_JR):
                    self.ocr_find([(822, 423, 890, 454), 'MAX'], clicked=True, touch_wait=1)
                    if self.get_rgb(717, 531, 'EE7047', True):
                        self.time_sleep(10)
                elif self.ocr_find(ImgEnumG.MR_JZT_OCR):  # 金字塔界面
                    times = self.get_num((381, 516, 415, 549))  # 剩余次数
                    if times > 0:
                        self.get_rgb(1053, 666, 'EE7047', True)
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"金字塔-无次数")
                        return True
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"金字塔-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"金字塔-超时异常")

    def jingying_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"菁英地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"菁英地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"菁英地城-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"菁英地城战斗中")
                self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"菁英地城-组队中")
                    self.time_sleep(15)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                    elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '菁英'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.ocr_find(ImgEnumG.MR_JZT_JR):  # 进入界面 和金字塔一样
                        self.ocr_find([(826, 424, 889, 454), 'MAX'], clicked=True, touch_wait=1)
                        if self.get_rgb(717, 531, 'EE7047', True):
                            self.time_sleep(10)
                    elif self.ocr_find(ImgEnumG.MR_JYDC_OCR):  # 菁英地城界面
                        times = self.get_num((411, 514, 443, 547))  # 剩余次数
                        if times > 0:
                            self.get_rgb(1053, 666, 'EE7047', True)
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"菁英地城-无次数")
                            return True
                    elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"菁英地城-战斗完成")
                        return True
                    else:
                        self.check_close()
        raise ControlTimeOut(r"菁英地城-超时异常")

    def meiri_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"每日地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"每日地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"每日地城-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"每日地城战斗")
                self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"每日地城-组队中")
                    self.time_sleep(15)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                    elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '每日'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.ocr_find(ImgEnumG.MR_MRDC_JR):  # 进入界面 和金字塔一样
                        self.ocr_find([(819, 279, 875, 310), 'MAX'], clicked=True, touch_wait=1)
                        if self.get_rgb(716, 626, 'EE7047', True):
                            self.time_sleep(10)
                    elif self.ocr_find(ImgEnumG.MR_MRDC_OCR):  # 每日地城界面
                        if self.get_rgb(143, 620, 'EE7546'):  # 混沌模式
                            self.get_rgb(151, 542, '2B3747', True)
                        times = self.get_num((342, 533, 373, 571))  # 剩余次数
                        if times > 0:
                            self.get_rgb(1078, 647, 'EE7047', True)
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"每日地城-无次数")
                            return True
                    elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"每日地城-战斗完成")
                        return True
                    else:
                        self.check_close()
        raise ControlTimeOut(r"每日地城-超时异常")

    def guaiwu_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团")
        self.sn.table_value.emit(self.mnq_name, 8, r"怪物狩猎团")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-战斗完成")
                    return True
                if self.ocr_find(ImgEnumG.GWSLT_ZDJS):  # 战斗结束
                    self.crop_image_find(ImgEnumG.MR_BAT_EXIT, touch_wait=3)
                    self.ocr_find(ImgEnumG.MR_YDZXD, True)
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团战斗中")
                    self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-组队中")
                    self.time_sleep(15)
                    self.ocr_find(ImgEnumG.ZD_KS, True)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                    elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '怪物狩'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.ocr_find(ImgEnumG.GWSLT_ZDJL):
                        self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                    elif self.ocr_find(ImgEnumG.MR_GWSLT_OCR):  # 怪物狩猎团界面
                        times = self.get_num((176, 336, 212, 363))  # 剩余次数
                        if times > 0:
                            self.get_rgb(1221, 650, 'EE7047', True)
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-无次数")
                            return True
                    elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-战斗完成")
                        return True
                    else:
                        self.check_close()
        raise ControlTimeOut(r"怪物狩猎团-超时异常")

    def tangbaobao_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝")
        self.sn.table_value.emit(self.mnq_name, 8, r"汤宝宝")
        _TIMES = 0
        _JR_TIME = 0
        _SWIPE_TIMES = 0
        _TASK_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                self.check_err()
                if self.ocr_find(ImgEnumG.TBB_CLGW):
                    self.air_touch((632, 494), touch_wait=1)
                    self.get_rgb(738, 627, 'EE7047', True)
                elif self.ocr_find(ImgEnumG.TBB_ZCRC):
                    if _TIMES < 3:
                        self.air_loop_find(ImgEnumG.UI_QR)
                        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-再次入场")
                        _TIMES += 1
                    else:
                        self.ocr_find(ImgEnumG.TBB_QX, True)
                        _TASK_OVER = True
                elif self.air_loop_find(ImgEnumG.UI_QR):
                    self.ocr_find(ImgEnumG.TBB_ZCTZ, True)
                elif not _TASK_OVER:
                    self.ocr_find(ImgEnumG.TBB_ZCTZ, True)
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-战斗完成")
                    return True
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"汤宝宝战斗中")
                    self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '理教室'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_TBB_OCR):  # 道场界面
                    if _JR_TIME > 3:
                        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-无次数")
                        return True
                    times = self.get_num((217, 415, 244, 442))  # 剩余次数
                    if times > 0:
                        if self.get_rgb(1093, 647, 'EE7047', True):
                            _JR_TIME += 1
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-无次数")
                        return True

                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.ocr_find(ImgEnumG.TBB_ZCTZ, True)
                    self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"汤宝宝-超时失败")

    def jinhua_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"进化系统")
        self.sn.table_value.emit(self.mnq_name, 8, r"进化系统")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"进化系统-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"进化系统战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '化系'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.ocr_find(ImgEnumG.QUIT_TEAM):
                    self.air_loop_find(ImgEnumG.UI_QR)
                elif self.ocr_find(ImgEnumG.MR_WLDC_JR):  # 入场选择
                    self.ocr_find([(951, 242, 1010, 274), 'MAX'], clicked=True, touch_wait=1)
                    self.get_rgb(734, 640, 'EE7047', True)
                elif self.ocr_find(ImgEnumG.MR_JHXT_OCR):  # 进化系统界面
                    times = self.get_num((292, 528, 327, 553))  # 剩余次数
                    if times > 0:
                        self.get_rgb(1047, 644, 'EE7047', True)
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"进化系统-无次数")
                        return True
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"进化系统-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"进化系统-超时异常")

    def ciyuan_task(self):
        s_time = time.time()
        _JR_TIMES = 0
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"次元入侵")
        self.sn.table_value.emit(self.mnq_name, 8, r"次元入侵")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"次元入侵-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"次元入侵战斗中")
                self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"次元入侵-组队中")
                    self.time_sleep(15)
                    self.ocr_find(ImgEnumG.ZD_KS, True)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                    elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '次元入侵'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.ocr_find(ImgEnumG.MR_CYRQ_OCR):  # 进化系统界面
                        if _JR_TIMES > 3:
                            self.sn.log_tab.emit(self.mnq_name, r"次元入侵-无次数")
                            return True
                        times = self.get_num((228, 540, 278, 564))  # 剩余次数
                        if times > 0:
                            if self.get_rgb(1055, 656, 'EE7047', True):
                                _JR_TIMES += 1
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"次元入侵-无次数")
                            return True
                    elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"次元入侵-战斗完成")
                        return True
                    else:
                        self.check_close()
        raise ControlTimeOut(r"次元入侵-超时失败")

    def minidc_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"迷你地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"迷你地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut * 2:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                self.check_err()
                if self.ocr_find(ImgEnumG.MNDC_JG):
                    self.get_rgb(564, 593, 'EE7047', True)
                    self.ocr_find([(401, 586, 877, 635), '移'], True)
                    self.ocr_find([(401, 586, 877, 635), '离'], True)
                    self.sn.log_tab.emit(self.mnq_name, r"迷你地城-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"迷你地城战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.ocr_find(ImgEnumG.AUTO_JG):  # 自动战斗结果
                    self.air_loop_find(ImgEnumG.UI_QR)
                elif self.ocr_find(ImgEnumG.MNDC_JR):
                    self.ocr_find(ImgEnumG.MNDC_FQ, True)
                elif self.ocr_find(ImgEnumG.MNDC_JS):
                    self.ocr_find(ImgEnumG.MNDC_JSQR, True)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '迷你'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_WLDC_JR):  # 入场选择
                    self.get_rgb(731, 629, 'EE7047', True)
                elif self.ocr_find(ImgEnumG.MR_MNDC_OCR):  # 迷你地城界面
                    times = self.get_num((1133, 567, 1173, 595))  # 剩余次数
                    if times == 0:
                        self.sn.log_tab.emit(self.mnq_name, r"迷你地城-无次数")
                        return True
                    else:
                        self.get_rgb(54, 138, '2B3747', True)
                        self.get_rgb(78, 214, '2B3747', True)
                        self.get_rgb(633, 331, 'FFFFFF', True)
                        self.get_rgb(1053, 650, 'EE7047', True)
                elif self.ocr_find(ImgEnumG.MNDC_JG):
                    self.get_rgb(564, 593, 'EE7047', True)
                    self.sn.log_tab.emit(self.mnq_name, r"迷你地城-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"迷你地城-超时失败")

    def star_tower_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"星光M塔")
        self.sn.table_value.emit(self.mnq_name, 8, r"星光M塔")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"星光M塔-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"星光M塔战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '星光M塔'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.ocr_find(ImgEnumG.QUIT_TEAM):
                    self.air_loop_find(ImgEnumG.UI_QR)
                elif self.ocr_find(ImgEnumG.MR_XGT_JR):  # 入场选择
                    self.air_loop_find(ImgEnumG.UI_QR)
                elif self.ocr_find(ImgEnumG.MR_XGT_OCR):  # 星光塔界面
                    if self.get_rgb(1167, 642, 'EE7047', True):
                        pass
                    elif self.get_rgb(1167, 642, 'C3C3C3'):
                        self.sn.log_tab.emit(self.mnq_name, r"星光塔-无次数")
                        return True
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"进化系统-战斗完成")
                    return True
                else:
                    self.check_close()

    def gw_park_task(self):
        s_time = time.time()
        _JR_TIMES = 0
        _TIMES = 0
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"怪物公园")
        self.sn.table_value.emit(self.mnq_name, 8, r"怪物公园")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut * 3:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                self.ocr_find(ImgEnumG.AUTO_BAT_OCR, True)
                if self.ocr_find(ImgEnumG.GWGY_FQ, True):
                    _TIMES += 1
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    if _TIMES > 2:
                        self.sn.log_tab.emit(self.mnq_name, r"怪物公园-战斗完成")
                        return True
                    _TIMES += 1
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"怪物公园战斗中")
                    self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '怪物公'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_WLDC_JR):
                    self.get_rgb(749, 633, 'EE7047', True)
                elif self.ocr_find(ImgEnumG.MR_GWGY_OCR):  # 怪物公园界面
                    if _JR_TIMES > 3:
                        self.sn.log_tab.emit(self.mnq_name, r"怪物公园-无次数")
                        return True
                    times = self.get_num((1179, 538, 1228, 562))  # 剩余次数
                    if times > 0:
                        if self.get_rgb(1084, 656, 'EE7047', True):
                            _JR_TIMES += 1
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"怪物公园-无次数")
                        return True
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"怪物公园-战斗完成")
                    return True
                else:
                    self.check_close()

        raise ControlTimeOut(r"怪物公园-超时失败")

    def boss_task(self, **kwargs):
        s_time = time.time()
        _YM = True if kwargs['王图设置']['炎魔'] == '1' else False  # 是否要打
        _PKJ = True if kwargs['王图设置']['皮卡啾'] == '1' else False
        _NH = True if kwargs['王图设置']['女皇'] == '1' else False
        _YM_ING = True  # 是否进行中
        _PKJ_ING = True  # 是否进行中
        _NH_ING = True  # 是否进行中
        _YM_KN = True if kwargs['王图设置']['炎魔难度'] == '1' else False  # 难度
        _PKJ_KN = True if kwargs['王图设置']['皮卡啾难度'] == '1' else False
        _NH_KN = True if kwargs['王图设置']['女皇难度'] == '1' else False
        _YM_OVER = False  # 是否完成
        _PKJ_OVER = False
        _NH_OVER = False
        _BAT_TIMES = 0
        _WAIT_TIMES = 0
        _WAIT_TEAM = False
        _WAIT_TEAM_TIMES = 0
        _SWIPE_TIMES = 0  # 滑动查找次数
        select_queue = kwargs['状态队列']['选择器']
        self.sn.log_tab.emit(self.mnq_name, r"boss远征")
        self.sn.table_value.emit(self.mnq_name, 8, r"boss远征")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.BOSS_DJ):
                    self.air_loop_find(ImgEnumG.UI_QR)
                self.air_touch(AirImgTools.turn_pos['left'], duration=1)
                r = random.randint(0, 3)
                if r > 1:
                    self.air_touch(AirImgTools.turn_pos['attack'])
                else:
                    self.air_touch(AirImgTools.turn_pos['c'])
                if _BAT_TIMES > 5:
                    self.crop_image_find(ImgEnumG.MR_BAT_EXIT)
                if self.ocr_find(ImgEnumG.YZD_JS):
                    self.air_touch(AirImgTools.turn_pos['right'], duration=5)
                    self.crop_image_find(ImgEnumG.MR_BAT_EXIT)
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    if _YM_ING:
                        _YM_OVER = True
                        _BAT_TIMES = 0
                    elif _PKJ_ING:
                        _PKJ_OVER = True
                        _BAT_TIMES = 0
                    elif _NH_ING:
                        _NH_OVER = True
                        _BAT_TIMES = 0
                    self.sn.log_tab.emit(self.mnq_name, r"boss远征-战斗完成")
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"boss远征战斗中")
                    self.time_sleep(15)
                    _BAT_TIMES += 1
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"boss远征-组队中")
                    self.time_sleep(15)
                    _WAIT_TIMES += 1
                    if _WAIT_TIMES > 4:
                        self.ocr_find(ImgEnumG.ZD_KS, True)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        if _WAIT_TEAM:
                            if _WAIT_TEAM_TIMES > 3:
                                _WAIT_TEAM = False
                            self.time_sleep(10)
                            _WAIT_TEAM_TIMES += 1
                        else:
                            self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                    elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '征'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.ocr_find(ImgEnumG.MR_XZD_OCR):  # boss远征界面
                        if self.get_rgb(1052, 648, 'C3C3C3'):
                            self.sn.log_tab.emit(self.mnq_name, r"boss远征-未到开启时间")
                            select_queue.task_over('AutoBoss')
                            return True
                        if _PKJ_OVER and _YM_OVER and _NH_OVER:
                            self.sn.log_tab.emit(self.mnq_name, r"boss远征-战斗完成")
                            select_queue.task_over('AutoBoss')
                            return True
                        elif _YM and not _YM_OVER:
                            if self.ocr_find(ImgEnumG.YM_READY, True):
                                if _YM_KN:
                                    self.get_rgb(156, 259, '2B3747', True)  # 困难
                                else:
                                    self.get_rgb(159, 339, '2B3747', True)
                                _YM_ING = True
                            elif self.ocr_find(ImgEnumG.YM_OVER):
                                _YM_OVER = True
                        elif _PKJ and not _PKJ_OVER:
                            if self.ocr_find(ImgEnumG.PKJ_READY, True):
                                if _PKJ_KN:
                                    self.get_rgb(156, 259, '2B3747', True)  # 困难
                                else:
                                    self.get_rgb(159, 339, '2B3747', True)
                                _PKJ_ING = True
                            elif self.ocr_find(ImgEnumG.PKJ_OVER):
                                _PKJ_OVER = True
                        elif _NH and not _NH_OVER:
                            if self.ocr_find(ImgEnumG.NH_READY, True):
                                if _NH_KN:
                                    self.get_rgb(156, 259, '2B3747', True)  # 困难
                                else:
                                    self.get_rgb(159, 339, '2B3747', True)
                                _NH_ING = True
                            elif self.ocr_find(ImgEnumG.NH_OVER):
                                _NH_OVER = True
                        if self.get_rgb(1055, 651, 'EE7047', True, touch_wait=3):
                            _WAIT_TEAM = True
                    else:
                        self.crop_image_find(ImgEnumG.UI_CLOSE)
                        self.crop_image_find(ImgEnumG.MR_BACK)
                        self.air_loop_find(ImgEnumG.UI_QR)
                        if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                            if not self.check_close():
                                self.sn.log_tab.emit(self.mnq_name, r"boss远征-异常失败")
                                return False
        raise ControlTimeOut(r"boss远征-超时失败")

    def hdboss_task(self, **kwargs):
        s_time = time.time()
        _JR_TIMES = 0
        _WAIT_TIMES = 0
        _SWIPE_TIMES = 0
        _IS_HD = True if kwargs['王图设置']['混沌炎魔'] == '1' else False
        select_queue = kwargs['状态队列']['选择器']
        self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔")
        self.sn.table_value.emit(self.mnq_name, 8, r"混沌炎魔")
        if not _IS_HD:
            self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔未设置")
            select_queue.task_over('AutoHDboss')
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.YZD_JS):
                    self.crop_image_find(ImgEnumG.MR_BAT_EXIT, touch_wait=3)
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-战斗完成")
                    select_queue.task_over('AutoHDboss')
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔战斗中")
                self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-组队中")
                    self.time_sleep(15)
                    _WAIT_TIMES += 1
                    self.ocr_find(ImgEnumG.ZD_KS, True)
                    if _WAIT_TIMES > 3:
                        self.air_touch((433, 257), touch_wait=1)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.ocr_find(ImgEnumG.MR_WLDC_PM):  # 排名结算
                        self.air_loop_find(ImgEnumG.UI_QR)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                    elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '混沌速'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.ocr_find(ImgEnumG.MR_WLDC_JR):  # 入场选择
                        self.ocr_find([(965, 233, 1043, 286), 'MAX'], clicked=True, touch_wait=1)
                        self.get_rgb(729, 629, 'EE7047', True)
                    elif self.ocr_find(ImgEnumG.MR_HD_OCR):  # 混沌远征界面
                        if _JR_TIMES > 3:
                            self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-无次数")
                            select_queue.task_over('AutoHDboss')
                            return True
                        times = self.get_ocrres((281, 531, 329, 566))  # 剩余次数
                        if times == '一':
                            if self.get_rgb(1180, 653, 'EE7047', True, touch_wait=2):
                                _JR_TIMES += 1
                        else:
                            self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-无次数")
                            select_queue.task_over('AutoHDboss')
                            return True
                    elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-战斗完成")
                        select_queue.task_over('AutoHDboss')
                        return True
                    else:
                        self.crop_image_find(ImgEnumG.UI_CLOSE)
                        self.air_loop_find(ImgEnumG.UI_QR)
                        if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                            if not self.check_close():
                                self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-异常失败")
                                return False
        raise ControlTimeOut(r"混沌炎魔-超时失败")

    def gonghui_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"公会任务")
        self.sn.table_value.emit(self.mnq_name, 8, r"公会任务")
        _JION = False
        _JION_TIMES = 0
        _JR_TIMES = 0
        _WXDC = False
        _RYZ = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.check_err()
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    if _WXDC and _RYZ:
                        self.sn.log_tab.emit(self.mnq_name, r"公会任务-战斗完成")
                        return True
                    elif _WXDC:
                        self.sn.log_tab.emit(self.mnq_name, r"公会无限地城-战斗完成")
                    elif _RYZ:
                        self.sn.log_tab.emit(self.mnq_name, r"公会荣誉战-战斗完成")
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"公会战斗中")
                    self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '公曾'], True):
                        self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                elif self.ocr_find(ImgEnumG.MR_GH_OCR):
                    if not self.ocr_find(ImgEnumG.JRGH_OCR, True):
                        if _WXDC and _RYZ:
                            self.sn.log_tab.emit(self.mnq_name, r"公会任务-战斗完成")
                            return True
                        if not _WXDC:
                            self.ocr_find(ImgEnumG.GH_WXDC, True)
                        else:
                            if not _RYZ:
                                self.ocr_find(ImgEnumG.GH_RYZ, True)
                elif self.ocr_find(ImgEnumG.MR_GHDC_OCR):
                    if _WXDC:
                        self.crop_image_find(ImgEnumG.MR_BACK)
                    else:
                        if self.get_rgb(482, 647, 'EE7047', True):
                            _WXDC = True
                elif self.ocr_find(ImgEnumG.MR_RYZ_OCR):
                    if _RYZ or _JR_TIMES > 3:
                        if _JR_TIMES > 3:
                            _RYZ = True
                        self.crop_image_find(ImgEnumG.MR_BACK)
                    else:
                        if self.get_rgb(433, 666, 'EE7047', True, touch_wait=2):
                            _RYZ = True
                            _JR_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_JRGH_OCR):
                    if _JION_TIMES > 10:
                        self.sn.log_tab.emit(self.mnq_name, r"无法加入公会,取消公会任务")
                        return True
                    self.ocr_find(ImgEnumG.GH_KSJR, True)
                    if self.get_rgb(840, 528, 'EE7047', True):
                        _JION_TIMES += 1
        raise ControlTimeOut(r'公会任务-超时异常')
