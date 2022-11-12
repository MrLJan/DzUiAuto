# -*- coding: utf-8 -*-
import time

from Enum.ResEnum import GlobalEnumG, ImgEnumG, RgbEnumG
from UiPage.BasePage import BasePageG
from Utils.LoadConfig import LoadConfig


class StateCheckG(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(StateCheckG, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def choose_task(self, **kwargs):
        select_queue = kwargs['状态队列']['选择器']
        use_mp = kwargs['挂机设置']['无蓝窗口']
        if select_queue.queue.empty():
            if not self.check_hpmp(use_mp):
                select_queue.put_queue('BuyY')
            if self.crop_image_find(ImgEnumG.BAG_MAX_IMG, False):
                select_queue.put_queue('BagSell')
        else:
            if not self.check_hpmp(use_mp):
                select_queue.put_queue('BuyY')
            if self.crop_image_find(ImgEnumG.BAG_MAX_IMG, False):
                select_queue.put_queue('BagSell')
            if self.check_team():
                select_queue.put_queue('ChooseTeam')
            if select_queue.queue.empty():
                return 1

    def check_hpmp(self, use_mp):
        _res_hpmp = self.check_hp_mp()
        if _res_hpmp == '':
            return True
        elif 'HP' in _res_hpmp:
            return False
        elif use_mp:
            if 'MP' in _res_hpmp:
                return False
        return True

    def check_team(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut / 2:
            if self.find_info('ingame_flag2'):
                self.crop_image_find(ImgEnumG.TEAM_TAB)
                if self.crop_image_find(ImgEnumG.EXIT_TEAM, False):
                    return True
                else:
                    return False
            else:
                self.check_close()
        return False

    def close_all(self):
        s_time = time.time()
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):
                self.sn.log_tab.emit(self.mnq_name, r"在游戏主界面")
                return True
            elif self.crop_image_find(ImgEnumG.GAME_ICON, False):
                self.sn.log_tab.emit(self.mnq_name, r"掉线")
                return True
            elif self.air_loop_find(ImgEnumG.MR_BAT_EXIT):
                self.back_ksdy()
            else:
                self.check_close()
        return False

    def check_roleinfo(self, **kwargs):
        s_time = time.time()
        select_queue = kwargs['状态队列']['选择器']
        auto_choose = kwargs['托管模式']
        _C_OVER = False  # 检查是否完成
        _C_LEVEL = False
        RED_GOLD = 0  # 红币
        GOLD = 0  # 金币
        _GOLD_NUM = LoadConfig.getconf(self.mnq_name, '金币', ini_name=self.mnq_name)
        BAT_NUM = 0  # 战力
        LEVEL = 0  # 等级
        STAR = 0  # 星力
        while time.time() - s_time < GlobalEnumG.UiCheckTimeOut:
            if self.find_info('ingame_flag2'):
                if not _C_LEVEL:
                    self.sn.log_tab.emit(self.mnq_name, r"检查等级、战力数")
                    LEVEL = self.check_num(0)
                    BAT_NUM = self.check_num(1)
                    if LEVEL != '0':
                        LoadConfig.writeconf(self.mnq_name, '等级', str(LEVEL), ini_name=self.mnq_name)
                        LoadConfig.writeconf(self.mnq_name, '战力', str(BAT_NUM), ini_name=self.mnq_name)
                        _C_LEVEL = True
                if _C_OVER:
                    kwargs['角色信息']['等级'] = LEVEL
                    kwargs['角色信息']['星力'] = STAR
                    kwargs['角色信息']['战力'] = BAT_NUM
                    kwargs['角色信息']['金币'] = GOLD
                    kwargs['角色信息']['红币'] = RED_GOLD
                    _T_GOLD = round((int(GOLD) - int(_GOLD_NUM)) / 10000, 2)
                    self.sn.table_value.emit(self.mnq_name, 3, f"{LEVEL}")
                    self.sn.table_value.emit(self.mnq_name, 4, f"{STAR}")
                    self.sn.table_value.emit(self.mnq_name, 5, f"{BAT_NUM}")
                    self.sn.table_value.emit(self.mnq_name, 6, f"{GOLD}")
                    self.sn.table_value.emit(self.mnq_name, 7, f"{str(_T_GOLD)}万")
                    LoadConfig.writeconf(self.mnq_name, '产金量', str(_T_GOLD) + '万', ini_name=self.mnq_name)
                    self.sn.log_tab.emit(self.mnq_name,
                                         f"等级：{LEVEL}_星力{STAR}_战力{BAT_NUM}_金币{GOLD}_红币{RED_GOLD}_产金{_T_GOLD}")
                    select_queue.task_over('CheckRole')
                    if auto_choose:
                        self.auto_choose_task(LEVEL, STAR, RED_GOLD, select_queue, **kwargs)
                    return True
                self.air_touch((1170, 39), touch_wait=3)
            elif self.get_rgb(RgbEnumG.BAG_GOLD_QR):
                if _C_OVER:
                    self.get_rgb(RgbEnumG.BAG_GOLD_QR, True)
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"检查金币、红币数量")
                    GOLD = self.gold_num(1)
                    RED_GOLD = self.gold_num(0)
                    LoadConfig.writeconf(self.mnq_name, '金币', str(GOLD), ini_name=self.mnq_name)
                    LoadConfig.writeconf(self.mnq_name, '红币', str(RED_GOLD), ini_name=self.mnq_name)
                    _C_OVER = True
            elif self.get_rgb(RgbEnumG.BAG_M):
                self.time_sleep(1)
                if _C_OVER:
                    self.back()
                else:
                    self.sn.log_tab.emit(self.mnq_name, r"检查星力")
                    STAR = self.check_num(2)
                    LoadConfig.writeconf(self.mnq_name, '星力', str(STAR), ini_name=self.mnq_name)
                    self.crop_image_find(ImgEnumG.BAG_GOLD, touch_wait=2)
            elif self.find_info('coin_enum', True):
                pass
            else:
                self.check_close()

    def auto_choose_task(self, level, star, red_gold, select_queue, **kwargs):
        exec_queue = kwargs['状态队列']['执行器']
        red_coin = kwargs['强化设置']['托管红币']
        if red_coin == '0':
            red_coin = '1'
        # _CW_FLAG = False if kwargs['角色信息']['宠物'] == '0' else True
        # _L2_FLAG = False if kwargs['角色信息']['60级'] == '0' else True
        # _L3_FLAG = False if kwargs['角色信息']['90级'] == '0' else True
        _L4_FLAG = False if kwargs['角色信息']['100级'] == '0' else True

        # if 90 < int(level) <= 100 and _L4_FLAG:
        #     LoadConfig.writeconf(self.mnq_name, '100级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['100级'] = '0'
        # if 60 < int(level) <= 90:
        #     LoadConfig.writeconf(self.mnq_name, '100级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['100级'] = '0'
        #     LoadConfig.writeconf(self.mnq_name, '90级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['90级'] = '0'
        # if 30 < int(level) <= 60 and _L2_FLAG:
        #     LoadConfig.writeconf(self.mnq_name, '100级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['100级'] = '0'
        #     LoadConfig.writeconf(self.mnq_name, '90级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['90级'] = '0'
        #     LoadConfig.writeconf(self.mnq_name, '60级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['60级'] = '0'
        # if int(level) <= 30 and _CW_FLAG:
        #     LoadConfig.writeconf(self.mnq_name, '100级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['100级'] = '0'
        #     LoadConfig.writeconf(self.mnq_name, '90级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['90级'] = '0'
        #     LoadConfig.writeconf(self.mnq_name, '60级', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['60级'] = '0'
        #     LoadConfig.writeconf(self.mnq_name, '宠物', '0', ini_name=self.mnq_name)
        #     kwargs['角色信息']['宠物'] = '0'
        if int(star) >= 40:
            # self.change_mapdata('3', '研究所102', **kwargs)
            self.sn.log_tab.emit(self.mnq_name, r"选择星图混经验")
            exec_queue.put_queue('AutoBat')
        else:
            self.sn.log_tab.emit(self.mnq_name, r"星力不足,继续做任务")
            exec_queue.put_queue('AutoTask')
        if int(level) > 100 and not _L4_FLAG:
            self.sn.log_tab.emit(self.mnq_name, r"大于100级,且配置中未检查装备技能")
            select_queue.put_queue('UseSkill')
            select_queue.put_queue('GetLevelReard')
        if int(red_gold) > int(red_coin) * 10000000:
            self.sn.log_tab.emit(self.mnq_name, f"红币数量大于【{red_coin}千万】,进行强化+升级装备")
            # select_queue.put_queue('CheckRole')
            select_queue.put_queue('UpEquip')
            select_queue.put_queue('StrongEquip')
