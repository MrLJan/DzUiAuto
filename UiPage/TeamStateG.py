# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG
from UiPage.BasePage import BasePageG


class TeamStateG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(TeamStateG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def check_team_state(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        task_id = kwargs['任务id']
        if task_id in ['3','4']:
            if not self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                if task_id == '3':
                    select_queue.put_queue('CheckXT')
                else:
                    select_queue.put_queue('CheckYT')
        if self.air_loop_find(ImgEnumG.GAME_ICON, False):
            select_queue.put_queue('Login')
        if self.air_loop_find(ImgEnumG.GAME_ICON, False):
            select_queue.put_queue('FuHuo')
        if self.ocr_find(ImgEnumG.HP_NULL_OCR) or self.ocr_find(ImgEnumG.MP_NULL_OCR):
            select_queue.put_queue('BuyY')
        if self.ocr_find(ImgEnumG.BAG_FULL):
            select_queue.put_queue('BagSell')

    def check_xt(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        _MAP = False
        _TEAM = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if _MAP and _TEAM:
                select_queue.task_over('CheckXT')
                return -1
            if not _TEAM:
                if self.choose_xt_team():
                    _TEAM = True
            if not _MAP:
                res_map, res_pd = self.check_map_pd(**kwargs)
                if not res_map:
                    if self.choose_xt_map():
                        _MAP = True
        return -1

    def check_yt(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        team_queue = kwargs['野图设置']['队伍队列']
        _MAP = False
        _PD = False
        _TEAM = False
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if _MAP and _TEAM and _PD:
                select_queue.task_over('CheckYT')
                return -1
            if not _MAP or not _PD:
                res_map, res_pd = self.check_map_pd(**kwargs)
                if not res_map:
                    if self.choose_yt_map():
                        _MAP = True
                if not res_pd:
                    if self.choose_pindao():
                        _PD = True
            else:
                if not _TEAM:
                    if team_queue.queue.empty():
                        team_queue.put_queue(kwargs['设备名称'])
                        if self.creat_team(**kwargs):
                            _TEAM = True
                        else:
                            team_queue.task_over(kwargs['设备名称'])
                    else:
                        if self.jion_team(**kwargs):
                            team_queue.put_queue(kwargs['设备名称'])
                            _TEAM = True
        return -1

    def check_map_pd(self, **kwargs):
        s_time = time.time()
        _MAP = False  # 是否在正确地图
        _PD = False  # 是否在正确频道
        _FLAG = False  # 检查是否完成
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut / 2:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _FLAG:
                    return _MAP, _PD
                self.air_touch((99, 99), duration=2)
            elif self.ocr_find(ImgEnumG.MAP_UI_OCR):
                if _FLAG:
                    self.air_loop_find(ImgEnumG.MR_TIP_CLOSE)
                else:
                    if kwargs['任务id'] == '3':
                        _PD = True
                        xt_num_now = self.get_num((932, 105, 1236, 141))
                        map_name = self.get_num((932, 105, 1236, 141))
                        xt_name = kwargs['地图名']
                        xt_num = kwargs['战斗数据']['地图识别'][-1]
                        if xt_num_now == xt_num and xt_name in map_name:
                            _MAP = True
                        _FLAG = True
                    else:
                        pd_num_now = self.get_num((874, 23, 1068, 63))
                        map_name = self.get_num((932, 105, 1236, 141))
                        yt_name = kwargs['地图名']
                        pd_num = kwargs['野图设置']['队伍频道']
                        if pd_num_now == pd_num:
                            _PD = True
                        if yt_name in map_name:
                            _MAP = True
                        _FLAG = True
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 4:
                    if not self.check_close():
                        return False
        return _MAP, _PD

    def choose_xt_map(self, xt_map=None):
        _times = 0
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.MR_MENU)
            if self.crop_image_find(ImgEnumG.UI_SET, False):  # 菜单界面
                self.ocr_find(ImgEnumG.MR_MENU_KSNR, True)
            if self.ocr_find(ImgEnumG.MR_UI_OCR):
                if not self.ocr_find([ImgEnumG.MR_AREA, '星力'], True):  # 星力战场
                    self.air_swipe((900, 438), (384, 438), 3)
            if self.ocr_find(ImgEnumG.MR_XLZC_OCR):
                if self.ocr_find([(1104, 164, 1158, 583), str(xt_map[-1])], True):
                    self.get_rgb(1117, 658, 'EE7047', True)
                else:
                    if _times > 2:
                        self.air_swipe((1092, 528), (1092, 298))
                    else:
                        self.air_swipe((1092, 298), (1092, 528))
            if self.ocr_find(ImgEnumG.XT_MOVE_QR):
                if self.get_rgb(699, 523, 'EE7047', True):
                    self.air_loop_find(ImgEnumG.UI_CLOSE)
                    while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
                        if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                            if self.crop_image_find(ImgEnumG.XT_FLAG, False):
                                if self.ocr_find(xt_map[0]):
                                    return True
                            return False
                        else:
                            self.air_loop_find(ImgEnumG.UI_CLOSE)
                    return False
            else:
                if time.time() - s_time > GlobalEnumG.UiCheckTimeOut / 2:
                    if not self.check_close():
                        return False
        return False

    def choose_yt_map(self, yt_map=None):
        s_time = time.time()
        MOVE_FLAG = False
        MOVE_FLAG2 = False
        WAIT_XL_TIMES = 0
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if MOVE_FLAG:
                    if self.ocr_find(yt_map[0]):
                        return True
                    self.choose_xt_map(yt_map)
                    MOVE_FLAG = False
                elif MOVE_FLAG2:
                    if self.ocr_find(ImgEnumG.MAP_XL_OCR):
                        self.time_sleep(5)
                        WAIT_XL_TIMES += 1
                    else:
                        if self.ocr_find(yt_map[0]):
                            return True
                        if WAIT_XL_TIMES > 10:
                            MOVE_FLAG2 = False
                else:
                    self.air_touch((99, 99))
            elif self.ocr_find(ImgEnumG.MAP_UI_OCR):
                if MOVE_FLAG:
                    self.air_loop_find(ImgEnumG.UI_CLOSE)
                else:
                    if self.ocr_find([(15, 88, 145, 705), yt_map[1]], True):
                        self.air_touch((718, 248), duration=2)
                        self.air_touch((248, 480), duration=2)
                    self.air_swipe((81, 470), (81, 251))
            elif self.ocr_find([(1003, 97, 1160, 142), yt_map[2]]):
                if not self.get_rgb(1132, 656, 'EE7047', True):
                    self.get_rgb(933, 657, '4C87AF', True)
            elif self.ocr_find(ImgEnumG.MAP_MOV_OCR):
                if self.get_rgb(713, 524, '4C87AF', True):
                    MOVE_FLAG = True
                if self.get_rgb(713, 524, 'EE7047', True):
                    MOVE_FLAG2 = True
            else:
                if not self.check_close():
                    return False

    def choose_xt_team(self):
        """星图找队伍"""
        s_time = time.time()
        WAIT_TIMES = 0  # 等待组队次数 1次10秒
        C_PINDAO = False  # 更换频道
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if C_PINDAO:
                    if self.change_pindao():
                        WAIT_TIMES = 0
                        C_PINDAO = False
                else:
                    self.crop_image_find(ImgEnumG.TEAM_TAB)
                    self.crop_image_find(ImgEnumG.TEAM_ZDJR)
                    self.crop_image_find(ImgEnumG.TEAM_ZDJR_QR)
            if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                pos = self.crop_image_find(ImgEnumG.EXIT_TEAM, False, get_pos=True)
                if pos[-1] < 270:
                    self.air_touch((pos[1], pos[-1]))  # 人数低于3人退队伍
                    self.get_rgb(724, 523, 'EE7047', True)
                else:
                    return True
            if self.ocr_find(ImgEnumG.TEAM_ZDJR_OCR):
                if WAIT_TIMES > 3:
                    self.air_touch((147, 350))
                    C_PINDAO = True
                else:
                    self.crop_image_find(ImgEnumG.TEAM_ZDJR_QR)
                    self.time_sleep(10)
                    WAIT_TIMES += 1
        return False

    def change_pindao(self, *args, **kwargs):
        """更换频道"""
        s_time = time.time()
        _FLAG = False
        while time.time() - s_time < 300:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _FLAG:
                    return True
                self.air_touch((99, 99), duration=2)
            elif self.ocr_find(ImgEnumG.PD_BG_OCR):
                _FLAG = False
                pindao_list = [(340, 314), (332, 533), (954, 317), (952, 529)]  # 频道坐标
                i = random.randint(0, 3)
                _pos = pindao_list[i]
                for _ in range(i):
                    self.air_swipe((639, 510), (639, 316))
                self.air_touch(_pos, duration=1)
                if self.get_rgb(549, 628, 'EE7047', True):
                    _FLAG = True
            elif self.ocr_find(ImgEnumG.MAP_UI_OCR):
                self.crop_image_find(ImgEnumG.PD_BG)
            else:
                if time.time() - s_time > 150:
                    if not self.check_close():
                        return False
        return False

    def choose_pindao(self, *args, **kwargs):
        s_time = time.time()
        _FIND_PD = kwargs['pd_num']
        _FIND_PD_F = kwargs['pd_num_f']
        _PD_POS = None
        _FIND = False
        _FLAG = False
        _HD_TIMES = 0
        while time.time() - s_time < 300:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                if _FLAG:
                    return True
                self.air_touch((99, 99), duration=2)
            elif self.ocr_find(ImgEnumG.PD_BG_OCR):
                _FLAG = False
                if not _FIND:
                    pindao_list = self.get_all_ocr((228, 153, 1048, 589))  # 频道坐标
                    for _pos in pindao_list:
                        _pd = ''.join(filter(lambda x: x.isdigit(), _pos[0]))
                        if _pd == _FIND_PD:
                            _PD_POS = _pos[1]
                            _FIND = True
                    if _FIND:
                        self.air_touch(_PD_POS, duration=1)
                        if self.get_rgb(549, 628, 'EE7047', True):
                            _FLAG = True
                    else:
                        if _HD_TIMES > 30:
                            _FIND_PD = _FIND_PD_F
                            _HD_TIMES = 0
                        if _HD_TIMES > 10:
                            self.air_swipe((639, 316), (639, 510))
                        else:
                            self.air_swipe((639, 510), (639, 316))
                            _HD_TIMES += 1
                else:
                    self.air_touch(_PD_POS, duration=1)
                    if self.get_rgb(549, 628, 'EE7047', True):
                        _FLAG = True
            elif self.ocr_find(ImgEnumG.MAP_UI_OCR):
                self.crop_image_find(ImgEnumG.PD_BG)
            else:
                if time.time() - s_time > 150:
                    if not self.check_close():
                        return False
        return False

    def creat_team(self, **kwargs):
        s_time = time.time()
        team_pwd = kwargs['野图设置']['组队密码']
        _PUT_PWD = False  # 输入密码标记
        _C_FLAG = False  # 组队成功标记
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.TEAM_TAB)
                if _C_FLAG:
                    if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                        return True
                    _C_FLAG = False
                else:
                    self.crop_image_find(ImgEnumG.TEAM_CLDW)
            elif self.ocr_find(ImgEnumG.TEAM_CLDW_OCR):
                if self.get_rgb(102, 521, '3B759B'):
                    self.get_rgb(563, 629, 'EE7047', True)
                else:
                    self.air_touch((102, 521), duration=2)
                    self.air_touch((942, 261))
            elif self.ocr_find(ImgEnumG.TEAM_PWD_OCR):
                if not _PUT_PWD:
                    for pwd in team_pwd:
                        self.air_touch(GlobalEnumG.PWD_POS[pwd], duration=2)
                    _PUT_PWD = True
                else:
                    put_res = self.get_ocrres((597, 212, 681, 246))
                    if put_res == team_pwd:
                        if self.air_loop_find(ImgEnumG.UI_QR):
                            _C_FLAG = True
                    else:
                        self.air_loop_find(ImgEnumG.UI_CLOSE)
                        _PUT_PWD = False
            else:
                if not self.check_close():
                    return False

        return False

    def jion_team(self, team_pwd):
        s_time = time.time()
        _pos_list = []
        _PUT_PWD = False
        _C_FLAG = False
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.crop_image_find(ImgEnumG.INGAME_FLAG2, False):
                self.crop_image_find(ImgEnumG.TEAM_TAB)
                self.crop_image_find(ImgEnumG.TEAM_XZDW)
                if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                    return True
            elif self.ocr_find(ImgEnumG.TEAM_PWD_OCR):
                if _C_FLAG:
                    if len(_pos_list) > 0:
                        _pos_list.pop(0)
                    self.air_loop_find(ImgEnumG.UI_CLOSE)
                if not _PUT_PWD:
                    for pwd in team_pwd:
                        self.air_touch(GlobalEnumG.PWD_POS[pwd], duration=1)
                    _PUT_PWD = True
                else:
                    put_res = self.get_ocrres((597, 212, 681, 246))
                    if put_res == team_pwd:
                        if self.air_loop_find(ImgEnumG.UI_QR):
                            _C_FLAG = True
                    else:
                        self.air_loop_find(ImgEnumG.UI_CLOSE)
                        _PUT_PWD = False
            elif self.ocr_find(ImgEnumG.MAP_UI_OCR):
                if self.ocr_find(ImgEnumG.JION_TEAM_OCR):
                    self.crop_image_find(ImgEnumG.MR_TIP_CLOSE)
                    return False  # 无队伍需要创建
                if len(_pos_list) == 0:
                    team_pos = self.find_all_pos(ImgEnumG.PWD_TEAM)
                    if team_pos[0]:
                        for pos in team_pos[-1]:
                            _pos_list.append(pos)
                    else:
                        return False
                else:
                    self.air_touch(_pos_list[0])
                    if self.get_rgb(1125, 647, 'C3C3C3'):
                        _pos_list.pop(0)
                        if len(_pos_list) > 0:
                            self.air_touch(_pos_list[-1])
                        else:
                            return False
                    self.get_rgb(1125, 647, 'EE7047', True)
        return False
