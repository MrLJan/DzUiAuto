# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import ImgEnumG, ColorEnumG, GlobalEnumG, BatEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import RestartTask, NotInGameErr
from Utils.LoadConfig import LoadConfig


class TaskAutoG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn, ocr):
        super(TaskAutoG, self).__init__()
        self.dev, self.serialno = devinfo
        self.sn = sn
        self.mnq_name = mnq_name
        self.cn_ocr = ocr

    def start_autotask(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        mrtask_queue = kwargs['每日任务']['每日任务队列']
        stop_task = kwargs['自动任务']['任务停止等级']
        use_stone = kwargs['自动任务']['随机使用石头']
        _CW_FLAG = False if kwargs['角色信息']['宠物'] == '0' else True
        _L2_FLAG = False if kwargs['角色信息']['60级'] == '0' else True
        _L3_FLAG = False if kwargs['角色信息']['90级'] == '0' else True
        s_time = time.time()
        t_time = time.time()
        level = LoadConfig.getconf(self.mnq_name, '等级', ini_name=self.mnq_name)
        if int(level) == 0:
            self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG,
                            **kwargs)
        if int(level) >= int(stop_task):
            self.sn.log_tab.emit(self.mnq_name, r"超过任务停止等级")
            return 1
        self.sn.log_tab.emit(self.mnq_name, r"任务进行中")
        _COLOR = self.rgb(447, 699)
        _COLOR_1 = 'FFFFFF'
        while True:
            if time.time() - s_time > GlobalEnumG.TaskCheckTime:
                self.check_err()
                s_time = time.time()
            if not self.air_loop_find(ImgEnumG.INGAME_FLAG2, False):
                if not self.get_rgb(1033, 414, 'EE7046', True):  # 完成/接受
                    self.air_touch((1168, 495))
                    if self.get_rgb(367, 565, '4C87AF', True):
                        pass
                    elif self.get_rgb(367, 565, 'EE7046', True):
                        pass
                    elif self.get_rgb(359, 636, 'EE7046', True):
                        pass  # 领取奖励
                    elif self.get_rgb(531, 632, 'EE7046', True):
                        pass  # 领取奖励
                    elif self.get_rgb(685, 515, 'EE7046', True):
                        pass
                    elif self.mulcolor_check(ColorEnumG.SKIP_NEW, touch_wait=1):
                        if self.crop_image_find(ImgEnumG.JN_TEACH, touch_wait=1):
                            self.skip_fever_buff()
                        self.skip_new()
                    elif self.get_rgb(1033, 414, 'EE7046', True):
                        pass
                    elif self.get_rgb(541, 537, 'EE7046', True):
                        pass
                    elif self.get_rgb(1140, 80, '415067', True):
                        pass
                    elif self.get_rgb(1140, 90, 'FFFFFF', True):
                        pass

                    elif self.mulcolor_check(ColorEnumG.SKIP_NEW, True):
                        pass
                    else:
                        self.close_window()
                elif self.get_rgb(563, 634, 'EE7046', True):
                    pass
                else:
                    self.air_loop_find(ImgEnumG.UI_QR)
            else:
                if self.crop_image_find(ImgEnumG.SKIP_NEW, touch_wait=1):
                    self.skip_new()
                elif self.get_rgb(394, 403, 'EE7046'):
                    self.air_touch((710, 204))
                self.get_rgb(835, 354, 'BC3B57', True)  # 自动分配技能
                self.get_rgb(737, 395, '617B96', True)  # 穿戴装备
                if self.check_is_stop():
                    if time.time() - t_time > GlobalEnumG.TaskCheckTime:
                        t_time = time.time()
                        self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG,
                                        **kwargs)
                if self.crop_image_find(ImgEnumG.AUTO_BAT, False) or self.get_rgb(427, 653, 'D3D3') or self.get_rgb(427,
                                                                                                                    653,
                                                                                                                    '7575'):  # self.crop_image_find(ImgEnumG.AUTO_BAT1):
                    self.get_rgb(711, 206, 'FEFFF5', True)  # 提示装备技能
                    if time.time() - t_time > GlobalEnumG.TaskCheckTime:
                        t_time = time.time()
                        self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG, **kwargs)
                    else:
                        if self.check_is_stop():
                            if not self.air_loop_find(ImgEnumG.TASK_POINT):
                                self.air_loop_find(ImgEnumG.TASK_TAB)
                        self.time_sleep(GlobalEnumG.TaskWaitTime)
                else:
                    if use_stone:
                        r = random.randint(0, 2)
                        if r == 0:
                            if self.get_rgb(1058, 376, '617A98', True):
                                self.time_sleep(GlobalEnumG.TaskWaitTime)
                        # else:
                        #     self.time_sleep(GlobalEnumG.TaskWaitTime)
                    # if self.check_is_stop():
                    #     if not self.air_loop_find(ImgEnumG.TASK_POINT):
                    #         self.air_loop_find(ImgEnumG.TASK_TAB)
                    self.time_sleep(GlobalEnumG.TaskWaitTime)

    def level_task(self, stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG, **kwargs):
        """到达等级后执行任务"""
        if self.crop_image_find(ImgEnumG.SKIP_NEW, touch_wait=1):
            if self.crop_image_find(ImgEnumG.JN_TEACH, touch_wait=1):
                self.skip_fever_buff()
            self.skip_new()
        res = self.check_rolelevel()
        if res[0] == 0 and res[-1] == 0:
            return 0
        if res[0] >= int(stop_task):
            self.sn.log_tab.emit(self.mnq_name, r"超过任务停止等级")
            return 1
        kwargs['角色信息']['等级'] = res[0]
        kwargs['角色信息']['战力'] = res[-1]
        LoadConfig.writeconf(self.mnq_name, '等级', str(res[0]), ini_name=self.mnq_name)
        LoadConfig.writeconf(self.mnq_name, '战力', str(res[-1]), ini_name=self.mnq_name)
        self.sn.table_value.emit(self.mnq_name, 3, f"{res[0]}")
        self.sn.table_value.emit(self.mnq_name, 5, f"{res[-1]}")
        if kwargs['角色信息']['等级'] >= 30 and not _CW_FLAG:
            select_queue.put_queue('UseSkill')
            select_queue.put_queue('UsePet')
            select_queue.put_queue('GetLevelReard')
            # select_queue.put_queue('CheckRole')
            _CW_FLAG = True
            raise NotInGameErr
        elif kwargs['角色信息']['等级'] >= 60 and not _L2_FLAG:
            r = random.randint(1, 3)
            mrtask_queue.put_queue(str(r))  # 武林
            select_queue.put_queue('AutoMR')
            select_queue.put_queue('UseSkill')
            select_queue.put_queue('GetLevelReard')
            # select_queue.put_queue('CheckRole')
            kwargs['角色信息']['60级'] = '1'
            _L2_FLAG = True
            raise NotInGameErr
        elif kwargs['角色信息']['等级'] >= 90 and not _L3_FLAG:
            r = random.randint(1, 3)
            exec_queue=kwargs['状态队列']['执行器']
            mrtask_queue.put_queue(str(r))  # 武林
            select_queue.put_queue('AutoMR')
            select_queue.put_queue('GetLevelReard')
            # select_queue.put_queue('CheckRole')
            self.change_mapdata('3','西边森林',**kwargs)
            kwargs['角色信息']['90级'] = True
            exec_queue.task_over('AutoTask')
            exec_queue.put_queue('AutoBat')
            _L3_FLAG = True
            raise NotInGameErr

    def check_rolelevel(self):
        res = [0, 0]
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.get_rgb(805, 376, '617A98', True):
                self.air_touch((852, 114))
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if self.check_is_stop():
                    self.air_touch((72, 17), touch_wait=2)
                else:
                    if not self.air_loop_find(ImgEnumG.TASK_POINT):
                        self.air_loop_find(ImgEnumG.TASK_TAB)
            elif self.mulcolor_check(ColorEnumG.ROLE_INFO):
                res = self.get_roleinfo([(328, 133, 498, 173), (319, 235, 524, 268)])
                self.mulcolor_check(ColorEnumG.ROLE_INFO, True)
                return res
            elif self.key_event(self.serialno, 'back'):
                self.mulcolor_check(ColorEnumG.EXIT_GAME, True, touch_wait=1)
            else:
                if time.time() - s_time > GlobalEnumG.SelectCtrTimeOut / 2:
                    self.close_window()
        return res

    def change_mapdata(self, xt_yt, map_name, **kwargs):
        kwargs['任务id'] = xt_yt
        kwargs['战斗数据']['地图数据'] = BatEnumG.MAP_DATA[xt_yt][map_name],
        kwargs['战斗数据']['地图识别'] = BatEnumG.MAP_OCR[map_name]
        kwargs['地图名'] = BatEnumG.MAP_OCR[map_name][0][-1]
        self.sn.table_value.emit(self.mnq_name, 2, map_name)
        LoadConfig.writeconf(self.mnq_name, '最近任务', map_name, ini_name=self.mnq_name)
