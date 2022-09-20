# -*- encoding=utf8 -*-
import random
import time

from transitions import Machine, State
from Enum.ResEnum import ImgEnumG, GlobalEnumG
from UiPage.LoginUiPage import LoginUiPageG
from UiPage.TaskAutoG import TaskAutoG
from Utils.Devicesconnect import DevicesConnect
from Utils.ThreadTools import check_mnq_thread, ThreadTools


class StateExecute(object):
    """状态执行器"""

    def __init__(self, devinfo,mnq_name,sn):
        self.devinfo = devinfo
        self.sn=sn
        self.mnq_name=mnq_name

    def autotask(self):
        return TaskAutoG(self.devinfo,self.mnq_name,self.sn).start_autotask()

    def automr(self):
        print('automr')

    def autobat(self):
        print('autobat')

    def checkstate(self):
        return LoginUiPageG(self.devinfo,self.mnq_name,self.sn).check_ingame()

    def nothing(self):
        print('nothing')


class StateSelect(object):
    """状态选择器"""

    def __init__(self, devinfo,mnq_name,sn):
        self.devinfo = devinfo
        self.sn=sn
        self.mnq_name=mnq_name

    def login_game(self):
        return LoginUiPageG(self.devinfo,self.mnq_name,self.sn).start_login()

    def check(self):
        return LoginUiPageG(self.devinfo,self.mnq_name,self.sn).check_ingame()

    def choose_task(self):
        return 0


execute_transition = [
    {'trigger': 'Exe_Nothing', 'source': '*', 'dest': 'Nothing'},
    {'trigger': 'Exe_CheckState', 'source': '*', 'dest': 'CheckState'},
]
select_transition = [
    {
        'trigger': 'Slt_Login_InGame', 'source': 'Login', 'dest': 'InGame', "conditions": "login_game"
    }
]


class StateMachine:
    """状态控制器"""

    def __init__(self, model, states, transitions, init_state):
        self.machine = Machine(model, states=states, transitions=transitions, initial=init_state)


# @catch_ex
class switch_case:
    """状态判断"""

    def __init__(self, exec_model, sele_model, mnq_name,taskid, mapid, sn):
        self.exec = exec_model
        self.select = sele_model
        self.mnq_name=mnq_name
        self.taskid = taskid
        self.sn = sn
        self.dotask = {
            1: exec_model
        }
        self.mapid = mapid
        self.exec_func = {
            'AutoTask': [self.exec.autotask, self.exec.Exe_CheckState],
            'AutoMR': [self.exec.automr, self.exec.Exe_CheckState],
            'AutoBat': [self.exec.autobat, self.exec.Exe_CheckState],
            'CheckState': [self.exec.checkstate, self.select.to_Check]
        }
        self.select_func = {
            'Login': [self.select.login_game, self.select.to_Check, self.select.to_InGame],
            'Check': [self.select.check, self.select.to_Login,self.select.to_InGame],
            'InGame': [self.select.choose_task]
        }

    def do_case(self):
        select_state = self.select.state
        if select_state != "InGame":
            self.select_machine_do()
        else:
            self.exec_machine_do()

    def exec_machine_do(self):
        exec_state = self.exec.state
        self.sn.table_value.emit(self.mnq_name, 8, f"{GlobalEnumG.States[exec_state]}")
        print(f"exec_machine_do{GlobalEnumG.States[exec_state]}")
        self.dictmap_do(exec_state)

    def select_machine_do(self):
        select_state = self.select.state
        print(f"select_state{GlobalEnumG.States[select_state]}")
        self.dictmap_do(select_state, 0)

    def dictmap_do(self, state, typeid=1):
        if typeid == 1:
            af_res = self.exec_func[state][0]()
            print(af_res)
            time.sleep(3)
            self.exec_func[state][af_res]()
        else:
            af_res = self.select_func[state][0]()
            print(af_res)
            time.sleep(3)
            self.select_func[state][af_res]()


if __name__ == '__main__':
    DevicesConnect('emulator-5554').connect_device()
    execute = StateExecute()
    select = StateSelect()
    mnq_thread_list = []
    StateMachine(execute, GlobalEnumG.ExecuteStates, execute_transition, "AutoTask")
    StateMachine(select, GlobalEnumG.SelectStates, select_transition, "Login")
    t1 = ThreadTools('t1', switch_case(execute, select, 1, 1).do_case)
    t1.start()
    # t1.join()
    # check_mnq_thread(f"t1", mnq_thread_list,switch_case(execute,select,1,1).do_case,thread_while=True)
