# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG, ColorEnumG
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
        return self.crop_image_find(ImgEnumG.PERSON_POS, clicked=False, get_pos=True)

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
                                louti_queue.task_over('1')
                                louti_queue.put_queue('2')
                                return i, map_data[0][-1]
            return 0, 0
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

    def find_jump_louti(self, louti_x, saodi_mode):
        """到达楼梯点后跳跃"""
        res, x, y = self._get_move_xy()
        for i in range(10):
            if i == 4:
                # print(f"reset_spend{i}")
                self.move_spend = 0
            res1, x1, y1 = self._get_move_xy()
            if res1 == 0:
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
                        self.move_turn('up', 0.31)
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
                    if louti_x in [1022, 1067]:  # 绳子长的补一下
                        self.move_turn('up', 0.42)
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
        if turn == 'left':
            self.move_turn('left', auto_time * 2)
            if saodi_mode == '0':
                if r == 0:
                    self.mul_point_touch(turn, 'attack', auto_time * 1.5)
                else:
                    self.mul_point_touch(turn, 'c', auto_time * 1.5)

        else:
            self.move_turn('right', auto_time * 2)
            if saodi_mode == '0':
                if r == 0:
                    self.mul_point_touch(turn, 'attack', auto_time * 1.5)
                else:
                    self.mul_point_touch(turn, 'c', auto_time * 1.5)

    def move_bat(self, i, key_time, zhiye_id, saodi_mode):
        if i == 1:
            if zhiye_id == '1':
                self.keep_bat_2('left', key_time, saodi_mode)
                self.double_jump('left')
                if saodi_mode == '0':
                    self.move_turn('f', 0.14)
                    self.move_turn('v', 0.32)
            else:
                self.keep_bat('left', key_time, saodi_mode)
                self.double_jump('left')
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
                self.double_jump('right')
            else:
                self.keep_bat('right', key_time, saodi_mode)
        elif i == 4:
            if zhiye_id == '1':
                self.keep_bat_2('right', key_time, saodi_mode)
                self.double_jump('right')

            else:
                self.keep_bat('right', key_time, saodi_mode)

    def keyboard_bat(self, **kwargs):
        map_data = kwargs['战斗数据']['地图数据']
        zhiye_id = kwargs['战斗数据']['职业类型']
        wait_queue = kwargs['战斗数据']['休息队列']
        saodi_mode = kwargs['战斗数据']['刷图模式']
        louti_queue = kwargs['战斗数据']['楼梯队列']
        turn_queue = kwargs['战斗数据']['方向队列']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        i = 0
        if self.ocr_find(ImgEnumG.HP_NULL_OCR, touch_wait=0):
            return -1
        elif self.ocr_find(ImgEnumG.MP_NULL_OCR, touch_wait=0) and use_mp:
            return -1
        elif self.ocr_find(ImgEnumG.BAG_FULL, touch_wait=0):
            return -1
        while True:
            if self.get_rgb(311,519,'4C87B0'):
                self.check_err()
            if self.get_rgb(587, 528, 'EE7046',True):pass
            if i % 5 == 0:
                self.mulcolor_check(ColorEnumG.BAT_RES, True, touch_wait=0)
                if not self.crop_image_find(ImgEnumG.INGAME_FLAG2, False, touch_wait=0):
                    return -1
                else:
                    self.get_rgb(836, 391, '607B96', True)
                    if not self.crop_image_find(ImgEnumG.AUTO_BAT, False, touch_wait=0):
                        self.air_touch((423, 655), touch_wait=2)  # 点击确认战斗结果
                    else:
                        self.crop_image_find(ImgEnumG.XC_IMG)
                    if self.air_loop_find(ImgEnumG.RES_EXIT_TEAM, False, touch_wait=0):
                        if not self.use_auto(10):
                            return -1
                    elif not self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                        return -1

            if map_data[-1][-1] > 870:
                k_time = round(random.randint(5, 10) / 10, 2)
            else:
                k_time = round(random.randint(10, 20) / 10, 2)
            res, map_x, map_y = self._get_move_xy()
            t_l = random.randint(1, 2)
            t_r = random.randint(3, 4)

            if not res:
                self.crop_image_find(ImgEnumG.S_MAP, touch_wait=1)
            else:
                turn, turn_y = self.find_map_move(map_data, map_x, map_y,
                                                  wait_queue, louti_queue)
                # print(turn, turn_y)
                if turn != 0:
                    if not self.move_up_louti(turn, turn_y, louti_queue, turn_queue, wait_queue, saodi_mode):
                        res4, map_x4, map_y4 = self._get_move_xy()
                        if map_x4 == map_x:
                            r = random.randint(0, 1)
                            if r == 0:
                                self.move_turn('left', 0.32)
                            else:
                                self.move_turn('right', 0.32)
                        res6, map_x6, map_y6 = self._get_move_xy()
                        if map_x4 == map_x6:
                            self.move_turn('up', 2.12)
                else:
                    res3, map_x3, map_y3 = self._get_move_xy()
                    if map_data[-1][0] > map_x3 > map_data[-1][1]:
                        turn_queue.task_over('right')
                        turn_queue.put_queue('left')
                    elif map_data[-1][2] > map_x3 > map_data[-1][-1]:
                        turn_queue.task_over('left')
                        turn_queue.put_queue('right')
                    else:
                        r = random.randint(0, 1)
                        if r == 0:
                            turn_queue.task_over('left')
                            turn_queue.put_queue('right')
                        else:
                            turn_queue.task_over('right')
                            turn_queue.put_queue('left')
                    move_to = turn_queue.get_task()
                    if move_to == 'left':
                        if zhiye_id == '1':
                            self.move_bat(t_l, k_time, zhiye_id, saodi_mode)
                        if zhiye_id == '0':
                            self.move_bat(t_l, k_time, zhiye_id, saodi_mode)
                    else:
                        if zhiye_id == '1':
                            self.move_bat(t_r, k_time, zhiye_id, saodi_mode)
                        if zhiye_id == '0':
                            self.move_bat(t_r, k_time, zhiye_id, saodi_mode)
                    res2, map_x2, map_y2 = self._get_move_xy()
                    if map_data[-1][-1] > 900:  # 随机下跳概率
                        r = random.randint(0, 1)
                    else:
                        r = random.randint(0, 3)
                    if r == 0 and map_y2 == 135:
                        self.mul_point_touch('down', 'jump', k_time=1.5, long_click=True)
                    if map_y2 < 132 or map_x2 == map_x3:
                        """右边触底"""
                        if zhiye_id == '1':
                            self.move_bat(t_l, k_time, zhiye_id, saodi_mode)
                        if zhiye_id == '0':
                            self.move_bat(t_l, k_time, zhiye_id, saodi_mode)
                        turn_queue.task_over('right')
                        turn_queue.put_queue('left')
                    if map_x2 == map_x3 and map_x2 not in range(1050, 1070):
                        """防止挂绳子上不动"""
                        self.move_turn('up', k_time / 10)
                        res5, map_x5, map_y5 = self._get_move_xy()
                        if res5 == 1060:
                            self.double_jump('left')
                        if map_y2 == map_y5:
                            self.move_turn('left', k_time / 10)
                            res6, map_x6, map_y6 = self._get_move_xy()
                            if map_x6 == map_x5:
                                self.move_turn('up', k_time / 5)
                                self.move_turn('left', k_time / 5)
            i += 1

    def double_jump(self, turn):
        self.mul_point_touch(turn, 'jump')
        # res, x, y = self._get_move_xy()
        # self.move_turn('left', 0.23)
        # self.mul_point_touch('left','up',long_click=True)
        # res1, x1, y1 = self._get_move_xy()
        # if y != y1:
        #     self.move_turn('up', 0.34)

    def use_auto(self, auto_time):
        s_time = time.time()
        AUTO_TIME = auto_time
        _NO_TIMECARD = False
        _AUTO_START = False
        _AUTO_OVER = False
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.mulcolor_check(ColorEnumG.BAT_MAIN):
                now_time = self.get_num((385, 352, 441, 388))  # 剩余时间
                if int(now_time) > 1:
                    if self.get_rgb(733, 563, 'EE7046', True):
                        _AUTO_START = True
                else:
                    if _NO_TIMECARD:
                        self.air_loop_find(ImgEnumG.UI_CLOSE)
                    else:
                        if self.get_rgb(897, 391, '617A95', True):
                            pass
                        elif self.get_rgb(709, 344, 'FFD741', True):
                            pass
                        elif self.get_rgb(840, 336, 'FFD741', True):
                            pass
                        elif self.get_rgb(908, 338, 'FFD741', True):
                            pass
                        else:
                            _NO_TIMECARD = True
            elif self.mulcolor_check(ColorEnumG.BAT_RES, True):
                self.air_loop_find(ImgEnumG.UI_QR)
                _AUTO_OVER = True
            elif self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _AUTO_OVER or _NO_TIMECARD:
                    if self.mulcolor_check(ColorEnumG.BAT_RES, True):
                        self.air_loop_find(ImgEnumG.UI_QR)
                    return True
                if not self.crop_image_find(ImgEnumG.AUTO_BAT, True):
                    if _AUTO_START:
                        self.time_sleep(AUTO_TIME)
                        self.air_touch((422, 655))
                        # _AUTO_OVER = True
                    else:
                        self.air_touch((422, 655))
            else:
                if not self.check_close():
                    return False
