# -*- coding: utf-8 -*-
import random
import time

from memory_profiler import profile

from Enum.ResEnum import ImgEnumG, GlobalEnumG, BatEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, FuHuoRoleErr
from Utils.LoadConfig import LoadConfig


class TaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(TaskAutoG, self).__init__()
        self.dev, self.serialno = devinfo
        self.sn = sn
        self.mnq_name = mnq_name

    def start_autotask(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        mrtask_queue = kwargs['每日任务']['每日任务队列']
        stop_task = kwargs['自动任务']['任务停止等级']
        use_stone = kwargs['自动任务']['随机使用石头']
        _CW_FLAG = False if kwargs['角色信息']['宠物'] == '0' else True
        _L2_FLAG = False if kwargs['角色信息']['60级'] == '0' else True
        _L3_FLAG = False if kwargs['角色信息']['90级'] == '0' else True
        s_time = time.time()
        # t_time = time.time()
        self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG,
                        **kwargs)
        self.sn.log_tab.emit(self.mnq_name, r"任务进行中")
        _COLOR = self.rgb(447, 699)
        _COLOR_1 = 'FFFFFF'
        while True:
            if time.time() - s_time > GlobalEnumG.SelectCtrTimeOut:
                self.check_close()
                s_time = time.time()
            if not self.find_info('ingame_flag2'):
                if self.find_info('task_close'):
                    if self.get_rgb([1033, 414, 'EE7047'], True):  # 完成/接受
                        pass
                    elif self.find_info('task_arrow', True,touch_wait=0):
                        pass
                    elif self.get_rgb([367, 565, '4C87AF'], True):
                        pass
                    elif self.get_rgb([361, 570, 'EE7047'], True):
                        pass
                    elif self.get_rgb([685, 515, 'EE7047'], True):
                        pass
                    elif self.get_rgb(RgbEnumG.CLOSE_GAME, True):
                        pass
                    elif self.get_rgb(RgbEnumG.EXIT_FOU, True):
                        pass
                    elif self.get_rgb(RgbEnumG.FUHUO_BTN):
                        if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                            raise FuHuoRoleErr
                    elif self.get_rgb(RgbEnumG.SKILL_M):
                        self.back()
                    elif self.find_info('ui_set'):
                        self.back()
                elif self.get_rgb([359, 636, 'EE7047'], True):
                    pass  # 领取奖励
                elif self.get_rgb([531, 632, 'EE7047'], True):
                    pass  # 领取奖励
                elif self.get_rgb(RgbEnumG.CLOSE_GAME, True):
                    pass
                elif self.get_rgb(RgbEnumG.EXIT_FOU, True):
                    pass
                elif self.get_rgb(RgbEnumG.SKIP_NEW, touch_wait=1):
                    if self.crop_image_find(ImgEnumG.JN_TEACH, touch_wait=1):
                        self.skip_fever_buff()
                    self.skip_new()
                elif self.get_rgb([1033, 414, 'EE7047'], True):
                    pass
                elif self.get_rgb([541, 537, 'EE7047'], True):
                    pass
                elif self.get_rgb([1140, 80, '415067'], True):
                    pass
                elif self.get_rgb([1140, 90, 'EE7047'], True):
                    pass
                elif self.get_rgb([528, 658, 'EE7047'], True):
                    pass
                elif self.get_rgb(RgbEnumG.SKIP_NEW, True):
                    pass
                elif self.air_loop_find(ImgEnumG.UI_QBLQ):
                    pass
                elif self.find_info('LB_close', True,touch_wait=0):
                    pass
                elif self.find_info('ingame_flag1',touch_wait=0):
                    if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                        pass
                    self.back()
                elif self.get_rgb(RgbEnumG.SKILL_M):
                    self.back()
                elif self.find_info('task_close', True,touch_wait=0):
                    pass
                elif self.find_info('task_arrow', True,touch_wait=0):
                    pass
                elif self.get_rgb([563, 634, 'EE7047'], True):
                    pass
                elif self.qr_or_qx(1):
                    pass
                else:
                    if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                        raise NotInGameErr
                    if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                        pass
                    self.back()
            else:
                if use_stone:
                    if self.find_info('xl_lkyd', True,touch_wait=0):
                        self.time_sleep(GlobalEnumG.TaskWaitTime)
                if self.get_rgb(RgbEnumG.SKIP_NEW, True):
                    self.skip_new()
                elif self.get_rgb([394, 403, 'EE7047']):
                    self.air_touch((710, 204))
                elif self.get_rgb([835, 354, 'BC3B57'], True):
                    pass  # 自动分配技能
                elif self.get_rgb([737, 395, '617B96'], True):  # 穿戴装备
                    for i in range(3):
                        self.get_rgb([737, 395, '617B96'], True)
                elif self.get_rgb([711, 206, 'FEFFF5'], True):
                    pass  # 提示装备技能
                else:
                    if self.find_info('bat_auto') or self.check_is_stop():
                        if time.time() - s_time > GlobalEnumG.TaskCheckTime:
                            self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG,
                                            **kwargs)
                            s_time = time.time()
                        if not self.find_info('task_point', True,touch_wait=0):
                            self.air_loop_find(ImgEnumG.TASK_TAB)
                        else:
                            self.time_sleep(2)
                    # if self.check_is_stop():
                    #     if not self.find_info('task_point', True):
                    #         self.air_loop_find(ImgEnumG.TASK_TAB)

    def level_task(self, stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG, **kwargs):
        """到达等级后执行任务"""
        if self.crop_image_find(ImgEnumG.SKIP_NEW, touch_wait=1):
            if self.crop_image_find(ImgEnumG.JN_TEACH, touch_wait=1):
                self.skip_fever_buff()
            self.skip_new()
        try:
            _res = int(self.check_num(0))
            _bat_res = self.check_num(1)
            if _res >= int(stop_task):
                self.sn.log_tab.emit(self.mnq_name, r"超过任务停止等级")
                return 1
        except Exception:
            return 0
        if _res != 0:
            kwargs['角色信息']['等级'] = _res
            kwargs['角色信息']['战力'] = _bat_res
            LoadConfig.writeconf(self.mnq_name, '等级', str(_res), ini_name=self.mnq_name)
            LoadConfig.writeconf(self.mnq_name, '战力', _bat_res, ini_name=self.mnq_name)
            self.sn.table_value.emit(self.mnq_name, 3, f"{_res}")
            self.sn.table_value.emit(self.mnq_name, 5, f"{_bat_res}")
            if 100 >= kwargs['角色信息']['等级'] >= 30 and not _CW_FLAG:
                select_queue.put_queue('UseSkill')
                select_queue.put_queue('UsePet')
                select_queue.put_queue('GetLevelReard')
                # select_queue.put_queue('CheckRole')
                _CW_FLAG = True
                raise NotInGameErr
            elif 100 >= kwargs['角色信息']['等级'] >= 60 and not _L2_FLAG:
                # r = random.randint(1, 3)
                # mrtask_queue.put_queue(str(r))  # 武林
                # select_queue.put_queue('AutoMR')
                select_queue.put_queue('UseSkill')
                select_queue.put_queue('GetLevelReard')
                # select_queue.put_queue('CheckRole')
                kwargs['角色信息']['60级'] = '1'
                _L2_FLAG = True
                raise NotInGameErr
            elif 100 >= kwargs['角色信息']['等级'] >= 90 and not _L3_FLAG:
                # r = random.randint(1, 3)
                # exec_queue = kwargs['状态队列']['执行器']
                select_queue.put_queue('CheckRole')
                # mrtask_queue.put_queue(str(r))  # 武林
                # select_queue.put_queue('AutoMR')
                select_queue.put_queue('UseSkill')
                select_queue.put_queue('GetLevelReard')
                # select_queue.put_queue('CheckRole')
                # self.sete_mapdata('3', '西边森林', **kwargs)
                # kwargs['角色信息']['90级'] = True
                # exec_queue.task_over('AutoTask')
                # exec_queue.put_queue('AutoBat')
                _L3_FLAG = True
                raise NotInGameErr

    def sete_mapdata(self, xt_yt, map_name, **kwargs):
        kwargs['任务id'] = xt_yt
        kwargs['战斗数据']['地图数据'] = BatEnumG.MAP_DATA[xt_yt][map_name],
        kwargs['战斗数据']['地图识别'] = BatEnumG.MAP_OCR[map_name]
        kwargs['地图名'] = BatEnumG.MAP_OCR[map_name][0][-1]
        self.sn.table_value.emit(self.mnq_name, 2, map_name)
        LoadConfig.writeconf(self.mnq_name, '最近任务', map_name, ini_name=self.mnq_name)
