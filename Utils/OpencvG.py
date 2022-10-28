# -*- coding: utf-8 -*-
import time

import numpy
from airtest.aircv import aircv
from airtest.core.android.touch_methods.base_touch import DownEvent, SleepEvent, UpEvent
from cnocr import CnOcr
from cv2 import cv2

from Enum.ResEnum import GlobalEnumG, ImgEnumG, OpenCvEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.OtherTools import OT
from Utils.ThreadTools import ThreadTools


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
                self.dev.touch((find_list[0][0][0], find_list[0][0][1]))
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
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[150:609, 1091:1156]
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
            print(ar, x, y, w1, h1)
            if 0.8 > ar > 0.5:  # 剔除异常点
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
        if len(all_list) > 0:
            _res_pos = []  # 存储返回结果
            _str = ''  # 拼接识别结果
            _x = 0  # 存储计算每行数字的坐标
            _y = 0
            for _ in range(len(all_list)):
                if len(all_list[_]) > 0:
                    for _t in all_list[_]:
                        _con = 0.8
                        for _p in OpenCvEnumG.STAR_NUM.keys():  # 匹配每个数字块的单个数字
                            res = cv2.matchTemplate(
                                cv2.resize(img1[_t[1]:_t[1] + _t[-1], _t[0]:_t[0] + _t[2]], (72, 128)),
                                numpy.load(_p), method=cv2.TM_CCOEFF_NORMED)
                            if numpy.any(res > _con):
                                _str = _str + OpenCvEnumG.STAR_NUM[_p]
                                _x = _t[0]
                                _y = _t[1]
                                _con = 100
                    if find_info == _str:
                        if clicked:
                            self.dev.touch((_x + 1091, _y + 150))
                        if t_log:
                            self.sn.log_tab.emit(self.mnq_name, f'T_{_str}_xy{_x + 1091}_{_y + 150}')
                        if touch_wait > 0:
                            time.sleep(touch_wait)
                        return True
                    _res_pos.append((_str, (_x + 1091, _y + 150)))
                    _str = ''
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f'F_{find_info}_没找到_all{_res_pos}')
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f'F_{find_info}_没找到')
        return False, []

    def find_pd_num(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[157:581, 239:1049]
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
                    self.dev.touch((_x + 239, _y + 157))
                if touch_wait > 0:
                    time.sleep(touch_wait)
                if t_log:
                    self.sn.log_tab(self.mnq_name, f"T_{find_info}_xy{(_x + 239, _y + 157)}")
                return True
            _res_pos.append((_pd_num, (_x + 239, _y + 157)))
            _pd_num = ''
        print(_res_pos)
        return False

    def check_ui(self, ui_info):
        x, y, x1, y1, ui_name = ui_info
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        _crop_img = self._img[y:y1, x:x1]
        _crop_img = cv2.resize(_crop_img, (128, 72))
        img1 = cv2.threshold(_crop_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        # img_closed = cv2.morphologyEx(img1, cv2.MORPH_CLOSE, sqKernel)
        # for _t in OpenCvEnumG.TEMP.keys():
        _cmp_ui = OpenCvEnumG.TEMP[ui_name]
        res = cv2.matchTemplate(
            img1,
            _cmp_ui, method=cv2.TM_CCOEFF_NORMED)
        if numpy.any(res > 0.9):
            print(f"res:{ui_name}_")
            return True
        return False

    def find_mr_task(self, find_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[158:580, 38:1268]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        _img1 = cv2.threshold(_crop_img.copy(), 250, 255, cv2.THRESH_TOZERO)[1]  # 转换为二值图像, thresh=63
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont, hierarchy = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 1.5 and h1 > 20:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        for _num in range(len(ori_list)):
            for _t in OpenCvEnumG.TEMP.keys():
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[_num][0], (72, 128)),
                    numpy.load(OpenCvEnumG.TEMP[_t]), method=cv2.TM_CCOEFF_NORMED)
                if numpy.any(_re > 0.7):
                    if _t == find_info:
                        if clicked:
                            self.dev.touch((ori_list[_num][-1][0] + 38, ori_list[_num][-1][-1] + 158))
                        if t_log:
                            self.sn.log_tab.emit(self.mnq_name,
                                                 f'T_{_t}_xy{ori_list[_num][-1][0] + 38}_{ori_list[_num][-1][-1] + 158}')
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
        _cmp_img = OpenCvEnumG.MENU[find_info]
        for _num in range(len(ori_list)):
            # for _t in OpenCvEnumG.MENU.keys():
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_num][0], (72, 128)),
                numpy.load(_cmp_img), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.7):
                # if _t == find_info:
                if clicked:
                    self.dev.touch((ori_list[_num][-1][0] + 800, ori_list[_num][-1][-1] + 62))
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name,
                                         f'T_{find_info}_xy{ori_list[_num][-1][0] + 800}_{ori_list[_num][-1][-1] + 62}')
                if touch_wait > 0:
                    time.sleep(touch_wait)
                return True
        return False

    def check_num(self, num_type, t_log=GlobalEnumG.TestLog):
        """检查战力-等级"""
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        if num_type == 1:
            # 战力
            _crop_img = self._img[64:91, 18:143]
        else:
            # 等级
            _crop_img = self._img[6:29, 33:98]
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 转换为二值图像, thresh=63
        res_cont, hierarchy = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 0.5 and h1 > 10:
                # print(ar, x, y, w1, h1)
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        _str_num = ''
        for row in range(len(ori_list)):
            for _t in OpenCvEnumG.BATNUM.keys():
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[row][0], (72, 128)),
                    numpy.load(OpenCvEnumG.BATNUM[_t]), method=cv2.TM_CCOEFF_NORMED)
                print(f're{_re}_{row}')
                if numpy.any(_re > 0.75):
                    _str_num = _str_num + _t
        if t_log:
            self.sn.log_tab.emit(self.mnq_name, f"{_str_num}")
        return _str_num

    def gold_num(self, num_type):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        if num_type == 1:
            # 金币
            _crop_img = self._img[371:409, 690:907]
        else:
            # 红币
            _crop_img = self._img[372:408, 401:631]
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 转换为二值图像, thresh=63
        res_cont, hierarchy = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 20 > h1 > 10:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        _gold_num = ''
        for row in range(len(ori_list)):
            for _t in OpenCvEnumG.GOLD_NUM.keys():
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[row][0], (72, 128)),
                    numpy.load(OpenCvEnumG.GOLD_NUM[_t]), method=cv2.TM_CCOEFF_NORMED)
                if numpy.any(_re > 0.8):
                    _gold_num = _gold_num + _t
        return _gold_num

    def check_hp_mp(self):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[365:389, 1127:1262]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 转换为二值图像, thresh=63
        img_closed = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont, hierarchy = cv2.findContours(img_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 1.5 and w1 > 15:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_res(ori_list, OpenCvEnumG.HP_MP)

    def check_ys_num(self):
        """检查药水购买数量"""
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[624:667, 717:823]
        _img1 = cv2.threshold(_crop_img.copy(), 140, 255, cv2.THRESH_BINARY_INV)[1]  # 转换为二值图像, thresh=63
        res_cont = cv2.findContours(_img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 0.8 > ar > 0.4 and h1 > 15:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_res(ori_list, OpenCvEnumG.YS_NUM)

    def check_map(self, map_name):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[624:667, 717:823]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        _img1 = cv2.threshold(_crop_img.copy(), 125, 255, cv2.THRESH_BINARY_INV)[1]  # 转换为二值图像, thresh=63
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_GRADIENT, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 1 and h1 > 15:
                ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_res(ori_list, OpenCvEnumG.HP_MP)

    def check_xt_map(self, map_name):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _cmp_res = OpenCvEnumG.XT_MAP_EX[map_name]
        _crop_img = self._img[97:145, 910:1279]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[
            1]  # 转换为二值图像, thresh=63
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 5 and h1 > 15:
                ori_list.append([_img2[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_text(ori_list, _cmp_res)

    def check_map_ex(self, map_name):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _cmp_res = OpenCvEnumG.XT_MAP_EX[map_name]
        _crop_img = self._img[91:118, 19:202]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        _img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY)[
            1]  # 转换为二值图像
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if ar > 3 and w1 > 50:
                ori_list.append([_img2[y:y + h1, x:x + w1], (x, y)])
        ori_list.reverse()
        return self._match_text(ori_list, _cmp_res)

    def back_ksdy(self):
        self._img = self.dev.snapshot()
        self._img = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        # _crop_img = self._img[y:y1, x:x1]
        _crop_img = self._img[167:688, 251:1035]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        _img1 = cv2.threshold(_crop_img.copy(), 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[
            1]  # 转换为二值图像
        _img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
        res_cont = cv2.findContours(_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        ori_list = []
        for cnt in res_cont:
            x, y, w1, h1 = cv2.boundingRect(cnt)
            ar = w1 / float(h1)
            if 10 > ar > 5 and w1 > 80:
                print(ar, x, y, w1, h1)
                ori_list.append([_img2[y:y + h1, x:x + w1], (x, y)])
        for _row in range(len(ori_list)):
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_row][0], (72, 128)),
                numpy.load(OT.npypath('back_ksdy')), method=cv2.TM_CCOEFF_NORMED)
            print(_re)
            if numpy.any(_re > 0.9):
                self.dev.touch((ori_list[_row][1][0]+251,ori_list[_row][1][-1]+167))
                return True
        return False
    @staticmethod
    def _match_res(ori_list, enum_res):
        """匹配数字"""
        _bat_num = ''
        for row in range(len(ori_list)):
            for _t in enum_res.keys():
                _re = cv2.matchTemplate(
                    cv2.resize(ori_list[row][0], (72, 128)),
                    numpy.load(enum_res[_t]), method=cv2.TM_CCOEFF_NORMED)
                if numpy.any(_re > 0.9):
                    _bat_num = _bat_num + _t
        return _bat_num

    @staticmethod
    def _match_text(ori_list, cmp_res):
        for _row in range(len(ori_list)):
            _re = cv2.matchTemplate(
                cv2.resize(ori_list[_row][0], (72, 128)),
                numpy.load(cmp_res), method=cv2.TM_CCOEFF_NORMED)
            if numpy.any(_re > 0.89):
                return True
            print(_re)
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
    def crop_image_find(self, area_temp, clicked=True, timeout=0.1, touch_wait=GlobalEnumG.TouchWaitTime,
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

    def find_all_pos(self, temp, timeout=GlobalEnumG.FindImgTimeOut):
        img = temp[-1]
        pos_list = []
        self._img = self.dev.snapshot()
        if self._img is not None:
            match_pos = img.match_all_in(self._img)
            if not match_pos:
                return False, (0, 0)
            for pos in match_pos:
                res = pos['result']
                pos_list.append(res)
            return True, pos_list
        return False, (0, 0)

    def air_loop_find(self, temp, clicked=True, timeout=GlobalEnumG.FindImgTimeOut,
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

    def air_touch(self, touch_xy, duration=0.2, touch_wait=0):
        self.dev.touch(touch_xy, duration=duration)
        if touch_wait > 0:
            time.sleep(touch_wait)

    def air_swipe(self, start_xy, end_xy, swipe_wait=0):
        self.dev.swipe(start_xy, end_xy)
        if swipe_wait > 0:
            time.sleep(swipe_wait)

    def move_turn(self, turn, k_time):
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


class CnOcrTool:
    def __init__(self):
        self.dev = None
        self.cn_ocr = None
        self._img = None
        self.sn = None
        self.mnq_name = None

    def ocr_find(self, ocr_list, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog,
                 get_pos=False):
        """
        范围查找文字，返回坐标
        :param ocr_list:查找文字范围和文字
        :param clicked: 是否点击
        :param touch_wait: 点击后等待时长
        :return: 查找结果
        """
        x1, y1, x2, y2 = ocr_list[0]
        self._img = self.dev.snapshot()
        if self._img is not None:
            img_fp = aircv.crop_image(self._img, (x1, y1, x2, y2))
            t1 = time.time()
            self.cn_ocr[-1].acquire()
            out = self.cn_ocr[0].ocr(img_fp)
            self.cn_ocr[-1].release()
            if len(out) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, f"f_{ocr_list}_time:{time.time() - t1}")
                return False
            for i in range(len(out)):
                ntext = out[i]['text']
                if t_log:
                    self.sn.log_tab.emit(self.mnq_name, ntext)
                if ocr_list[-1] in ntext:
                    npar = out[i]['position']
                    ls = npar.tolist()
                    lx = int((ls[-2][0] + ls[0][0]) / 2)
                    ly = int((ls[-2][-1] + ls[0][-1]) / 2)
                    if clicked:
                        self.dev.touch((lx + x1, ly + y1))
                        if touch_wait > 0:
                            time.sleep(touch_wait)
                    if t_log:
                        self.sn.log_tab.emit(self.mnq_name, f"T_{ocr_list}_time:{time.time() - t1}")
                    time.sleep(touch_wait)
                    if get_pos:
                        return lx + x1, ly + y1
                    return True
        time.sleep(touch_wait / 2)
        return False

    def get_all_text(self, ocr_list):
        find_pos_list = []
        x1, y1, x2, y2 = ocr_list[0]
        self._img = self.dev.snapshot()
        if self._img is not None:
            self.cn_ocr[-1].acquire()
            img_fp = aircv.crop_image(self._img, (x1, y1, x2, y2))
            out = self.cn_ocr[0].ocr(img_fp)
            self.cn_ocr[-1].release()
            if len(out) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                return find_pos_list
            for i in range(len(out)):
                ntext = out[i]['text']
                if ocr_list[-1] in ntext:
                    npar = out[i]['position']
                    ls = npar.tolist()
                    lx = int((ls[-2][0] + ls[0][0]) / 2)
                    ly = int((ls[-2][-1] + ls[0][-1]) / 2)
                    find_pos_list.append((lx + x1, ly + y1))
        time.sleep(GlobalEnumG.WaitTime)
        return find_pos_list

    def get_ocrres(self, area, t_log=GlobalEnumG.TestLog):
        """
        范围查找文字，返回坐标
        :param ocr_list:查找文字范围和文字
        :return: 查找结果
        """
        self._img = self.dev.snapshot()
        if self._img is not None:
            img_fp = aircv.crop_image(self._img, area)
            self.cn_ocr[-1].acquire()
            out = self.cn_ocr[0].ocr_for_single_line(img_fp)
            self.cn_ocr[-1].release()
            if len(out) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                return ''
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"get_ocrres:{area}_ntext:{out['text']}")
            time.sleep(GlobalEnumG.WaitTime)
            return out['text']
        return ''

    def get_roleinfo(self, area_list, t_log=GlobalEnumG.TestLog):
        self._img = self.dev.snapshot()
        img_area = []
        out_list = []
        ntext_list = []
        if self._img is not None:
            for _a in area_list:
                img_fp = aircv.crop_image(self._img, _a)
                img_area.append(img_fp)
            self.cn_ocr[-1].acquire()
            for _img in img_area:
                out = self.cn_ocr[0].ocr(_img)
                if len(out) > 0:
                    out_list.append(out)
            self.cn_ocr[-1].release()
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"get_roleinfo:out_{out_list}")
            if len(out_list) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                return False
            for _o in out_list:
                ntext = ''.join(filter(lambda x: x.isdigit(), _o[0]['text']))
                try:
                    ntext_list.append(int(ntext))
                except ValueError:
                    ntext_list.append(0)
            time.sleep(GlobalEnumG.WaitTime)
            if t_log:
                self.sn.log_tab.emit(self.mnq_name, f"get_roleinfo:ntext_list_{ntext_list}")
            return ntext_list
        return ntext_list


if __name__ == '__main__':
    # img_fp = r'D:\DzAutoUi\Res\img\21.bmp'
    # res, dev = DevicesConnect('emulator-5554').connect_device()
    res2, dev2 = DevicesConnect('127.0.0.1:5555').connect_device()
    # print(res2, dev2)
    # cv2.setNumThreads(1)
    # cv2.ocl.setUseOpenCL(False)
    # torch.set_num_threads(1)
    # torch.no_grad()
    # torch.set_grad_enabled(False)
    cnocr = CnOcr(rec_model_name='densenet_lite_136-fc',
                  det_model_name='db_shufflenet_v2_small')  # 'ch_PP-OCRv3_det')  # ch_PP-OCRv3繁体中文匹配模型
    ocr_lock = ThreadTools.new_lock()
    cn_ocr = [cnocr, ocr_lock]
    # img=G.DEVICE.snapshot()
    # aircv.imwrite(r'D:\DzAutoUi\Res\img\21.png',img)
    # loop_find(img_fp)
    c = CnOcrTool()
    a = AirImgTools()
    o = OpenCvTools()
    c.dev = dev2
    a.dev = dev2
    o.dev = dev2
    c.cn_ocr = cn_ocr
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
    r = o.check_num(2)
    # if not r:
    print(r)
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
