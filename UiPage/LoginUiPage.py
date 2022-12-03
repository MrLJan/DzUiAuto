# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import ImgEnumG, GlobalEnumG, RgbEnumG, MulColorEnumG, WorldEnumG
from UiPage.BasePage import BasePageG
from Utils.ExceptionTools import NotInGameErr, ControlTimeOut, FuHuoRoleErr, NetErr, MoGuErr


class LoginUiPageG(BasePageG):
    def __init__(self, devinfo, sn):
        super(LoginUiPageG, self).__init__()
        self.dev, self.mnq_name = devinfo
        self.sn = sn

    def start_login(self, **kwargs):
        self.sn.log_tab.emit(self.mnq_name, r"开始登录")
        select_queue = kwargs['状态队列']['选择器']
        s_time = time.time()
        _WAIT_GX = 0
        _WAIT_TIMES = 0
        while time.time() - s_time < GlobalEnumG.LoginGameTimeOut:
            if self.pic_find(ImgEnumG.GAME_ICON, False):
                self.start_game()
            elif self.pic_find(ImgEnumG.UI_ERR_IMG):
                pass
            elif self.pic_find(ImgEnumG.LOGIN_FLAG, False) or self.word_find(WorldEnumG.NEXON):
                if not self.cmp_rgb(RgbEnumG.GX_XZ, True):
                    self.touch((875, 390))  # 点击空白区域登录
                    self.sn.log_tab.emit(self.mnq_name, r"等待进入选角界面")
                    self.time_sleep(10)
            elif self.mul_color(MulColorEnumG.GAME_START, True):
                self.sn.log_tab.emit(self.mnq_name, r"等待进入游戏")
                self.time_sleep(10)
            elif self.find_color(MulColorEnumG.IGAME):
                self.sn.log_tab.emit(self.mnq_name, r"登录成功")
                select_queue.task_over('Login')
                return -1
            elif self.cmp_rgb(RgbEnumG.PET_END):
                self.touch((908, 97), touch_wait=1)
            elif self.cmp_rgb(RgbEnumG.HD_BJBS, True):
                pass
            elif self.cmp_rgb(RgbEnumG.HD_BJBS, True):
                pass
            elif self.cmp_rgb(RgbEnumG.EXIT_FOU, True):  # 退出游戏-否
                pass
            elif self.cmp_rgb(RgbEnumG.CLOSE_GAME, True):
                pass
            elif self.pic_find(ImgEnumG.GX_XZ_ING, False):
                if not self.cmp_rgb(RgbEnumG.GX_XZ_BACK, True):
                    if _WAIT_GX > 60:
                        self.sn.log_tab.emit(self.mnq_name, r"更新超10分钟,重启游戏")
                        self.stop_game()
                    self.sn.log_tab.emit(self.mnq_name, r"等待更新")
                    self.time_sleep(10)
                    _WAIT_GX += 1
            elif self.word_find(WorldEnumG.DATA_UP):
                self.sn.log_tab.emit(self.mnq_name, r"提示数据更新,重启游戏")
                self.stop_game()
            else:
                if _WAIT_TIMES > 2:
                    if not self.check_err():
                        _WAIT_TIMES = 0
                _WAIT_TIMES += 1
        self.sn.log_tab.emit(self.mnq_name, r"登录超10分钟,重启游戏")
        self.stop_game()
        return 0

    def check_ingame(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        if self.net_err():
            self.sn.log_tab.emit(self.mnq_name, r"网络断开_等待重连")
            raise NetErr
        elif self.pic_find(ImgEnumG.MOGU, False) or self.pic_find(ImgEnumG.MOGU1, False) or self.pic_find(
                ImgEnumG.JUBAO,
                False):
            self.sn.log_tab.emit(self.mnq_name, r"出现举报/蘑菇")
            self.stop_game()
            raise MoGuErr
        elif self.find_color(MulColorEnumG.IGAME):
            self.mul_color(MulColorEnumG.LB_TIP, True)
            self.sn.log_tab.emit(self.mnq_name, r"检查到在游戏中")
            # if kwargs['角色信息']['等级'] == 0:
            #     select_queue.put_queue('CheckRole')
            if self.pic_find(ImgEnumG.TIP, False):
                self.touch((1239, 34), touch_wait=2)
            if self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                if self.pic_find(ImgEnumG.CZ_FUHUO):
                    self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                    raise FuHuoRoleErr
            if self.pic_find(ImgEnumG.MR_BAT_EXIT):
                self.back_ksdy()
            select_queue.task_over('Check')
            return -1

        elif self.pic_find(ImgEnumG.GAME_ICON, False):
            self.sn.log_tab.emit(self.mnq_name, r"检查到掉线")
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        elif self.pic_find(ImgEnumG.CZ_FUHUO):
            self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
            select_queue.task_over('Check')
            select_queue.put_queue('FuHuo')
            return -1
        elif self.pic_find(ImgEnumG.LOGIN_FLAG, False) or self.mul_color(MulColorEnumG.GAME_START, True) or self.word_find(WorldEnumG.NEXON):
            self.sn.log_tab.emit(self.mnq_name, r"检查到在登录相关界面")
            self.cmp_rgb(RgbEnumG.GX_XZ, True)
            self.cmp_rgb(RgbEnumG.CLOSE_GAME, True)  # 退出游戏-否
            select_queue.task_over('Check')
            select_queue.put_queue('Login')
            return -1
        else:
            if self.mul_color(MulColorEnumG.TASK_CLOSE) and kwargs['任务id'] == '1':
                # self.sn.log_tab.emit(self.mnq_name, r"检查到任务界面")
                while not self.find_color(MulColorEnumG.IGAME):
                    if self.cmp_rgb([1033, 414, 'ee7046'], True):  # 完成/接受
                        self.sn.log_tab.emit(self.mnq_name, r"完成/接受")  # 完成/接受
                    elif self.word_find(WorldEnumG.TASK_ARROW, True, touch_wait=0):
                        self.sn.log_tab.emit(self.mnq_name, r"点击对话箭头")
                    elif self.cmp_rgb([367, 565, '4c87b0'], True):
                        pass
                    elif self.cmp_rgb([361, 570, 'ee7046'], True):
                        pass
                    elif self.cmp_rgb([685, 515, 'ee7046'], True):
                        pass
                    elif self.cmp_rgb(RgbEnumG.CLOSE_GAME, True):
                        pass
                    elif self.cmp_rgb(RgbEnumG.EXIT_FOU, True):
                        pass
                    else:
                        self.close_all(**kwargs)
                select_queue.task_over('Check')
                return -1
            self.close_all(**kwargs)
        return 0

    def close_all(self, **kwargs):
        s_time = time.time()
        task_id = kwargs['任务id']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            self.sn.log_tab.emit(self.mnq_name, r"检查界面")
            if self.cmp_rgb(RgbEnumG.EXIT_FOU, True) or self.cmp_rgb(RgbEnumG.CLOSE_GAME, True):  # 退出游戏-否
                pass
            elif self.net_err():
                self.sn.log_tab.emit(self.mnq_name, r"网络断开_等待重连")
                raise NetErr
            elif self.pic_find(ImgEnumG.MOGU, False) or self.pic_find(ImgEnumG.MOGU1, False) or self.pic_find(
                    ImgEnumG.JUBAO,
                    False):
                self.sn.log_tab.emit(self.mnq_name, r"出现举报/蘑菇")
                self.stop_game()
                raise MoGuErr
            elif self.pic_find(ImgEnumG.UI_ERR_IMG):
                pass
            elif not self.check_now_app():
                raise NotInGameErr
            elif self.find_color(MulColorEnumG.IGAME):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                if self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                    if self.pic_find(ImgEnumG.CZ_FUHUO):
                        self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                        raise FuHuoRoleErr
                if self.pic_find(ImgEnumG.MR_BAT_EXIT, touch_wait=3):
                    # self.ocr_find(ImgEnumG.MR_YDZXD, True)
                    self.back_ksdy()
                if self.pic_find(ImgEnumG.TIP, False):
                    self.touch((1239, 34), touch_wait=2)
                self.cmp_rgb(RgbEnumG.TC_1, True)
                break
            elif self.pic_find(ImgEnumG.GAME_ICON, False):
                self.sn.log_tab.emit(self.mnq_name, r"掉线")
                raise NotInGameErr
            elif self.pic_find(ImgEnumG.LOGIN_FLAG) or self.mul_color(MulColorEnumG.GAME_START, True) or self.word_find(WorldEnumG.NEXON):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏登录主界面")
                break
            elif self.cmp_rgb(RgbEnumG.FUHUO_BTN):
                if self.pic_find(ImgEnumG.CZ_FUHUO):
                    self.sn.log_tab.emit(self.mnq_name, r"检查到死亡")
                    raise FuHuoRoleErr
            elif self.mul_color(MulColorEnumG.LB_TIP, True):
                pass
            elif self.mul_color(MulColorEnumG.COIN_ENUM, True):
                pass
            elif self.cmp_rgb(RgbEnumG.WL_QX, True):
                pass
            elif self.mul_color(MulColorEnumG.TASK_CLOSE, True):
                pass
            elif self.cmp_rgb(RgbEnumG.PET_END):
                self.touch((908, 97), touch_wait=1)
            elif self.cmp_rgb(RgbEnumG.GX_XZ_BACK, True):
                pass
            elif self.word_find(WorldEnumG.TASK_ARROW, True, touch_wait=0):
                pass
            elif self.cmp_rgb([1033, 414, 'ee7046'], True):
                pass
            elif self.word_find(WorldEnumG.SKIP, True):
                pass
            elif self.word_find(WorldEnumG.DATA_UP):
                self.sn.log_tab.emit(self.mnq_name, r"提示数据更新,重启游戏")
                self.stop_game()
            else:
                if task_id in ['1']:
                    if self.mul_color(MulColorEnumG.TASK_CLOSE):
                        for i in range(3):
                            self.word_find(WorldEnumG.TASK_ARROW,True)
                    self.cmp_rgb([1033, 414, 'ee7046'], True)
                    self.cmp_rgb([359, 636, 'ee7046'], True)
                self.back()

    def close_game(self):
        self.stop_game()

    def fuhuo_check(self, **kwargs):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"复活检查")
        select_queue = kwargs['状态队列']['选择器']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        task_id = kwargs['任务id']
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_color(MulColorEnumG.IGAME):
                self.mul_color(MulColorEnumG.LB_TIP,True)
                if self.cmp_rgb(RgbEnumG.FUHUO_BTN,True):
                    if self.pic_find(ImgEnumG.CZ_FUHUO):
                        self.time_sleep(2)
                _res_hp_mp = self.check_hp_mp()
                if _res_hp_mp != '':
                    if 'HP' in _res_hp_mp:
                        select_queue.put_queue('BuyY')
                    elif use_mp:
                        if 'MP' in _res_hp_mp:
                            select_queue.put_queue('BuyY')
                elif self.pic_find(ImgEnumG.BAG_MAX_IMG, False):
                    select_queue.put_queue('BagSell')
                if task_id == '1':
                    select_queue.put_queue('UseSkill')
                    select_queue.put_queue('GetLevelReard')
                select_queue.task_over('FuHuo')
                return -1
            elif self.pic_find(ImgEnumG.CZ_FUHUO):
                pass
            else:
                self.close_all(**kwargs)
        raise ControlTimeOut('复活检查-超时异常')

    def wait_net_err(self, **kwargs):
        s_time = time.time()
        self.sn.log_tab.emit(self.mnq_name, r"网络检查")
        select_queue = kwargs['状态队列']['选择器']
        while time.time() - s_time < GlobalEnumG.LoginGameTimeOut / 5:
            if self.net_err():
                self.sn.log_tab.emit(self.mnq_name, f"网络异常,已等待{round(time.time() - s_time, 2)}秒,超300秒自动重启游戏")
                self.time_sleep(10)
            elif self.find_color(MulColorEnumG.IGAME):
                select_queue.task_over('NetErr')
                return -1
            else:
                self.close_all(**kwargs)
        self.sn.log_tab.emit(self.mnq_name, r"网络无法连接,重启游戏")
        self.stop_game()
        raise ControlTimeOut('网络检查-超时异常')
