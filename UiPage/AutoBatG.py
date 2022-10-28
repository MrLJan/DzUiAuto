# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG, RgbEnumG
from UiPage.BasePage import BasePageG


class AutoBatG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn, ocr):
        super(AutoBatG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.move_spend = 0
        self.cn_ocr = ocr

    def _get_move_xy(self):
        res = self.crop_image_find(ImgEnumG.PERSON_POS, clicked=False, get_pos=True)
        if not res[0]:
            self.crop_image_find(ImgEnumG.S_MAP, touch_wait=1)
        return res

    def find_map_move(self, map_data, map_x, map_y, wait_queue, louti_queue):
        if map_y == map_data[0][-1] and not louti_queue.check_queue('1') and map_y != 135:
            louti_queue.queue.queue.clear()
            louti_queue.put_queue('1')
        # if map_louti[-1] == 135 and map_y in [148, 156, 150]:
        #     louti_queue.queue.queue.clear()
        #     louti_queue.put_queue('1')
        if louti_queue.queue.empty() or louti_queue.check_queue('1'):
            if abs(map_y - map_data[0][-1]) <= 2:
                if map_data[0][0] == 928:
                    r = random.randint(0, 1)
                else:
                    r = random.randint(0, 2)
                if r > 0:
                    for i in map_data[0]:
                        if not wait_queue.queue.empty():
                            return i, map_data[0][-1]
                        else:
                            if abs(map_x - i) <= map_data[3][0]:
                                if i == 1050 and abs(map_x - i) >= 10:
                                    return 0, 0
                                louti_queue.task_over('1')
                                louti_queue.put_queue('2')
                                return i, map_data[0][-1]
        elif louti_queue.check_queue('2'):
            if abs(map_y - map_data[1][-1]) <= 2:
                if map_data[1][0] == 995:
                    r = random.randint(0, 5)
                    if r > 0:
                        return 0, 0
                for i in map_data[1]:
                    if not wait_queue.queue.empty():
                        return i, map_data[1][-1]
                    else:
                        if abs(map_x - i) <= map_data[3][1]:
                            louti_queue.task_over('2')
                            louti_queue.put_queue('3')
                            return i, map_data[1][-1]
            return 0, 0
        elif louti_queue.check_queue('3'):
            if abs(map_y - map_data[2][-1]) <= 2:
                for i in map_data[2]:
                    if not wait_queue.queue.empty():
                        return i, map_data[2][-1]
                    else:
                        if abs(map_x - i) <= map_data[3][1]:
                            louti_queue.task_over('3')
                            louti_queue.put_queue('1')
                            return i, map_data[2][-1]
            return 0, 0
        return 0, 0

    def find_jump_louti(self, louti_x, saodi_mode):
        """到达楼梯点后跳跃"""
        res, x, y = self._get_move_xy()
        res2, x2, y2 = True, 0, 0
        for i in range(10):
            if i == 4:
                # print(f"reset_spend{i}")
                self.move_spend = 0
            res1, x1, y1 = self._get_move_xy()
            if x1 == 0:
                self.move_turn('left', 1.2)
                if y1 != y:
                    return False, x1
            else:
                if y1 != y:
                    return False, x1
                if x1 in range(louti_x - 5, louti_x + 5):
                    if louti_x in [972, 975, 1096, 1151, 1171]:
                        self.move_turn('jump', 0.32)
                        self.time_sleep(1)
                        self.move_turn('jump', 0.38)
                        self.time_sleep(1)
                    if louti_x in [898, 989, 1096, 1100, 1211, 1212]:
                        self.move_turn('jump', 0.25)
                        self.time_sleep(1)
                    self.move_turn('jump', 0.32)
                    if louti_x in [1096]:
                        self.double_jump('left')
                    return True, x1
                if x1 - louti_x < 0:
                    # print(self.move_spend)
                    if self.move_spend == 0:
                        t = abs(x1 - louti_x) / 28
                        self.move_turn('right', t)
                        res_1, x_1, y_1 = self._get_move_xy()
                        if res_1 == 1:
                            if res_1 == 1:
                                spend = abs(x1 - x_1) / t
                                if 10 < spend < 45:
                                    # print(f"spend:{spend}")
                                    self.move_spend = spend
                    else:
                        t = abs(x1 - louti_x) / self.move_spend
                        if t > 5:
                            t = abs(x1 - louti_x) / 28
                        self.move_turn('right', t)
                    if t > 0.7:
                        if saodi_mode == '0':
                            self.move_turn('attack', 0.23)
                else:
                    # print(self.move_spend)
                    if self.move_spend == 0:
                        t = abs(x1 - louti_x) / 28
                        self.move_turn('left', t)
                        res_2, x_2, y_2 = self._get_move_xy()
                        if res_2 == 1:
                            spend = abs(x1 - x_2) / t
                            if 10 < spend < 45:
                                # print(f"spend:{spend}")
                                self.move_spend = spend
                    else:
                        t = abs(x1 - louti_x) / self.move_spend
                        self.move_turn('left', t)
                    if t > 0.5:
                        if saodi_mode == '0':
                            self.move_turn('attack', 0.23)
                    if i > 8:
                        _r = random.randint(0, 1)
                        if _r == 0:
                            self.double_jump('right')
                        else:
                            self.double_jump('left')
                # res2, x2, y2 = self._get_move_xy()

        res1, x1, y1 = self._get_move_xy()
        return True, x1

    def move_up_louti(self, louti_x, louti_y, louti_queue, turn_queue, wait_queue, saodi_mode):
        """反复移动至楼梯点附近"""
        for i in range(3):
            res, now_x = self.find_jump_louti(louti_x, saodi_mode)
            if not res:
                return False
            if now_x - louti_x > 1:
                if self.move_spend == 0:
                    self.move_turn('left', abs(now_x - louti_x) / 30)
                else:
                    self.move_turn('left', abs(now_x - louti_x) / self.move_spend)
            elif now_x - louti_x < 0:
                if self.move_spend == 0:
                    self.move_turn('right', abs(now_x - louti_x) / 30)
                else:
                    self.move_turn('right', abs(now_x - louti_x) / self.move_spend)
            res2, x2, y2 = self._get_move_xy()
            if y2 != louti_y:
                if not wait_queue.queue.empty():
                    r = random.randint(10, 30)
                    self.sn.log_tab.emit(self.mnq_name, f"爬绳子在线休息{r}秒")
                    self.time_sleep(r)
                    self.sn.log_tab.emit(self.mnq_name, f"休息结束")
                    wait_queue.task_over(True)
                else:
                    self.move_turn('up', 1.42)
                    if louti_x in [1212, 1022, 1067]:  # 绳子长的补一下
                        self.move_turn('up', 0.67)
                    if louti_x in [1036]:
                        self.move_turn('jump', 0.38)
                    # self.keypress_and_up(self.dm, "up", 2.12)
                return True
            # if i == 1:
            #     self.move_turn('up', 1.84)
            # self.keypress_and_up(self.dm, "up", 1.84)
        return False

    def keep_bat(self, turn, auto_time, saodi_mode):
        """长按技能职业，幻影"""
        r = random.randint(1, 20)
        if saodi_mode == '1':
            self.move_turn(turn, auto_time * 1.5)
        else:
            if r > 1:
                self.mul_point_touch(turn, 'attack', auto_time * 1.5, True)
            else:
                self.mul_point_touch(turn, 'c', auto_time * 1.5, True)

    def keep_bat_2(self, turn, auto_time, saodi_mode):
        r = random.randint(0, 1)
        self.move_turn(turn, auto_time * 2)
        if saodi_mode == '0':
            if r == 0:
                self.mul_point_touch(turn, 'attack', auto_time * 1.5)
            else:
                self.mul_point_touch(turn, 'c', auto_time * 1.5)

    def move_bat(self, move_to, key_time, zhiye_id, saodi_mode):
        if move_to == 'left':
            i = random.randint(1, 2)
        else:
            i = random.randint(3, 4)
        if i == 1:
            if zhiye_id == '1':
                self.double_jump('left')
                self.keep_bat_2('left', key_time, saodi_mode)
                if saodi_mode == '0':
                    self.move_turn('f', 0.14)
                    self.move_turn('v', 0.32)
            else:
                self.double_jump('left')
                self.keep_bat('left', key_time, saodi_mode)

        elif i == 2:
            if zhiye_id == '1':
                self.keep_bat_2('left', key_time, saodi_mode)
            else:
                self.keep_bat('left', key_time, saodi_mode)
        elif i == 3:
            if zhiye_id == '1':
                if saodi_mode == '0':
                    self.move_turn('c', 0.19)
                    self.move_turn('d', 0.34)
                self.keep_bat_2('right', key_time, saodi_mode)
            else:
                self.keep_bat('right', key_time, saodi_mode)
        elif i == 4:
            if zhiye_id == '1':
                self.double_jump('right')
                self.keep_bat_2('right', key_time, saodi_mode)
            else:
                self.double_jump('right')
                self.keep_bat('right', key_time, saodi_mode)

    def keyboard_bat(self, **kwargs):
        auto_choose = kwargs['托管模式']
        if auto_choose:
            self.get_mapdata(**kwargs)
            map_data = kwargs['战斗数据']['地图数据'][0]
        else:
            map_data = list(kwargs['战斗数据']['地图数据'])
        select_queue = kwargs['状态队列']['选择器']
        zhiye_id = kwargs['战斗数据']['职业类型']
        wait_queue = kwargs['战斗数据']['休息队列']
        saodi_mode = kwargs['战斗数据']['刷图模式']
        louti_queue = kwargs['战斗数据']['楼梯队列']
        turn_queue = kwargs['战斗数据']['方向队列']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        use_autobat = kwargs['挂机设置']['混合自动按键']
        use_time = int(kwargs['挂机设置']['挂机卡时长'])
        bat_sleep = kwargs['挂机设置']['随机休息']
        bat_sleep_mode = kwargs['挂机设置']['休息方式']
        min_x = map_data[-1][-1]
        dingshi = True if kwargs['每日任务']['定时任务'] == '1' else False
        _r = random.randint(30, 60)
        _use = time.time()
        _s_time = time.time()
        _c_time = time.time()
        i = 0
        _res_hp_mp = self.check_hp_mp()
        if _res_hp_mp != '':
            if use_mp:
                if 'MP' in _res_hp_mp:
                    return -1
        # elif self.ocr_find(ImgEnumG.MP_NULL_OCR, touch_wait=0) and use_mp:
        #     return -1
        elif self.ocr_find(ImgEnumG.BAG_FULL, touch_wait=0):
            return -1
        while True:
            if dingshi:
                if self.get_time_to_dotask(**kwargs) == 0:
                    return 0
            if bat_sleep:
                if time.time() - _s_time > _r * 100:
                    _s_time = time.time()
                    _t = random.randint(20, 30)
                    if bat_sleep_mode == '1':
                        self.sn.log_tab.emit(self.mnq_name, f"在线休息{_t}秒")
                        self.time_sleep(_t)
                    else:
                        self.stop_game(self.serialno)
                        self.sn.log_tab.emit(self.mnq_name, f"离线休息{_t * 30}秒")
                        self.time_sleep(_t * 30)
            if use_autobat:
                if time.time() - _use > use_time * 10:
                    _use = time.time()
                    self.use_auto(use_time, **kwargs)
            if self.get_rgb(RgbEnumG.FUHUO_BTN):
                self.check_err()
            if self.get_rgb(RgbEnumG.BAT_JG, True): pass
            if time.time() - _c_time > GlobalEnumG.CheckRoleTime:
                select_queue.put_queue("CheckRole")
                return 0
            if i % 5 == 0:
                if not self.crop_image_find(ImgEnumG.INGAME_FLAG2, False, touch_wait=0):
                    return -1
                else:
                    # self.get_rgb(836, 391, '607B96', True)
                    if self.get_rgb([736, 394, '617B96']):
                        self.air_touch((845, 390))
                    if not self.crop_image_find(ImgEnumG.AUTO_BAT, False, touch_wait=0):
                        self.air_touch((423, 655), touch_wait=2)  # 点击确认战斗结果
                    else:
                        self.crop_image_find(ImgEnumG.XC_IMG)
                    if self.air_loop_find(ImgEnumG.RES_EXIT_TEAM, False, touch_wait=0):
                        if not self.use_auto(10, **kwargs):
                            return -1
                    elif not self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                        return -1
                    if self.crop_image_find(ImgEnumG.BAG_MAX_IMG, False):
                        return -1
            if min_x > 871:
                k_time = round(random.randint(5, 10) / 10, 2)
            else:
                k_time = round(random.randint(10, 20) / 10, 2)
            res, map_x, map_y = self._get_move_xy()
            if not res:
                self.crop_image_find(ImgEnumG.S_MAP, touch_wait=1)
            else:
                turn, turn_y = self.find_map_move(map_data, map_x, map_y, wait_queue, louti_queue)
                if turn != 0:
                    if not self.move_up_louti(turn, turn_y, louti_queue, turn_queue, wait_queue, saodi_mode):
                        res4, map_x4, map_y4 = self._get_move_xy()
                        if map_x4 == map_x:
                            _i = random.randint(0, 1)
                            if _i == 0:
                                self.move_turn('left', 0.32)
                            else:
                                self.move_turn('right', 0.32)
                        res6, map_x6, map_y6 = self._get_move_xy()
                        if map_x4 == map_x6:
                            self.move_turn('up', 1.12)
                else:
                    res3, map_x3, map_y3 = self._get_move_xy()
                    if map_data[-1][0] > map_x3 > map_data[-1][1]:
                        turn_queue.task_over('right')
                        turn_queue.put_queue('left')
                    elif map_data[-1][2] > map_x3 > map_data[-1][-1]:
                        turn_queue.task_over('left')
                        turn_queue.put_queue('right')
                    else:
                        _ro = random.randint(0, 10)
                        if _ro > 5:
                            _o = random.randint(0, 1)
                            if _o == 0:
                                turn_queue.task_over('left')
                                turn_queue.put_queue('right')
                            else:
                                turn_queue.task_over('right')
                                turn_queue.put_queue('left')
                    move_to = turn_queue.get_task()
                    if not move_to:
                        _t = random.randint(0, 1)
                        if _t == 0:
                            move_to = 'left'
                            turn_queue.put_queue('left')
                        else:
                            move_to = 'right'
                            turn_queue.put_queue('right')
                    self.move_bat(move_to, k_time, zhiye_id, saodi_mode)
                    res2, map_x2, map_y2 = self._get_move_xy()
                    if map_data[-1][-1] > 900:  # 随机下跳概率
                        r = random.randint(0, 1)
                    else:
                        r = random.randint(0, 3)
                    if r == 0 and map_y2 == 135:
                        self.jump_down_touch()
                    if map_y2 < 135:
                        """右边触底"""
                        if zhiye_id == '1':
                            self.move_bat(move_to, k_time, zhiye_id, saodi_mode)
                        if zhiye_id == '0':
                            self.move_bat(move_to, k_time, zhiye_id, saodi_mode)
                        turn_queue.task_over('right')
                        turn_queue.put_queue('left')
                    if map_x2 == map_x3 and map_x2 not in range(1050, 1070):
                        """防止挂绳子上不动"""
                        self.double_jump(move_to)
                        self.move_turn('up', k_time / 10)
                        res5, map_x5, map_y5 = self._get_move_xy()
                        if res5 == 1060:
                            self.double_jump(move_to)
                        if map_y2 == map_y5:
                            self.double_jump('left')
                            res6, map_x6, map_y6 = self._get_move_xy()
                            if map_x6 == map_x5:
                                self.double_jump('right')
            i += 1

    def double_jump(self, turn):
        self.double_jump_touch(turn)
        res, x, y = self._get_move_xy()
        self.time_sleep(0.2)
        res1, x1, y1 = self._get_move_xy()
        if y == y1 or x == x1:
            self.move_turn('up', 1.54)

    def use_auto(self, auto_time, **kwargs):
        s_time = time.time()
        AUTO_TIME = auto_time
        _EXIT_GAME = True if kwargs['挂机设置']['离线使用挂机卡'] == '1' else False
        _EXIT_TIME = kwargs['挂机设置']['离线时长']
        _NO_TIMECARD = False
        _AUTO_START = False
        _AUTO_OVER = False
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.get_rgb(RgbEnumG.BAT_AUTO_M):
                if not self.get_rgb(RgbEnumG.AUTO_TIME):
                    now_time = self.get_num((385, 352, 441, 388))  # 剩余时间
                    if int(now_time) > 1:
                        if self.get_rgb(RgbEnumG.BAT_AUTO_QR, True):
                            _AUTO_START = True
                    else:
                        if _NO_TIMECARD:
                            self.air_loop_find(ImgEnumG.UI_CLOSE)
                        else:
                            if self.get_rgb(RgbEnumG.AUTO_FREE, True):
                                pass
                            elif self.get_rgb(RgbEnumG.AUTO_10, True):
                                pass
                            elif self.get_rgb(RgbEnumG.AUTO_30, True):
                                pass
                            elif self.get_rgb(RgbEnumG.AUTO_60, True):
                                pass
                            else:
                                _NO_TIMECARD = True
                else:
                    if self.get_rgb(RgbEnumG.BAT_AUTO_QR, True):
                        _AUTO_START = True
            elif self.get_rgb(RgbEnumG.BAT_JG, True):
                _AUTO_OVER = True
            elif self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _AUTO_OVER or _NO_TIMECARD:
                    self.get_rgb(RgbEnumG.BAT_JG, True)
                    return True
                if not self.crop_image_find(ImgEnumG.AUTO_BAT, True):
                    if _AUTO_START:
                        if _EXIT_GAME:
                            self.stop_game(self.serialno)
                            self.time_sleep(_EXIT_TIME * 60)
                        else:
                            self.time_sleep(AUTO_TIME)
                            self.air_touch((422, 655))
                        # _AUTO_OVER = True
                    else:
                        self.air_touch((422, 655))
            else:
                self.check_close()

    def get_time_to_dotask(self, **kwargs):
        _t = kwargs['定时设置']['距离任务开始时间']
        _t_time = kwargs['定时设置']['启动时间']
        if time.time() - _t_time > _t:
            random_tasktime = kwargs['挂机设置']['任务延时']
            boss_map = kwargs['王图设置']['混王图']
            hd_boss = kwargs['王图设置']['混沌炎魔']
            meiri_time = kwargs['每日任务']['每日时间']
            select_queue = kwargs['状态队列']['选择器']
            _id = kwargs['定时设置']['定时任务ID']
            if _id == 0:
                select_queue.put_queue('AutoMR')
                kwargs['定时设置']['定时任务ID'] = 1
                return 0
            elif _id in [2, 3] and boss_map == '1':
                if hd_boss == '1':
                    select_queue.put_queue('AutoHDboss')
                select_queue.put_queue('AutoBoss')
                kwargs['定时设置']['定时任务ID'] = 1
                return 0
            else:
                pass
            now_time = int(time.time())
            date = meiri_time  # 设定时间 0
            date2 = f" 23:59:59"  # 跨天判断 1
            date3 = f" 12:00:00"  # 固定时间点 2
            date4 = f" 20:00:00"  # 固定时间点 3
            time_now = time.strftime("%Y-%m-%d", time.localtime())
            time_now1 = time_now + date
            time_now2 = time_now + date2
            if boss_map == '1':
                time_now3 = time_now + date3
                time_now4 = time_now + date4
            else:
                time_now3 = time_now + date2
                time_now4 = time_now + date2
            trigger_time = int(time.mktime(time.strptime(time_now1, "%Y-%m-%d %H:%M:%S")))
            trigger_time2 = int(time.mktime(time.strptime(time_now2, "%Y-%m-%d %H:%M:%S")))
            trigger_time3 = int(time.mktime(time.strptime(time_now3, "%Y-%m-%d %H:%M:%S")))
            trigger_time4 = int(time.mktime(time.strptime(time_now4, "%Y-%m-%d %H:%M:%S")))
            seconds = (trigger_time - now_time) + random_tasktime
            seconds2 = (trigger_time2 - now_time) + random_tasktime
            seconds3 = (trigger_time3 - now_time) + random_tasktime
            seconds4 = (trigger_time4 - now_time) + random_tasktime
            if -1500 < seconds3 < 0:
                seconds3 = 0
            if -1500 < seconds4 < 0:
                seconds4 = 0
            li = [seconds, seconds2, seconds3, seconds4]
            _t = 99999
            for _ in li:
                if _t > int(_) > 0:
                    _t = _
            kwargs['定时设置']['定时任务ID'] = li.index(_t)  # 存储下一次的任务
            kwargs['定时设置']['距离任务开始时间'] = _t  # 计算出的等待时间
            kwargs['定时设置']['启动时间'] = time.time()  # 更新计算时间
            if kwargs['定时设置']['定时任务ID'] == 0:
                self.sn.log_tab.emit(self.mnq_name, f"距离每日任务开始还有{_t}秒")
            elif kwargs['定时设置']['定时任务ID'] in [2, 3]:
                self.sn.log_tab.emit(self.mnq_name, f"距离混boss图开始还有{_t}秒")
