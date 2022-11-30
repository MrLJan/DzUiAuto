# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, WorldEnumG, MulColorEnumG, ImgEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.OtherTools import OT, catch_ex


class ColorCvTools:
    def __init__(self):
        self.dev = None
        self.sn = None
        self.mnq_name = None

    def check_num(self, type_id=0):
        """
        检查数字,0=金币，1=红币,2=星力
        """
        if type_id == 0:
            # 金币
            self.dev.UseDict(3)
            num_res = self.dev.FindStrFastExS(692, 373, 914, 412, '0|1|2|3|4|5|6|7|8|9', '68717B-272522', 0.7)
        elif type_id == 1:
            # 红币
            self.dev.UseDict(3)
            num_res = self.dev.FindStrFastExS(399, 372, 620, 412, '0|1|2|3|4|5|6|7|8|9', '68717B-272522', 0.9)
        elif type_id == 2:
            # 星力
            self.dev.UseDict(5)
            num_res = self.dev.FindStrFastExS(251, 219, 314, 243, '0|1|2|3|4|5|6|7|8|9', 'BBBCBE-434240', 0.9)
        elif type_id == 3:
            # 战力
            self.dev.UseDict(6)
            num_res = self.dev.FindStrFastExS(39, 65, 158, 85, '0|1|2|3|4|5|6|7|8|9', 'B0B2B7-4F4D48', 0.9)
        elif type_id == 4:
            # 等级
            self.dev.UseDict(4)
            num_res = self.dev.FindStrFastExS(25, 3, 106, 29, '0|1|2|3|4|5|6|7|8|9', 'D7B70F-28210F', 0.8)
        elif type_id == 5:
            # 强化等级
            self.dev.UseDict(10)
            num_res = self.dev.FindStrFastExS(275, 284, 373, 326, '0|1|2|3|4|5|6|7|8|9', '6B747D-2A2725', 0.8)
        elif type_id == 6:
            # 频道数
            self.dev.UseDict(8)
            num_res = self.dev.FindStrFastExS(924, 20, 1063, 67, '0|1|2|3|4|5|6|7|8|9', 'D47155-2B0A05', 0.7)
        else:
            return '0'
        gold_num = ''
        gold_res = num_res.split('|')
        for _n in gold_res:
            gold = _n.split(',')
            gold_num = gold_num + gold[0]
        if gold_num == '':
            gold_num = '0'
        return gold_num

    def word_find(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime,
                  t_log=GlobalEnumG.TestLog):
        try:
            dict_index, _x, _y, _x1, _y1, _find_name, _offset_color, _sim = find_info
            self.dev.UseDict(dict_index)
            word_res = self.dev.FindStrFastE(_x, _y, _x1, _y1, _find_name, _offset_color, _sim)
            word_res, word_x, word_y = word_res.split('|')
            if word_res != '-1':
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f'find_word:{_find_name}_x,y:{word_x},{word_y}_T')
                if clicked:
                    self.touch((int(word_x), int(word_y)))
                    if touch_wait > 0:
                        time.sleep(touch_wait)
                return True
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'find_word:{_find_name}_x,y:{word_x},{word_y}_F')
            return False
        except TypeError:
            return False

    def mul_color(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime,
                  t_log=GlobalEnumG.TestLog):
        _x, _y, _x1, _y1, _first_color, _offset_color, _sim, _dir, _find_name = find_info
        res, find_x, find_y = self.dev.FindMultiColor(_x, _y, _x1, _y1, _first_color, _offset_color, _sim, _dir)
        if res == 1:
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'find:{_find_name}_x,y:{find_x},{find_y}_T')
            if clicked:
                self.touch((find_x, find_y))
                if touch_wait > 0:
                    time.sleep(touch_wait)
            return True
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f'find:{_find_name}_x,y:{find_x},{find_y}_F')
        return False

    @catch_ex
    def cmp_rgb(self, rgb_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime,
                t_log=GlobalEnumG.TestLog):
        """获取某一像素点RBG数据"""
        get_x, get_y, find_color = rgb_info
        _cmp_res = self.dev.CmpColor(get_x, get_y, find_color, sim=1)
        if _cmp_res == 0:
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'find:{find_color}_x,y:{get_x},{get_y}_T')
            if clicked:
                self.touch((get_x, get_y))
                if touch_wait > 0:
                    time.sleep(touch_wait)
            return True
        if t_log:
            _color = self.rgb(get_x, get_y)
            self.sn.log_tab.emit(self.mnq_name, f'find:{find_color}_[{_color}]_x,y:{get_x},{get_y}_F')
        return False

    def cmp_rgb_list(self, rgb_list, rgb_xy, t_log=GlobalEnumG.TestLog):
        """检查单点多个颜色"""
        _cmp_res = self.rgb(rgb_xy[0], rgb_xy[-1])
        if _cmp_res in rgb_list:
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'cmp_rgb_list:{_cmp_res}_[{rgb_list}]_x,y:{rgb_xy}_T')
            return True
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f'cmp_rgb_list:{_cmp_res}_[{rgb_list}]_x,y:{rgb_xy}_F')
        return False

    def find_color(self, find_info, clicked=False, t_log=GlobalEnumG.TestLog, wait_touch=GlobalEnumG.TouchWaitTime):
        x, y, x1, y1, color = find_info
        res = self.dev.FindColorE(x, y, x1, y1, color, 1, 0)
        xy = res.split('|')
        if xy[0] != '-1':
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'find_color:{find_info}_T')
            if clicked:
                t_x = int(xy[0])
                t_y = int(xy[-1])
                self.touch((t_x, t_y))
                time.sleep(wait_touch)
            return True
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f'find_color:{find_info}_F')
        return False

    def auto_time_block(self):
        res = self.dev.FindColor(320, 253, 563, 482, '4D9DFB-000000', 1, 0)
        if res[0] == 1:
            return True
        return False

    def task_block(self):
        """幻影紫色任务"""
        res = self.dev.FindColorE(73, 184, 351, 407, 'CA4FEE-0E0611', 1, 0)
        xy = res.split('|')
        if xy[0] != '-1':
            t_x = int(xy[0])
            t_y = int(xy[-1])
            self.touch((t_x, t_y))
            return True
        return False

    @catch_ex
    def rgb(self, get_x, get_y):
        return self.dev.GetColor(get_x, get_y)

    # @catch_ex
    def check_ui(self, find_ui):
        """检查界面ui名称"""
        return self.word_find([2, 9, 15, 477, 74, find_ui, 'CDD1D7-322E28', 0.9])

    def find_xt_num(self, find_info, clicked=False):
        """查找星图"""
        return self.word_find([7, 649, 158, 915, 587, find_info, '9A9A9A-4D4D4D', 0.9], clicked)

    def find_pd_num(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        """查找频道"""
        self.dev.UseDict(8)
        res = self.dev.FindStrFastEx(231, 157, 1051, 595, '0|1|2|3|4|5|6|7|8|9', '4E7355-44274A', 0.90)
        pd_num = ''
        res = res.split('|')
        max_x = 280
        res_list = []
        max_y = 0
        for pd in res:
            p = pd.split(',')
            if res.index(pd) == 0:
                max_y = int(p[-1])
            if abs(int(p[1]) - max_x) > 50 or 1 < abs(int(p[-1]) - max_y) < 10:
                if find_info in pd_num:
                    if t_log:
                        self.sn.log_tab.emit(self.mnq_name, f"找到频道_{find_info}_list{res_list}")
                    if clicked:
                        self.touch((int(max_x), int(max_y)), touch_wait=touch_wait)
                    return True
                if pd_num != '':
                    res_list.append(int(pd_num))
                pd_num = ''
                pd_num = pd_num + p[0]
            else:
                pd_num = pd_num + p[0]
            max_x = int(p[1])
            max_y = int(p[-1])
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f"没找到频道_{find_info}_list{res_list}")
        return False

    def find_zbz(self):
        """检查装备中,位置坐标"""
        zb_list = []
        self.dev.UseDict(0)
        res = self.dev.FindStrFastExS(736, 236, 1255, 376, '装备中', 'C3C3C4-3C3C3B', 0.9)
        res1 = res.split('|')
        for _i in res1:
            p = _i.split(',')
            zb_list.append((int(p[1]), int(p[-1])))
        return zb_list

    def find_mr_task(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        """查找每日任务入口"""
        return self.word_find([1, 16, 160, 1265, 515, find_info, 'D4D3D3-2B2C2C', 0.9], clicked, touch_wait, t_log)

    def enum_find(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        return self.word_find([0, 804, 66, 1263, 622, find_info, 'C5C6C7-3A3938', 0.9], clicked, touch_wait, t_log)

    def check_hp_mp(self):
        """检查药品是否为空"""
        self.dev.UseDict(0)
        res_fast = self.dev.FindStrFastExS(1130, 369, 1248, 389, 'HP|MP', 'D8D8D7-272728', 0.9)
        s_list = res_fast.split('|')
        res_str = ''
        if len(s_list) != 0:
            for _ in s_list:
                _r = _.split(',')
                res_str = res_str + _r[0]
        return res_str

    def check_put_num(self, type_id):
        """检查药水购买数量 或 组队密码输入数量"""
        self.dev.UseDict(9)
        # 538, 205, 749, 254
        if type_id == 0:
            find_res = self.dev.FindStrFastExS(717, 624, 823, 667, '0|1|2|3|4|5|6|7|8|9', '646D7A-282623', 0.9)
        else:
            find_res = self.dev.FindStrFastExS(538, 205, 749, 254, '0|1|2|3|4|5|6|7|8|9', 'ABABAB-282828', 0.7)
        res_num = ''
        _res = find_res.split('|')
        for _n in _res:
            gold = _n.split(',')
            res_num = res_num + gold[0]
        if res_num == '':
            res_num = '0'
        return res_num

    def map_yt(self, map_name):
        """在地图界面，选择地图区域，例 时间神殿、未来之门"""
        return self.word_find([11, 14, 81, 150, 708, map_name, 'D1D2D4-2E2D2B', 0.8], True,t_log=False)

    def map_ex(self, map_name, type_id=1):
        if type_id == 1:
            """星图"""
            return self.word_find([7, 40, 87, 202, 121, f"{map_name}ex", 'B6B6B6-494949', 0.8], clicked=False)
        else:
            return self.word_find([11, 40, 87, 202, 121, f"{map_name}ex", 'B6B6B6-494949', 0.9], clicked=False)

    def back_ksdy(self):
        """检查返回至快速单元"""
        return self.word_find(WorldEnumG.BACN_KSDY, clicked=True)

    def check_boss_end(self, boss_id):
        """检查boss图是否完成"""
        if boss_id == 0:
            """炎魔"""
            _boss_res = self.word_find(WorldEnumG.YM_READY)
        elif boss_id == 1:
            """皮卡啾"""
            _boss_res = self.word_find(WorldEnumG.PKJ_READY)
        else:
            """女皇"""
            _boss_res = self.word_find(WorldEnumG.NH_READY)
        return _boss_res

    def qr_tip(self):
        """检查确认、取消弹窗"""
        if self.word_find(WorldEnumG.QR_BTN, clicked=True):
            self.sn.log_tab.emit(self.mnq_name, r"点击弹窗按钮")
            return True
        return False

    def net_err(self):
        """检查网路异常弹窗"""
        return self.word_find(WorldEnumG.NET_ERR)

    def touch(self, touplexy, touch_wait=1, duration=0.3):
        int_x, int_y = touplexy
        self.dev.MoveTo(int_x, int_y)
        self.dev.LeftDown()
        time.sleep(duration)
        self.dev.LeftUp()
        if touch_wait > 0:
            time.sleep(touch_wait)


class DmImgTools:
    def __init__(self):
        self.dev = None
        self._img = None
        self.sn = None
        self.mnq_name = None

    turn_pos = {
        'up': (146, 471),
        'down': (144, 629),
        'left': (79, 543),
        'right': (239, 544),
        'jump': (1207, 624),
        'attack': (1074, 619),
        'c': (948, 659),
        'v': (958, 559),
        'd': (1054, 501),
        'f': (1148, 505)
    }

    def key_event(self, key, wait_time=2.0, k_time=0.5):
        self.dev.KeyDownChar(key)
        time.sleep(k_time)
        self.dev.KeyUpChar(key)
        time.sleep(wait_time)

    @catch_ex
    def pic_find(self, temp, clicked=True, touch_wait=GlobalEnumG.TouchWaitTime, get_pos=False,
                 t_log=GlobalEnumG.TestLog,
                 loop=0):
        """
        循环查找图片并点击，超时返回
        """
        area, delta_color, pic_name = temp
        x, y, x1, y1 = area
        if loop > 0:
            s_time = time.time()
            while time.time() - s_time < loop:
                dm_ret = self.dev.FindPic(x, y, x1, y1, OT.imgpath(pic_name), delta_color, 0.7, 0)
                if dm_ret[-1] != -1:
                    if clicked:
                        self.touch_ex(dm_ret, touch_wait)
                    if get_pos:
                        return dm_ret
                    if t_log:
                        self.sn.log_tab.emit(self.mnq_name, f"loop_find:{temp}")
                    return True
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"f_loop_find:{temp}")
            if get_pos:
                return 0, 0
            return False
        else:
            dm_ret = self.dev.FindPic(x, y, x1, y1, OT.imgpath(pic_name), delta_color, 0.7, 0)
            if dm_ret[-1] == -1:
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f"f_pic_find:{temp}")
                if get_pos:
                    return 0, 0
                return False
            else:
                if clicked:
                    self.touch_ex(dm_ret, touch_wait)
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f"pic_find:{temp}")
                if get_pos:
                    return dm_ret
                return True

    def touch_ex(self, dm_ret, touch_wait=0):
        self.dev.MoveToEx(dm_ret[1], dm_ret[-1], GlobalEnumG.TouchEx, GlobalEnumG.TouchEy)
        self.dev.LeftClick()
        if touch_wait > 0:
            time.sleep(touch_wait)

    @catch_ex
    def air_all_find(self, temp, t_log=GlobalEnumG.TestLog):
        area, delta_color, pic_name = temp
        x1, y1, x2, y2 = area
        res = self.dev.FindPicEx(x1, y1, x2, y2, f"{pic_name}.bmp", delta_color, 0.9, 0)
        r1 = res.split('|')
        rl = []
        if r1[0] == '':
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, r"没有找到密码队伍")
            return rl
        if len(r1) > 0:
            for i in r1:
                r2 = i.split(',')
                find_x = int(r2[1])
                find_y = int(r2[-1])
                rl.append([find_x, find_y])
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, r"找到密码队伍")
            return rl
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, r"没有找到密码队伍")
        return rl

    @catch_ex
    def dm_swipe(self, start_xy, end_xy, swipe_wait=GlobalEnumG.TouchWaitTime):
        self.dev.MoveTo(end_xy[0], end_xy[-1])
        self.dev.LeftDown()
        time.sleep(0.5)
        self.dev.MoveTo(start_xy[0], start_xy[-1])
        time.sleep(0.5)
        self.dev.MoveTo(end_xy[0], end_xy[-1])
        time.sleep(0.5)
        self.dev.LeftUp()
        if swipe_wait > 0:
            time.sleep(swipe_wait)

    def touch(self, touplexy, touch_wait=1, duration=0.1):
        int_x, int_y = touplexy
        self.dev.MoveTo(int_x, int_y)
        self.dev.LeftDown()
        time.sleep(duration)
        self.dev.LeftUp()
        if touch_wait > 0:
            time.sleep(touch_wait)

    @catch_ex
    def move_turn(self, turn, k_time, jump_mode=False):
        if jump_mode and 2 > k_time > 0.1:
            self.key_double_jump(turn, k_time)
        else:
            # _pos = self.turn_pos[turn]
            self.key_event(turn, k_time=k_time, wait_time=0)
            # self.touch(_pos, touch_wait=0, duration=k_time)

    def get_move_xy(self):
        res, x, y = self.dev.FindMultiColor(864, 75, 1257, 193,
                                            "FFE230",
                                            "0|1|FFDB28,0|2|FFD91F,0|3|FFD718,1|3|FFD718,2|3|FFD718,3|3|F9D71E,-1|3|FDDA22,-2|3|FDDA23,-3|3|FCD923,-3|1|FDDA23,-2|-1|FFF34A,-2|-1|FFF34A,0|-1|FFF34A,1|-1|FFF147,2|-1|FFF147,3|-1|F9F049,3|0|F9EA40",
                                            0.9, 1)

        # res, x, y=self.dev.FindColorBlock(850,65,1264,207,'7F7C71-807C71', 0.7, 50,414,142)
        return res, x, y

    @catch_ex
    def mul_point_touch(self, turn, action, k_time=1, long_click=False):
        """多点长按，控制移动"""
        if long_click:
            time.sleep(k_time / 10)
            self.dev.KeyDownChar(action)
            time.sleep(k_time / 10)
            self.dev.KeyDownChar(turn)
            time.sleep(k_time * 1.5)
            self.dev.KeyUpChar(turn)
            time.sleep(k_time / 10)
            self.dev.KeyUpChar(action)
            time.sleep(k_time / 10)
        else:
            _s_time = time.time()
            while time.time() - _s_time < k_time:
                self.dev.KeyDownChar(turn)
                time.sleep(k_time)
                self.dev.KeyUpChar(turn)
                self.key_event(action, k_time=0.22, wait_time=0)

    @catch_ex
    def double_jump_touch(self, turn):
        self.dev.KeyDownChar(turn)
        time.sleep(0.2)
        self.key_event('x', k_time=0.14, wait_time=0.2)
        self.key_event('x', k_time=0.23, wait_time=0)
        self.dev.KeyUpChar(turn)

    @catch_ex
    def jump_down_touch(self):
        self.dev.KeyDownChar("down")
        time.sleep(1)
        self.key_event("x", k_time=0.32, wait_time=0)
        self.dev.KeyUpChar("down")

    def key_double_jump(self, turn, k_time=3):
        if turn == 'left':
            _k_pos = (78, 453)
        else:
            _k_pos = (216, 453)
        self.touch(_k_pos, duration=k_time)


if __name__ == '__main__':
    dev = DevicesConnect.dm_init()
    DevicesConnect.bind_windows(dev, 794136)
    o = ColorCvTools()
    o.dev = dev
    a = DmImgTools()
    a.dev = dev
    # r=a.pic_find(ImgEnumG.EXIT_TEAM,t_log=False)
    # r=a.dm_swipe((1093, 535), (1093, 314))
    r=o.cmp_rgb([687, 524, 'ee7046'], True,t_log=False)
    # r=o.find_color([495,237,794,344,'EB8D6B-0B2229'],True,t_log=False)
    # r=o.word_find(WorldEnumG.INGAME_FLAG,False,t_log=False)
    # r=o.mul_color(MulColorEnumG.LB_TIP,False,t_log=False)
    # o.touch(r[0])
    print(r)
