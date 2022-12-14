# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import FuHuoRoleErr, NetErr


class AutoBatG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(AutoBatG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
        self.move_spend = 0

    def _get_move_xy(self):
        res = self.crop_image_find(ImgEnumG.PERSON_POS, clicked=False, get_pos=True)
        if not res[0]:
            self.crop_image_find(ImgEnumG.S_MAP, touch_wait=1)
        return res

    @staticmethod
    def find_map_move(map_data, map_x, map_y, wait_queue, louti_queue):
        if map_y == map_data[0][-1] and not louti_queue.check_queue('1') and map_y != 135:
            louti_queue.queue.queue.clear()
            louti_queue.put_queue('1')
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

    def find_jump_louti(self, louti_x, saodi_mode, j_mode):
        """????????????????????????"""
        res, x, y = self._get_move_xy()
        for i in range(5):
            if i == 5:
                # print(f"reset_spend{i}")
                self.move_spend = 0
            res1, x1, y1 = self._get_move_xy()
            if x1 == 0:
                self.move_turn('left', 1.2, jump_mode=j_mode)
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
                        self.double_jump('left', jump_mode=j_mode)
                    return True, x1
                if x1 - louti_x < 0:
                    if i > 2:
                        self.double_jump('right', jump_mode=j_mode)
                    # print(self.move_spend)
                    if self.move_spend == 0:
                        t = abs(x1 - louti_x) / 28
                        self.move_turn('right', t, jump_mode=j_mode)
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
                        self.move_turn('right', t, jump_mode=j_mode)
                    if t > 0.7:
                        if saodi_mode == '0':
                            self.move_turn('attack', 0.23)
                else:
                    # print(self.move_spend)
                    if i > 2:
                        self.double_jump('left', jump_mode=j_mode)
                    if self.move_spend == 0:
                        t = abs(x1 - louti_x) / 28
                        self.move_turn('left', t, jump_mode=j_mode)
                        res_2, x_2, y_2 = self._get_move_xy()
                        if res_2 == 1:
                            spend = abs(x1 - x_2) / t
                            if 10 < spend < 45:
                                # print(f"spend:{spend}")
                                self.move_spend = spend
                    else:
                        t = abs(x1 - louti_x) / self.move_spend
                        self.move_turn('left', t, jump_mode=j_mode)
                    if t > 0.5:
                        if saodi_mode == '0':
                            self.move_turn('attack', 0.23)
                    # if i > 8:
                    #     _r = random.randint(0, 1)
                    #     if _r == 0:
                    #         self.double_jump('right',jump_mode=j_mode)
                    #     else:
                    #         self.double_jump('left',jump_mode=jump_mode)
                # res2, x2, y2 = self._get_move_xy()

        res1, x1, y1 = self._get_move_xy()
        return True, x1

    def move_up_louti(self, louti_x, louti_y, wait_queue, saodi_mode, j_mode):
        """??????????????????????????????"""
        for i in range(3):
            res, now_x = self.find_jump_louti(louti_x, saodi_mode, j_mode)
            if not res:
                return False
            if now_x - louti_x > 1:
                if self.move_spend == 0:
                    self.move_turn('left', abs(now_x - louti_x) / 30, jump_mode=j_mode)
                else:
                    self.move_turn('left', abs(now_x - louti_x) / self.move_spend, jump_mode=j_mode)
            elif now_x - louti_x < 0:
                if self.move_spend == 0:
                    self.move_turn('right', abs(now_x - louti_x) / 30, jump_mode=j_mode)
                else:
                    self.move_turn('right', abs(now_x - louti_x) / self.move_spend, jump_mode=j_mode)
            res2, x2, y2 = self._get_move_xy()
            if y2 != louti_y or y2 == 135:
                if not wait_queue.queue.empty():
                    r = random.randint(10, 30)
                    self.sn.log_tab.emit(self.mnq_name, f"?????????????????????{r}???")
                    self.time_sleep(r)
                    self.sn.log_tab.emit(self.mnq_name, f"????????????")
                    wait_queue.task_over(True)
                else:
                    self.move_turn('up', 1.42)
                    if louti_x in [1212, 1022, 1067, 1198]:  # ?????????????????????
                        self.move_turn('up', 0.67)
                    if louti_x in [1022, 949]:
                        self.move_turn('up', 0.67)
                    if louti_x in [1036]:
                        self.move_turn('jump', 0.38)
                    # self.keypress_and_up(self.dm, "up", 2.12)
                return True
            # if i == 1:
            #     self.move_turn('up', 1.84)
            # self.keypress_and_up(self.dm, "up", 1.84)
        return False

    def keep_bat(self, turn, auto_time, saodi_mode, j_mode):
        """???????????????????????????"""
        r = random.randint(1, 20)
        if saodi_mode == '1':
            self.move_turn(turn, auto_time * 1.5, jump_mode=j_mode)
        else:
            if r > 1:
                self.mul_point_touch(turn, 'attack', auto_time * 1.5, True)
            else:
                self.mul_point_touch(turn, 'c', auto_time * 1.5, True)

    def keep_bat_2(self, turn, auto_time, saodi_mode, j_mode):
        r = random.randint(0, 1)
        self.move_turn(turn, auto_time * 2, jump_mode=j_mode)
        if saodi_mode == '0':
            if r == 0:
                self.mul_point_touch(turn, 'attack', auto_time * 1.5)
            else:
                self.mul_point_touch(turn, 'c', auto_time * 1.5)

    def move_bat(self, move_to, key_time, zhiye_id, saodi_mode, j_mode):
        if move_to == 'left':
            i = random.randint(1, 2)
        else:
            i = random.randint(3, 4)
        if i == 1:
            if zhiye_id == '1':
                self.double_jump('left', jump_mode=j_mode)
                self.keep_bat_2('left', key_time, saodi_mode, j_mode)
                if saodi_mode == '0':
                    self.move_turn('f', 0.14)
                    self.move_turn('v', 0.32)
            else:
                self.double_jump('left', jump_mode=j_mode)
                self.keep_bat('left', key_time, saodi_mode, j_mode)
        elif i == 2:
            if zhiye_id == '1':
                self.keep_bat_2('left', key_time, saodi_mode, j_mode)
            else:
                self.keep_bat('left', key_time, saodi_mode, j_mode)
        elif i == 3:
            if zhiye_id == '1':
                if saodi_mode == '0':
                    self.move_turn('c', 0.19)
                    self.move_turn('d', 0.34)
                self.keep_bat_2('right', key_time, saodi_mode, j_mode)
            else:
                self.keep_bat('right', key_time, saodi_mode, j_mode)
        elif i == 4:
            if zhiye_id == '1':
                self.double_jump('right', jump_mode=j_mode)
                self.keep_bat_2('right', key_time, saodi_mode, j_mode)
            else:
                self.double_jump('right', jump_mode=j_mode)
                self.keep_bat('right', key_time, saodi_mode, j_mode)

    def keyboard_bat(self, **kwargs):
        auto_choose = kwargs['????????????']
        if auto_choose:
            kwargs = self.get_mapdata(**kwargs)
        task_id = kwargs['??????id']
        map_data = list(kwargs['????????????']['????????????'])
        select_queue = kwargs['????????????']['?????????']
        zhiye_id = kwargs['????????????']['????????????']
        wait_queue = kwargs['????????????']['????????????']
        saodi_mode = kwargs['????????????']['????????????']
        louti_queue = kwargs['????????????']['????????????']
        turn_queue = kwargs['????????????']['????????????']
        use_mp = kwargs['????????????']['????????????']
        use_autobat = kwargs['????????????']['??????????????????']
        use_time = int(kwargs['????????????']['???????????????'])
        bat_sleep = kwargs['????????????']['????????????']
        bat_sleep_mode = kwargs['????????????']['????????????']
        j_mode = kwargs['????????????']['????????????']
        _IS_EXIT = False if kwargs['????????????']['????????????'] == '0' else True
        min_x = map_data[-1][-1]
        dingshi = True if kwargs['????????????']['????????????'] == '1' else False
        _r = random.randint(30, 60)
        _use = time.time()
        _s_time = time.time()
        _c_time = time.time()
        i = 0
        self.check_level_star()
        _res_hp_mp = self.check_hp_mp()
        if _res_hp_mp != '':
            if 'HP' in _res_hp_mp:
                return -1
            if use_mp:
                if 'MP' in _res_hp_mp:
                    return -1
        if self.crop_image_find(ImgEnumG.BAG_MAX_IMG, False):
            return -1
        self.find_info('bat_xc', True)
        while True:
            if dingshi:
                if self.get_time_to_dotask(**kwargs) == 0:
                    return 0
            if bat_sleep:
                if time.time() - _s_time > _r * 100:
                    _s_time = time.time()
                    _t = random.randint(20, 30)
                    if bat_sleep_mode == '1':
                        self.sn.log_tab.emit(self.mnq_name, f"????????????{_t}???")
                        self.time_sleep(_t)
                    else:
                        self.stop_game()
                        self.sn.log_tab.emit(self.mnq_name, f"????????????{_t * 30}???")
                        self.time_sleep(_t * 30)
            if use_autobat:
                if time.time() - _use > use_time * 10:
                    _use = time.time()
                    self.use_auto(use_time, **kwargs)
            if self.get_rgb(RgbEnumG.FUHUO_BTN):
                raise FuHuoRoleErr
            if self.get_rgb(RgbEnumG.BAT_JG, True):
                pass
            if time.time() - _c_time > GlobalEnumG.CheckRoleTime:
                select_queue.put_queue("CheckRole")
                return 0
            if self.find_info('team_tip_exit'):
                if not self.use_auto(10, **kwargs):
                    return -1
            if i % 5 == 0:
                if not self.find_info('ingame_flag2'):
                    return -1
                else:
                    if i % 10 == 0:
                        _res_hp_mp = self.check_hp_mp()
                        if _res_hp_mp != '':
                            if 'HP' in _res_hp_mp:
                                return -1
                            if use_mp:
                                if 'MP' in _res_hp_mp:
                                    return -1
                    if self.get_rgb([736, 394, '617B96']):
                        self.air_touch((845, 390))
                    if not self.crop_image_find(ImgEnumG.AUTO_BAT, False, touch_wait=0):
                        self.air_touch((423, 655), touch_wait=2)  # ????????????????????????
                    if self.net_err():
                        self.sn.log_tab.emit(self.mnq_name, r"????????????_????????????")
                        raise NetErr
                    # else:
                    # self.crop_image_find(ImgEnumG.XC_IMG)
                    # self.find_info('bat_xc',True)
                    # if self.air_loop_find(ImgEnumG.RES_EXIT_TEAM, False, touch_wait=0):
                    #     if not self.use_auto(10, **kwargs):
                    #         return -1
                    if not self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                        return -1
                    if _IS_EXIT and task_id != '4':
                        pos = self.crop_image_find(ImgEnumG.EXIT_TEAM, False, get_pos=True)
                        if pos[-1] < 270:
                            self.air_touch((pos[1], pos[-1]), touch_wait=1)  # ????????????3????????????
                            if self.get_rgb(RgbEnumG.EXIT_TEAM, True):
                                self.sn.log_tab.emit(self.mnq_name, r"????????????3???,????????????")
                            return -1
            if min_x > 871:
                k_time = round(random.randint(5, 10) / 10, 2)
            else:
                k_time = round(random.randint(10, 20) / 10, 2)
            res, map_x, map_y = self._get_move_xy()
            if not res:
                self.crop_image_find(ImgEnumG.S_MAP, touch_wait=1)
            else:
                if not j_mode:
                    turn, turn_y = self.find_map_move(map_data, map_x, map_y, wait_queue, louti_queue)
                    if turn != 0:
                        if not self.move_up_louti(turn, turn_y, wait_queue, saodi_mode, False):
                            res4, map_x4, map_y4 = self._get_move_xy()
                            if map_x4 == map_x:
                                _i = random.randint(0, 1)
                                if _i == 0:
                                    self.move_turn('left', 0.32, jump_mode=j_mode)
                                else:
                                    self.move_turn('right', 0.32, jump_mode=j_mode)
                            res6, map_x6, map_y6 = self._get_move_xy()
                            if map_x4 == map_x6:
                                self.move_turn('up', 1.12)

                res3, map_x3, map_y3 = self._get_move_xy()
                if map_data[-1][0] > map_x3 > map_data[-1][1]:
                    turn_queue.task_over('right')
                    turn_queue.put_queue('left')
                elif map_data[-1][2] > map_x3 > map_data[-1][-1]:
                    turn_queue.task_over('left')
                    turn_queue.put_queue('right')
                # else:
                #     _ro = random.randint(0, 10)
                #     if _ro > 5:
                #         _o = random.randint(0, 1)
                #         if _o == 0:
                #             turn_queue.task_over('left')
                #             turn_queue.put_queue('right')
                #         else:
                #             turn_queue.task_over('right')
                #             turn_queue.put_queue('left')
                move_to = turn_queue.get_task()
                if not move_to:
                    _t = random.randint(0, 1)
                    if _t == 0:
                        move_to = 'left'
                        turn_queue.put_queue('left')
                    else:
                        move_to = 'right'
                        turn_queue.put_queue('right')
                self.move_bat(move_to, k_time, zhiye_id, saodi_mode, j_mode)
                res2, map_x2, map_y2 = self._get_move_xy()
                if map_data[-1][-1] > 900:  # ??????????????????
                    r = random.randint(0, 1)
                else:
                    r = random.randint(0, 3)
                if r == 0 and map_y2 == 135:
                    self.jump_down_touch()
                if map_y2 < 135:
                    """????????????"""
                    if zhiye_id == '1':
                        self.move_bat(move_to, k_time, zhiye_id, saodi_mode, j_mode)
                    if zhiye_id == '0':
                        self.move_bat(move_to, k_time, zhiye_id, saodi_mode, j_mode)
                    turn_queue.task_over('right')
                    turn_queue.put_queue('left')
                if map_data[-1][0] > map_x2 > map_data[-1][1]:
                    self.double_jump('left', jump_mode=j_mode)
                elif map_data[-1][2] > map_x2 > map_data[-1][-1]:
                    self.double_jump('right', jump_mode=j_mode)
                if map_x2 == map_x3 and map_x2 not in range(1050, 1070):
                    """????????????????????????"""
                    self.double_jump(move_to, jump_mode=j_mode)
                    if j_mode:
                        self.move_turn(move_to, k_time / 10)
                    else:
                        self.move_turn('up', k_time / 10)
                    res5, map_x5, map_y5 = self._get_move_xy()
                    if res5 == 1060:
                        self.double_jump(move_to, jump_mode=j_mode)
                    if map_y2 == map_y5:
                        self.double_jump('left', jump_mode=j_mode)
                        res6, map_x6, map_y6 = self._get_move_xy()
                        if map_x6 == map_x5:
                            self.double_jump('right', jump_mode=j_mode)
            i += 1

    def double_jump(self, turn, jump_mode=True):
        if jump_mode:
            self.double_jump_touch(turn)
            res, x, y = self._get_move_xy()
            self.time_sleep(0.2)
            res1, x1, y1 = self._get_move_xy()
            if y == y1 or x == x1:
                self.move_turn('up', 1.54)
        else:
            self.key_double_jump(turn)

    def use_auto(self, auto_time, **kwargs):
        s_time = time.time()
        AUTO_TIME = auto_time
        _EXIT_GAME = True if kwargs['????????????']['?????????????????????'] == '1' else False
        _EXIT_TIME = kwargs['????????????']['????????????']
        _NO_TIMECARD = False
        _AUTO_START = False
        _AUTO_OVER = False
        _USE_CARD=False
        while time.time() - s_time < GlobalEnumG.TaskCheckTime:
            if self.get_rgb(RgbEnumG.BAT_AUTO_M):
                if not _AUTO_START:
                    now_time = self.check_time_num()  # ????????????
                    if int(now_time) > 1:
                        if self.get_rgb(RgbEnumG.BAT_AUTO_QR, True):
                            _AUTO_START = True
                else:
                    if _AUTO_START:
                        if _USE_CARD:
                            self.back()
                            # self.air_loop_find(ImgEnumG.UI_CLOSE)
                        else:
                            if self.get_rgb(RgbEnumG.AUTO_FREE, True):
                                _USE_CARD=True
                            elif self.get_rgb(RgbEnumG.AUTO_10, True):
                                _USE_CARD=True
                            elif self.get_rgb(RgbEnumG.AUTO_30, True):
                                _USE_CARD=True
                            elif self.get_rgb(RgbEnumG.AUTO_60, True):
                                _USE_CARD=True
                            else:
                                _NO_TIMECARD = True
                                _USE_CARD = True
            elif self.get_rgb(RgbEnumG.BAT_JG, True):
                _AUTO_OVER = True
            elif self.find_info('ingame_flag2'):
                if _AUTO_OVER or _NO_TIMECARD:
                    self.get_rgb(RgbEnumG.BAT_JG, True)
                    return True
                if not self.crop_image_find(ImgEnumG.AUTO_BAT, True) or not self.find_info('bat_auto'):
                    if _AUTO_START:
                        if _EXIT_GAME:
                            self.stop_game()
                            self.time_sleep(_EXIT_TIME * 60)
                        else:
                            self.time_sleep(AUTO_TIME)
                            self.air_touch((422, 655),touch_wait=GlobalEnumG.TouchWaitTime)
                        # _AUTO_OVER = True
                    else:
                        self.air_touch((422, 655),touch_wait=GlobalEnumG.TouchWaitTime)
            else:
                self.check_err()

    def get_time_to_dotask(self, **kwargs):
        _t = kwargs['????????????']['????????????????????????']
        _t_time = kwargs['????????????']['????????????']
        if time.time() - _t_time > _t:
            random_tasktime = kwargs['????????????']['????????????']
            boss_map = kwargs['????????????']['?????????']
            hd_boss = kwargs['????????????']['????????????']
            meiri_time = kwargs['????????????']['????????????']
            select_queue = kwargs['????????????']['?????????']
            _id = kwargs['????????????']['????????????ID']
            if _id == 0:
                select_queue.put_queue('AutoMR')
                kwargs['????????????']['????????????ID'] = 1
                return 0
            elif _id in [2, 3] and boss_map == '1':
                if hd_boss == '1':
                    select_queue.put_queue('AutoHDboss')
                select_queue.put_queue('AutoBoss')
                kwargs['????????????']['????????????ID'] = 1
                return 0
            else:
                pass
            now_time = int(time.time())
            date = meiri_time  # ???????????? 0
            date2 = f" 23:59:59"  # ???????????? 1
            date3 = f" 12:00:00"  # ??????????????? 2
            date4 = f" 20:00:00"  # ??????????????? 3
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
            kwargs['????????????']['????????????ID'] = li.index(_t)  # ????????????????????????
            kwargs['????????????']['????????????????????????'] = _t  # ????????????????????????
            kwargs['????????????']['????????????'] = time.time()  # ??????????????????
            if kwargs['????????????']['????????????ID'] == 0:
                self.sn.log_tab.emit(self.mnq_name, f"??????????????????????????????{_t}???")
            elif kwargs['????????????']['????????????ID'] in [2, 3]:
                self.sn.log_tab.emit(self.mnq_name, f"?????????boss???????????????{_t}???")
