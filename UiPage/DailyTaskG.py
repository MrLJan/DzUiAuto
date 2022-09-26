# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG
from UiPage.BasePage import BasePageG
from Utils.LoadConfig import LoadConfig
import random


class DailyTaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(DailyTaskAutoG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def dailytask_start(self, **kwargs):
        task_list = kwargs['每日任务']['任务列表']
        taskid = kwargs['任务id']
        exec_queue = kwargs['状态队列']['执行器']
        select_queue = kwargs['状态队列']['选择器']
        mrtask_queue = kwargs['每日任务']['每日任务队列']
        if len(task_list) == 0:
            exec_queue.task_over('AutoMR')
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
            '10':self.star_tower_task,
            '11': self.gw_park_task
        }
        while not mrtask_queue.queue.empty():
            _id = mrtask_queue.get_task()
            res = do_task[_id]()
            if res:
                mrtask_queue.task_over(_id)
                self.back_mr_main()
            else:
                if not self.check_close():
                    select_queue.put_queue('Check')
                    return 0
        exec_queue.task_over('AutoMR')
        if taskid in ['3', '4']:
            exec_queue.put_queue('AutoBat')
        return 1

    def back_mr_main(self):
        for i in range(10):
            self.air_loop_find(ImgEnumG.MR_BACK, timeout=1, touch_wait=3)
            self.ocr_find(ImgEnumG.MR_YDZXD,True)
            if self.ocr_find(ImgEnumG.MR_UI_OCR):
                return True
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                return True
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
        self.check_close()

    def test(self):
        return True

    def wulin_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"武林道场")
        self.sn.table_value.emit(self.mnq_name, 8, r"武林道场")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
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
                    self.ocr_find([ImgEnumG.MR_AREA, '武陵道'], True)
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
                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                    self.air_loop_find(ImgEnumG.UI_QR)
                    if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                        if not self.check_close():
                            self.sn.log_tab.emit(self.mnq_name, r"武林道场-异常失败")
                            return False
        self.sn.log_tab.emit(self.mnq_name, r"武林道场-超时失败")
        return False

    def jinzita_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"金字塔")
        self.sn.table_value.emit(self.mnq_name, 8, r"金字塔")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
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
                    self.ocr_find([ImgEnumG.MR_AREA, r'塔'], True)
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
                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                    if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                        if not self.check_close():
                            self.sn.log_tab.emit(self.mnq_name, r"金字塔-异常失败")
                            return False
        return False

    def jingying_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"菁英地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"菁英地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
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
                        self.ocr_find([ImgEnumG.MR_AREA, '菁英'], True)
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
                        self.crop_image_find(ImgEnumG.UI_CLOSE)
                        if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                            if not self.check_close():
                                self.sn.log_tab.emit(self.mnq_name, r"菁英地城-异常失败")
                                return False
        return False

    def meiri_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"每日地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"每日地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
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
                        self.ocr_find([ImgEnumG.MR_AREA, '每日'], True)
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
                        self.crop_image_find(ImgEnumG.UI_CLOSE)
                        if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                            if not self.check_close():
                                self.sn.log_tab.emit(self.mnq_name, r"每日地城-异常失败")
                                return False
        return False

    def guaiwu_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团")
        self.sn.table_value.emit(self.mnq_name, 8, r"怪物狩猎团")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-战斗完成")
                    return True
                if self.ocr_find(ImgEnumG.GWSLT_ZDJS):  # 战斗结束
                    self.crop_image_find(ImgEnumG.MR_BAT_EXIT)
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
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
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
                        self.crop_image_find(ImgEnumG.UI_CLOSE)
                        if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                            if not self.check_close():
                                self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-异常失败")
                                return False

    def tangbaobao_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝")
        self.sn.table_value.emit(self.mnq_name, 8, r"汤宝宝")
        _TIMES = 0
        _JR_TIME = 0
        _TASK_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
                if self.ocr_find(ImgEnumG.TBB_ZCRC):
                    if _TIMES < 3:
                        self.air_loop_find(ImgEnumG.UI_QR)
                        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-再次入场")
                        _TIMES += 1
                    else:
                        self.ocr_find(ImgEnumG.TBB_QX, True)
                        _TASK_OVER = True
                elif not _TASK_OVER:
                    self.ocr_find(ImgEnumG.TBB_ZCTZ, True)
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-战斗完成")
                    return True
                elif self.air_loop_find(ImgEnumG.UI_QR):
                    self.ocr_find(ImgEnumG.TBB_ZCTZ, True)
                self.sn.log_tab.emit(self.mnq_name, r"汤宝宝战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.ocr_find(ImgEnumG.MR_UI_OCR):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '寳寳的'], True):
                        self.air_swipe((925, 432), (400, 432), swipe_wait=1)
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
                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                    self.air_loop_find(ImgEnumG.UI_QR)
                    if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                        if not self.check_close():
                            self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-异常失败")
                            return False
        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-超时失败")
        return False

    def jinhua_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"进化系统")
        self.sn.table_value.emit(self.mnq_name, 8, r"进化系统")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
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
                        self.air_swipe((925, 432), (400, 432), swipe_wait=1)
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
                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                    self.air_loop_find(ImgEnumG.UI_QR)
                    if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                        if not self.check_close():
                            self.sn.log_tab.emit(self.mnq_name, r"进化系统-异常失败")
                            return False
        self.sn.log_tab.emit(self.mnq_name, r"进化系统-超时失败")
        return False

    def ciyuan_task(self):
        s_time = time.time()
        _JR_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"次元入侵")
        self.sn.table_value.emit(self.mnq_name, 8, r"次元入侵")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
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
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
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
                        self.crop_image_find(ImgEnumG.UI_CLOSE)
                        self.air_loop_find(ImgEnumG.UI_QR)
                        if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                            if not self.check_close():
                                self.sn.log_tab.emit(self.mnq_name, r"次元入侵-异常失败")
                                return False
        self.sn.log_tab.emit(self.mnq_name, r"次元入侵-超时失败")
        return False

    def minidc_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"迷你地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"迷你地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
                if self.ocr_find(ImgEnumG.MR_YDZXD, True):
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
                    self.ocr_find([ImgEnumG.MR_AREA, '迷你'], True)
                elif self.ocr_find(ImgEnumG.MR_WLDC_JR):  # 入场选择
                    self.get_rgb(731, 629, 'EE7047', True)
                elif self.ocr_find(ImgEnumG.MR_MNDC_OCR):  # 迷你地城界面
                    times = self.get_num((1133, 567, 1173, 595))  # 剩余次数
                    if times > 0:
                        self.get_rgb(54, 138, '2B3747', True)
                        self.get_rgb(78, 214, '2B3747', True)
                        self.get_rgb(572, 427, 'FFD742', True)
                        self.get_rgb(1053, 650, 'EE7047', True)
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"迷你地城-无次数")
                        return True
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"迷你地城-战斗完成")
                    return True
                else:
                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                    self.air_loop_find(ImgEnumG.UI_QR)
                    if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                        if not self.check_close():
                            self.sn.log_tab.emit(self.mnq_name, r"迷你地城-异常失败")
                            return False
        self.sn.log_tab.emit(self.mnq_name, r"迷你地城-超时失败")
        return False

    def star_tower_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"星光M塔")
        self.sn.table_value.emit(self.mnq_name, 8, r"星光M塔")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            pass

    def gw_park_task(self):
        s_time = time.time()
        _JR_TIMES = 0
        _TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"怪物公园")
        self.sn.table_value.emit(self.mnq_name, 8, r"怪物公园")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                return False
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False):
                self.ocr_find(ImgEnumG.AUTO_BAT_OCR,True)
                if self.ocr_find(ImgEnumG.GWGY_FQ,True):
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
                        self.air_swipe((925, 432), (400, 432), swipe_wait=1)
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
                    self.crop_image_find(ImgEnumG.UI_CLOSE)
                    self.air_loop_find(ImgEnumG.UI_QR)
                    if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                        if not self.check_close():
                            self.sn.log_tab.emit(self.mnq_name, r"怪物公园-异常失败")
                            return False
        self.sn.log_tab.emit(self.mnq_name, r"怪物公园-超时失败")
        return False

    def boss_task(self):
        s_time = time.time()
        _YM = False
        _PKJ = False
        _NH=False
        _YM_OVER=False
        _PKJ_OVER = False
        _NH_OVER = False
        self.sn.log_tab.emit(self.mnq_name, r"boss远征")
        self.sn.table_value.emit(self.mnq_name, 8, r"boss远征")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            pass
