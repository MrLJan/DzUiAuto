# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG, BatEnumG, MulColorEnumG, WorldEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import FuHuoRoleErr, BuyYErr, NotInGameErr


class TeamStateG(BasePageG):
    def __init__(self, devinfo, sn):
        super(TeamStateG, self).__init__()
        self.dev, self.mnq_name = devinfo
        self.sn = sn
        self.ksnr_pos = (0, 0)

    def check_team_state(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        task_id = kwargs['任务id']
        gold = kwargs['角色信息']['金币']
        if int(gold) < 1:
            select_queue.put_queue('CheckRole')
        self.sn.log_tab.emit(self.mnq_name, r"检查队伍状态")
        self.sn.table_value.emit(self.mnq_name, 8, r"检查队伍状态")
        if task_id in ['3', '4', '99']:
            # if not self.pic_find(ImgEnumG.EXIT_TEAM, False):
            if task_id in ['3', '99']:
                select_queue.put_queue('CheckXT')
            else:
                select_queue.put_queue('CheckYT')
        if self.pic_find(ImgEnumG.GAME_ICON, False):
            select_queue.put_queue('Login')
        if self.pic_find(ImgEnumG.CZ_FUHUO, False):
            select_queue.put_queue('FuHuo')
            raise FuHuoRoleErr
        _res_hpmp = self.check_hp_mp()
        if _res_hpmp != '':
            if 'HP' in _res_hpmp:
                self.sn.log_tab.emit(self.mnq_name, r"检查HP")
                select_queue.put_queue('BuyY')
                raise BuyYErr
            if use_mp:
                if 'MP' in _res_hpmp:
                    self.sn.log_tab.emit(self.mnq_name, r"检查MP")
                    select_queue.put_queue('BuyY')
                    raise BuyYErr
        if self.pic_find(ImgEnumG.BAG_MAX_IMG, False):
            self.sn.log_tab.emit(self.mnq_name, r"检查背包状态")
            select_queue.put_queue('BagSell')
        self.skip_new()
        return 2

    def check_xt(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        auto_choose = kwargs['托管模式']
        if auto_choose:
            kwargs = self.get_mapdata(**kwargs)
        map_data = kwargs['战斗数据']['地图识别']
        _MAP = False
        _TEAM = False
        self.sn.log_tab.emit(self.mnq_name, r"检查星图状态")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _MAP and _TEAM:
                    select_queue.task_over('CheckXT')
                    return -1
                if not _MAP:
                    res_map, res_pd = self.check_in_map(**kwargs)
                    if not res_map:
                        self.sn.log_tab.emit(self.mnq_name, r"当前地图不正确")
                        if self.choose_xt_map(map_data):
                            _MAP = True
                        else:
                            return -1
                    else:
                        _MAP = True
                if not _TEAM:
                    self.sn.log_tab.emit(self.mnq_name, r"当前没有队伍")
                    if self.choose_xt_team(**kwargs):
                        _TEAM = True
                    else:
                        return -1
            else:
                self.check_close()
        return -1

    def check_yt(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        team_queue = kwargs['野图设置']['队伍队列']
        team_event = kwargs['野图设置']['队伍锁']
        map_data = kwargs['战斗数据']['地图识别']
        _MAP = False
        _PD = False
        _TEAM = False
        _WAIT_CREAT = 0
        self.sn.log_tab.emit(self.mnq_name, r"检查野图状态")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _MAP and _TEAM and _PD:
                    select_queue.task_over('CheckYT')
                    return -1
                if self.pic_find(ImgEnumG.GAME_ICON, False):
                    select_queue.put_queue('Login')
                    return -1
                if not _MAP:
                    res_map = self.map_ex(map_data[-1], 0)
                    if self.find_color(MulColorEnumG.XT_FLAG) or not res_map:
                        self.sn.log_tab.emit(self.mnq_name, r"当前地图不正确")
                        if self.choose_yt_map(map_data):
                            _MAP = True
                    else:
                        _MAP = True
                if not _PD:
                    if self.choose_pindao(**kwargs):
                        _PD = True
                else:
                    if not _TEAM:
                        for i in range(2):
                            if self.pic_find(ImgEnumG.EXIT_TEAM, False):
                                team_num = team_queue.queue.qsize() - 1
                                pos = self.pic_find(ImgEnumG.EXIT_TEAM, False, get_pos=True)
                                if pos[-1] > (180 + team_num * 35) and team_num >= 0:
                                    self.touch((pos[1], pos[-1]), touch_wait=1)  # 人数低于3人退队伍
                                    if self.cmp_rgb(RgbEnumG.EXIT_TEAM, True):
                                        self.sn.log_tab.emit(self.mnq_name, r"不在设定队伍中")
                                else:
                                    team_queue.put_queue(kwargs['设备名称'])
                                    _TEAM = True
                            else:
                                self.pic_find(ImgEnumG.TEAM_TAB)
                                if self.pic_find(ImgEnumG.TEAM_XZDW, False):
                                    _TEAM = False
                                    if team_queue.check_queue(kwargs['设备名称']):
                                        team_queue.task_over(kwargs['设备名称'])
                        if team_event.is_set():
                            for wt in range(6):
                                if not team_event.is_set():
                                    break
                                if _WAIT_CREAT > 5:
                                    if team_queue.queue.empty():
                                        team_event.clear()
                                        self.sn.log_tab.emit(self.mnq_name, "等待过长,自行创建")
                                else:
                                    self.sn.log_tab.emit(self.mnq_name, "已经有窗口在创建队伍,等待创建")
                                    self.time_sleep(10)
                                    _WAIT_CREAT += 1
                        else:
                            if team_queue.queue.empty():
                                self.sn.log_tab.emit(self.mnq_name, "没有队伍,本窗口尝试创建")
                                team_event.set()
                                if self.creat_team(**kwargs):
                                    self.sn.log_tab.emit(self.mnq_name, "创建队伍-成功")
                                    team_queue.put_queue(kwargs['设备名称'])
                                    _TEAM = True
                                else:
                                    self.sn.log_tab.emit(self.mnq_name, "创建队伍-失败")
                                team_event.clear()
                            else:
                                if not _TEAM:
                                    if team_queue.queue.qsize() == 1:
                                        if team_queue.check_queue(kwargs['设备名称']):
                                            self.sn.log_tab.emit(self.mnq_name, "没有队伍,本窗口尝试创建")
                                            team_event.set()
                                            if self.creat_team(**kwargs):
                                                self.sn.log_tab.emit(self.mnq_name, "创建队伍-成功")
                                                team_queue.put_queue(kwargs['设备名称'])
                                                _TEAM = True
                                            else:
                                                self.sn.log_tab.emit(self.mnq_name, "创建队伍-失败")
                                            team_event.clear()
                                        else:
                                            if not team_event.is_set():
                                                if self.jion_team(**kwargs):
                                                    self.sn.log_tab.emit(self.mnq_name, "加入队伍-成功")
                                                    team_queue.put_queue(kwargs['设备名称'])
                                                    _TEAM = True
                                                else:
                                                    self.sn.log_tab.emit(self.mnq_name, "加入队伍-失败")
                                    elif self.jion_team(**kwargs):
                                        self.sn.log_tab.emit(self.mnq_name, "加入队伍-成功")
                                        team_queue.put_queue(kwargs['设备名称'])
                                        _TEAM = True
                                    else:
                                        self.sn.log_tab.emit(self.mnq_name, "加入队伍-失败")
            else:
                self.check_close()
        return -1

    def check_in_map(self, **kwargs):
        s_time = time.time()
        _EX_FLAG = False  # 外部检查地图
        _MAP = False  # 是否在正确地图
        _PD = False  # 是否在正确频道
        _FLAG = False  # 检查是否完成
        auto_choose = kwargs['托管模式']
        if auto_choose:
            kwargs = self.get_mapdata(**kwargs)
        _MAP_NAME = BatEnumG.MAP_OCR[kwargs['地图名']][-1]
        _ID = kwargs['任务id']
        self.sn.log_tab.emit(self.mnq_name, r"检查地图、频道")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut / 2:
            if self.pic_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            if self.pic_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
            if self.find_color(MulColorEnumG.IGAME):
                return self.map_ex(_MAP_NAME), True
            else:
                self.check_close()

    def choose_xt_map(self, map_data=None):
        _times = 0
        s_time = time.time()
        _M_OVER = False
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"选择星图地图")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _M_OVER:
                    return True
                if self.pic_find(ImgEnumG.EXIT_TEAM, False):
                    pos = self.pic_find(ImgEnumG.EXIT_TEAM, False, get_pos=True)
                    if pos[-1] < 420:
                        self.touch((pos[1], pos[-1]), touch_wait=1)  # 人数低于3人退队伍
                        if self.cmp_rgb(RgbEnumG.EXIT_TEAM, True):
                            self.sn.log_tab.emit(self.mnq_name, r"退出已有队伍")
                self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
            elif self.word_find(WorldEnumG.SET_BTN):  # 菜单界面
                self.enum_find('快速内容', True)
            elif self.cmp_rgb(RgbEnumG.KSDY):  # 星力战场
                if not self.find_mr_task('星力战场', True):
                    if _SWIPE_TIMES < 3:
                        self.dm_swipe((925, 432), (400, 432), swipe_wait=1)
                    else:
                        if _SWIPE_TIMES > 6:
                            _SWIPE_TIMES = 0
                        self.dm_swipe((400, 432), (925, 432), swipe_wait=1)
                    _SWIPE_TIMES += 1
            elif self.cmp_rgb(RgbEnumG.XLZC_YDQR, True):
                self.back()
                while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
                    if self.find_color(MulColorEnumG.IGAME):
                        self.cmp_rgb(RgbEnumG.XLZC_YDOK, True)  # 移动完成 确认
                        if self.mul_color(MulColorEnumG.XT_STAR):
                            if self.find_xt_num(map_data[0], True):
                                return True
                        return False
                    else:
                        self.check_close()
                return False
            elif self.cmp_rgb(RgbEnumG.XLZC):
                if self.cmp_rgb(RgbEnumG.XLZC_YD, True):
                    pass
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"查找星图")
                    _res = self.find_xt_num(str(map_data[0]), True)
                    if _res:
                        self.sn.log_tab.emit(self.mnq_name, r"找到星图")
                        self.cmp_rgb(RgbEnumG.ENUM_BTN, True)
                        self.cmp_rgb(RgbEnumG.XLZC_YD, True)
                        _M_OVER = True
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"星图不在当前界面")
                        if self.find_xt_num('194'):
                            _times = 0
                        elif self.find_xt_num('10'):
                            self.sn.log_tab.emit(self.mnq_name, r"已滑到顶端,向下滑")
                            _times = 7
                        if _times > 6:
                            self.dm_swipe((1092, 528), (1092, 298), swipe_wait=1)  # 下滑
                        else:
                            self.dm_swipe((1092, 298), (1092, 528), swipe_wait=1)  # 上滑
                        _times += 1
            else:
                self.check_close()
        return False

    def choose_yt_map(self, map_data=None):
        s_time = time.time()
        MOVE_FLAG = False  # 瞬间移动失败
        MOVE_FLAG2 = False  # 寻路
        _USE_MOVE = False  # 石头足够使用石头
        _C_FLAG = False  # 大地图选择
        WAIT_XL_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"选择野图地图")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):  # 移动完成
                self.cmp_rgb(RgbEnumG.QR, True)
                if MOVE_FLAG:
                    if not self.find_color(MulColorEnumG.XT_FLAG) and self.map_ex(map_data[-1], 0):  # 检查地图名
                        return True
                    self.choose_xt_map(map_data)
                    MOVE_FLAG = False
                    _C_FLAG = False
                elif MOVE_FLAG2:
                    if WAIT_XL_TIMES > 10:
                        MOVE_FLAG2 = False
                        _USE_MOVE = False
                    if self.cmp_rgb([575, 221, '617a95']):
                        self.time_sleep(5)
                        WAIT_XL_TIMES += 1
                    else:
                        if not self.find_color(MulColorEnumG.XT_FLAG) and self.map_ex(map_data[-1], 0):  # 检查地图名
                            return True
                        else:
                            WAIT_XL_TIMES += 1
                            self.time_sleep(10)
                else:
                    if not self.find_color(MulColorEnumG.XT_FLAG) and self.map_ex(map_data[-1], 0):  # 检查地图名
                        return True
                    self.touch((99, 99), touch_wait=3)
            elif MOVE_FLAG and self.cmp_rgb(RgbEnumG.MAP_SJYD_QR, True):
                pass
            elif _USE_MOVE and self.cmp_rgb(RgbEnumG.MAP_XLQR, True):
                pass
            elif self.cmp_rgb(RgbEnumG.MAP_ERR, True):
                self.sn.log_tab.emit(self.mnq_name, r"无法瞬间移动,改从星图出发")
                MOVE_FLAG = True  # 无法瞬间移动,该从星图出发
            elif self.cmp_rgb(RgbEnumG.BG_PINDAO):
                if _USE_MOVE:
                    MOVE_FLAG2 = True
                if MOVE_FLAG:
                    self.back()
                else:
                    if not _C_FLAG:
                        if self.map_yt(map_data[1]):
                            if map_data[1] == 'ldsh':
                                self.touch((718, 248), touch_wait=2)
                                self.touch((248, 480), touch_wait=2)
                            elif map_data[1] == 'wlzm':
                                if map_data[-1] == 'wqk':
                                    self.touch((488, 479), touch_wait=2)
                                    self.touch((378, 594), touch_wait=2)
                                else:
                                    self.touch((707, 218), touch_wait=2)
                                    self.touch((807, 469), touch_wait=2)
                            elif map_data[1] == 'sjsd':
                                self.touch((553, 220), touch_wait=2)
                                self.touch((538, 433), touch_wait=2)
                            elif map_data[1] == 'mnesl':
                                self.touch((628, 644), touch_wait=2)
                                self.touch((386, 181), touch_wait=2)
                            elif map_data[1] == 'alsl':
                                self.touch((656, 411), touch_wait=2)
                                self.touch((424, 195), touch_wait=2)
                            if self.cmp_rgb(RgbEnumG.MAP_SJYD):
                                _C_FLAG = True
                        else:
                            self.dm_swipe((81, 470), (81, 251))
                    else:
                        if self.cmp_rgb(RgbEnumG.MAP_XL, True):
                            _USE_MOVE = True  # 寻路移动开始
                        elif self.cmp_rgb(RgbEnumG.MAP_SJYD, True):
                            MOVE_FLAG = True  # 瞬间移动

            else:
                self.check_close()

    def choose_xt_team(self, **kwargs):
        """星图找队伍"""
        s_time = time.time()
        WAIT_TIMES = 0  # 等待组队次数 1次10秒
        C_PINDAO = False  # 更换频道
        _IS_EXIT = False if kwargs['挂机设置']['人少退组'] == '0' else True
        self.sn.log_tab.emit(self.mnq_name, r"选择星图队伍")
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.pic_find(ImgEnumG.EXIT_TEAM, False):
                if _IS_EXIT:
                    pos = self.pic_find(ImgEnumG.EXIT_TEAM, False, get_pos=True)
                    if pos[-1] < 270:
                        self.touch((pos[1], pos[-1]), touch_wait=1)  # 人数低于3人退队伍
                        if self.cmp_rgb(RgbEnumG.EXIT_TEAM, True):
                            self.sn.log_tab.emit(self.mnq_name, r"人数少于3人,退组重组")
                        C_PINDAO = True
                    else:
                        return True
                else:
                    return True
            # elif self.ocr_find(ImgEnumG.TEAM_ZDJR_OCR):
            elif self.word_find(WorldEnumG.AUTO_JION):
                if WAIT_TIMES > 2:
                    self.sn.log_tab.emit(self.mnq_name, f"已等待{(WAIT_TIMES + 1) * 10}秒,切换频道重新组队")
                    self.touch((147, 350), touch_wait=GlobalEnumG.TouchWaitTime)
                    C_PINDAO = True
                else:
                    self.cmp_rgb(RgbEnumG.TEAM_ZDJR_QR, True)
                    self.sn.log_tab.emit(self.mnq_name, f"等待自动加入....")
                    self.time_sleep(10)
                    WAIT_TIMES += 1
            elif self.find_color(MulColorEnumG.IGAME):
                if C_PINDAO:
                    if self.change_pindao():
                        WAIT_TIMES = 0
                        C_PINDAO = False
                else:
                    if not self.cmp_rgb(RgbEnumG.TEAM_ZDJR, True):
                        if not self.word_find(WorldEnumG.AUTO_JION):
                            self.pic_find(ImgEnumG.TEAM_TAB)
                    self.cmp_rgb(RgbEnumG.TEAM_ZDJR_QR, True)
            else:
                self.check_err()
        self.sn.log_tab.emit(self.mnq_name, r"选择星图地图-超时失败")
        return False

    def change_pindao(self):
        """更换频道"""
        s_time = time.time()
        _FLAG = False
        self.sn.log_tab.emit(self.mnq_name, r"变更频道")
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _FLAG:
                    return True
                self.touch((99, 99), touch_wait=4)
            elif self.cmp_rgb(RgbEnumG.MAP_QWPD):
                _FLAG = False
                pindao_list = [(340, 314), (332, 533), (954, 317), (952, 529), (561, 521), (771, 515),
                               (737, 298), (530, 293), (977, 409), (314, 407), (573, 175), (734, 185)]  # 频道坐标
                i = random.randint(0, 11)
                r = random.randint(0, 3)
                _pos = pindao_list[i]
                self.sn.log_tab.emit(self.mnq_name, r"随机选择频道")
                for _ in range(r):
                    self.dm_swipe((639, 510), (639, 316))
                self.touch(_pos, touch_wait=5)
                if self.cmp_rgb(RgbEnumG.MAP_QWPD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"等待频道变更")
                    _FLAG = True
                    self.time_sleep(5)
            elif self.cmp_rgb(RgbEnumG.BG_PINDAO, True):
                pass
            else:
                self.check_close()
        return False

    def choose_pindao(self, **kwargs):
        s_time = time.time()
        _FIND_PD = kwargs['野图设置']['队伍频道'][0]
        _FIND_PD_F = kwargs['野图设置']['队伍频道备用'][0]
        _FIND = False
        _FLAG = False
        _C_PD = False
        _HD_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, f"选择频道{_FIND_PD}")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _FLAG:
                    return True
                self.touch((99, 99), touch_wait=4)
            elif self.cmp_rgb(RgbEnumG.MAP_QWPD):
                if _FLAG:
                    self.back()
                else:
                    if not _FIND:
                        if self.find_pd_num(_FIND_PD, True):
                            self.sn.log_tab.emit(self.mnq_name, f"找到频道_{_FIND_PD}")
                            _FIND = True
                            if self.cmp_rgb(RgbEnumG.MAP_QWPD, True):
                                _FLAG = True
                        else:
                            self.sn.log_tab.emit(self.mnq_name, f"查找频道_{_FIND_PD}")
                            if _HD_TIMES > 25:
                                self.sn.log_tab.emit(self.mnq_name, f"查找失败,启动备用频道_{_FIND_PD_F}")
                                _FIND_PD = _FIND_PD_F
                                _HD_TIMES = 0
                            if _HD_TIMES > 10:
                                self.dm_swipe((639, 316), (639, 510))
                                _HD_TIMES += 1
                            else:
                                self.dm_swipe((639, 510), (639, 316))
                                _HD_TIMES += 1
                    else:
                        if self.cmp_rgb(RgbEnumG.MAP_QWPD, True):
                            _FLAG = True
                            self.time_sleep(5)
            elif self.cmp_rgb(RgbEnumG.BG_PINDAO):
                if not _C_PD:
                    pd_res = self.check_num(6)
                    if pd_res == _FIND_PD or pd_res == _FIND_PD_F:
                        self.sn.log_tab.emit(self.mnq_name, f"当前频道{pd_res}")
                        _FLAG = True
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"当前频道不正确")
                        self.cmp_rgb(RgbEnumG.BG_PINDAO, True)
                    _C_PD = True
                else:
                    if _FLAG:
                        self.back()
                    else:
                        self.cmp_rgb(RgbEnumG.BG_PINDAO, True)
            else:
                self.check_close()
        return False

    def creat_team(self, **kwargs):
        s_time = time.time()
        team_pwd = kwargs['野图设置']['组队密码']
        _PUT_PWD = False  # 输入密码标记
        _C_FLAG = False  # 组队成功标记
        self.sn.log_tab.emit(self.mnq_name, r"创建队伍")
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if _C_FLAG:
                    if self.cmp_rgb(RgbEnumG.TEAM_CLDW):
                        _C_FLAG = False
                    elif self.pic_find(ImgEnumG.EXIT_TEAM, False):
                        return True
                    else:
                        self.pic_find(ImgEnumG.TEAM_TAB)
                else:
                    # if not self.pic_find(ImgEnumG.TEAM_CLDW):
                    if not self.cmp_rgb(RgbEnumG.TEAM_CLDW, True):
                        self.pic_find(ImgEnumG.TEAM_TAB, touch_wait=2)
                    if self.pic_find(ImgEnumG.EXIT_TEAM, False):
                        return True
            elif self.cmp_rgb(RgbEnumG.TEAM_CLDW_M):
                if self.cmp_rgb(RgbEnumG.TEAM_MMDW):
                    self.cmp_rgb(RgbEnumG.TEAM_CLQR, True)
                else:
                    self.cmp_rgb([102, 521, 'dfdfdf'], True)
                    self.cmp_rgb([942, 261, 'dfdfdf'], True)
            elif self.cmp_rgb(RgbEnumG.TEAM_QRMM):
                if not _PUT_PWD:
                    for pwd in team_pwd:
                        self.touch(GlobalEnumG.PWD_POS[pwd], duration=1)
                    _PUT_PWD = True
                else:
                    put_res = self.check_put_num(1)
                    if team_pwd in put_res:
                        if self.qr_tip():
                            _C_FLAG = True
                    else:
                        self.back()
                        _PUT_PWD = False
            else:
                self.check_close()
        return False

    def jion_team(self, **kwargs):
        s_time = time.time()
        team_pwd = kwargs['野图设置']['组队密码']
        _POS_LIST = []  # 识别出的带密码的队伍
        _PUT_PWD = False  # 输入密码操作
        _C_FLAG = False
        _C_TEAM = False  # 更换密码队伍
        _S_TEAM = False  # 滑动队伍列表
        _F_FLAG = False  # 首次检查加入队伍
        _SWIPE_TIMES = 0
        map_data = kwargs['战斗数据']['地图识别']
        self.sn.log_tab.emit(self.mnq_name, r"加入队伍")
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                if self.find_color(MulColorEnumG.XT_FLAG) or not self.map_ex(map_data[-1], 0):  # 检查地图名
                    return True
                if self.pic_find(ImgEnumG.EXIT_TEAM, False):
                    return True
                else:
                    _C_FLAG = False
                if not self.cmp_rgb(RgbEnumG.TEAM_XZDW, True):
                    self.pic_find(ImgEnumG.TEAM_TAB)
            elif self.cmp_rgb(RgbEnumG.TEAM_QRMM):
                if _C_FLAG:
                    self.back()
                    _C_TEAM=True
                else:
                    if not _PUT_PWD:
                        for pwd in team_pwd:
                            self.touch(GlobalEnumG.PWD_POS[pwd], duration=1)
                        _PUT_PWD = True
                    else:
                        put_res = self.check_put_num(1)
                        if put_res == team_pwd:
                            if self.cmp_rgb(RgbEnumG.TEAM_QRMM, True):
                                _C_FLAG = True
                        else:
                            self.back()
                            _PUT_PWD = False
            elif self.cmp_rgb(RgbEnumG.BG_PINDAO):
                if _C_TEAM:
                    _C_FLAG=False
                if _C_FLAG:
                    self.back()
                # if self.ocr_find(ImgEnumG.JION_TEAM_OCR):
                if self.word_find(WorldEnumG.TEAM_NULL):
                    self.back()
                    return False  # 无队伍需要创建
                if len(_POS_LIST) == 0:
                    if _S_TEAM:
                        self.dm_swipe((1093, 535), (1093, 314))
                        _S_TEAM = False
                    team_pos = self.air_all_find(ImgEnumG.PWD_TEAM)
                    if len(team_pos) != 0:
                        _POS_LIST = team_pos
                    else:
                        if _SWIPE_TIMES > 5:
                            self.cmp_rgb(RgbEnumG.TEAM_CXZL, True)
                            _SWIPE_TIMES = 0
                        self.dm_swipe((1093, 535), (1093, 314))
                        _SWIPE_TIMES += 1
                else:
                    self.touch(_POS_LIST[0], touch_wait=2)
                    if self.cmp_rgb(RgbEnumG.TEAM_SQJR_F):
                        _POS_LIST.pop(0)
                        if len(_POS_LIST) == 0:
                            _S_TEAM = True
                    else:
                        if self.cmp_rgb(RgbEnumG.TEAM_SQJR, True):
                            _POS_LIST.pop(0)
                            if len(_POS_LIST) == 0:
                                _S_TEAM = True
                            _C_TEAM=False
            else:
                self.check_close()
        return False

    def move_shenmi(self):
        for i in range(10):
            self.mul_color(MulColorEnumG.S_MAP, True)  # 打开小地图
            res, x1, y1 = self.get_move_xy()
            if x1 in range(1007, 1013):
                self.touch(self.turn_pos['up'])
                return True
            else:
                if x1 - 1010 > 0:
                    self.touch(self.turn_pos['left'], abs(x1 - 1010) / 28)
                else:
                    self.touch(self.turn_pos['right'], abs(x1 - 1010) / 28)
        return False
