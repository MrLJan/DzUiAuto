# -*- coding: utf-8 -*-
import random
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG, BatEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import FuHuoRoleErr, BuyYErr, NotInGameErr


class TeamStateG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(TeamStateG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name
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
            # if not self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
            if task_id in ['3', '99']:
                select_queue.put_queue('CheckXT')
            else:
                select_queue.put_queue('CheckYT')
        if self.air_loop_find(ImgEnumG.GAME_ICON, False):
            select_queue.put_queue('Login')
        if self.air_loop_find(ImgEnumG.CZ_FUHUO, False):
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
        if self.crop_image_find(ImgEnumG.BAG_MAX_IMG, False):
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
            if self.find_info('ingame_flag2'):
                if _MAP and _TEAM:
                    select_queue.task_over('CheckXT')
                    return -1
                if not _MAP:
                    res_map, res_pd = self.check_map_pd(**kwargs)
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
        _WAIT_CREAT=0
        self.sn.log_tab.emit(self.mnq_name, r"检查野图状态")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):
                # if self.ocr_find(ImgEnumG.TKDK_OCR):
                #     self.move_shenmi()
                if _MAP and _TEAM and _PD:
                    select_queue.task_over('CheckYT')
                    return -1
                if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                    select_queue.put_queue('Login')
                    return -1
                if not _MAP or not _PD:
                    res_map, res_pd = self.check_map_pd(**kwargs)
                    if not res_map:
                        self.sn.log_tab.emit(self.mnq_name, r"当前地图不正确")
                        if self.choose_yt_map(map_data):
                            _MAP = True
                    else:
                        _MAP = True
                    if not res_pd:
                        self.sn.log_tab.emit(self.mnq_name, r"当前频道不正确")
                        if self.choose_pindao(**kwargs):
                            _PD = True
                    else:
                        _PD = True
                else:
                    for i in range(2):
                        if self.in_team() and self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                            team_queue.put_queue(kwargs['设备名称'])
                            _TEAM = True
                        else:
                            self.crop_image_find(ImgEnumG.TEAM_TAB)
                    if not _TEAM:
                        if team_event.is_set():
                            if _WAIT_CREAT>3:
                                if team_queue.queue.empty():
                                    team_event.clear()
                                    self.sn.log_tab.emit(self.mnq_name, "等待过长,自行创建")
                            else:
                                self.sn.log_tab.emit(self.mnq_name, "已经有窗口在创建队伍,等待创建")
                                self.time_sleep(10)
                                _WAIT_CREAT+=1
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
                                elif self.jion_team(**kwargs):
                                    self.sn.log_tab.emit(self.mnq_name, "加入队伍-成功")
                                    team_queue.put_queue(kwargs['设备名称'])
                                    _TEAM = True
                                else:
                                    self.sn.log_tab.emit(self.mnq_name, "加入队伍-失败")
            else:
                self.check_close()
        return -1

    def check_map_pd(self, **kwargs):
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
            if self.air_loop_find(ImgEnumG.GAME_ICON, False):
                raise NotInGameErr
            if self.crop_image_find(ImgEnumG.CZ_FUHUO):
                raise FuHuoRoleErr
            if self.find_info('ingame_flag2'):
                if _FLAG:
                    if _ID == '4':
                        if self.find_info('xt_flag'):
                            _MAP = False
                    # if _ID in ['3', '99']:
                    # if not self.find_info('xt_flag'):
                    #     _MAP = False
                    return _MAP, _PD
                self.air_touch((99, 99), touch_wait=3)
                # self.check_err()
            elif self.get_rgb(RgbEnumG.BG_PINDAO):
                self.time_sleep(2)
                if _FLAG:
                    self.back()
                else:
                    if not self.get_rgb(RgbEnumG.MAP_SJYD):
                        if self.get_rgb(RgbEnumG.BG_PINDAO):  # 打开界面不正确
                            self.back()
                    else:
                        if kwargs['任务id'] == '3':
                            _PD = True
                            for i in range(1,3):
                                if self.check_xt_map(_MAP_NAME,cont_res=abs(0.69-(i/10))):
                                    _MAP = True
                                    break
                            _FLAG = True
                        else:
                            pd_num_now = self.check_num(3)
                            pd_num = kwargs['野图设置']['队伍频道']
                            if pd_num_now in str(pd_num):
                                _PD = True
                            if self.check_map(_MAP_NAME):
                                _MAP = True
                            return _MAP, _PD
                            # _FLAG = True
            else:
                if time.time() - s_time > 60:
                    s_time = time.time()
                    self.check_close()
        return _MAP, _PD

    def choose_xt_map(self, map_data=None):
        _times = 0
        s_time = time.time()
        _M_OVER = False
        _SWIPE_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, r"选择星图地图")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):
                if _M_OVER:
                    return True
                if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                    pos = self.crop_image_find(ImgEnumG.EXIT_TEAM, False, get_pos=True)
                    if pos[-1] < 420:
                        self.air_touch((pos[1], pos[-1]), touch_wait=1)  # 人数低于3人退队伍
                        if self.get_rgb(RgbEnumG.EXIT_TEAM, True):
                            self.sn.log_tab.emit(self.mnq_name, r"退出已有队伍")
                self.find_info('ui_enum', True)
            elif self.find_info('ui_set'):  # 菜单界面
                self.enum_find('ksnr', True)
            elif self.get_rgb(RgbEnumG.KSDY):  # 星力战场
                if not self.find_mr_task('xl', True):
                    if _SWIPE_TIMES < 3:
                        self.air_swipe((925, 432), (400, 432), swipe_wait=1)
                    else:
                        if _SWIPE_TIMES > 6:
                            _SWIPE_TIMES = 0
                        self.air_swipe((400, 432), (925, 432), swipe_wait=1)
                    _SWIPE_TIMES += 1
            elif self.get_rgb(RgbEnumG.XLZC_YDQR, True):
                self.back()
                while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
                    if self.find_info('ingame_flag2'):
                        self.get_rgb(RgbEnumG.XLZC_YDOK, True)  # 移动完成 确认
                        if self.find_info('xt_flag'):
                            if self.find_xt_num(map_data[0], True)[0]:
                                return True
                        return False
                    else:
                        self.check_close()
                return False
            elif self.get_rgb(RgbEnumG.XLZC):
                if self.get_rgb(RgbEnumG.XLZC_YD, True):
                    pass
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"查找星图")
                    _res, _pos = self.find_xt_num(str(map_data[0]), True)
                    if _res:
                        self.sn.log_tab.emit(self.mnq_name, r"找到星图")
                        self.find_info('ui_enum', True)
                        self.get_rgb(RgbEnumG.XLZC_YD, True)
                        _M_OVER = True
                    else:
                        self.sn.log_tab.emit(self.mnq_name, r"星图不在当前界面")
                        for _i in _pos:
                            if '194' == _i[0]:
                                _times = 0
                            elif '10' == _i[0]:
                                self.sn.log_tab.emit(self.mnq_name, r"已滑到顶端,向下滑")
                                _times = 7
                        if _times > 6:
                            self.air_swipe((1092, 528), (1092, 298), swipe_wait=1)  # 下滑
                        else:
                            self.air_swipe((1092, 298), (1092, 528), swipe_wait=1)  # 上滑
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
            if self.find_info('ingame_flag2'):  # 移动完成
                self.get_rgb(RgbEnumG.QR, True)
                if MOVE_FLAG:
                    if self.check_map_ex(map_data[-1], 1):  # 检查地图名
                        return True
                    self.choose_xt_map(map_data)
                    MOVE_FLAG = False
                    _C_FLAG = False
                elif MOVE_FLAG2:
                    if WAIT_XL_TIMES > 10:
                        MOVE_FLAG2 = False
                        _USE_MOVE = False
                    if self.find_info('xl_lkyd'):
                        self.time_sleep(5)
                        WAIT_XL_TIMES += 1
                    else:
                        if self.check_map_ex(map_data[-1], 1):
                            return True
                        else:
                            WAIT_XL_TIMES += 1
                            self.time_sleep(10)
                else:
                    self.air_touch((99, 99), touch_wait=3)
            elif self.get_rgb(RgbEnumG.MAP_XLQR, True):
                pass
            elif self.get_rgb(RgbEnumG.MAP_ERR, True):
                MOVE_FLAG = True  # 无法瞬间移动,该从星图出发
            elif self.get_rgb(RgbEnumG.BG_PINDAO):
                if _USE_MOVE:
                    MOVE_FLAG2 = True
                if MOVE_FLAG:
                    self.back()
                else:
                    if not _C_FLAG:
                        if not self.check_map(map_data[-1]):
                            if self.map_yt(map_data[1]):
                                if map_data[1] == 'ldsh':
                                    self.air_touch((718, 248), touch_wait=2)
                                    self.air_touch((248, 480), touch_wait=2)
                                elif map_data[1] == 'wlzm':
                                    if map_data[-1] == 'wqk':
                                        self.air_touch((488, 479), touch_wait=2)
                                        self.air_touch((378, 594), touch_wait=2)
                                    else:
                                        self.air_touch((707, 218), touch_wait=2)
                                        self.air_touch((807, 469), touch_wait=2)
                                elif map_data[1] == 'sjsd':
                                    self.air_touch((553, 220), touch_wait=2)
                                    self.air_touch((538, 433), touch_wait=2)
                                elif map_data[1] == 'mnesl':
                                    self.air_touch((628, 644), touch_wait=2)
                                    self.air_touch((386, 181), touch_wait=2)
                                elif map_data[1] == 'alsl':
                                    self.air_touch((656, 411), touch_wait=2)
                                    self.air_touch((424, 195), touch_wait=2)
                                if self.get_rgb(RgbEnumG.MAP_SJYD):
                                    _C_FLAG = True
                            else:
                                self.air_swipe((81, 470), (81, 251))
                    else:
                        if self.get_rgb(RgbEnumG.MAP_XL, True):
                            _USE_MOVE = True  # 寻路移动开始
                        elif self.get_rgb(RgbEnumG.MAP_SJYD, True):
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
            if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                pos = self.crop_image_find(ImgEnumG.EXIT_TEAM, False, get_pos=True)
                if _IS_EXIT:
                    if pos[-1] < 270:
                        self.air_touch((pos[1], pos[-1]), touch_wait=1)  # 人数低于3人退队伍
                        if self.get_rgb(RgbEnumG.EXIT_TEAM, True):
                            self.sn.log_tab.emit(self.mnq_name, r"人数少于3人,退组重组")
                        C_PINDAO = True
                    else:
                        return True
                else:
                    if pos[0]:
                        return True
            # elif self.ocr_find(ImgEnumG.TEAM_ZDJR_OCR):
            elif self.find_info('team_zdjr'):
                if WAIT_TIMES > 2:
                    self.sn.log_tab.emit(self.mnq_name, f"已等待{(WAIT_TIMES + 1) * 10}秒,切换频道重新组队")
                    self.air_touch((147, 350), touch_wait=GlobalEnumG.TouchWaitTime)
                    C_PINDAO = True
                else:
                    self.sn.log_tab.emit(self.mnq_name, f"等待自动加入....")
                    self.get_rgb(RgbEnumG.TEAM_ZDJR_QR, True)
                    self.time_sleep(10)
                    WAIT_TIMES += 1
            elif self.find_info('ingame_flag2'):
                if C_PINDAO:
                    if self.change_pindao():
                        WAIT_TIMES = 0
                        C_PINDAO = False
                else:
                    if not self.get_rgb(RgbEnumG.TEAM_ZDJR, True):
                        if not self.find_info('team_zdjr'):
                            self.air_loop_find(ImgEnumG.TEAM_TAB)
                    self.get_rgb(RgbEnumG.TEAM_ZDJR_QR, True)
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
            if self.find_info('ingame_flag2'):
                if _FLAG:
                    return True
                self.air_touch((99, 99), touch_wait=4)
            elif self.get_rgb(RgbEnumG.MAP_QWPD):
                _FLAG = False
                pindao_list = [(340, 314), (332, 533), (954, 317), (952, 529), (561, 521), (771, 515),
                               (737, 298), (530, 293), (977, 409), (314, 407), (573, 175), (734, 185)]  # 频道坐标
                i = random.randint(0, 11)
                r = random.randint(0, 3)
                _pos = pindao_list[i]
                self.sn.log_tab.emit(self.mnq_name, r"随机选择频道")
                for _ in range(r):
                    self.air_swipe((639, 510), (639, 316))
                self.air_touch(_pos, touch_wait=5)
                if self.get_rgb(RgbEnumG.MAP_QWPD, True):
                    self.sn.log_tab.emit(self.mnq_name, r"等待频道变更")
                    _FLAG = True
                    self.time_sleep(5)
            elif self.get_rgb(RgbEnumG.BG_PINDAO, True):
                pass
            else:
                self.check_close()
        return False

    def choose_pindao(self, **kwargs):
        s_time = time.time()
        _FIND_PD = kwargs['野图设置']['队伍频道'][0]
        _FIND_PD_F = kwargs['野图设置']['队伍频道备用'][0]
        # _PD_POS = None
        _FIND = False
        _FLAG = False
        _HD_TIMES = 0
        self.sn.log_tab.emit(self.mnq_name, f"选择频道{_FIND_PD}")
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):
                if _FLAG:
                    return True
                self.air_touch((99, 99), touch_wait=4)
            elif self.get_rgb(RgbEnumG.MAP_QWPD):
                if not _FIND:
                    if self.find_pd_num(_FIND_PD, True):
                        self.sn.log_tab.emit(self.mnq_name, f"找到频道_{_FIND_PD}")
                        _FIND = True
                        if self.get_rgb(RgbEnumG.MAP_QWPD, True):
                            _FLAG = True
                    else:
                        self.sn.log_tab.emit(self.mnq_name, f"查找频道_{_FIND_PD}")
                        if _HD_TIMES > 25:
                            self.sn.log_tab.emit(self.mnq_name, f"查找失败,启动备用频道_{_FIND_PD_F}")
                            _FIND_PD = _FIND_PD_F
                            _HD_TIMES = 0
                        if _HD_TIMES > 10:
                            self.air_swipe((639, 316), (639, 510))
                            _HD_TIMES += 1
                        else:
                            self.air_swipe((639, 510), (639, 316))
                            _HD_TIMES += 1
                else:
                    # self.air_touch(_PD_POS, duration=1)
                    if self.get_rgb(RgbEnumG.MAP_QWPD, True):
                        _FLAG = True
                        self.time_sleep(5)
            elif self.get_rgb(RgbEnumG.BG_PINDAO, True):
                pass
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
            if self.find_info('ingame_flag2'):
                if _C_FLAG:
                    if self.find_info('team_cldw'):
                        _C_FLAG=False
                    elif self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                        return True
                    else:
                        if not self.in_team():
                            self.crop_image_find(ImgEnumG.TEAM_TAB)
                else:
                    # if not self.crop_image_find(ImgEnumG.TEAM_CLDW):
                    if not self.find_info('team_cldw',True):
                        self.crop_image_find(ImgEnumG.TEAM_TAB, touch_wait=2)
                    if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                        return True
            elif self.get_rgb(RgbEnumG.TEAM_CLDW_M):
                if self.get_rgb(RgbEnumG.TEAM_MMDW):
                    self.get_rgb(RgbEnumG.TEAM_CLQR, True)
                else:
                    self.get_rgb([102, 521,'E0E0E0'],True)
                    self.get_rgb([942, 261, 'DFDFDF'], True)#397AA0
                    # self.air_touch((102, 521), touch_wait=2)
                    # self.air_touch((942, 261))
            elif self.get_rgb(RgbEnumG.TEAM_QRMM):
                if not _PUT_PWD:
                    for pwd in team_pwd:
                        self.air_touch(GlobalEnumG.PWD_POS[pwd], duration=1)
                    _PUT_PWD = True
                else:
                    put_res = self.check_put_num(1)
                    if team_pwd in put_res:
                        if self.qr_or_qx(1):
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
        _F_FLAG = False  # 首次检查加入队伍
        self.sn.log_tab.emit(self.mnq_name, r"加入队伍")
        while time.time() - s_time < GlobalEnumG.SelectCtrTimeOut:
            if self.find_info('ingame_flag2'):
                if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                    return True
                if not self.crop_image_find(ImgEnumG.TEAM_XZDW):
                    self.crop_image_find(ImgEnumG.TEAM_TAB)
            elif self.get_rgb(RgbEnumG.TEAM_QRMM):
                if _C_FLAG:
                    self.back()
                else:
                    if not _PUT_PWD:
                        for pwd in team_pwd:
                            self.air_touch(GlobalEnumG.PWD_POS[pwd], duration=1)
                        _PUT_PWD = True
                    else:
                        put_res = self.check_put_num(1)
                        if put_res == team_pwd:
                            if self.get_rgb(RgbEnumG.TEAM_QRMM, True):
                                _C_FLAG = True
                        else:
                            self.back()
                            _PUT_PWD = False
            elif self.get_rgb(RgbEnumG.BG_PINDAO):
                if _C_FLAG:
                    self.back()
                # if self.ocr_find(ImgEnumG.JION_TEAM_OCR):
                if self.find_info('team_null'):
                    self.back()
                    return False  # 无队伍需要创建
                if len(_POS_LIST) == 0:
                    team_pos = self.air_all_find(ImgEnumG.PWD_TEAM)
                    if len(team_pos) > 0:
                        _POS_LIST = team_pos
                    else:
                        self.air_swipe((1093, 535), (1093, 314))
                else:
                    self.air_touch(_POS_LIST[0], touch_wait=2)
                    if self.get_rgb(RgbEnumG.TEAM_SQJR_F):
                        _POS_LIST.pop(0)
                    else:
                        self.get_rgb(RgbEnumG.TEAM_SQJR, True)
            else:
                self.check_close()
        return False

    def move_shenmi(self):
        for i in range(10):
            self.crop_image_find(ImgEnumG.S_MAP)  # 打开小地图
            res, x1, y1 = self.crop_image_find(ImgEnumG.PERSON_POS, clicked=False, get_pos=True)
            if x1 in range(1007, 1013):
                self.air_touch(self.turn_pos['up'])
                return True
            else:
                if x1 - 1010 > 0:
                    self.air_touch(self.turn_pos['left'], abs(x1 - 1010) / 28)
                else:
                    self.air_touch(self.turn_pos['right'], abs(x1 - 1010) / 28)
        return False
