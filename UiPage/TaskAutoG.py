# -*- coding: utf-8 -*-
import random
import time
from Enum.ResEnum import ImgEnumG, GlobalEnumG, BatEnumG, RgbEnumG, MulColorEnumG, WorldEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, FuHuoRoleErr, BagFullerr
from Utils.LoadConfig import LoadConfig


class TaskAutoG(BasePageG):
    def __init__(self, devinfo, sn):
        super(TaskAutoG, self).__init__()
        self.dev, self.mnq_name = devinfo
        self.sn = sn

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
        self.check_level_star()
        if self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG,
                           **kwargs) == 1:
            return 1
        self.sn.log_tab.emit(self.mnq_name, r"任务进行中")
        _COLOR = self.rgb(447, 699)
        _COLOR_1 = 'FFFFFF'
        __i = 0
        while True:
            self.sn.log_tab.emit(self.mnq_name, r"任务进行中..")
            if time.time() - s_time > GlobalEnumG.SelectCtrTimeOut:
                self.check_close()
                s_time = time.time()
            if self.pic_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            if self.pic_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
            if not self.find_color(MulColorEnumG.IGAME):
                if self.mul_color(MulColorEnumG.TASK_CLOSE):
                    if self.cmp_rgb([1033, 414, 'ee7046'], True):  # 完成/接受
                        self.sn.log_tab.emit(self.mnq_name, r"完成/接受")  # 完成/接受
                    elif self.word_find(WorldEnumG.TASK_ARROW, True):
                        for i in range(3):
                            self.word_find(WorldEnumG.TASK_ARROW, True)
                            if self.cmp_rgb([1033, 414, 'ee7046'], True):
                                break
                        self.sn.log_tab.emit(self.mnq_name, r"点击对话箭头")
                    elif self.cmp_rgb([367, 565, '4c87b0'], True):
                        pass
                    elif self.cmp_rgb([361, 570, 'ee7046'], True):
                        pass
                    elif self.cmp_rgb([685, 515, 'ee7046'], True):
                        pass
                    elif self.cmp_rgb(RgbEnumG.CLOSE_GAME, True):
                        pass
                    elif self.cmp_rgb(RgbEnumG.EXIT_FOU, True):
                        pass
                    elif self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                        if self.pic_find(ImgEnumG.CZ_FUHUO):
                            raise FuHuoRoleErr
                    elif self.cmp_rgb(RgbEnumG.SKILL_M):
                        self.back()
                    elif self.word_find(WorldEnumG.SET_BTN):
                        self.back()
                elif self.cmp_rgb([359, 636, 'ee7046'], True):
                    self.sn.log_tab.emit(self.mnq_name, r"领取奖励")  # 领取奖励
                elif self.cmp_rgb([531, 632, 'ee7046'], True):
                    pass  # 领取奖励
                elif self.cmp_rgb([685, 515, 'ee7046'], True):
                    pass  # 幻影技能确认
                elif self.cmp_rgb(RgbEnumG.CLOSE_GAME, True):
                    pass
                elif self.cmp_rgb(RgbEnumG.EXIT_FOU, True):
                    pass
                elif self.cmp_rgb(RgbEnumG.SKIP_NEW, touch_wait=1):
                    if self.pic_find(ImgEnumG.JN_TEACH, touch_wait=1):
                        self.skip_fever_buff()
                    self.skip_new()
                elif self.cmp_rgb([1033, 414, 'ee7046'], True):
                    pass
                elif self.cmp_rgb([541, 537, 'ee7046'], True):
                    pass
                elif self.cmp_rgb([1140, 80, '415066'], True):
                    pass
                elif self.cmp_rgb([1140, 90, 'ee7046'], True):
                    pass
                elif self.cmp_rgb([528, 658, 'ee7046'], True):
                    pass
                elif self.cmp_rgb(RgbEnumG.SKIP_NEW, True):
                    pass
                elif self.pic_find(ImgEnumG.UI_QBLQ):
                    pass
                elif self.find_color(MulColorEnumG.IGAME):
                    if self.pic_find(ImgEnumG.CZ_FUHUO):
                        pass
                    self.back()
                elif self.cmp_rgb(RgbEnumG.SKILL_M):
                    self.back()
                elif self.word_find(WorldEnumG.TASK_ARROW, True, touch_wait=0):
                    pass
                elif self.cmp_rgb([563, 634, 'ee7046'], True):
                    pass
                elif self.qr_tip():
                    pass
                else:
                    if __i > 2:
                        self.back()
                        __i = 0
                    else:
                        __i += 1
            else:
                __i = 0
                if use_stone:
                    if self.cmp_rgb([737, 203, '617a95'], True):
                        self.time_sleep(GlobalEnumG.TaskWaitTime)
                    # if self.find_info('xl_lkyd', True,touch_wait=0):
                    #     self.time_sleep(GlobalEnumG.TaskWaitTime)
                if self.cmp_rgb(RgbEnumG.SKIP_NEW, True):
                    self.skip_new()
                elif self.cmp_rgb([394, 403, 'ee7046']):
                    self.touch((710, 204))
                elif self.cmp_rgb([735, 345, 'bc3c57'], True):
                    pass  # 自动分配技能
                elif self.cmp_rgb([835, 354, 'bc3b57'], True):
                    pass
                elif self.cmp_rgb([711, 206, 'FEFFF5'], True):
                    pass  # 提示装备技能
                elif self.cmp_rgb([737, 395, '617a95']):  # 穿戴装备
                    self.cmp_rgb([835, 354, 'bc3b57'], True)
                    self.cmp_rgb([735, 345, 'bc3c57'], True)
                    self.sn.log_tab.emit(self.mnq_name, r"穿戴装备")
                    for i in range(3):
                        self.cmp_rgb([737, 395, '617a95'], True)
                else:
                    if self.find_color([70, 179, 339, 390, 'ff00ce-000000']):
                        self.sn.log_tab.emit(self.mnq_name, r"做完主线任务停止任务")
                        return 1
                    if not self.word_find(WorldEnumG.TASK_AUTO) and self.find_color(MulColorEnumG.IGAME):
                        if self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG,
                                           **kwargs) == 1:
                            return 1
                        if self.pic_find(ImgEnumG.BAG_MAX_IMG):
                            self.sn.log_tab.emit(self.mnq_name, r"背包满了,清理背包")
                            raise BagFullerr
                        if not self.mul_color(MulColorEnumG.INGAME_FLAG) and self.find_color(MulColorEnumG.IGAME):
                            self.back()
                        if not self.cmp_rgb([476, 216, '617a95']):
                            if not self.mul_color(MulColorEnumG.TASK_POINT, True, touch_wait=0):
                                self.pic_find(ImgEnumG.TASK_TAB)
                                if not self.mul_color(MulColorEnumG.TASK_POINT, True, touch_wait=0):
                                    self.task_block()
                            self.time_sleep(3)
                    else:
                        if self.find_color(MulColorEnumG.IGAME):
                            if self.level_task(stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG,
                                               **kwargs) == 1:
                                return 1
                    self.time_sleep(2)

    def level_task(self, stop_task, select_queue, mrtask_queue, _CW_FLAG, _L2_FLAG, _L3_FLAG, **kwargs):
        """到达等级后执行任务"""
        if self.pic_find(ImgEnumG.SKIP_NEW, touch_wait=1):
            if self.pic_find(ImgEnumG.JN_TEACH, touch_wait=1):
                self.skip_fever_buff()
            self.skip_new()
        try:
            _res = int(self.check_num(4))
            _bat_res = self.check_num(3)
            self.sn.table_value.emit(self.mnq_name, 3, f"{_res}")
            self.sn.table_value.emit(self.mnq_name, 5, f"{_bat_res}")
            LoadConfig.writeconf(self.mnq_name, '等级', str(_res), ini_name=self.mnq_name)
            LoadConfig.writeconf(self.mnq_name, '战力', str(_bat_res), ini_name=self.mnq_name)
            self.sn.log_tab.emit(self.mnq_name, f"等级:{_res}_战力:{_bat_res}")
            if _res >= int(stop_task):
                self.sn.log_tab.emit(self.mnq_name, r"超过任务停止等级")
                return 1
        except Exception as e:
            print(e)
            return 0
        if _res != 0 and kwargs['自动任务']['成长奖励检查']:
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
                if self.word_find(WorldEnumG.TASK_AUTO):
                    self.touch((448, 654), touch_wait=2)
                raise NotInGameErr
            elif 100 >= kwargs['角色信息']['等级'] >= 60 and not _L2_FLAG:
                r = random.randint(1, 3)
                mrtask_queue.put_queue(str(r))  # 武林
                select_queue.put_queue('AutoMR')
                select_queue.put_queue('UseSkill')
                select_queue.put_queue('GetLevelReard')
                # select_queue.put_queue('CheckRole')
                kwargs['角色信息']['60级'] = '1'
                _L2_FLAG = True
                if self.word_find(WorldEnumG.TASK_AUTO):
                    self.touch((448, 654), touch_wait=2)
                raise NotInGameErr
            elif 100 >= kwargs['角色信息']['等级'] >= 90 and not _L3_FLAG:
                r = random.randint(1, 3)
                # exec_queue = kwargs['状态队列']['执行器']
                # select_queue.put_queue('CheckRole')
                mrtask_queue.put_queue(str(r))  # 武林
                select_queue.put_queue('AutoMR')
                select_queue.put_queue('UseSkill')
                select_queue.put_queue('GetLevelReard')
                # select_queue.put_queue('CheckRole')
                # self.sete_mapdata('3', '西边森林', **kwargs)
                # kwargs['角色信息']['90级'] = True
                # exec_queue.task_over('AutoTask')
                # exec_queue.put_queue('AutoBat')
                _L3_FLAG = True
                if self.word_find(WorldEnumG.TASK_AUTO):
                    self.touch((448, 654), touch_wait=2)
                raise NotInGameErr
        return 0

    def sete_mapdata(self, xt_yt, map_name, **kwargs):
        kwargs['任务id'] = xt_yt
        kwargs['战斗数据']['地图数据'] = BatEnumG.MAP_DATA[xt_yt][map_name],
        kwargs['战斗数据']['地图识别'] = BatEnumG.MAP_OCR[map_name]
        kwargs['地图名'] = BatEnumG.MAP_OCR[map_name][0][-1]
        self.sn.table_value.emit(self.mnq_name, 2, map_name)
        LoadConfig.writeconf(self.mnq_name, '最近任务', map_name, ini_name=self.mnq_name)
