# -*- coding: utf-8 -*-
import random

from Enum.ResEnum import ImgEnumG
from UiPage.BasePage import BasePageG


class AutoBatG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(AutoBatG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.move_spend = 0

    def _get_move_xy(self):
        return self.crop_image_find(ImgEnumG.PERSON_POS, clicked=False, get_pos=True)

    def find_map_move(self, map_data, map_x, map_y, auto_wait, louti_queue):
        # if map_y == map_louti[-1] and not louti_queue.check_queue('1') and map_y != 135:
        #     louti_queue.queue.queue.clear()
        #     louti_queue.put_queue('1')
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
                        if not auto_wait.queue.empty():
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
                    if not auto_wait.queue.empty():
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
                    if not auto_wait.queue.empty():
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
        for i in range(5):
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
                    if louti_x in [1172, 972]:
                        self.move_turn('jump', 0.32)
                        self.time_sleep(0.5)
                        self.move_turn('jump', 0.18)
                        self.time_sleep(0.5)
                    if louti_x in [1128, 1144]:
                        self.move_turn('jump', 0.18)
                        self.time_sleep(0.5)
                    self.move_turn('jump', 0.32)
                    return True, x1
                if x1 - louti_x < 0:
                    print(self.move_spend)
                    if self.move_spend == 0:
                        t = abs(x1 - louti_x) / 28
                        self.move_turn('right',t)
                        res_1, x_1, y_1 = self._get_move_xy()
                        if res_1 == 1:
                            if res_1 == 1:
                                spend = abs(x1 - x_1) / t
                                if 10 < spend < 45:
                                    print(f"spend:{spend}")
                                    self.move_spend = spend
                    else:
                        t = abs(x1 - louti_x) / self.move_spend
                        if t > 5:
                            t = abs(x1 - louti_x) / 28
                        self.move_turn('right',t)
                    if t > 0.7:
                        if saodi_mode == 0:
                            self.move_turn('z', 0.23)
                else:
                    print(self.move_spend)
                    if self.move_spend == 0:
                        t = abs(x1 - louti_x) / 28
                        self.move_turn('left',t)
                        res_2, x_2, y_2 = self._get_move_xy()
                        if res_2 == 1:
                            spend = abs(x1 - x_2) / t
                            if 10 < spend < 45:
                                print(f"spend:{spend}")
                                self.move_spend = spend
                    else:
                        t = abs(x1 - louti_x) / self.move_spend
                        self.move_turn('left',t)
                    if t > 0.7:
                        if saodi_mode == 0:
                            self.move_turn('z', 0.23)
                    if i > 8:
                        self.move_turn('left',0.31)
        res1, x1, y1 = self._get_move_xy()
        return True, x1

    def move_up_louti(self, louti_x, louti_y, louti_queue, turn_queue, auto_wait, saodi_mode):
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
                if not auto_wait.queue.empty():
                    r = random.randint(10, 30)
                    self.sn.log_tab.emit(self.mnq_name, f"爬绳子在线休息{r}秒")
                    self.time_sleep(r)
                    self.sn.log_tab.emit(self.mnq_name, f"休息结束")
                    auto_wait.task_over(True)
                else:
                    self.move_turn('up', 1.42)
                    # self.keypress_and_up(self.dm, "up", 2.12)
                return True
            # if i == 1:
            #     self.move_turn('up', 1.84)
                # self.keypress_and_up(self.dm, "up", 1.84)
        return False

    def keep_bat(self, turn, auto_time, saodi_mode):
        """长按技能职业，幻影"""
        r = random.randint(1, 20)
        if saodi_mode == 1:
            self.move_turn('left', auto_time * 1.5)
        else:
            if r > 1:
                self.mul_point_touch(turn, 'z', auto_time * 1.5, True)
            else:
                self.mul_point_touch(turn, 'c', auto_time * 1.5, True)

    def keep_bat_2(self, turn, auto_time, saodi_mode):
        r = random.randint(0, 1)
        if turn == 'left':
            self.move_turn('left', auto_time * 2)
            if saodi_mode == 0:
                if r == 0:
                    self.mul_point_touch(turn, 'z', auto_time * 1.5)
                else:
                    self.mul_point_touch(turn, 'c', auto_time * 1.5)

        else:
            self.move_turn('right', auto_time * 2)
            if saodi_mode == 0:
                if r == 0:
                    self.mul_point_touch(turn, 'z', auto_time * 1.5)
                else:
                    self.mul_point_touch(turn, 'c', auto_time * 1.5)

    def move_bat(self, i, key_time, zhiye_id, saodi_mode):
        if i == 1:
            if zhiye_id == 1:
                self.keep_bat_2('left', key_time, saodi_mode)
                self.double_jump('left')
                if saodi_mode == 0:
                    self.move_turn('f', 0.14)
                    self.move_turn('v', 0.32)
            else:
                self.keep_bat('left', key_time, saodi_mode)
                self.double_jump('left')
        elif i == 2:
            if zhiye_id == 1:
                self.keep_bat_2('left', key_time, saodi_mode)
            else:
                self.keep_bat('left', key_time, saodi_mode)
        elif i == 3:
            if zhiye_id == 1:
                if saodi_mode == 0:
                    self.move_turn('c', 0.19)
                    self.move_turn('d', 0.34)
                self.keep_bat_2('right', key_time, saodi_mode)
                self.double_jump('right')
            else:
                self.keep_bat('right', key_time, saodi_mode)
        elif i == 4:
            if zhiye_id == 1:
                self.keep_bat_2('right', key_time, saodi_mode)
                self.double_jump('right')

            else:
                self.keep_bat('right', key_time, saodi_mode)

    def keyboard_bat(self, map_data, zhiye_id, auto_wait, saodi_mode, louti_queue, turn_queue):
        self.crop_image_find(ImgEnumG.S_MAP)
        if not self.ocr_find(ImgEnumG.AUTO_BAT_OCR):
            self.air_touch((418, 655))  # 关闭自动战斗
            # 点击确认战斗结果
        for i in range(6):
            if i % 5 == 0:
                print('检查战斗异常')
            k_time = round(random.randint(10, 20) / 10, 2)
            print(f"{k_time}k_time")
            res, map_x, map_y = self._get_move_xy()
            print(f"k1_{map_x}_{map_y}")
            t_l = random.randint(1, 2)
            t_r = random.randint(3, 4)
            if not res:
                self.crop_image_find(ImgEnumG.S_MAP)
            else:
                turn, turn_y = self.find_map_move(map_data, map_x, map_y,
                                                  auto_wait, louti_queue)
                print(turn,turn_y)
                if turn != 0:
                    if not self.move_up_louti(turn, turn_y, louti_queue, turn_queue, auto_wait, saodi_mode):
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
                    # if self.map_id == '4' and self.task_id == 3:
                    #     if 1150 > map_x3 > 1140:
                    #         # if abs(map_x3 - 1153) > abs(map_x3 - 1245):
                    #         turn_queue.task_over('right')
                    #         turn_queue.put_queue('left')
                    #     if 1000 > map_x3 > 950:
                    #         # if abs(map_x3 - 966) > abs(map_x3 - 868):
                    #         turn_queue.task_over('left')
                    #         turn_queue.put_queue('right')
                    #         louti_queue.queue.queue.clear()
                    #         louti_queue.put_queue('1')
                    #     move_to = turn_queue.get_task()
                    #     if move_to == 'left':
                    #         if zhiye_id == 1:
                    #             self.turn_left_or_right(t_l, key_time, zhiye_id, saodi_mode)
                    #         if zhiye_id == 0:
                    #             self.turn_left_or_right(t_l, key_time, zhiye_id, saodi_mode)
                    #     else:
                    #         if zhiye_id == 1:
                    #             self.turn_left_or_right(t_r, key_time, zhiye_id, saodi_mode)
                    #         if zhiye_id == 0:
                    #             self.turn_left_or_right(t_r, key_time, zhiye_id, saodi_mode)
                    #     res2, map_x2, map_y2 = self.get_move_xy(self.dm)
                    #     r = random.randint(0, 3)
                    #     if r == 0 and map_y2 == 137:
                    #         self.jump_down()
                    # elif self.map_id == '11' and self.task_id == 3:
                    #     if 1155 > map_x3 > 1100:
                    #         # if abs(map_x3 - 1153) > abs(map_x3 - 1245):
                    #         turn_queue.task_over('right')
                    #         turn_queue.put_queue('left')
                    #     if 1000 > map_x3 > 950:
                    #         # if abs(map_x3 - 966) > abs(map_x3 - 868):
                    #         turn_queue.task_over('left')
                    #         turn_queue.put_queue('right')
                    #         louti_queue.queue.queue.clear()
                    #         louti_queue.put_queue('1')
                    #     move_to = turn_queue.get_task()
                    #     if move_to == 'left':
                    #         if zhiye_id == 1:
                    #             self.turn_left_or_right(t_l, key_time, zhiye_id, saodi_mode)
                    #         if zhiye_id == 0:
                    #             self.turn_left_or_right(t_l, key_time, zhiye_id, saodi_mode)
                    #     else:
                    #         if zhiye_id == 1:
                    #             self.turn_left_or_right(t_r, key_time, zhiye_id, saodi_mode)
                    #         if zhiye_id == 0:
                    #             self.turn_left_or_right(t_r, key_time, zhiye_id, saodi_mode)
                    #     res2, map_x2, map_y2 = self.get_move_xy(self.dm)
                    #     r = random.randint(0, 5)
                    #     if r == 0 and map_y2 in [137, 118, 129]:
                    #         self.jump_down()
                    # else:
                    if map_data[-1][0] > map_x3 > map_data[-1][1]:
                        turn_queue.task_over('right')
                        turn_queue.put_queue('left')
                    if map_data[-1][2] > map_x3 > map_data[-1][-1]:
                        turn_queue.task_over('left')
                        turn_queue.put_queue('right')
                    move_to = turn_queue.get_task()
                    if move_to == 'left':
                        if zhiye_id == 1:
                            self.move_bat(t_l, k_time , zhiye_id, saodi_mode)
                        if zhiye_id == 0:
                            self.move_bat(t_l, k_time, zhiye_id, saodi_mode)
                    else:
                        if zhiye_id == 1:
                            self.move_bat(t_r, k_time , zhiye_id, saodi_mode)
                        if zhiye_id == 0:
                            self.move_bat(t_r, k_time, zhiye_id, saodi_mode)
                    res2, map_x2, map_y2 = self._get_move_xy()
                    r = random.randint(0, 3)
                    if r == 0 and map_y2 == 135:
                        self.mul_point_touch('down', 'jump',long_click=True)
                    if res2 == 0:
                        """右边触底"""
                        if zhiye_id == 1:
                            self.move_bat(t_l, k_time , zhiye_id, saodi_mode)
                        if zhiye_id == 0:
                            self.move_bat(t_l, k_time, zhiye_id, saodi_mode)
                        turn_queue.task_over('right')
                        turn_queue.put_queue('left')
                    if map_x2 == map_x3 and map_x2 not in range(1050, 1070)  :
                        """防止挂绳子上不动"""
                        self.move_turn('up', k_time / 10)
                        res5, map_x5, map_y5 = self._get_move_xy()
                        if map_y2 == map_y5:
                            self.move_turn('left', k_time / 10)
                            res6, map_x6, map_y6 = self._get_move_xy()
                            if map_x6 == map_x5:
                                self.move_turn('up', k_time / 5)
                                self.move_turn('left', k_time / 5)
            return True

    def double_jump(self,turn):
        self.mul_point_touch(turn, 'jump')
        res,x,y=self._get_move_xy()
        self.move_turn('left', 0.23)
        res1,x1,y1=self._get_move_xy()
        if x==x1 and y!=y1:
            self.move_turn('up', 0.34)