# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, ControlTimeOut
import random

from Utils.OpencvG import AirImgTools


class DailyTaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn, ocr):
        super(DailyTaskAutoG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.cn_ocr = ocr
        self.ksnr_pos = (0, 0)

    def dailytask_start(self, **kwargs):
        task_list = kwargs['每日任务']['任务列表']
        select_queue = kwargs['状态队列']['选择器']
        mrtask_queue = kwargs['每日任务']['每日任务队列']
        is_gonghui = kwargs['每日任务']['公会']
        level = kwargs['角色信息']['等级']
        if len(task_list) == 0:
            select_queue.task_over('AutoMR')
            select_queue.put_queue('GetReward')
            select_queue.put_queue('BagClear')
            select_queue.put_queue('BagSell')
            return -1
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
            # '9': self.guaiwu_task,
            '9': self.star_tower_task,
            '10': self.gw_park_task
        }
        self.skip_new()
        while not mrtask_queue.queue.empty():
            _id = mrtask_queue.get_task()
            if 100 <= level < 140 and _id == '10':
                mrtask_queue.task_over(_id)
            elif level < 100 and _id in ['5', '6', '9', '10']:
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
        if level >= 100:
            if is_gonghui:
                self.gonghui_task()
        select_queue.task_over('AutoMR')  # 顺序队列,先进后出
        select_queue.put_queue('GetReward')
        select_queue.put_queue('BagClear')
        select_queue.put_queue('BagSell')
        return -1

    def back_mr_main(self):
        self.sn.log_tab.emit(self.mnq_name, r"返回")
        for i in range(10):
            self.crop_image_find(ImgEnumG.MR_BACK, timeout=1, touch_wait=3)
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT):
                self.ocr_find(ImgEnumG.MR_YDZXD, True)
            if self.get_rgb(RgbEnumG.KSDY):
                return True
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                pass
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            else:
                self.back(self.serialno)
            self.time_sleep(2)
        self.check_close()

    def wulin_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        _JION_TIMES = 1
        self.sn.log_tab.emit(self.mnq_name, r"武林道场")
        self.sn.table_value.emit(self.mnq_name, 8, r"武林道场")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.get_rgb(RgbEnumG.JHXT_END):
                    if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"武林道场-战斗完成")
                        return True
                self.sn.log_tab.emit(self.mnq_name, r"武林道场战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.get_rgb(RgbEnumG.WL_PM, True):  # 排名结算
                    pass
                elif self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):  # 离开队伍
                    pass
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '武陵道'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.WL_JRQR):  # 入场选择
                    if _JION_TIMES > 3:
                        self.sn.log_tab.emit(self.mnq_name, r"武林道场-无次数")
                        return True
                    else:
                        self.air_touch((976, 242), touch_wait=1)
                        self.air_touch((729, 629), touch_wait=1)
                        _JION_TIMES += 1
                elif self.get_rgb(RgbEnumG.WL_M):  # 道场界面
                    # times = self.get_num((157, 516, 188, 543))  # 剩余次数
                    # if times > 0:
                    self.get_rgb(RgbEnumG.WL_JR, True)
                    # else:
                    #     self.sn.log_tab.emit(self.mnq_name, r"武林道场-无次数")
                    #     return True
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"武林道场-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"武林道场-超时失败")

    def jinzita_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        _JION = False
        _WAIT_TIMES = 1
        self.sn.log_tab.emit(self.mnq_name, r"金字塔")
        self.sn.table_value.emit(self.mnq_name, 8, r"金字塔")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                self.sn.log_tab.emit(self.mnq_name, r"金字塔战斗中")
                self.time_sleep(10)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r'金字塔-组队中')
                    self.time_sleep(15)
                    self.get_rgb(RgbEnumG.TEAM_KS, True, touch_wait=3)  # 开始
                elif self.get_rgb(RgbEnumG.JZT_END, True):
                    pass
                elif self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    if _JION:
                        if _WAIT_TIMES > 3:
                            self.time_sleep(10)
                            _JION = False
                            _WAIT_TIMES = 0
                        _WAIT_TIMES += 1
                    else:
                        self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos, touch_wait=2)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, r'学塔'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.JZT_JRQR):
                    self.air_touch((846, 439), touch_wait=2)
                    # # self.ocr_find([(822, 423, 890, 454), 'MAX'], clicked=True, touch_wait=1)
                    if self.get_rgb(RgbEnumG.JZT_JRQR, True):
                        self.time_sleep(3)
                        _JION = True
                elif self.get_rgb(RgbEnumG.BACK):  # 金字塔界面
                    # times = self.get_num((381, 516, 415, 549))  # 剩余次数
                    # if times > 0:
                    if _JION:
                        self.sn.log_tab.emit(self.mnq_name, r"金字塔-战斗完成")
                        return True
                    self.get_rgb(RgbEnumG.JZT_JR, True)
                    # else:
                    #     self.sn.log_tab.emit(self.mnq_name, r"金字塔-无次数")
                    #     return True

                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"金字塔-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"金字塔-超时异常")

    def jingying_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        _JION = False
        WAIT_TEAM = False
        self.sn.log_tab.emit(self.mnq_name, r"菁英地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"菁英地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.get_rgb(RgbEnumG.JYDC_END, True):
                    self.sn.log_tab.emit(self.mnq_name, r"菁英地城-战斗完成")
                    return True
                self.sn.log_tab.emit(self.mnq_name, r"菁英地城战斗中")
                self.time_sleep(10)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"菁英地城-组队中")
                    self.time_sleep(15)
                    self.get_rgb(RgbEnumG.TEAM_KS, True, touch_wait=3)  # 开始
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                        if not WAIT_TEAM:
                            self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.get_rgb(RgbEnumG.JYDC_END, True):
                        self.sn.log_tab.emit(self.mnq_name, r"菁英地城-战斗完成")
                        return True
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        if self.ksnr_pos[0] == 0:
                            pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                            self.ksnr_pos = tuple(pos)
                        else:
                            self.air_touch(self.ksnr_pos, touch_wait=2)
                    elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '菁英'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.get_rgb(RgbEnumG.JZT_JRQR):  # 进入界面 和金字塔一样
                        if self.get_rgb(RgbEnumG.JYDC_MAX, True):
                            if self.get_rgb(RgbEnumG.JZT_JRQR, True, touch_wait=3):
                                _JION = True
                    elif self.get_rgb(RgbEnumG.BACK):  # 菁英地城界面
                        if _JION:
                            self.sn.log_tab.emit(self.mnq_name, r"菁英地城-战斗完成")
                            return True
                        self.get_rgb(RgbEnumG.JR, True)
                    elif self.get_rgb(RgbEnumG.JYDC_END, True):
                        self.sn.log_tab.emit(self.mnq_name, r"菁英地城-战斗完成")
                        return True
                    else:
                        self.check_close()
        raise ControlTimeOut(r"菁英地城-超时异常")

    def meiri_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        _JION_TIMES = 1
        _C_OVER = False
        self.sn.log_tab.emit(self.mnq_name, r"每日地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"每日地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
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
                    self.get_rgb(RgbEnumG.TEAM_KS, True, touch_wait=3)  # 开始
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        if self.ksnr_pos[0] == 0:
                            pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                            self.ksnr_pos = tuple(pos)
                        else:
                            self.air_touch(self.ksnr_pos, touch_wait=2)
                    elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '每日'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 6:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.get_rgb(RgbEnumG.MRDC_JRQR):  # 进入界面 和金字塔一样
                        if _JION_TIMES > 3:
                            _C_OVER = True
                        if _C_OVER:
                            self.back(self.serialno)
                        # self.ocr_find([(819, 279, 875, 310), 'MAX'], clicked=True, touch_wait=1)
                        self.air_touch((833, 282))
                        if self.get_rgb(RgbEnumG.MRDC_JRQR, True):
                            _JION_TIMES += 1
                    elif self.get_rgb(RgbEnumG.BACK):  # 每日地城界面
                        if _C_OVER:
                            self.sn.log_tab.emit(self.mnq_name, r"每日地城-无次数")
                            return True
                        if self.get_rgb(RgbEnumG.MRDC_HD):  # 混沌模式
                            self.air_touch((151, 542))
                        self.get_rgb(RgbEnumG.MRDC_JR, True)
                    elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"每日地城-战斗完成")
                        return True
                    else:
                        self.check_close()
        raise ControlTimeOut(r"每日地城-超时异常")

    def guaiwu_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        _JION_TIEMS = 1
        _BAT_END = False
        self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团")
        self.sn.table_value.emit(self.mnq_name, 8, r"怪物狩猎团")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut * 3:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if _BAT_END:
                    if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-战斗完成")
                        _BAT_END = False
                    elif self.ocr_find(ImgEnumG.GWSLT_ZDJS):  # 战斗结束
                        self.crop_image_find(ImgEnumG.MR_BAT_EXIT, touch_wait=3)
                        self.ocr_find(ImgEnumG.MR_YDZXD, True)
                        _BAT_END = False
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团战斗中")
                    self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-组队中")
                    self.time_sleep(15)
                    self.get_rgb(RgbEnumG.TEAM_KS, True, touch_wait=3)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        if self.ksnr_pos[0] == 0:
                            pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                            self.ksnr_pos = tuple(pos)
                        else:
                            self.air_touch(self.ksnr_pos, touch_wait=2)
                    elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '怪物狩'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 7:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.get_rgb(RgbEnumG.GWSL_END):
                        _BAT_END = True
                        if self.ocr_find(ImgEnumG.GWSLT_ZDJL):
                            self.back(self.serialno)
                    elif self.get_rgb(RgbEnumG.BACK):  # 怪物狩猎团界面
                        if _JION_TIEMS > 3:
                            self.sn.log_tab.emit(self.mnq_name, r"怪物狩猎团-无次数")
                            return True
                        if self.get_rgb(RgbEnumG.JR, True, touch_wait=2):
                            _JION_TIEMS += 1
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
        _JR_TIME = 1
        _SWIPE_TIMES = 0
        _TASK_OVER = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut * 3:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.get_rgb(RgbEnumG.TBB_QR, True):
                    pass
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    pass
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"汤宝宝战斗中")
                    self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '理教室'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 7:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.BACK):  # 汤宝宝界面
                    if _JR_TIME > 3:
                        self.sn.log_tab.emit(self.mnq_name, r"汤宝宝-无次数")
                        return True
                    if self.get_rgb(RgbEnumG.MRDC_JR, True):
                        _JR_TIME += 1
                else:
                    self.check_close()
        raise ControlTimeOut(r"汤宝宝-超时失败")

    def jinhua_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        _JION_TIMES = 1
        self.sn.log_tab.emit(self.mnq_name, r"进化系统")
        self.sn.table_value.emit(self.mnq_name, 8, r"进化系统")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                self.get_rgb(RgbEnumG.QR, True)
                if self.get_rgb(RgbEnumG.JHXT_END):
                    if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"进化系统-战斗完成")
                        return True
                    self.get_rgb(RgbEnumG.JHXT_END, True)
                self.sn.log_tab.emit(self.mnq_name, r"进化系统战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):  # 离开队伍
                    pass
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos, touch_wait=2)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '化系'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 7:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.MR_EXIT_TEAM, True):
                    pass
                elif self.get_rgb(RgbEnumG.JHXT_JRQR):  # 入场选择
                    self.air_touch((953, 244))
                    self.get_rgb(RgbEnumG.JHXT_JRQR, True)
                elif self.get_rgb(RgbEnumG.BACK):  # 进化系统界面
                    if _JION_TIMES > 3:
                        self.sn.log_tab.emit(self.mnq_name, r"进化系统-无次数")
                        return True
                    if self.get_rgb(RgbEnumG.JR, True):
                        _JION_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"进化系统-战斗完成")
                    return True
                else:
                    self.check_close()
        raise ControlTimeOut(r"进化系统-超时异常")

    def ciyuan_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        _BAT = False
        _JION_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"次元入侵")
        self.sn.table_value.emit(self.mnq_name, 8, r"次元入侵")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut * 2:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.get_rgb(RgbEnumG.CYRQ_END):
                    if self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"次元入侵-战斗完成")
                        _BAT = False
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"次元入侵战斗中")
                    self.time_sleep(15)
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"次元入侵-组队中")
                    self.time_sleep(15)
                    self.get_rgb(RgbEnumG.TEAM_KS, True, touch_wait=3)  # 开始
                elif self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos, touch_wait=2)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '次元入侵'], True):
                        if _SWIPE_TIMES <= 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 6:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.CYQR_JR_QR):
                    self.air_touch((817, 452), touch_wait=1)
                    if self.get_rgb(RgbEnumG.CYQR_JR_QR1, True):
                        _JION_TIMES += 1
                elif self.get_rgb(RgbEnumG.BACK):  # 次元入侵系统界面
                    if self.get_rgb(RgbEnumG.CYRQ_JR_F) or _JION_TIMES > 3:
                        self.sn.log_tab.emit(self.mnq_name, r"次元入侵-无次数")
                        return True
                    self.get_rgb(RgbEnumG.CYRQ_JR, True)
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"次元入侵-战斗完成")
                    _BAT = False
                else:
                    self.check_close()
        raise ControlTimeOut(r"次元入侵-超时失败")

    def minidc_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"迷你地城")
        self.sn.table_value.emit(self.mnq_name, 8, r"迷你地城")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut * 2:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.get_rgb(RgbEnumG.MNDC_JG):
                    if self.ocr_find(ImgEnumG.MNDC_JG):
                        self.get_rgb(RgbEnumG.MNDC_JG_QR, True)
                        self.ocr_find([(401, 586, 877, 635), '移'], True)
                        self.ocr_find([(401, 586, 877, 635), '离'], True)
                        self.sn.log_tab.emit(self.mnq_name, r"迷你地城-战斗完成")
                        return True
                elif self.get_rgb(RgbEnumG.BAT_JG, True):
                    pass
                self.sn.log_tab.emit(self.mnq_name, r"迷你地城战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.get_rgb(RgbEnumG.BAT_JG, True):
                    pass
                elif self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):  # 离开队伍
                    pass
                elif self.get_rgb(RgbEnumG.MNDC_JG_LK):
                    if self.ocr_find(ImgEnumG.MNDC_JG):
                        self.get_rgb(RgbEnumG.MNDC_JG_LK, True)
                    self.sn.log_tab.emit(self.mnq_name, r"迷你地城-战斗完成")
                    return True
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos, touch_wait=2)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '迷你'], True):
                        if _SWIPE_TIMES <= 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 7:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.MNDC_JRQR, True):  # 入场选择
                    pass
                elif self.get_rgb(RgbEnumG.BACK):  # 迷你地城界面
                    self.get_rgb(RgbEnumG.MNDC_XZ, True)
                    self.get_rgb(RgbEnumG.MNDC_XZ2, True)
                    self.get_rgb(RgbEnumG.MNDC_XZ3, True)
                    self.get_rgb(RgbEnumG.MNDC_JR, True)
                elif self.get_rgb(RgbEnumG.MNDC_END, True):
                    self.sn.log_tab.emit(self.mnq_name, r"迷你地城-战斗完成")
                    return True
                elif self.ocr_find(ImgEnumG.AUTO_JG):  # 自动战斗结果
                    self.air_loop_find(ImgEnumG.UI_QR)
                elif self.ocr_find(ImgEnumG.MNDC_JR):
                    self.ocr_find(ImgEnumG.MNDC_FQ, True)
                elif self.ocr_find(ImgEnumG.MNDC_JS):
                    self.ocr_find(ImgEnumG.MNDC_JSQR, True)
                else:
                    self.check_close()
        raise ControlTimeOut(r"迷你地城-超时失败")

    def star_tower_task(self):
        s_time = time.time()
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"星光M塔")
        self.sn.table_value.emit(self.mnq_name, 8, r"星光M塔")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut * 3:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                self.sn.log_tab.emit(self.mnq_name, r"星光M塔战斗中")
                self.time_sleep(15)
            else:
                if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                    self.crop_image_find(ImgEnumG.MR_MENU)
                elif self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):  # 离开队伍
                    pass
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos, touch_wait=2)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '星光M塔'], True):
                        if _SWIPE_TIMES < 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 7:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.MR_EXIT_TEAM, True):
                    # self.air_loop_find(ImgEnumG.UI_QR)
                    pass
                elif self.ocr_find(ImgEnumG.MR_XGT_JR):  # 入场选择
                    self.air_loop_find(ImgEnumG.UI_QR)
                elif self.get_rgb(RgbEnumG.BACK):  # 星光塔界面
                    if self.get_rgb(RgbEnumG.XGT_JR, True):
                        pass
                    elif self.get_rgb(RgbEnumG.XGT_JR_F):
                        self.sn.log_tab.emit(self.mnq_name, r"星光塔-无次数")
                        return True
                elif self.get_rgb(RgbEnumG.XGT_JR, True):
                    pass
                elif self.get_rgb(RgbEnumG.XGT_ZCJR, True):
                    pass
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"星光M塔-战斗完成")
                    # return True
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
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                # self.ocr_find(ImgEnumG.AUTO_BAT_OCR, True)
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
                elif self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):  # 离开队伍
                    pass
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos, touch_wait=2)
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if not self.ocr_find([ImgEnumG.MR_AREA, '怪物公'], True):
                        if _SWIPE_TIMES <= 3:
                            self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                        else:
                            if _SWIPE_TIMES > 7:
                                _SWIPE_TIMES = 0
                            self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                        _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.GWGY_JRQR, True):
                    pass
                elif self.get_rgb(RgbEnumG.BACK):  # 怪物公园界面
                    if _JR_TIMES > 3:
                        self.sn.log_tab.emit(self.mnq_name, r"怪物公园-无次数")
                        return True
                    if self.get_rgb(RgbEnumG.GWGY_JR_F):
                        self.sn.log_tab.emit(self.mnq_name, r"怪物公园-无次数")
                        return True
                    if self.get_rgb(RgbEnumG.GWGY_JR, True):
                        _JR_TIMES += 1
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"怪物公园-战斗完成")
                    return True
                else:
                    self.check_close()

        raise ControlTimeOut(r"怪物公园-超时失败")

    def boss_task(self, **kwargs):
        s_time = time.time()
        _LEVEL = int(kwargs['角色信息']['等级'])
        _YM = True if kwargs['王图设置']['炎魔'] == '1' else False  # 是否要打
        _PKJ = True if kwargs['王图设置']['皮卡啾'] == '1' else False
        _NH = True if kwargs['王图设置']['女皇'] == '1' else False
        _YM_ING = False  # 是否进行中
        _PKJ_ING = False  # 是否进行中
        _NH_ING = False  # 是否进行中
        _YM_KN = True if kwargs['王图设置']['炎魔难度'] == '1' else False  # 难度
        _PKJ_KN = True if kwargs['王图设置']['皮卡啾难度'] == '1' else False
        _NH_KN = True if kwargs['王图设置']['女皇难度'] == '1' else False
        _YM_OVER = False if _YM else True  # 是否完成
        _PKJ_OVER = False if _PKJ else True
        _NH_OVER = False if _NH else True
        _R_BAT = False  # 失败
        _BAT_TIMES = 0
        _WAIT_TIMES = 0
        _WAIT_TEAM = False
        _WAIT_TEAM_TIMES = 0
        _SWIPE_TIMES = 0  # 滑动查找次数
        select_queue = kwargs['状态队列']['选择器']
        self.sn.log_tab.emit(self.mnq_name, r"boss远征")
        self.sn.table_value.emit(self.mnq_name, 8, r"boss远征")
        if _LEVEL < 70:
            self.sn.log_tab.emit(self.mnq_name, r"等级低于70级无法混boss")
            return True
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.MR_BAT_EXIT, False, touch_wait=3):
                if self.ocr_find(ImgEnumG.BOSS_DJ):
                    self.air_loop_find(ImgEnumG.UI_QR)
                self.air_touch(AirImgTools.turn_pos['left'], duration=1)
                r = random.randint(0, 3)
                if r > 1:
                    self.air_touch(AirImgTools.turn_pos['attack'])
                else:
                    self.air_touch(AirImgTools.turn_pos['left'], duration=1)
                    self.air_touch(AirImgTools.turn_pos['c'])
                if _BAT_TIMES > 6:
                    self.sn.log_tab.emit(self.mnq_name, r"boss远征战斗超过1分钟,退组重打")
                    self.air_touch(AirImgTools.turn_pos['right'], duration=1)
                    self.crop_image_find(ImgEnumG.MR_BAT_EXIT)
                    _R_BAT = True
                if self.ocr_find(ImgEnumG.YZD_JS):
                    self.air_touch(AirImgTools.turn_pos['right'], duration=5)
                    self.crop_image_find(ImgEnumG.MR_BAT_EXIT)
                elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                    if _YM_ING:
                        if not _R_BAT:
                            _YM_OVER = True
                            _R_BAT = False
                        _YM_ING = False
                        _BAT_TIMES = 0
                    elif _PKJ_ING:
                        if not _R_BAT:
                            _PKJ_OVER = True
                            _R_BAT = False
                        _PKJ_ING = False
                        _BAT_TIMES = 0
                    elif _NH_ING:
                        if not _R_BAT:
                            _NH_OVER = True
                            _R_BAT = False
                        _NH_ING = False
                        _BAT_TIMES = 0
                    self.sn.log_tab.emit(self.mnq_name, r"boss远征-战斗完成")
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"boss远征战斗中")
                    self.time_sleep(10)
                    _BAT_TIMES += 1
            else:
                if self.air_loop_find(ImgEnumG.TEMA_ING, False):
                    self.sn.log_tab.emit(self.mnq_name, r"boss远征-组队中")
                    self.time_sleep(15)
                    _WAIT_TIMES += 1
                    if _WAIT_TIMES > 4:
                        self.air_touch((434, 256))
                        if self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):
                            _WAIT_TEAM = False
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                        if _WAIT_TEAM:
                            if _WAIT_TEAM_TIMES > 3:
                                self.air_touch((434, 256))
                                if self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):
                                    _WAIT_TEAM = False
                            self.time_sleep(10)
                            _WAIT_TEAM_TIMES += 1
                        else:
                            self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        if self.ksnr_pos[0] == 0:
                            pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                            self.ksnr_pos = tuple(pos)
                        else:
                            self.air_touch(self.ksnr_pos, touch_wait=2)
                    elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '征'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 7:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.get_rgb(RgbEnumG.BACK):  # boss远征界面
                        if self.get_rgb(RgbEnumG.YZD_JR_F):
                            self.sn.log_tab.emit(self.mnq_name, r"boss远征-未到开启时间")
                            select_queue.task_over('AutoBoss')
                            return True
                        if _PKJ_OVER and _YM_OVER and _NH_OVER:
                            self.sn.log_tab.emit(self.mnq_name, r"boss远征-战斗完成")
                            select_queue.task_over('AutoBoss')
                            return True
                        elif _YM and not _YM_OVER:
                            if self.crop_image_find(ImgEnumG.YM):
                                if _YM_KN and _LEVEL >= 100:
                                    self.get_rgb(RgbEnumG.YZD_KN, True)  # 困难
                                else:
                                    self.get_rgb(RgbEnumG.YZD_PT, True)
                                _YM_ING = True
                            elif self.ocr_find(ImgEnumG.YM_OVER):
                                _YM_OVER = True
                        elif _PKJ and not _PKJ_OVER:
                            if self.crop_image_find(ImgEnumG.PKJ):
                                if _LEVEL<100:
                                    _PKJ_OVER = True
                                elif _PKJ_KN and _LEVEL >= 120:
                                    self.get_rgb(RgbEnumG.YZD_KN, True)  # 困难
                                else:
                                    self.get_rgb(RgbEnumG.YZD_PT, True)
                                _PKJ_ING = True
                            elif self.ocr_find(ImgEnumG.PKJ_OVER):
                                _PKJ_OVER = True
                        elif _NH and not _NH_OVER:
                            if self.crop_image_find(ImgEnumG.NH):
                                if _LEVEL<100:
                                    _NH_OVER = True
                                elif _NH_KN and _LEVEL >= 120:
                                    self.get_rgb(RgbEnumG.YZD_KN, True)  # 困难
                                else:
                                    self.get_rgb(RgbEnumG.YZD_PT, True)
                                _NH_ING = True
                            elif self.ocr_find(ImgEnumG.NH_OVER):
                                _NH_OVER = True
                        if _YM_ING or _PKJ_ING or _NH_ING:
                            if _WAIT_TEAM:
                                if _YM_ING:
                                    _YM_OVER = True
                                if _PKJ_ING:
                                    _PKJ_OVER = True
                                if _NH_ING:
                                    _NH_OVER = True
                            elif self.get_rgb(RgbEnumG.YZD_JR, True):
                                _WAIT_TEAM = True
                    else:
                        self.check_close()
        select_queue.task_over('AutoBoss')
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
                    # self.ocr_find(ImgEnumG.ZD_KS, True)
                    if _WAIT_TIMES > 3:
                        self.get_rgb(RgbEnumG.TEAM_KS, True, touch_wait=3)  # 开始
                        self.air_touch((433, 257), touch_wait=1)
                else:
                    if self.crop_image_find(ImgEnumG.INGAME_FLAG, False):
                        self.crop_image_find(ImgEnumG.MR_MENU)
                    elif self.ocr_find(ImgEnumG.MR_WLDC_PM):  # 排名结算
                        self.air_loop_find(ImgEnumG.UI_QR)
                    elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                        if self.ksnr_pos[0] == 0:
                            pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                            self.ksnr_pos = tuple(pos)
                        else:
                            self.air_touch(self.ksnr_pos, touch_wait=2)
                    elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                        if not self.ocr_find([ImgEnumG.MR_AREA, '混沌速'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 7:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                    elif self.get_rgb(RgbEnumG.BACK):  # 混沌远征界面
                        if _JR_TIMES > 3:
                            self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-无次数")
                            select_queue.task_over('AutoHDboss')
                            return True
                        if self.get_rgb(RgbEnumG.JR, True):
                            _JR_TIMES += 1
                    elif self.ocr_find(ImgEnumG.MR_YDZXD, True):
                        self.sn.log_tab.emit(self.mnq_name, r"混沌炎魔-战斗完成")
                        select_queue.task_over('AutoHDboss')
                        return True
                    else:
                        self.check_close()
        select_queue.task_over('AutoHDboss')
        raise ControlTimeOut(r"混沌炎魔-超时失败")

    def gonghui_task(self):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"公会任务")
        self.sn.table_value.emit(self.mnq_name, 8, r"公会任务")
        _JION = False
        _SWIPE_TIMES = 1
        _JION_TIMES = 1
        _JR_TIMES = 0
        _WXDC = False
        _RYZ = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
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
                if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                    if not self.crop_image_find(ImgEnumG.MR_MENU):
                        self.air_touch((1239, 36))
                elif self.get_rgb(RgbEnumG.EXIT_TEAM_QR, True):  # 离开队伍
                    pass
                elif self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                    if self.ksnr_pos[0] == 0:
                        pos = self.ocr_find(ImgEnumG.MR_MENU_KSNR, True, get_pos=True)
                        self.ksnr_pos = tuple(pos)
                    else:
                        self.air_touch(self.ksnr_pos, touch_wait=2)
                elif self.get_rgb(RgbEnumG.GH_JR, True):
                    _JION_TIMES += 1  # 确认加入公会按钮
                elif self.get_rgb(RgbEnumG.KSDY):  # 快速单元界面
                    if self.get_rgb(RgbEnumG.GH_M):
                        if _WXDC and _RYZ:
                            self.sn.log_tab.emit(self.mnq_name, r"公会任务-战斗完成")
                            return True
                        if not _WXDC:
                            self.ocr_find(ImgEnumG.GH_WXDC, True)
                        else:
                            if not _RYZ:
                                self.ocr_find(ImgEnumG.GH_RYZ, True)
                    else:
                        if not self.ocr_find([ImgEnumG.MR_AREA, '公'], True):
                            if _SWIPE_TIMES < 3:
                                self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                            else:
                                if _SWIPE_TIMES > 7:
                                    _SWIPE_TIMES = 0
                                self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                            _SWIPE_TIMES += 1
                elif self.get_rgb(RgbEnumG.GH_WXDC):
                    if _WXDC:
                        self.crop_image_find(ImgEnumG.MR_BACK)
                    else:
                        if self.get_rgb(RgbEnumG.GH_WXDC_JR_F):
                            _WXDC = True
                        elif self.get_rgb(RgbEnumG.GH_WXDC_JR, True):
                            _WXDC = True
                elif self.get_rgb(RgbEnumG.GH_RYZ):
                    self.air_loop_find(ImgEnumG.UI_QR)
                    if _RYZ or _JR_TIMES > 3:
                        if _JR_TIMES > 3:
                            _RYZ = True
                        self.get_rgb(RgbEnumG.GH_RYZ, True)
                    else:
                        if self.get_rgb(RgbEnumG.GH_RYZ_JR, True, touch_wait=2):
                            _RYZ = True
                            _JR_TIMES += 1
                        elif self.get_rgb(RgbEnumG.GH_RYZ_JR_F):
                            _RYZ = True
                elif self.get_rgb(RgbEnumG.GH_XJR):
                    if _JION_TIMES > 10:
                        self.sn.log_tab.emit(self.mnq_name, r"无法加入公会,取消公会任务")
                        return True
                    self.air_touch((666, 679), touch_wait=1)
                    if self.get_rgb(RgbEnumG.GH_JRQR, True):
                        _JION_TIMES += 1
                elif self.air_loop_find(ImgEnumG.JRGH_IMG):
                    pass

                else:
                    self.check_close()

        raise ControlTimeOut(r'公会任务-超时异常')
