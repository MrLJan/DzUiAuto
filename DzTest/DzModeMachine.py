# -*- coding: utf-8 -*-
import random
import time

from airtest.core.error import DeviceConnectionError, AdbShellError, AdbError
from transitions import Machine
from Enum.ResEnum import GlobalEnumG, BatEnumG
from UiPage.AutoBatG import AutoBatG
from UiPage.DailyTaskG import DailyTaskAutoG
from UiPage.LoginUiPage import LoginUiPageG
from UiPage.RewardG import RewardG
from UiPage.StateCheckG import StateCheckG
from UiPage.TaskAutoG import TaskAutoG
from UiPage.TeamStateG import TeamStateG
from UiPage.UpRoleG import UpRoleG
from Utils.ExceptionTools import MrTaskErr, ControlTimeOut, BuyYErr, NotInGameErr, RestartTask, FuHuoRoleErr, \
    BagFullerr, StopTaskErr
from Utils.LoadConfig import LoadConfig
from Utils.OtherTools import catch_ex


class StateExecute(object):
    """状态执行器"""

    def __init__(self, devinfo, mnq_name, sn):
        self.devinfo = devinfo
        self.sn = sn
        self.mnq_name = mnq_name

    def autotask(self, **kwargs):
        return TaskAutoG(self.devinfo, self.mnq_name, self.sn).start_autotask(**kwargs)

    def autobat(self, **kwargs):
        return AutoBatG(self.devinfo, self.mnq_name, self.sn).keyboard_bat(**kwargs)

    def checkstate(self, **kwargs):
        return TeamStateG(self.devinfo, self.mnq_name, self.sn).check_team_state(**kwargs)


class StateSelect(object):
    """状态选择器"""

    def __init__(self, devinfo, mnq_name, sn):
        self.devinfo = devinfo
        self.sn = sn
        self.mnq_name = mnq_name

    def login_game(self, **kwargs):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).start_login(**kwargs)

    def closegame(self):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).close_game()

    def check_ingame(self, **kwargs):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).check_ingame(**kwargs)

    def fuhuo(self, **kwargs):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).fuhuo_check(**kwargs)

    def checkroleinfo(self, **kwargs):
        return StateCheckG(self.devinfo, self.mnq_name, self.sn).check_roleinfo(**kwargs)

    def getlevelreard(self, **kwargs):
        return RewardG(self.devinfo, self.mnq_name, self.sn).level_reward(**kwargs)

    def calculationgold(self, **kwargs):
        return RewardG(self.devinfo, self.mnq_name, self.sn).calculationgold(**kwargs)

    def autoboss(self, **kwargs):
        return DailyTaskAutoG(self.devinfo, self.mnq_name, self.sn).boss_task(**kwargs)

    def hdboss(self, **kwargs):
        return DailyTaskAutoG(self.devinfo, self.mnq_name, self.sn).hdboss_task(**kwargs)

    def automr(self, **kwargs):
        return DailyTaskAutoG(self.devinfo, self.mnq_name, self.sn).dailytask_start(**kwargs)

    def buyyao(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).buyyao(**kwargs)

    def bagsell(self, **kwargs):
        return RewardG(self.devinfo, self.mnq_name, self.sn).bagsell(**kwargs)

    def bagclear(self, **kwargs):
        return RewardG(self.devinfo, self.mnq_name, self.sn).bag_clear(**kwargs)

    def useskill(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).useskill(**kwargs)

    def usepet(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).usepet(**kwargs)

    def upequip(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).upequip(**kwargs)

    def strongequip(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).strongequip(**kwargs)

    def getreward(self, **kwargs):
        return RewardG(self.devinfo, self.mnq_name, self.sn).get_reward(**kwargs)

    def checkxtteam(self, **kwargs):
        return TeamStateG(self.devinfo, self.mnq_name, self.sn).check_xt(**kwargs)

    def checkytteam(self, **kwargs):
        return TeamStateG(self.devinfo, self.mnq_name, self.sn).check_yt(**kwargs)

    def choose_task(self, **kwargs):
        return StateCheckG(self.devinfo, self.mnq_name, self.sn).choose_task(**kwargs)

    def back_ingame(self, **kwargs):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).close_all(**kwargs)


execute_transition = [
    {'trigger': 'Exe_Nothing', 'source': '*', 'dest': 'Nothing'},
    {'trigger': 'Exe_CheckState', 'source': '*', 'dest': 'CheckState'},
    {'trigger': 'Exe_AutoTask', 'source': 'AutoTask', 'dest': 'CheckState', 'unless': 'autotask'},
    {'trigger': 'Exe_AutoMR', 'source': 'AutoMR', 'dest': 'CheckState', 'unless': 'automr'},
    {'trigger': 'Exe_AutoBat', 'source': 'AutoBat', 'dest': 'CheckState', 'unless': 'autobat'},
]
select_transition = [
    {'trigger': 'Slt_InGame', 'source': '*', 'dest': 'InGame', 'before': 'back_ingame'},
]


class StateMachine:
    """状态控制器"""

    def __init__(self, model, states, transitions, init_state):
        self.machine = Machine(model, states=states, transitions=transitions, initial=init_state)


@catch_ex
class switch_case:
    """状态判断"""

    def __init__(self, sn, **kwargs):
        self.exec = kwargs['执行器']
        self.select = kwargs['选择器']
        self.mnq_name = kwargs['机器名']
        self.dev_name = kwargs['设备名']
        self.mnq_thread_list = kwargs['线程列表']
        self.queue_dic = kwargs['队列']
        self.exec_queue = self.queue_dic['执行器任务队列']
        self.select_queue = self.queue_dic['选择器任务队列']
        self.dingshi = LoadConfig.getconf('全局配置', '定时任务')
        self.boss_map = LoadConfig.getconf('全局配置', '混王图')
        self.hd_boss = LoadConfig.getconf('全局配置', '混沌炎魔')
        self.random_tasktime = random.randint(200, 600)  # 随机定时任务等待时间
        self.meiri_time = self.get_task_time()  # 获取每日任务设定时间
        # self._t_time = time.time()  # 计算任务时间时的当前时间
        # self._t = 0  # 距离下次任务的时间
        # self._id = 1  # 下次定时任务的id
        self._c_time = time.time()  # 计算产出时间时的当前时间
        self.login_time = LoadConfig.getconf(self.mnq_name, '最近登录时间', ini_name=self.mnq_name)
        self._r_time = time.time() if self.login_time == '0' else float(self.login_time)
        self.taskid, self.mapname = self.get_taskid(kwargs['任务名'])
        self.sn = sn
        self.team_id, self.pd_num = self.get_team_id(kwargs['位置信息'])
        self.use_mp = self.get_use_mp(kwargs['位置信息'])
        self.data_dic = self.get_data_dic()
        self.exec_func = {
            'AutoTask': [self.exec.autotask, self.exec.to_Nothing, self.exec.to_AutoTask],
            'AutoBat': [self.exec.autobat, self.exec.to_Nothing, self.exec.to_CheckTeamState],
            'Nothing': [self.exec.to_Nothing, self.exec.to_Nothing, self.exec.to_Nothing],
            'CheckTeamState': [self.exec.checkstate, self.exec.to_Nothing, self.exec.to_AutoBat],
            'Wait': [self.exec.to_Nothing]
        }
        self.select_func = {
            'InGame': [self.select.choose_task, self.select.to_Login, self.select.to_FuHuo,
                       self.select.to_BuyY, self.select.to_BagSell, self.select.to_UseSkill, self.select.to_UsePet,
                       self.select.to_UpEquip, self.select.to_StrongEquip],
            'Check': [self.select.check_ingame, self.select.to_Check, self.select.to_InGame],
            'AutoChoose': [self.select.checkroleinfo, self.select.to_CheckRole, self.select.to_Check],
            'Login': [self.select.login_game, self.select.to_Login, self.select.to_Check],
            'FuHuo': [self.select.fuhuo, self.select.to_FuHuo, self.select.to_Check],
            'BuyY': [self.select.buyyao, self.select.to_BuyY, self.select.to_Check],
            'BagSell': [self.select.bagsell, self.select.to_BagSell, self.select.to_Check],
            'BagClear': [self.select.bagclear, self.select.to_BagClear, self.select.to_Check],
            'UseSkill': [self.select.useskill, self.select.to_UseSkill, self.select.to_Check],
            'UsePet': [self.select.usepet, self.select.to_UsePet, self.select.to_Check],
            'UpEquip': [self.select.upequip, self.select.to_UpEquip, self.select.to_Check],
            'StrongEquip': [self.select.strongequip, self.select.to_StrongEquip, self.select.to_Check],
            'GetReward': [self.select.getreward, self.select.to_GetReward, self.select.to_Check],
            'CheckXT': [self.select.checkxtteam, self.select.to_CheckXT, self.select.to_Check],
            'CheckYT': [self.select.checkytteam, self.select.to_CheckYT, self.select.to_Check],
            'AutoBoss': [self.select.autoboss, self.select.to_AutoBoss, self.select.to_Check],
            'AutoHDboss': [self.select.hdboss, self.select.to_AutoHDboss, self.select.to_Check],
            'AutoMR': [self.select.automr, self.select.to_AutoMR, self.select.to_Check],
            'CheckRole': [self.select.checkroleinfo, self.select.to_CheckRole, self.select.to_Check],
            'GetLevelReard': [self.select.getlevelreard, self.select.to_GetLevelReard, self.select.to_Check],
            'CheckGold': [self.select.calculationgold, self.select.to_CheckGold, self.select.to_Check]
        }

    def get_taskid(self, task_name):
        """获取地图和任务id"""
        all_task = BatEnumG.TASK_ID.keys()
        xt_map = BatEnumG.MAP_DATA['3'].keys()
        yt_map = BatEnumG.MAP_DATA['4'].keys()
        _C_ROLE = False
        if LoadConfig.getconf(self.mnq_name, '等级', ini_name=self.mnq_name) == '0':
            _C_ROLE = True
        # if LoadConfig.getconf()
        if task_name in all_task:
            _id = BatEnumG.TASK_ID[task_name]['id']
            if _id in ['1']:
                # self.select_queue.put_queue('CheckRole')
                self.exec_queue.put_queue(BatEnumG.TASK_ID[task_name]['state'])
            elif _id == '5':
                self.exec_queue.put_queue('Nothing')
                self.select_queue.put_queue('AutoHDboss')
                self.select_queue.put_queue(BatEnumG.TASK_ID[task_name]['state'])
            elif _id == '99':
                self.select_queue.put_queue('CheckRole')
            else:
                self.exec_queue.put_queue('Nothing')
                self.select_queue.put_queue(BatEnumG.TASK_ID[task_name]['state'])
                if _C_ROLE:
                    self.select_queue.put_queue('CheckRole')
            return BatEnumG.TASK_ID[task_name]['id'], 'NULL'
        elif task_name in xt_map:
            if _C_ROLE:
                self.select_queue.put_queue('CheckRole')
            self.exec_queue.put_queue('AutoBat')
            return '3', task_name
        elif task_name in yt_map:
            if _C_ROLE:
                self.select_queue.put_queue('CheckRole')
            self.exec_queue.put_queue('AutoBat')
            return '4', task_name
        else:
            raise KeyError("任务名称有误")

    @staticmethod
    def get_use_mp(index_dic):
        no_mp_list = LoadConfig.getconf('全局配置', '无蓝窗口').split(',')
        mnq_index = index_dic['index']
        if mnq_index in no_mp_list:
            return False
        return True

    def get_data_dic(self):
        data = {
            '设备名称': self.mnq_name,
            '任务id': self.taskid,
            '托管模式': True if self.taskid == '99' else False,
            '地图名': self.mapname,
            '任务结束关闭游戏': True if LoadConfig.getconf('全局配置', '任务结束关闭游戏') == '1' else False,
            '角色信息': {
                '等级': int(LoadConfig.getconf(self.mnq_name, '等级', ini_name=self.mnq_name)),
                '星力': int(LoadConfig.getconf(self.mnq_name, '星力', ini_name=self.mnq_name)),
                '战力': int(LoadConfig.getconf(self.mnq_name, '战力', ini_name=self.mnq_name)),
                '金币': int(LoadConfig.getconf(self.mnq_name, '金币', ini_name=self.mnq_name)),
                '红币': int(LoadConfig.getconf(self.mnq_name, '红币', ini_name=self.mnq_name)),
                '产金量': LoadConfig.getconf(self.mnq_name, '产金量', ini_name=self.mnq_name),
                '宠物': LoadConfig.getconf(self.mnq_name, '宠物', ini_name=self.mnq_name),
                '60级': LoadConfig.getconf(self.mnq_name, '60级', ini_name=self.mnq_name),
                '90级': LoadConfig.getconf(self.mnq_name, '90级', ini_name=self.mnq_name),
                '100级': LoadConfig.getconf(self.mnq_name, '100级', ini_name=self.mnq_name),
            },
            '状态队列': {
                '执行器': self.exec_queue,
                '选择器': self.select_queue
            },
            '战斗数据': {
                '地图数据': [] if self.taskid not in ['3', '4'] else BatEnumG.MAP_DATA[self.taskid][self.mapname],
                '地图识别': BatEnumG.MAP_OCR[self.mapname],
                '无蓝': LoadConfig.getconf('全局配置', '无蓝窗口'),
                '刷图模式': LoadConfig.getconf('全局配置', '扫地模式'),
                '职业类型': LoadConfig.getconf('全局配置', '职业类型'),
                '楼梯队列': self.queue_dic['楼梯队列'],
                '方向队列': self.queue_dic['方向队列'],
                '休息队列': self.queue_dic['休息队列']
            },
            '挂机设置': {
                '混合自动按键': True if LoadConfig.getconf('全局配置', '混合自动按键') == '1' else False,
                '挂机卡时长': LoadConfig.getconf('全局配置', '挂机卡时长'),
                '人少退组': LoadConfig.getconf('全局配置', '人少退组'),
                '定时任务': LoadConfig.getconf('全局配置', '定时任务'),
                '随机休息': True if LoadConfig.getconf('全局配置', '随机休息') == '1' else False,
                '休息方式': LoadConfig.getconf('全局配置', '在线休息'),
                '离线使用挂机卡': LoadConfig.getconf('全局配置', '离线使用挂机卡'),
                '离线时长': int(LoadConfig.getconf('全局配置', '离线时长')),
                '无蓝窗口': self.use_mp,
                '任务延时': self.random_tasktime,
                '跳跃模式':True if LoadConfig.getconf('全局配置', '跳跃模式') == '1' else False,
            },
            '野图设置': {
                '队伍id': self.team_id,
                '队伍频道': self.pd_num,
                '队伍频道备用': ['50'],
                '队伍队列': self.queue_dic['队伍队列'][self.team_id],
                '队伍锁': self.queue_dic['队伍锁'][self.team_id],
                '组队密码': LoadConfig.getconf('野图配置', '组队密码')
            },
            '商店设置': {
                'HP等级': LoadConfig.getconf('全局配置', 'hp等级'),
                'HP数量': LoadConfig.getconf('全局配置', 'hp数量'),
                'MP等级': LoadConfig.getconf('全局配置', 'mp等级'),
                'MP数量': LoadConfig.getconf('全局配置', 'mp数量'),
            },
            '王图设置': {
                '混王图': LoadConfig.getconf('全局配置', '混王图'),
                '炎魔': LoadConfig.getconf('全局配置', '炎魔'),
                '炎魔难度': LoadConfig.getconf('全局配置', '炎魔难度'),
                '皮卡啾': LoadConfig.getconf('全局配置', '皮卡啾'),
                '皮卡啾难度': LoadConfig.getconf('全局配置', '皮卡啾难度'),
                '女皇': LoadConfig.getconf('全局配置', '女皇'),
                '女皇难度': LoadConfig.getconf('全局配置', '女皇难度'),
                '混沌炎魔': LoadConfig.getconf('全局配置', '混沌炎魔'),
            },
            '自动任务': {
                '任务停止等级': LoadConfig.getconf('全局配置', '任务停止等级'),
                '随机使用石头': True if LoadConfig.getconf('全局配置', '随机使用石头') == '1' else False,
            },
            '每日任务': {
                '定时任务': self.dingshi,
                '每日时间': self.meiri_time,
                '任务列表': self.get_mr_task(),
                '每日任务队列': self.queue_dic['每日任务队列'],
                '公会': True if LoadConfig.getconf('全局配置', '公会内容') == '1' else False
            },
            '定时设置': {
                '启动时间': time.time(),  # 计算任务时间时的当前时间
                '距离任务开始时间': 0,  # 距离下次任务的时间
                '定时任务ID': 1,  # 下次定时任务的id
            },
            '强化设置': {
                '托管红币': LoadConfig.getconf('全局配置', '托管红币'),
                '目标等级': LoadConfig.getconf('全局配置', '强化等级'),
                '幸运卷轴': True if LoadConfig.getconf('全局配置', '幸运卷轴') == '1' else False,
                '盾牌卷轴': True if LoadConfig.getconf('全局配置', '盾牌卷轴') == '1' else False,
                '保护卷轴': True if LoadConfig.getconf('全局配置', '保护卷轴') == '1' else False,
                '强化优惠卷': True if LoadConfig.getconf('全局配置', '强化优惠卷') == '1' else False,
            }

        }
        return data

    def get_team_id(self, index_dic):
        try:
            member = [list(LoadConfig().getconf("野图配置", "1队成员").split(',')),
                      list(LoadConfig().getconf("野图配置", "2队成员").split(',')),
                      list(LoadConfig().getconf("野图配置", "3队成员").split(',')),
                      list(LoadConfig().getconf("野图配置", "4队成员").split(',')),
                      list(LoadConfig().getconf("野图配置", "5队成员").split(',')),
                      list(LoadConfig().getconf("野图配置", "6队成员").split(',')),
                      list(LoadConfig().getconf("野图配置", "7队成员").split(',')), ]
            # ---
            pdnum = [list(LoadConfig().getconf("野图配置", "1队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "2队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "3队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "4队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "5队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "6队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "7队频道").split(','))]
            mnq_index = index_dic['index']
            team_num = ''
            pindao_num = []
            for _me in member:
                if mnq_index in _me:
                    team_num = 'team' + str(member.index(_me) + 1)
                    pindao_num = pdnum[member.index(_me)]
                    break
            if team_num == '':
                team_num = 'team7'
                pindao_num = pdnum[0]
            if self.taskid == 4:
                self.sn.log_tab.emit(self.mnq_name, f"队伍{team_num},频道：{pindao_num}")
            return team_num, pindao_num
        except KeyError as e:
            print(f"野图配置有误,检查配置表 {e}")
            return '31', 6

    @staticmethod
    def get_mr_task():
        task_list = []
        task_name = ['武陵', '金字塔', '菁英地城', '每日地城', '进化系统', '次元入侵', '汤宝宝',
                     '迷你地城', '星光塔', '怪物公园']
        for i in task_name:

            r = LoadConfig.getconf("全局配置", i)
            if r == '1':
                index = str(task_name.index(i) + 1)
                task_list.append(index)
        random.shuffle(task_list)  # 打乱顺序
        return task_list

    def do_case(self):
        try:
            # if self.taskid in ['3', '4']:
            #     self.get_time_to_dotask()  # 计算是否有定时任务需要进行
            # self.calculation_gold()
            # self.check_roleinfo()
            select_state = self.select.state
            if select_state != "InGame":
                self.select_machine_do()
            else:
                if self.select_queue.queue.empty() and self.exec_queue.queue.empty():
                    self.exec_machine_do()
                elif self.select_queue.queue.empty():
                    task_state = self.exec_queue.get_task()  # 获取执行器任务
                    self.exec_queue.task_over(task_state)  # 清空执行器
                    self.exec_func[task_state][2]()  # 切换执行器状态
                else:
                    task = self.select_queue.get_task()  # 获取选择器任务
                    self.select_func[task][1]()  # 切换选择器状态
        except (ConnectionResetError, DeviceConnectionError, ConnectionAbortedError, AdbShellError, AdbError,TypeError):
            self.sn.log_tab.emit(self.mnq_name, f"模拟器adb连接异常断开,尝试重连")
            self.sn.restart.emit(self.mnq_name, self.mnq_thread_list)
        except RestartTask:
            self.sn.restart.emit(self.mnq_name, self.mnq_thread_list)
        except MrTaskErr:
            self.sn.log_tab.emit(self.mnq_name, f"每日任务异常,开始检查")
            self.select.to_Check()
        except ControlTimeOut as e:
            self.sn.log_tab.emit(self.mnq_name, e.task)
            self.select.to_Check()
        except BuyYErr:
            self.select.to_BuyY()
        except BagFullerr:
            self.select.to_BagSell()
        except NotInGameErr:
            self.select.to_Check()
        except FuHuoRoleErr:
            self.select.to_FuHuo()

    def exec_machine_do(self):
        exec_state = self.exec.state
        self.sn.table_value.emit(self.mnq_name, 8, f"{GlobalEnumG.StatesInfo[exec_state]['name']}")
        self.sn.log_tab.emit(self.mnq_name, f"------{GlobalEnumG.StatesInfo[exec_state]['name']}------")
        if exec_state == 'Nothing':
            if self.data_dic['任务结束关闭游戏']:
                self.select.closegame()
                self.sn.table_value.emit(self.mnq_name, 8, "无任务")
                self.sn.log_tab.emit(self.mnq_name, "任务完成,关闭游戏,待机")
            else:
                self.sn.table_value.emit(self.mnq_name, 8, "无任务")
                self.sn.log_tab.emit(self.mnq_name, "任务完成,未设置后续任务,待机")
            time.sleep(99999)
        else:
            self.dictmap_do(exec_state)

    def select_machine_do(self):
        select_state = self.select.state
        self.sn.table_value.emit(self.mnq_name, 8, f"{GlobalEnumG.StatesInfo[select_state]['name']}")
        self.sn.log_tab.emit(self.mnq_name, f"------{GlobalEnumG.StatesInfo[select_state]['name']}------")
        self.dictmap_do(select_state, 0)

    def dictmap_do(self, state, typeid=1):
        if typeid == 1:
            af_res = self.exec_func[state][0](**self.data_dic)
            if af_res != 0:
                self.exec_func[state][af_res](**self.data_dic)
        else:
            se_res = self.select_func[state][0](**self.data_dic)
            if se_res != 0:
                self.select_func[state][-1](**self.data_dic)

    @staticmethod
    def get_task_time():
        """计算每日任务开始时间"""
        meiri_task_time = LoadConfig.getconf('全局配置', '固定每日时间')
        meiri_time_list = meiri_task_time.split(':')
        meiri_time_h = meiri_time_list[0]
        meiri_time_m = meiri_time_list[-1]
        if int(meiri_time_h) <= 9:
            meiri_time_h = '0' + meiri_time_h
        if int(meiri_time_m) <= 9:
            meiri_time_m = '0' + meiri_time_m
        meiri_time = f" {meiri_time_h}:{meiri_time_m}:00"  # 设定时间
        return meiri_time

    def calculation_gold(self):
        if time.time() - self._c_time > GlobalEnumG.CheckRoleTime:
            self.select_queue.put_queue("CheckGold")
            self._c_time = time.time()
