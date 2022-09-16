# -*- encoding=utf8 -*-
import random
import time

from transitions import Machine, State
from res.ResEnum import ResEnumG, ColorEnumG
from tools.DmPublicTools import DmPublic
from tools.LoadConfig import LoadConfig
from tools.OtherTools import catch_ex, DTools
from tools.QueueManageTools import QueueManage
from tools.ThreadTools import ThreadTools
from uipage.G.AutoKeyG import AutoKeyG
from uipage.G.AutoTeamG import AutoTeamG
from uipage.G.DailyTaskAutoG import DailyTaskAutoG
from uipage.G.GetRewardG import GetRewardG
from uipage.G.LoginAuto import LoginAutoG
from uipage.G.TaskAutoG import TaskAutoToolG


class StateExecute(object):
    """状态执行器"""

    def __init__(self, row_num, dm_obj, sn, mnq_name,task_id,map_id):
        self.dm = dm_obj
        self.row_num = int(row_num)
        self.sn = sn
        self.mnq_name = mnq_name
        self.task_id=task_id
        self.map_id=map_id

    def login_game(self, role_index, is_change_role):
        return LoginAutoG(self.dm, self.sn, self.mnq_name).begin_login(role_index, is_change_role)

    def start_autotask(self,use_stone):
        return TaskAutoToolG(self.dm, self.sn, self.mnq_name).start_autotask(use_stone)

    def back_main(self):
        return GetRewardG(self.dm, self.sn, self.mnq_name).back_mainui()

    def check_game(self):
        return LoginAutoG(self.dm, self.sn, self.mnq_name).check_ingame()

    def start_game(self):
        if LoginAutoG(self.dm, self.sn, self.mnq_name).start_game():
            return True
        return False

    def start_dailytask(self, row_num, is_gonghui, task_queue):
        return DailyTaskAutoG(self.dm, self.sn, self.mnq_name, row_num).dailytask_start(is_gonghui, task_queue)

    def check_zudui(self, map_id, use_mp):
        return AutoKeyG(self.dm, self.sn, self.mnq_name).check_zudui(map_id, use_mp)

    def move_back(self, map_id):
        return AutoKeyG(self.dm, self.sn, self.mnq_name).move_back(map_id)

    def get_pet(self):
        return TaskAutoToolG(self.dm, self.sn, self.mnq_name).get_pet()

    def use_skill(self):
        return TaskAutoToolG(self.dm, self.sn, self.mnq_name).use_skill()

    def level_reward(self):
        return TaskAutoToolG(self.dm, self.sn, self.mnq_name).level_reward()

    def set_new_game(self):
        return GetRewardG(self.dm, self.sn, self.mnq_name).set_new_game()

    def open_box(self):
        return GetRewardG(self.dm, self.sn, self.mnq_name).open_box()

    def choose_equip(self):
        return GetRewardG(self.dm, self.sn, self.mnq_name).choose_equip()

    def upgrade_equip(self):
        return GetRewardG(self.dm, self.sn, self.mnq_name).upgrade_equip()

    def buy_yaoshui(self, use_mp):
        return AutoKeyG(self.dm, self.sn, self.mnq_name).check_yaoshui(use_mp)

    def choose_team(self, map_id, is_exit_team):
        return AutoKeyG(self.dm, self.sn, self.mnq_name).choose_team(map_id, is_exit_team)

    def start_auto(self, open_auto, map_louti, map_louti2, map_max_y, zhiye_id, use_mp):
        return AutoKeyG(self.dm, self.sn, self.mnq_name).auto_battle(open_auto, map_louti, map_louti2, map_max_y,
                                                                     zhiye_id, use_mp)

    def autotime(self, is_exitgame, use_auto):
        return AutoTeamG(self.dm, self.sn, self.mnq_name,self.task_id,self.map_id).auto_team(is_exitgame, use_auto)

    def autokeyboard(self, map_louti, map_louti2, map_louti3, louti_gailv, zhiye_id, use_mp, team_queue, is_exit_team,
                     task_id, auto_wait, saodi_mode, louti_queue, turn_queue):
        return AutoTeamG(self.dm, self.sn, self.mnq_name,self.task_id,self.map_id).keyboard_team(map_louti, map_louti2, map_louti3, louti_gailv,
                                                                        zhiye_id, use_mp, team_queue, is_exit_team,
                                                                        task_id, auto_wait, saodi_mode, louti_queue,
                                                                        turn_queue)

    def bag_soul(self):
        return AutoKeyG(self.dm, self.sn, self.mnq_name).bag_soul()

    def check_zuduiteam(self, use_mp, map_id, team_queue, team_event):
        return AutoTeamG(self.dm, self.sn, self.mnq_name,self.task_id,self.map_id).check_zuduiteam(use_mp, map_id, team_queue, team_event
                                                                          )

    def nothing_unbindwindows(self):
        return self.dm.UnBindWindow()

    def check_map(self):
        return AutoTeamG(self.dm, self.sn, self.mnq_name,self.task_id,self.map_id).check_map()

    def check_pindao(self, pindao_num):
        return AutoTeamG(self.dm, self.sn, self.mnq_name,self.task_id,self.map_id).check_pindao(pindao_num)

    def exit_team(self):
        return

    def creat_team(self, team_pwd, team_event, team_queue):
        return AutoTeamG(self.dm, self.sn, self.mnq_name,self.task_id,self.map_id).creat_team(team_pwd, team_event, team_queue)

    def choose_yetu(self, team_pwd, team_queue):
        return AutoTeamG(self.dm, self.sn, self.mnq_name,self.task_id,self.map_id).choose_yetu(team_pwd, team_queue)

    def gold_num(self):
        return LoginAutoG(self.dm, self.sn, self.mnq_name).gold_num()

    def get_zhanli(self):
        return DmPublic.check_zhanli_num(self.dm)

    def get_level(self):
        return DmPublic.check_level_num(self.dm)

    def close_all_windows(self):
        return LoginAutoG(self.dm, self.sn, self.mnq_name).close_all_windows()

    def close_game(self):
        return LoginAutoG(self.dm, self.sn, self.mnq_name).clear_game()

    def boss_map(self, row_num, boss_index, role_level, is_hd_boss):
        return DailyTaskAutoG(self.dm, self.sn, self.mnq_name, row_num).do_boss_map(boss_index, role_level, is_hd_boss)

    def check_equip(self):
        return TaskAutoToolG(self.dm, self.sn, self.mnq_name).check_equip()

    def open_bag(self):
        return TaskAutoToolG(self.dm, self.sn, self.mnq_name).open_bag()

    def ingame_change_role(self, role_index):
        return LoginAutoG(self.dm, self.sn, self.mnq_name).ingame_change_role(role_index)
    # def fuhuo(self, map_id):
    #     if self.back_main():
    #         self.buy_yaoshui()
    #         self.check_map(map_id)
    #         return True
    #     else:
    #         self.check_game()


class StateMachine:
    """状态控制器"""
    state_list = [
        State(name='InGame'),
        State(name='NotInGame'),
        State(name='Login'),
        State(name='Check'),
        State(name='CheckZuDui'),
        State(name='CheckTeam'),
        State(name='AutoTask'),
        State(name='DailyTask'),
        State(name='AutoBat'),
        State(name='AutoTeam'),
        State(name='Nothing'),
        State(name='CheckMap'),
        State(name='CheckPinDao'),
        State(name='CreatTeam', on_enter='back_main'),
        State(name='ChooseTeam'),
        State(name='FuHuo'),
        State(name='FuhuoAuto'),
        State(name='BuyYao'),
        State(name='MoveBack'),
        State(name='AutoTime'),
        State(name='AutoKeyBoard'),
        State(name='BossBattle'),
        State(name='GetLevelReward'),
        State(name='NewCount'),
        State(name='ChangeRole')

    ]
    transition_list = [
        {'trigger': 'trigger_login_game', 'source': 'Login', 'dest': 'InGame', "conditions": "login_game"},
        {'trigger': 'trigger_start_autotask', 'source': '*', 'dest': 'AutoTask'},
        {'trigger': 'trigger_start_dailytask', 'source': '*', 'dest': 'DailyTask'},
        {'trigger': 'trigger_start_auto', 'source': 'InGame', 'dest': 'AutoBat'},
        {'trigger': 'trigger_back_main', 'source': '*', 'dest': 'InGame', "conditions": "back_main"},
        {'trigger': 'trigger_check_game', 'source': '*', 'dest': 'NotInGame', "conditions": "check_game"},
        {'trigger': 'trigger_start_game', 'source': 'NotInGame', 'dest': 'Login', "conditions": "start_game"},
        {'trigger': 'trigger_start_autoteam', 'source': 'InGame', 'dest': 'AutoTeam'},
        {'trigger': 'trigger_check_zudui', 'source': 'InGame', 'dest': 'CheckZuDui'},
        {'trigger': 'trigger_check_team', 'source': 'InGame', 'dest': 'CheckTeam'},
        {'trigger': 'trigger_boos_battle', 'source': '*', 'dest': 'BossBattle'},
        {'trigger': 'trigger_new_count', 'source': '*', 'dest': 'NewCount'},
        {'trigger': 'trigger_to_Nothing', 'source': '*', 'dest': 'Nothing'}

    ]

    def __init__(self, model, init_state):
        self.machine = Machine(model, states=self.state_list, transitions=self.transition_list, initial=init_state)


# @catch_ex
class switch_case:
    """状态判断"""
    @catch_ex
    def __init__(self, dev, exec_model, mnq_thread_list, task_id, row_num, mnq_index ,task_queue, map_id=0,sn=None):
        pass

    def do_case(self):
        now_state = self.modle.state
        state_name = ResEnumG.state_name.value
        if now_state == "NotInGame":
            pass
        if now_state == "Login":
            pass
        if now_state == "Check":
            pass
if __name__ == '__main__':
    pass


