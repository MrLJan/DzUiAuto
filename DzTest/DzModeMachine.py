# -*- encoding=utf8 -*-
import random
import time

from transitions import Machine
from Enum.ResEnum import ImgEnumG, GlobalEnumG, BatEnumG
from UiPage.AutoBatG import AutoBatG
from UiPage.DailyTaskG import DailyTaskAutoG
from UiPage.LoginUiPage import LoginUiPageG
from UiPage.RewardG import RewardG
from UiPage.StateCheckG import StateCheckG
from UiPage.TaskAutoG import TaskAutoG
from UiPage.TeamStateG import TeamStateG
from UiPage.UpRoleG import UpRoleG
from Utils.Devicesconnect import DevicesConnect
from Utils.LoadConfig import LoadConfig
from Utils.ThreadTools import ThreadTools


class StateExecute(object):
    """状态执行器"""

    def __init__(self, devinfo, mnq_name, sn):
        self.devinfo = devinfo
        self.sn = sn
        self.mnq_name = mnq_name

    def autotask(self, **kwargs):
        return TaskAutoG(self.devinfo, self.mnq_name, self.sn).start_autotask(**kwargs)

    def automr(self, **kwargs):
        return DailyTaskAutoG(self.devinfo, self.mnq_name, self.sn).dailytask_start(**kwargs)

    def autoboos(self, **kwargs):
        return 1

    def autobat(self, **kwargs):
        return AutoBatG(self.devinfo, self.mnq_name, self.sn).keyboard_bat(**kwargs)

    def checkstate(self, **kwargs):
        return TeamStateG(self.devinfo, self.mnq_name, self.sn).check_team_state(**kwargs)

    def nothing(self):
        print('nothing')


class StateSelect(object):
    """状态选择器"""

    def __init__(self, devinfo, mnq_name, sn):
        self.devinfo = devinfo
        self.sn = sn
        self.mnq_name = mnq_name

    def login_game(self, **kwargs):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).start_login(**kwargs)

    def check_ingame(self, **kwargs):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).check_ingame(**kwargs)

    def fuhuo(self):
        return 1

    def buyyao(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).buyyao(**kwargs)

    def bagsell(self, **kwargs):
        return RewardG(self.devinfo, self.mnq_name, self.sn).bagsell(**kwargs)

    def useskill(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).useskill(**kwargs)

    def usepet(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).usepet(**kwargs)

    def upequip(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).upequip(**kwargs)

    def strongequip(self, **kwargs):
        return RewardG(self.devinfo, self.mnq_name, self.sn).get_reward()

    def getreward(self, **kwargs):
        return UpRoleG(self.devinfo, self.mnq_name, self.sn).strongequip(**kwargs)

    def checkxtteam(self, **kwargs):
        return TeamStateG(self.devinfo, self.mnq_name, self.sn).check_xt(**kwargs)

    def checkytteam(self, **kwargs):
        return TeamStateG(self.devinfo, self.mnq_name, self.sn).check_yt(**kwargs)

    def choose_task(self, **kwargs):
        return StateCheckG(self.devinfo, self.mnq_name, self.sn).choose_task(**kwargs)

    def back_ingame(self, **kwargs):
        return LoginUiPageG(self.devinfo, self.mnq_name, self.sn).close_all()


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


# @catch_ex
class switch_case:
    """状态判断"""

    def __init__(self, sn, **kwargs):
        self.exec = kwargs['执行器']
        self.select = kwargs['选择器']
        self.mnq_name = kwargs['机器名']
        self.queue_dic = kwargs['队列']
        self.exec_queue = self.queue_dic['执行器任务队列']
        self.select_queue = self.queue_dic['选择器任务队列']
        self.taskid, self.mapname = self.get_taskid(kwargs['任务名'])
        self.sn = sn
        self.team_id, self.pd_num = self.get_team_id(kwargs['位置信息'])
        self.data_dic = self.get_data_dic()
        self.dotask = {
            1: self.exec
        }
        self.exec_func = {
            'AutoTask': [self.exec.autotask, self.exec.to_Nothing,self.exec.to_AutoTask, self.exec.checkstate],
            'AutoMR': [self.exec.automr, self.exec.to_Nothing, self.exec.to_AutoMR,self.exec.checkstate],
            'AutoBoss': [],
            'AutoBat': [self.exec.autobat, self.exec.to_Nothing,self.exec.to_AutoBat, self.exec.checkstate],
        }
        self.select_func = {
            'InGame': [self.select.choose_task, self.select.to_Login, self.select.to_FuHuo,
                       self.select.to_BuyY, self.select.to_BagSell, self.select.to_UseSkill, self.select.to_UsePet,
                       self.select.to_UpEquip, self.select.to_StrongEquip],
            'Check': [self.select.check_ingame, self.select.to_Check,self.select.to_InGame],
            'Login': [self.select.login_game, self.select.to_Login, self.select.to_Check],
            'FuHuo': [self.select.fuhuo, self.select.to_FuHuo, self.select.to_Check],
            'BuyY': [self.select.buyyao, self.select.to_BuyY, self.select.to_Check],
            'BagSell': [self.select.bagsell, self.select.to_BagSell, self.select.to_Check],
            'UseSkill': [self.select.useskill, self.select.to_UseSkill, self.select.to_Check],
            'UsePet': [self.select.usepet, self.select.to_UsePet, self.select.to_Check],
            'UpEquip': [self.select.upequip, self.select.to_UpEquip, self.select.to_Check],
            'StrongEquip': [self.select.strongequip, self.select.to_StrongEquip, self.select.to_Check],
            'GetReward': [self.select.strongequip, self.select.to_GetReward, self.select.to_Check],
            'CheckXT': [self.select.checkxtteam, self.select.to_CheckXT, self.select.to_Check],
            'CheckYT': [self.select.checkytteam, self.select.to_CheckYT, self.select.to_Check],
        }

    def get_taskid(self, task_name):
        """获取地图和任务id"""
        all_task = BatEnumG.TASK_ID.keys()
        xt_map = BatEnumG.MAP_DATA['3'].keys()
        yt_map = BatEnumG.MAP_DATA['4'].keys()
        if task_name in all_task:
            _id = BatEnumG.TASK_ID[task_name]['id']
            if _id in ['0', '1', '2']:
                self.exec_queue.put_queue(BatEnumG.TASK_ID[task_name]['state'])
            else:
                self.select_queue.put_queue(BatEnumG.TASK_ID[task_name]['state'])
            return BatEnumG.TASK_ID[task_name]['id'], 'NULL'
        elif task_name in xt_map:
            self.exec_queue.put_queue('AutoBat')
            return '3', task_name
        elif task_name in yt_map:
            self.exec_queue.put_queue('AutoBat')
            return '4', task_name
        else:
            raise KeyError("任务名称有误")

    def get_data_dic(self):
        data = {
            '设备名称': self.mnq_name,
            '任务id': self.taskid,
            '地图名': BatEnumG.MAP_OCR[self.mapname][0][-1],
            '状态队列': {
                '执行器':self.exec_queue,
                '选择器':self.select_queue
            },
            '战斗数据': {
                '地图数据': [] if self.taskid not in ['3','4'] else BatEnumG.MAP_DATA[self.taskid][self.mapname],
                '地图识别': BatEnumG.MAP_OCR[self.mapname],
                '无蓝': LoadConfig.getconf('全局配置', '无蓝窗口'),
                '刷图模式': LoadConfig.getconf('全局配置', '扫地模式'),
                '职业类型': LoadConfig.getconf('全局配置', '职业类型'),
                '楼梯队列': self.queue_dic['楼梯队列'],
                '方向队列': self.queue_dic['方向队列']
            },
            '挂机设置': {
                '人少退组': LoadConfig.getconf('全局配置', '人少退组'),
                '定时任务': LoadConfig.getconf('全局配置', '定时任务'),
                '随机休息': LoadConfig.getconf('全局配置', '随机休息')
            },
            '野图设置': {
                '队伍id': self.team_id,
                '队伍频道': self.pd_num,
                '队伍队列': self.queue_dic['队伍队列'][self.team_id],
                '组队密码': LoadConfig.getconf('野图配置', '组队密码')
            },
            '商店设置': {
                'HP等级': LoadConfig.getconf('全局配置', 'hp等级'),
                'HP数量': LoadConfig.getconf('全局配置', 'hp数量'),
                'MP等级': LoadConfig.getconf('全局配置', 'mp等级'),
                'MP数量': LoadConfig.getconf('全局配置', 'mp数量'),
            },
            '每日任务': {
                '任务列表': self.get_mr_task(),
                '每日任务队列': self.queue_dic['每日任务队列']},
            '强化设置': {
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
                      list(LoadConfig().getconf("野图配置", "6队成员").split(','))]
            # ---
            pdnum = [list(LoadConfig().getconf("野图配置", "1队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "2队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "3队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "4队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "5队频道").split(',')),
                     list(LoadConfig().getconf("野图配置", "6队频道").split(','))]
            mnq_index = index_dic['index']
            team_num = ''
            pindao_num = []
            for _me in member:
                if mnq_index == _me:
                    team_num = 'team' + str(member.index(_me))
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

    def change_mapdata(self):
        # self.data_dic[]
        pass

    def get_mr_task(self):
        task_list = []
        task_name = ['武陵', '金字塔', '菁英地城', '每日地城', '进化系统', '次元入侵', '汤宝宝',
                     '迷你地城', '怪物狩猎团', '星光塔', '怪物公园']
        for i in task_name:
            r = LoadConfig.getconf("全局配置", i)
            if r == '1':
                index = str(task_name.index(i) + 1)
                task_list.append(index)
        random.shuffle(task_list)  # 打乱顺序
        return task_list

    def do_case(self):
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

    def exec_machine_do(self):
        exec_state = self.exec.state
        self.sn.table_value.emit(self.mnq_name, 8, f"{GlobalEnumG.StatesInfo[exec_state]['name']}")
        self.sn.log_tab.emit(self.mnq_name, f"------{GlobalEnumG.StatesInfo[exec_state]['name']}------")
        if exec_state == 'Nothing':
            self.sn.table_value.emit(self.mnq_name, 8,"无任务")
            self.sn.log_tab.emit(self.mnq_name,"任务完成,未设置后续任务,待机")
            time.sleep(99999)
        else:
            self.dictmap_do(exec_state)

    def select_machine_do(self):
        select_state = self.select.state
        self.sn.log_tab.emit(self.mnq_name, f"------{GlobalEnumG.StatesInfo[select_state]['name']}------")
        self.dictmap_do(select_state, 0)

    def dictmap_do(self, state, typeid=1):
        if typeid == 1:
            af_res = self.exec_func[state][0](**self.data_dic)
            if af_res != 0:
                self.exec_func[state][af_res](**self.data_dic)
        else:
            self.select_func[state][0](**self.data_dic)
            self.select_func[state][-1](**self.data_dic)
