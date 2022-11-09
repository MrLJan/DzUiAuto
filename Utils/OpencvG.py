# -*- coding: utf-8 -*-
import time

import numpy
from airtest.aircv import aircv
from airtest.core.android.touch_methods.base_touch import DownEvent, SleepEvent, UpEvent
from cv2 import cv2

from Enum.ResEnum import GlobalEnumG, OpenCvEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.OtherTools import OT


class OpenCvTools:
    def __init__(self):
        self.dev = None
        self.sn = None
        self._img = None
        self.mnq_name = None

    def get_rgb(self, rgb_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime,
                t_log=GlobalEnumG.TestLog):
        """获取某一像素点RBG数据"""
        get_x, get_y, find_color = rgb_info
        self._img = self.dev.snapshot()
        if self._img is not None:
            _color = self.nd_to_hex(self._img[get_y, get_x])
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'expoint:{_color}_find:{find_color}_x,y:{get_x},{get_y}')
            if find_color in _color:
                if clicked:
                    self.dev.touch((get_x, get_y))
                    if touch_wait > 0:
                        time.sleep(touch_wait)
                return True
        return False

    def rgb(self, get_x, get_y):
        self._img = self.dev.snapshot()
        _color = self._img[get_y, get_x]  # 横屏1280x720
        return self.nd_to_hex(_color)

    @staticmethod
    def nd_to_hex(ndarry):
        _point = ''
        for _p in ndarry:
            _point = str(hex(_p))[-2:].replace('x', '0').upper() + _point
        return _point

    def mulcolor_check(self, find_list, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog,
                       get_grb=False):
        """对比多个点的颜色，只要有一个错误就返回"""
        self._img = self.dev.snapshot()
        if self._img is not None:
            c_list = []
            if get_grb:
                _list = find_list
            else:
                _list = find_list[0]
            for _p in _list:
                if get_grb:
                    _color = self.nd_to_hex(self._img[_p[1], _p[0]])
                    c_list.append((_p[0], _p[1], _color))
                else:
                    if _p[-1] not in self.nd_to_hex(self._img[_p[1], _p[0]]):
                        if t_log:
                            self.sn.log_tab.emit(self.mnq_name,
                                                 f"{_p},{self.nd_to_hex(self._img[_p[1], _p[0]])} {find_list[-1]}")
                        return False
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, c_list)
            if clicked:
                self.dev.touch((find_list[0][0][0], find_list[0][0][1]), duration=0.1)
                if touch_wait > 0:
                    time.sleep(touch_wait)
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'T_{find_list[-1]}')
                time.sleep(GlobalEnumG.WaitTime)
            return True
        return False

    def find_color(self, get_x, get_y, get_x1, get_y1, f_color):
        """
        指定范围查找颜色
        :param get_x:
        :param get_y:
        :param get_x1:
        :param get_y1:
        :param f_color: 需要查找的颜色
        :return: 返回找到的坐标
        """
        for x in range(get_x, get_x1):
            for y in range(get_y, get_y1):
                color = self.get_rgb(x, y)
                if color == f_color:
                    return x, y
        return False

    def find_xt_num(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        """查找星图"""
        _crop_img = self._get_crop_img(1091, 159, 1156, 609)
        pos_list = []
        all_list = []
        pos_y = None  # 判定识别文字是否同一行
        s_index = 0  # 切片起始位置
        ret1, img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 转换为二值图像, thresh=63
        res_cont = cv2.findContours(img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        for _i in range(len(res_cont)):
            x, y, w1, h1 = cv2.boundingRect(res_cont[_i])
            if pos_y is None:
                pos_y = y
            ar = w1 / float(h1)
            if 1.5 > ar > 0.5:  # 剔除异常点
                pos_list.append((x, y, w1, h1))
        pos_list.reverse()
        for _ in range(len(pos_list)):
            if pos_y == pos_list[_][1]:
                if _ == len(pos_list) - 1:
                    all_list.append(pos_list[s_index:])
                else:
                    pass
            else:
                e_index = _
                all_list.append(pos_list[s_index:e_index])
                s_index = _
                pos_y = pos_list[_][1]
        # 分别识别每行数字
        _res_pos = []  # 存储返回结果
        if len(all_list) > 0:
            _str = ''  # 拼接识别结果
            _x = 0  # 存储计算每行数字的坐标
            _y = 0
            for _ in range(len(all_list)):
                if len(all_list[_]) > 0:
                    for _t in all_list[_]:
                        _con = 0.8
                        for _p in range(11):  # 匹配每个数字块的单个数字
                            res = cv2.matchTemplate(
                                cv2.resize(img1[_t[1]:_t[1] + _t[-1], _t[0]:_t[0] + _t[2]], (72, 128)),
                                numpy.load(OT.npypath(f'p{_p}')), method=cv2.TM_CCOEFF_NORMED)
                            if numpy.any(res > _con):
                                if _p == 10:
                                    _p = 44
                                _str = _str + str(_p)
                                _x = _t[0]
                                _y = _t[1]
                                _con = 100
                    if find_info == _str:
                        if clicked:
                            self.dev.touch((_x + 1091, _y + 150), duration=0.1)
                        if t_log:
                            self.sn.log_tab.emit(self.mnq_name, f'T_{_str}_xy{_x + 1091}_{_y + 150}')
                        if touch_wait > 0:
                            time.sleep(touch_wait)
                        return True, _res_pos
                if _str != '':
                    _res_pos.append((_str, (_x + 1091, _y + 150)))
                _str = ''
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'F_{find_info}_没找到_all{_res_pos}')
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f'F_{find_info}_没找到')
        return False, _res_pos

    def find_pd_num(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        """查找频道"""
        _crop_img = self._get_crop_img(239, 157, 1049, 581)
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        res_cont = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:  # 筛选数字大轮廓
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar < 0.8 and h1 > 15:
                ori_list.append([x, y, w1, h1])
        ori_list.reverse()  # 调整顺序
        all_list = []  # 存储分块
        _pos_x = None  # 判定是否同一块
        s_index = 0  # 切片索引
        for _ in range(len(ori_list)):
            if _pos_x is None:
                _pos_x = ori_list[_][0]
            if abs(_pos_x - ori_list[_][0]) <= 100:
                if _ == len(ori_list) - 1:
                    all_list.append(ori_list[s_index:])
                else:
                    pass
            else:
                e_index = _
                all_list.append(ori_list[s_index:e_index])
                s_index = _
                _pos_x = ori_list[_][0]
        _pd_num = ''
        _res_pos = []  # 存储所有结果
        _x = 0  # 存储计算每行数字的坐标
        _y = 0
        for _row in range(len(all_list)):
            for _t in all_list[_row]:
                _con = 0.8
                for _p in OpenCvEnumG.GOLD_NUM.keys():
                    _re = cv2.matchTemplate(
                        cv2.resize(_img1[_t[1]:_t[1] + _t[-1], _t[0]:_t[0] + _t[2]], (72, 128)),
                        numpy.load(OpenCvEnumG.GOLD_NUM[_p]), method=cv2.TM_CCOEFF_NORMED)
                    if numpy.any(_re > 0.8):
                        _pd_num = _pd_num + _p
                        _x = _t[0]  # 存储计算每行数字的坐标
                        _y = _t[1]
            if _pd_num == find_info:
                if clicked:
                    self.dev.touch((_x + 239, _y + 157), duration=0.1)
                if touch_wait > 0:
                    time.sleep(touch_wait)
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f"T_{find_info}_xy{(_x + 239, _y + 157)}")
                return True
            _res_pos.append((_pd_num, (_x + 239, _y + 157)))
            _pd_num = ''
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f"T_{_res_pos}")
        time.sleep(1)  # 防止过快
        return False

    def find_zbz(self):
        _crop_img = self._get_crop_img(734, 224, 1260, 380)
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        res_cont, hierarchy = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 1 > ar > 0.9 and h1 > 13:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list = sorted(ori_list, key=lambda _t: _t[-1][0])
        _res_pos = []
        for _row in range(len(ori_list)):
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_row][0], (72, 128)),
                numpy.load(OT.npypath('zb_zbz')), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.9):
                _x, _y = ori_list[_row][1]
                _res_pos.append((_x + 739, _y + 227))
        return _res_pos

    def find_mr_task(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        """查找每日任务"""
        _crop_img = self._get_crop_img(38, 158, 1268, 580)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY_INV)[1]  # 转换为二值图像, thresh=63
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_GRADIENT, sqKernel)
        res_cont, hierarchy = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 5 > ar > 1 and w1 > 50:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        _cmp_img = OT.npypath(f'mr_{find_info}')
        for _num in range(len(ori_list)):
            # for _t in OpenCvEnumG.TEMP.keys():
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_num][0], (72, 128)),
                numpy.load(_cmp_img), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.7):
                if clicked:
                    self.dev.touch((ori_list[_num][-1][0] + 38, ori_list[_num][-1][-1] + 158), duration=0.1)
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name,
                                         f'T_{find_info}_xy{ori_list[_num][-1][0] + 38}_{ori_list[_num][-1][-1] + 158}')
                if touch_wait > 0:
                    time.sleep(touch_wait)
                return True
        return False

    def enum_find(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[62:632, 800:1263]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        _img1 = cv2.threshold(_crop_img.copy(), 245, 255, cv2.THRESH_TOZERO)[1]  # 转换为二值图像, thresh=63
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont, hierarchy = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 5 > ar > 2 and h1 < 20:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        _cmp_img = OT.npypath(find_info)
        for _num in range(len(ori_list)):
            # for _t in OpenCvEnumG.MENU.keys():
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_num][0], (72, 128)),
                numpy.load(_cmp_img), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.6):
                # if _t == find_info:
                if clicked:
                    self.dev.touch((ori_list[_num][-1][0] + 800, ori_list[_num][-1][-1] + 62), duration=0.1)
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name,
                                         f'T_{find_info}_xy{ori_list[_num][-1][0] + 800}_{ori_list[_num][-1][-1] + 62}')
                if touch_wait > 0:
                    time.sleep(touch_wait)
                return True
        return False

    def check_num(self, num_type, t_log=GlobalEnumG.TestLog):
        """检查战力-等级"""
        _cnt_res = 0.8
        if num_type == 1:
            # 战力
            _crop_img = self._get_crop_img(18, 64, 143, 91)
            _cnt_res = 0.69
        elif num_type == 2:
            # 星力
            _crop_img = self._get_crop_img(223, 215, 356, 247)
        elif num_type == 3:
            # 频道
            _crop_img = self._get_crop_img(952, 20, 1070, 63)
        else:
            # 等级 0
            _cnt_res = 0.69
            _crop_img = self._get_crop_img(19, 3, 111, 32)
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 转换为二值图像, thresh=63
        if num_type == 2:
            res_cont, hierarchy = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        else:
            res_cont, hierarchy = cv2.findContours(_img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        _sort_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if num_type == 2:
                if 0.7 > ar > 0.1 and h1 > 5:
                    _sort_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
            else:
                if ar > 0.5 and h1 > 10:
                    # print(ar, x, y, w1, h1)
                    _sort_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        # ori_list.reverse()
        ori_list = sorted(_sort_list, key=lambda _t: _t[-1][0])  # 按照x大小 从小到大排序
        _str_num = ''
        for row in range(len(ori_list)):
            for _t in range(10):
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[row][0], (72, 128)),
                    numpy.load(OT.npypath(f'z{_t}')), method=cv2.TM_CCOEFF_NORMED)
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f're{_re}_{row}')
                if numpy.any(_re > _cnt_res):
                    _str_num = _str_num + str(_t)
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f"{_str_num}")
        if _str_num == '':
            _str_num = '0'
        return _str_num

    def gold_num(self, num_type):
        if num_type == 1:
            # 金币
            _crop_img = self._get_crop_img(690, 371, 907, 409)
        else:
            # 红币
            _crop_img = self._get_crop_img(401, 372, 631, 408)
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 转换为二值图像, thresh=63
        res_cont, hierarchy = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            # ar = w1 / float(h1)
            if 20 > h1 > 10:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list = sorted(ori_list, key=lambda _t: _t[-1][0])
        _gold_num = ''
        for row in range(len(ori_list)):
            for _t in OpenCvEnumG.GOLD_NUM.keys():
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[row][0], (72, 128)),
                    numpy.load(OpenCvEnumG.GOLD_NUM[_t]), method=cv2.TM_CCOEFF_NORMED)
                if numpy.any(_re > 0.8):
                    _gold_num = _gold_num + _t
        if _gold_num == '':
            _gold_num = '0'
        return _gold_num

    def check_time_num(self, type_id=0):
        if type_id == 0:
            """检查自动时间"""
            _crop_img = self._get_crop_img(374, 345, 502, 392)
            _cnt_res = 0.69
        else:
            """强化界面检查强化等级"""
            _crop_img = self._get_crop_img(286, 282, 368, 331)
            _cnt_res = 0.79
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 转换为二值图像, thresh=63
        res_cont, hierarchy = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 1 > ar > 0.1 and h1 > 10:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list = sorted(ori_list, key=lambda _t: _t[-1][0])
        _time_num = ''
        for row in range(len(ori_list)):
            for _t in range(10):
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[row][0], (72, 128)),
                    numpy.load(OT.npypath(f'g{_t}')), method=cv2.TM_CCOEFF_NORMED)
                # print(_re)
                if numpy.any(_re > _cnt_res):
                    _time_num = _time_num + str(_t)
        if _time_num == '':
            _time_num = '0'
        return _time_num

    def check_hp_mp(self):
        """检查药品是否为空"""
        _crop_img = self._get_crop_img(1127, 365, 1262, 389)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY)[1]  # 转换为二值图像, thresh=63
        img_closed = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont, hierarchy = cv2.findContours(img_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 1.5 and w1 > 15:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_res(ori_list, OpenCvEnumG.HP_MP, cont_res=0.79)

    def check_put_num(self, type_id):
        """检查药水购买数量 或 组队密码输入数量"""
        if type_id == 0:
            """检查药水"""
            _crop_img = self._get_crop_img(717, 624, 823, 667)
        else:
            _crop_img = self._get_crop_img(538, 205, 749, 254)
        _img1 = cv2.threshold(_crop_img.copy(), 140, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[
            1]  # 转换为二值图像
        res_cont = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 0.8 > ar > 0.4 and h1 > 5:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list = sorted(ori_list, key=lambda _t: _t[-1][0])
        return self._match_res(ori_list, OpenCvEnumG.YS_NUM, cont_res=0.69)

    def check_map(self, map_name, t_log=GlobalEnumG.TestLog):
        """在主界面 检查地图名"""
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f"check_map_{map_name}")
        _cmp_res = OT.mapnpy(f'yt_{map_name}')
        _crop_img = self._get_crop_img(910, 97, 1279, 145)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        _img1 = cv2.threshold(_crop_img.copy(), 125, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[
            1]  # 转换为二值图像, thresh=63
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 1 and h1 > 15:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_text(ori_list, _cmp_res, cont_res=0.7)

    def map_yt(self, map_name, t_log=GlobalEnumG.TestLog):
        """在地图界面，选择地图区域，例 时间神殿、未来之门"""
        _cmp_img = OT.mapnpy(f'map_{map_name}')
        _crop_img = self._get_crop_img(2, 76, 155, 716)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY)[1]  # 转换为二值图像
        _img1_e = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_OTSU)[1]
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_GRADIENT, sqKernel)
        _img2_e = cv2.morphologyEx(_img1_e, cv2.MORPH_GRADIENT, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        res_cont_e = cv2.findContours(_img2_e, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 5 > ar > 0.5 and h1 > 20:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        for _cnt_e in res_cont_e:
            x, y, w1, h1 = cv2.boundingRect(_cnt_e)
            ar = w1 / float(h1)
            if 5 > ar > 0.5 and h1 > 20:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        _res, _pos = self._match_text(ori_list, _cmp_img, clicked=True, cont_res=0.6)
        if _res:
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"map_yt_{map_name}")
            self.dev.touch((_pos[0] + 2, _pos[-1] + 76), duration=0.1)
            time.sleep(1)
        return _res

    def check_xt_map(self, map_name, cont_res=0.69):
        """在地图界面检查 地图名"""
        _cmp_res = OT.mapnpy(f'xt_{map_name}')
        _crop_img = self._get_crop_img(910, 97, 1279, 145)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
        _img1 = cv2.threshold(_crop_img.copy(), 130, 255, cv2.THRESH_BINARY_INV)[
            1]  # 转换为二值图像
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 1 and w1 > 50:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_text(ori_list, _cmp_res, cont_res=cont_res)

    def check_map_ex(self, map_name, type_id='3'):
        """检查主界面地图名"""
        if type_id == '3':
            _cmp_res = OT.mapnpy(f'xt_{map_name}_e')
        else:
            _cmp_res = OT.mapnpy(f'yt_{map_name}_e')
        _crop_img = self._get_crop_img(19, 91, 202, 118)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[
            1]  # 转换为二值图像
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 1 and w1 > 20:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        return self._match_text(ori_list, _cmp_res, cont_res=0.69)

    def back_ksdy(self):
        """检查返回至快速单元"""
        _crop_img = self._get_crop_img(251, 167, 1035, 688)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY)[1]
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_GRADIENT, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 10 > ar > 1 and w1 > 100:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        for _row in range(len(ori_list)):
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_row][0], (72, 128)),
                numpy.load(OT.npypath('exit_ydzxd')), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.9):
                self.dev.touch((ori_list[_row][1][0] + 251,
                                ori_list[_row][1][-1] + 167))
                return True
        return False

    def check_boss_end(self, boss_id):
        if boss_id == 0:
            """炎魔"""
            _crop_img = self._get_crop_img(89, 121, 239, 177)
        elif boss_id == 1:
            """皮卡啾"""
            _crop_img = self._get_crop_img(703, 115, 901, 186)
        else:
            """女皇"""
            _crop_img = self._get_crop_img(1033, 117, 1221, 187)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
        _img1 = cv2.threshold(_crop_img.copy(), 150, 255, cv2.THRESH_BINARY)[1]  # 转换为二值图像, thresh=63
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 5 > ar > 2 and w1 > 1:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        _cmp_img = OT.npypath('mr_boss_clear')
        return self._match_text(ori_list, _cmp_img, cont_res=0.7)

    def qr_or_qx(self, type_id=0):
        # self.sn.log_tab.emit(self.mnq_name, r"检查弹窗按钮")
        if type_id == 0:
            _cmp_img = OT.npypath('ui_qx')  # 取消
        else:
            _cmp_img = OT.npypath('ui_qr')  # 确认
        _crop_img = self._get_crop_img(228, 73, 1014, 665)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY)[1]
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_GRADIENT, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 2 > ar > 1.72 and w1 > 22:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        for _row in range(len(ori_list)):
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_row][0], (72, 128)),
                numpy.load(_cmp_img), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.7):
                self.sn.log_tab.emit(self.mnq_name, r"点击弹窗按钮")
                self.dev.touch((ori_list[_row][1][0] + 228,
                                ori_list[_row][1][-1] + 73))
                return True
        return False

    def net_err(self):
        _crop_img = self._get_crop_img(430, 319, 848, 460)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[
            1]  # 转换为二值图像
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 5 and w1 > 200:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        _cmp_img = OT.npypath('net_err')
        return self._match_text(ori_list, _cmp_img, cont_res=0.8)

    def ys_contrl(self, ys_info):
        """药水登录、卸载、立即前往"""
        _crop_img = self._get_crop_img(789, 159, 918, 688)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY)[
            1]  # 转换为二值图像
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_GRADIENT, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 5 > ar > 1 and w1 > 20:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        _cmp_img = OT.npypath(ys_info)
        for _row in range(len(ori_list)):
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_row][0], (72, 128)),
                numpy.load(_cmp_img), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.79):
                _tx, _ty = ori_list[_row][1]
                self.dev.touch((_tx + 789, _ty + 159), duration=0.1)
                return True
        return False

    def _get_crop_img(self, x, y, x1, y1):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        return self._img[y:y1, x:x1]

    def find_info(self, find_info, clicked=False, t_log=GlobalEnumG.TestLog):
        _data = OpenCvEnumG.FIND_INFO[find_info]
        _x, _y, _x1, _y1 = _data[0]
        _k_size, _thr_value, _thr_method, _mor_method, _cont_method, _comp_rate = _data[-1]
        _crop_img = self._get_crop_img(_x, _y, _x1, _y1)
        sqKernel = self._kernel(_k_size)
        _img1 = self._threshold_img(_crop_img, _thr_value, _thr_method)  # 转换为二值图像, thresh=63
        _img2 = self._morphology(_img1, _mor_method, sqKernel)
        res_cont = self._findcont(_img2, _cont_method)
        ori_list = []
        _cnt_data = _data[1]
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if _cnt_data[0] > ar > _cnt_data[1] and w1 > _cnt_data[2] and h1 > _cnt_data[-1]:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        _cmp_img = OT.npypath(find_info)
        if clicked:
            _res, _pos = self._match_text(ori_list, _cmp_img, clicked=clicked, cont_res=_comp_rate)
            if _res:
                self.dev.touch((_pos[0] + _x, _pos[-1] + _y), duration=0.1)
        else:
            _res = self._match_text(ori_list, _cmp_img, clicked=clicked, cont_res=_comp_rate)
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f"_res{_res}_{find_info}")
        time.sleep(1)  # 防止操作过快
        return _res

    def in_team(self):
        """判定是否在组队中，1/6 ZZZ"""
        _crop_img = self._get_crop_img(6, 344, 59, 384)
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY)[1]
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_GRADIENT, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 5 > ar > 1 and w1 > 20 and h1 > 10:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        _cmp_img = OT.npypath('ZZZ')
        if self._match_text(ori_list, _cmp_img):
            return True
        else:
            _cmp_img = OT.npypath('EXP')
        return self._match_text(ori_list, _cmp_img)

    @staticmethod
    def _kernel(k_size):
        """返回任意大小核心"""
        if k_size == 0:
            return None
        return cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))

    @staticmethod
    def _threshold_img(crop_img, thr_value, thr_method):
        """处理二值化图像"""
        if thr_method == 0:
            return cv2.threshold(crop_img.copy(), thr_value, 255, cv2.THRESH_BINARY)[1]
        elif thr_method == 1:
            return cv2.threshold(crop_img.copy(), thr_value, 255, cv2.THRESH_BINARY_INV)[1]
        elif thr_method == 2:
            return cv2.threshold(crop_img.copy(), thr_value, 255, cv2.THRESH_TRUNC)[1]
        elif thr_method == 3:
            return cv2.threshold(crop_img.copy(), thr_value, 255, cv2.THRESH_TOZERO)[1]
        elif thr_method == 4:
            return cv2.threshold(crop_img.copy(), thr_value, 255, cv2.THRESH_TOZERO_INV)[1]
        elif thr_method == 5:
            return cv2.threshold(crop_img.copy(), thr_value, 255, cv2.THRESH_OTSU)[1]
        elif thr_method == 6:
            return cv2.threshold(crop_img.copy(), thr_value, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    @staticmethod
    def _morphology(mor_img, mor_method, mor_kernel):
        """形态操作"""
        if mor_method == 0:
            return cv2.morphologyEx(mor_img, cv2.MORPH_GRADIENT, mor_kernel)
        elif mor_method == 1:
            return cv2.morphologyEx(mor_img, cv2.MORPH_CLOSE, mor_kernel)
        elif mor_method == 2:
            return cv2.morphologyEx(mor_img, cv2.MORPH_OPEN, mor_kernel)
        elif mor_method == 99:
            return None

    @staticmethod
    def _findcont(cont_img, cont_method):
        """轮廓查找"""
        if cont_method == 0:
            return cv2.findContours(cont_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        elif cont_method == 1:
            return cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    @staticmethod
    def _match_res(ori_list, enum_res, cont_res=0.9, t_log=GlobalEnumG.TestLog):
        """匹配数字"""
        _bat_num = ''
        for row in range(len(ori_list)):
            for _t in enum_res.keys():
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[row][0], (72, 128)),
                    numpy.load(enum_res[_t]), method=cv2.TM_CCOEFF_NORMED)
                if t_log:
                    print(_re)
                if numpy.any(_re > cont_res):
                    _bat_num = _bat_num + _t
        return _bat_num

    @staticmethod
    def _match_text(ori_list, cmp_res, clicked=False, cont_res=0.79, t_log=GlobalEnumG.TestLog):
        for _row in range(len(ori_list)):
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_row][0], (72, 128)),
                numpy.load(cmp_res), method=cv2.TM_CCOEFF_NORMED)
            if t_log:
                print(_re)
            if numpy.any(_re > cont_res):
                if clicked:
                    return True, ori_list[_row][-1]
                return True
        if clicked:
            return False, (0, 0)
        return False


class AirImgTools:
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

    # @staticmethod
    def crop_image_find(self, area_temp, clicked=True, touch_wait=GlobalEnumG.TouchWaitTime,
                        get_pos=False, t_log=GlobalEnumG.TestLog):
        """区域找图"""
        self._img = self.dev.snapshot()
        if self._img is not None:
            area = area_temp[0]
            temp = area_temp[-1]
            crop_img = aircv.crop_image(self._img, area)
            res = temp.match_in(crop_img)
            if res:
                pos = (res[0] + area[0], res[1] + area[1])
                if clicked:
                    self.dev.touch(pos)
                    if touch_wait > 0:
                        time.sleep(touch_wait)
                if get_pos:
                    if t_log:
                        self.sn.log_tab.emit(self.mnq_name, f"crop_image_find:{temp}")
                    return True, pos[0], pos[-1]
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f"crop_image_find:{temp}")
                return True
            if get_pos:
                return False, 0, 0
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"f_crop_image_find:{temp}")
            return False
        return False

    def air_loop_find(self, temp, clicked=True,
                      touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        """
        循环查找图片并点击，超时返回
        """
        img = temp[-1]
        self._img = self.dev.snapshot()
        if self._img is not None:
            match_pos = img.match_in(self._img)
            if not match_pos:
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f"f_air_loop_find:{temp}")
                return False
            if match_pos:
                if clicked:
                    self.dev.touch(match_pos)
                    if touch_wait > 0:
                        time.sleep(touch_wait)
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"air_loop_find:{temp}")
            return True
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f"f_air_loop_find:{temp}")
        return False

    def air_all_find(self, temp, t_log=GlobalEnumG.TestLog):
        img = temp[-1]
        self._img = self.dev.snapshot()
        _pos_list = []
        if self._img is not None:
            match_pos = img.match_all_in(self._img)
            for _match in match_pos:
                _pos_list.append(_match['result'])
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"air_all_find:{temp}_{match_pos}")
        return _pos_list

    def air_touch(self, touch_xy, duration=0.2, touch_wait=1):
        self.dev.touch(touch_xy, duration=duration)
        if touch_wait > 0:
            time.sleep(touch_wait)

    def air_swipe(self, start_xy, end_xy, swipe_wait=0):
        self.dev.swipe(start_xy, end_xy)
        if swipe_wait > 0:
            time.sleep(swipe_wait)

    def move_turn(self, turn, k_time, jump_mode=False):
        if jump_mode and 2>k_time > 1:
            self.key_double_jump(turn, k_time)
        else:
            _pos = self.turn_pos[turn]
            self.air_touch(_pos, duration=k_time)

    def mul_point_touch(self, turn, action, k_time=1, long_click=False):
        """多点长按，控制移动"""

        t_pos = self.turn_pos[turn]
        a_pos = self.turn_pos[action]
        if long_click:
            multitouch_event = [
                DownEvent(t_pos, 0),  # 手指1按下(100, 100)
                DownEvent(a_pos, 1),  # 手指2按下(200, 200)
                SleepEvent(k_time),
                UpEvent(1), UpEvent(0)
            ]
        else:
            if action == 'jump' and turn != 'down':
                multitouch_event = [
                    DownEvent(self.turn_pos['up'], 2),
                    DownEvent(t_pos, 0),  # 手指1按下(100, 100)
                    DownEvent(a_pos, 1),  # 手指2按下(200, 200)
                    UpEvent(1),
                    SleepEvent(0.1),
                    DownEvent(a_pos, 1),
                    SleepEvent(0.1),
                    UpEvent(1),
                    SleepEvent(k_time),
                    UpEvent(2),
                    UpEvent(0)
                ]
                # UpEvent(0), UpEvent(1)]  # 2个手指分别抬起
            else:
                multitouch_event = [
                    DownEvent(t_pos, 0),  # 手指1按下(100, 100)
                    DownEvent(a_pos, 1),  # 手指2按下(200, 200)
                    UpEvent(1),
                    SleepEvent(0.1),
                    DownEvent(a_pos, 1),
                    SleepEvent(0.1),
                    UpEvent(1),
                    SleepEvent(k_time),
                    UpEvent(0)
                ]
                # UpEvent(0), UpEvent(1)]  # 2个手指分别抬起
        self.dev.touch_proxy.perform(multitouch_event)

    def double_jump_touch(self, turn, k_time=0.2):
        t_pos = self.turn_pos[turn]
        up_pos = self.turn_pos['up']
        a_pos = self.turn_pos['jump']
        multitouch_event = [
            DownEvent(t_pos, 0),  # 手指1按下(100, 100)
            DownEvent(a_pos, 2),  # 手指2按下(200, 200)
            UpEvent(2),
            SleepEvent(0.1),
            DownEvent(a_pos, 2),
            SleepEvent(0.1),
            DownEvent(up_pos, 1),
            UpEvent(2), SleepEvent(k_time), UpEvent(0), UpEvent(1)
        ]
        self.dev.touch_proxy.perform(multitouch_event)

    def jump_down_touch(self, k_time=1):
        t_pos = self.turn_pos['down']
        a_pos = self.turn_pos['jump']
        multitouch_event = [
            DownEvent(t_pos, 0),  # 手指1按下(100, 100)
            SleepEvent(k_time),
            DownEvent(a_pos, 1),  # 手指2按下(200, 200)
            SleepEvent(0.1),
            UpEvent(0), UpEvent(1),
        ]
        self.dev.touch_proxy.perform(multitouch_event)

    def key_double_jump(self, turn, k_time=3):
        if turn == 'left':
            _k_pos = (78, 453)
        else:
            _k_pos = (216, 453)
        self.air_touch(_k_pos, duration=k_time)


if __name__ == '__main__':
    # img_fp = r'D:\DzAutoUi\Res\img\21.bmp'
    # res, dev = DevicesConnect('emulator-5554').connect_device()
    res2, dev2 = DevicesConnect('127.0.0.1:5555').connect_device()
    o = OpenCvTools()
    o.dev = dev2
    a = AirImgTools()
    a.dev = dev2
    # r=o.mulcolor_check(ColorEnumG.LOGIN_MAIN)
    # while True:
    # a.double_jump_touch('right')

    #     t1=time.time()
    #     r=a.crop_image_find(ImgEnumG.INGAME_FLAG2,False)
    #     print(r,time.time()-t1)
    # ui_list = [92, 16, 241, 63, 'xl']
    # r = o.check_ui(ui_list)
    t1 = time.time()
    # r=o.enum_find('ksnr',True,touch_wait=0)
    # while True:
    # r = o.check_num(3,t_log=False)
    # r=o.net_err()
    # r = RewardG.RewardG((dev2, '127.0.0.1:5555'), 'ld1', sn).get_hd_reward()
    # r = o.find_xt_num('144', t_log=False)
    # r = o.check_map('wqk')
    # r=o.find_zbz()
    # r=o.net_err()
    # r=o.qr_or_qx(1)
    # r=o.find_mr_task('wl',True,t_log=False)
    # r = o.check_xt_map('130')
    # r = o.ys_contrl('ys_ljqw')
    # r = o.check_xt_map('120')
    # r = o.check_boss_end(0)
    # r=o.gold_num(2)'
    # r=a.crop_image_find(ImgEnumG.PERSON_POS, clicked=False, get_pos=True,t_log=False)
    # r=o.check_num(2,t_log=False)
    # r=o.check_xt_map('136')
    for t in range(1,3):
        print(t)
    # r = a.air_all_find(ImgEnumG.PWD_TEAM,t_log=False)
    # r = o.check_num(1, t_log=False)
    # if not r:
    # if r != '':
    #     print(r, 1)
    # r=o.find_xt_num('55',True)
    # r = o.find_mr_task('wl', True, touch_wait=0)
    print(time.time() - t1)
    # r=c.get_ocrres([395, 647, 450, 663],t_log=False)
    # r=o.rgb(1146,213)
    # r = o.get_rgb([1146, 213,'415067'],t_log=False)
    # r=a.crop_image_find(ImgEnumG.INGAME_FLAG2, touch_wait=2,t_log=False)

    # r=a.air_loop_find(ImgEnumG.ZB_TS,False)
    # r=c.get_ocrres([33,1,86,29],t_log=True)
    # print(r)
    # for x in range(532,578):
    #     for y in range(514,550):
    #         print(f"{x},{y},{o.rgb(x,y)}")
    # r = a.crop_image_find(ImgEnumG.UI_SET, False)

    # while True:
    #     r=c.crop_image_find(ImgEnumG.PERSON_POS,clicked=False,get_pos=True)
    #     print(r)
    # r = c.mul_point_touch('down', 'jdown', k_time=1)

    # r=c.mul_point_touch('down', 'jump',long_click=True)
    # louti_queue = QueueManage(1)
    # turn_queue = QueueManage(1)
    # auto_wait = QueueManage(1)
    # map_data=BatEnumG.MAP_DATA['爱奥斯塔入口']
    # while True:
    #     AutoBatG.AutoBatG((dev2,'emulator-5554'),1,1).keyboard_bat(map_data, 1,auto_wait,1,louti_queue,turn_queue)
    # r=StateCheckG.StateCheckG((dev2,'emulator-5554'),1,1).get_num((685,189,721,218))
    # r=TeamStateG.TeamStateG((dev2,'emulator-5554'),1,1).choose_pindao()

    # r=UpRoleG.UpRoleG((dev2,'emulator-5554'),'ld1',1).strongequip()
    # r=RewardG.RewardG((dev2,'emulator'),'ld1',1).get_equip()
    # r=a.crop_image_find(ImgEnumG.L_BS)
    # r=a.air_loop_find(ImgEnumG.FJ_HE2)
    # r=a.find_all_pos(ImgEnumG.ZB_TS)

    # r = c.ocr_find([(0, 0, 1280, 720), 'LV'])
    # a.air_swipe((925, 432), (400, 432))x
    # r = c.get_ocrres((41, 66, 165, 87))  # ((568,313,708,346))#自勤速腺中

    # c_l = [
    #     ColorEnumG.LOGIN_CLOSE, ColorEnumG.LOGIN_MAIN, ColorEnumG.LOGIN_START,
    #     ColorEnumG.MAIN_UI, ColorEnumG.PET_TIME_END, ColorEnumG.QD_HD_BJBS, ColorEnumG.QD_HD_BJBS_CLOSE,
    #     ColorEnumG.QD_MY, ColorEnumG.HD_LB, ColorEnumG.BAG_MAIN, ColorEnumG.BAG_SELL, ColorEnumG.BAG_GOLD,
    #     ColorEnumG.BAG_SX, ColorEnumG.TASK_CLOSE, ColorEnumG.MR_KSDY, ColorEnumG.WL_MAIN, ColorEnumG.WL_JR,
    #     ColorEnumG.JZT_MAIN, ColorEnumG.JZT_JR, ColorEnumG.MRDC_MAIN, ColorEnumG.MRDC_JR, ColorEnumG.JHXT_MAIN,
    #     ColorEnumG.JHXT_JR, ColorEnumG.YZD_MAIN, ColorEnumG.GWSLT_MAIN, ColorEnumG.TBB_MAIN, ColorEnumG.TBB_JR,
    #     ColorEnumG.TBB_ZCJR, ColorEnumG.XLZC_MAIN, ColorEnumG.CYRQ_MAIN, ColorEnumG.MNDC_MAIN, ColorEnumG.MNDC_JR,
    #     ColorEnumG.XGT_MAIN, ColorEnumG.EXIT_TEAM, ColorEnumG.HDYZD_MAIN, ColorEnumG.GH_MAIN, ColorEnumG.GH_WXDC,
    #     ColorEnumG.MAIL_MAIN, ColorEnumG.KT_MAIN, ColorEnumG.PET_MAIN, ColorEnumG.JN_MAIN, ColorEnumG.YS_LOGIN,
    #     ColorEnumG.YS_SHOP, ColorEnumG.YS_XQ, ColorEnumG.YS_GM_QR
    # ]
    # screen=dev2.snapshot()
    # cv2.cv2.setNumThreads(1)
    # cv2.cv2.ocl.setUseOpenCL(False)
    # while True:
    #     t1 = time.time()
    #     # o.screen = dev2.snapshot()
    #     # r = DailyTaskG.DailyTaskAutoG((dev2, 'emulator-5556'), 1, 1,cn_ocr).wulin_task()
    #     # r=o.mulcolor_check(ColorEnumG.LOGIN_START, clicked=True,test=False)
    #     r = o.mulcolor_check(ColorEnumG.MR_KSDY, test=False)
    #     #     for _f in c_l:
    #     #         r = o.mulcolor_check(_f,test=False)
    #     #         print(r, time.time() - t1)
    #     #     r=a.crop_image_find(ImgEnumG.TEAM_FIND)
    #     #     r = c.ocr_find([(0, 0, 1280, 720), 'LV'])
    #     print(r, time.time() - t1)
    # while True:
    #     r=a.crop_image_find(ImgEnumG.PERSON_POS,clicked=False,get_pos=True)
    #     print(r)
    #     time.sleep(1)
#
