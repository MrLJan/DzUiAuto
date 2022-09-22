# -*- encoding=utf8 -*-
import sys
import time

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer

from DzTest.DzModeMachine import switch_case, StateExecute, StateMachine, StateSelect, execute_transition, \
    select_transition
from Utils.LoadConfig import LoadConfig
from Utils.MnqTools import MnqTools
from Utils.OtherTools import OT, catch_ex
from Utils.QtSignals import QtSignals
from Utils.QueueManageTools import QueueManage
from Utils.ThreadTools import ThreadTools, check_mnq_thread
from Utils.AdbUtils import PhoneDevives
from Enum.ResEnum import GlobalEnumG
from Utils.Devicesconnect import DevicesConnect


class DzUi:
    def __init__(self):
        self.ui_main = uic.loadUi(OT.abspath('/QtUI/dzmain.ui'))
        self.ui_main.setWindowTitle(f"岛主-{2.0}_认证群号：795973610 自助提卡网：www.huoniu.buzz")
        self.ui_main.setWindowIcon(QtGui.QIcon(OT.abspath("/res/dz_icon.ico")))
        # 禁止窗口拉伸
        self.ui_main.setFixedSize(self.ui_main.width(), self.ui_main.height())
        # # 获取句柄窗口按钮
        self.ui_main.get_windows.clicked.connect(self._get_windows_pid)
        # # 开启/关闭模拟器按钮
        # self.ui_main.start_mnq_all_btn.clicked.connect(lambda: self.mnq_start_quit(True))
        # self.ui_main.quit_mnq_all_btn.clicked.connect(lambda: self.mnq_start_quit(False))
        # self.ui_main.open_index_mnq_btn.clicked.connect(self.start_mnq_index)
        # # self.ui_main.start_mnq_all_btn.setEnabled(False)
        # # self.ui_main.quit_mnq_all_btn.setEnabled(False)
        # # 全选,取消选中,执行选中,停止选中
        # self.ui_main.choose_stop_btn.clicked.connect(self.stop_choose)
        # self.ui_main.choose_all_btn.clicked.connect(self.choose_all)
        # self.ui_main.choose_cannel_btn.clicked.connect(self.cannel_choose)
        # self.ui_main.choose_todo_btn.clicked.connect(self.todo_choose)
        # # 延时启动
        # self.ui_main.yanshi_btn.clicked.connect(self.yanshi_todo_choose)
        # # 滚模拟器
        # self.ui_main.roll_mnq_btn.clicked.connect(self.roll_mnq_dotask)
        # # 任务树
        # self.set_tasktree(self.ui_main.task_tree_widget)
        # self.ui_main.set_task_btn.clicked.connect(self._set_task_list)
        # self.ui_main.add_diy_task1_btn.clicked.connect(self.add_diy_task1_btn)
        # self.ui_main.add_diy_task2_btn.clicked.connect(self.add_diy_task2_btn)
        # # 停止/打开配置
        # self.ui_main.close_all_task_btn.clicked.connect(self.close_all_task)
        # self.ui_main.open_set_btn.clicked.connect(self.open_set)
        # # 窗口排序
        # self.ui_main.win_index_btn.clicked.connect(self.windows_index)
        # ---------------设置界面-------------------
        # self.ui_main.hwnd_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,99}")))
        # self.ui_main.skip_mnqindex_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,99}")))
        # self.ui_main.team_pwd_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,4}")))
        # self.ui_main.auto_time_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.task_level_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.qh_level_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,2}")))
        # self.ui_main.zhiye_edit.setValidator(QRegExpValidator(QRegExp("[0-9,]+$")))
        # self.ui_main.d_use_mp_edit.setValidator(QRegExpValidator(QRegExp("[0-9,]+$")))
        # self.ui_main.start_mnq_index_edit.setValidator(QRegExpValidator(QRegExp("[0-9,]+$")))
        # self.ui_main.d1_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        # self.ui_main.d2_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        # self.ui_main.d3_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        # self.ui_main.d4_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        # self.ui_main.d5_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        # self.ui_main.d6_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        # self.ui_main.d1_pindao_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.d2_pindao_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.d3_pindao_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.d4_pindao_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.d5_pindao_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.d6_pindao_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        # self.ui_main.get_gold_time_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,99}")))
        # 设置保存按钮
        # self.ui_main.save_setting_btn.clicked.connect(self.save_setting)
        # self.ui_main.save_setting_btn_2.clicked.connect(self.save_setting)
        # self.set_setting_label(self.ui_main.line_mnqpath, "路径", "模拟器路径")
        # self.set_lineedit_text(self.ui_main.start_mnq_index_edit, "全局配置", "启动模拟器序号")
        # self.set_lineedit_text(self.ui_main.auto_time_edit, "全局配置", "离线时长")
        # self.set_lineedit_text(self.ui_main.autobat_time_edit, "全局配置", "挂机卡时长")
        # self.set_lineedit_text(self.ui_main.qh_level_edit, "全局配置", "强化等级")
        # self.set_lineedit_text(self.ui_main.task_level_edit, "全局配置", "任务停止等级")
        # self.set_lineedit_text(self.ui_main.zhiye_edit, "野图配置", "短按窗口")
        # self.set_lineedit_text(self.ui_main.d_use_mp_edit, "全局配置", "无蓝窗口")
        # self.set_lineedit_text(self.ui_main.autobat_time_edit, "全局配置", "挂机卡时长")
        # self.set_lineedit_text(self.ui_main.team_pwd_edit, "野图配置", "组队密码")
        # self.set_lineedit_text(self.ui_main.diy_task1_edit, "全局配置", "自定义一")
        # self.set_lineedit_text(self.ui_main.diy_task2_edit, "全局配置", "自定义二")
        # self.set_lineedit_text(self.ui_main.d1_duiyuan_edit, "野图配置", "1队成员")
        # self.set_lineedit_text(self.ui_main.d2_duiyuan_edit, "野图配置", "2队成员")
        # self.set_lineedit_text(self.ui_main.d3_duiyuan_edit, "野图配置", "3队成员")
        # self.set_lineedit_text(self.ui_main.d1_pindao_edit, "野图配置", "1队频道")
        # self.set_lineedit_text(self.ui_main.d2_pindao_edit, "野图配置", "2队频道")
        # self.set_lineedit_text(self.ui_main.d3_pindao_edit, "野图配置", "3队频道")
        # self.set_lineedit_text(self.ui_main.get_gold_time_edit, "全局配置", "检查产出")
        # self.set_zhiyebox_text(self.ui_main.zhiye_choose_box, "全局配置", "职业类型")
        # self.set_check_box_text(self.ui_main.is_exitgame_box, "全局配置", "离线使用挂机卡")
        # self.set_check_box_text(self.ui_main.is_exit_team_box, "全局配置", "人少退组")
        # self.set_check_box_text(self.ui_main.is_change_role_box, "全局配置", "自动切换角色")
        # self.set_check_box_text(self.ui_main.pkj_box, "全局配置", "混皮卡啾")
        # self.set_check_box_text(self.ui_main.nh_box, "全局配置", "混女皇")
        # self.set_check_box_text(self.ui_main.hd_boss_box, "全局配置", "混沌炎魔")
        # self.set_check_box_text(self.ui_main.close_game_box, "全局配置", "任务结束关闭游戏")
        # self.set_check_box_text(self.ui_main.gonghui_box, "全局配置", "公会内容")
        # self.set_check_box_text(self.ui_main.boss_check_box, "全局配置", "混王图")
        # self.set_check_box_text(self.ui_main.meiti_check_box, "全局配置", "定时任务")
        # self.set_check_box_text(self.ui_main.open_auto_box, "全局配置", "混合自动按键")
        # self.set_check_box_text(self.ui_main.wulin_box, "全局配置", "武陵")
        # self.set_check_box_text(self.ui_main.jinzita_box, "全局配置", "金字塔")
        # self.set_check_box_text(self.ui_main.jinghua_box, "全局配置", "进化系统")
        # self.set_check_box_text(self.ui_main.jingying_box, "全局配置", "菁英地城")
        # self.set_check_box_text(self.ui_main.startower_box, "全局配置", "星光塔")
        # self.set_check_box_text(self.ui_main.gw_park_box, "全局配置", "怪物公园")
        # self.set_check_box_text(self.ui_main.meiri_box, "全局配置", "每日地城")
        # self.set_check_box_text(self.ui_main.ciyuan_box, "全局配置", "次元入侵")
        # self.set_check_box_text(self.ui_main.guaiwu_box, "全局配置", "怪物狩猎团")
        # self.set_check_box_text(self.ui_main.tangbaobao_box, "全局配置", "汤宝宝")
        # self.set_check_box_text(self.ui_main.mini_dc_box, "全局配置", "迷你地城")
        # self.set_check_box_text(self.ui_main.qh_youhui_box, "全局配置", "强化优惠卷")
        # self.set_check_box_text(self.ui_main.xinyun_box, "全局配置", "幸运卷轴")
        # self.set_check_box_text(self.ui_main.dunpai_box, "全局配置", "盾牌卷轴")
        # self.set_check_box_text(self.ui_main.baohu_box, "全局配置", "保护卷轴")
        # self.set_check_box_text(self.ui_main.auto_wait_box, "全局配置", "随机休息")
        # self.set_check_box_text(self.ui_main.saodi_box, "全局配置", "扫地模式")
        # self.set_check_box_text(self.ui_main.use_stone_box, "全局配置", "随机使用石头")
        # self.set_combobox_text(self.ui_main.mode_choose_box, "路径", "绑定模式")
        # self.set_combobox_text(self.ui_main.hp_box, "全局配置", "HP等级")
        # self.set_combobox_text(self.ui_main.mp_box, "全局配置", "MP等级")
        # self.set_radio_btn(self.ui_main.radioButton, '全局配置', '离线休息')
        # self.set_radio_btn(self.ui_main.radioButton2, '全局配置', '在线休息')
        #
        # # 设置定时
        # self.set_meiri_time_box(self.ui_main.meiri_time_box, "全局配置", "固定每日时间", True)
        # self.set_meiri_time_box(self.ui_main.fenz_box, "全局配置", "固定每日时间", False)
        # dm 设置tablewidget
        self.ui_main.windows_pid.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭水平进度条
        # self.ui_main.windows_pid.doubleClicked.connect(self.windows_click)
        # self.ui_main.windows_pid.itemClicked.connect(self.item_choose)
        self.ui_main.windows_pid.setColumnCount(12)  # 设置列数
        self.ui_main.windows_pid.setColumnWidth(0, 40)
        self.ui_main.windows_pid.setColumnWidth(1, 95)
        self.ui_main.windows_pid.setColumnWidth(2, 70)
        self.ui_main.windows_pid.setColumnWidth(3, 60)
        self.ui_main.windows_pid.setColumnWidth(4, 60)
        self.ui_main.windows_pid.setColumnWidth(5, 90)
        self.ui_main.windows_pid.setColumnWidth(6, 75)
        self.ui_main.windows_pid.setColumnWidth(7, 75)
        self.ui_main.windows_pid.setColumnWidth(8, 90)
        self.ui_main.windows_pid.setColumnWidth(9, 100)
        self.ui_main.windows_pid.setColumnWidth(10, 75)
        self.ui_main.windows_pid.setColumnWidth(11, 90)
        self.ui_main.windows_pid.setShowGrid(False)

        # 重定向print输出信号
        self.sn = QtSignals()  # 初始化信号类
        sys.stdout = QtSignals(text_signal=self.console_output)
        sys.stderr = QtSignals(text_signal=self.console_output)

        self.sn.message_box.connect(self.get_messagebox)  # 弹窗消息信号
        self.sn.label_text.connect(self.set_label_text)  # 版本号label信号
        self.sn.windows_pid.connect(self.set_windows_pid)  # 窗口句柄信号
        self.sn.table_value.connect(self.set_table_value)  # 更改单元格状态栏文本
        # self.sn.task_over_signal.connect(self.roll_mnq_dotask)
        # self.sn.close_mnq_index.connect(self.close_taskover_mnq)  # 关闭无任务模拟器
        # self.sn.btn_enable.connect(self.set_btn_enable)
        self.sn.log_tab.connect(self.log_tab_output)  # 输出窗口日志
        self.log_tab_dic = {}  # 存储窗口日志edit组件
        self.start_btn_dic = {}  # 存储窗口开始按钮
        self.stop_btn_dic = {}  # 存储窗口关闭按钮
        self.btn_widget_dic = {}  # 存储窗口按钮布局
        self.mnq_rownum_dic = {}  # 存储窗口行号
        self.mnq_name_old_list = []  # 存储旧窗口名
        self.mnq_name_pop_list = []  # 存储需要删除的窗口
        self.mnq_name_flag = None
        self.dev_obj_list = {}  # 初始化每个模拟器的连接对象
        self.mnq_thread_tid = {}  # 存储每个模拟器的线程tid
        # self.ui_main.filechoose_btn.clicked.connect(self.choose_mnq_file)
        self.get_time = 5
        self.get_timer = QTimer()
        self.get_timer.setInterval(1000)
        self.get_timer.timeout.connect(self.timer_refresh)
        self.stop_time = 15
        self.stop_timer = QTimer()
        self.stop_timer.setInterval(1000)
        # self.stop_timer.timeout.connect(self.close_btnrefresh)
        self.mnq_timer_time = 10
        self.mnq_timer = QTimer()
        self.index_queue = QueueManage()
        self.mnq_timer.setInterval(1000)
        # self.mnq_timer.timeout.connect(self.open_mnq_dotask)
        self.roll_mnq_time = 10
        self.roll_mnq_timer = QTimer()
        self.roll_mnq_queue = QueueManage()
        self.roll_mnq_timer.setInterval(1000)

        # self.team_event_dic = self.get_team_event()
        # self.team_queue_dic = self.get_team_queue()

    #
    @staticmethod
    def set_tableitem_center(item):
        """初始化单元格写入文本"""
        ritem = QTableWidgetItem(str(item))  # 设置写入文本
        ritem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 文本居中对齐
        return ritem

    @staticmethod
    def set_label_text(label_obj, text):
        """设置标签文本内容"""
        label_obj.setText(text)

    def set_table_value(self, mnq_name, col_num, value):
        """设置table单元格值"""
        try:
            row_num = self.mnq_rownum_dic[mnq_name]
            self.ui_main.windows_pid.setItem(row_num, col_num, self.set_tableitem_center(value))
        except Exception as e:
            print(e)

    def get_messagebox(self, title, text):
        """消息弹窗"""
        QMessageBox.information(self.ui_main, title, text)

    def table_btn_row(self):
        """生成列表按钮组件"""
        widget = QWidget()
        start_task_btn = QPushButton('启动')  # 启动
        stop_task_btn = QPushButton('停止')  # 停止
        start_task_btn.clicked.connect(self.start_task_row)
        stop_task_btn.clicked.connect(self.stop_task_row)
        hLayout = QHBoxLayout()
        hLayout.addWidget(start_task_btn)
        hLayout.addWidget(stop_task_btn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget, start_task_btn, stop_task_btn

    def index_check_box(self, index):
        """生成列表序号勾选框"""
        checkbox = QtWidgets.QCheckBox(str(index))
        checkbox.setCheckState(Qt.Checked)
        return checkbox

    def start_task_row(self):
        """
        列表开始按钮点击事件
        """
        try:
            button = self.ui_main.windows_pid.sender()
            if button:  # 确定位置
                row_num = self.ui_main.windows_pid.indexAt(button.parent().pos()).row()
                mnq_index = str(self.ui_main.windows_pid.cellWidget(row_num, 0).text())
                mnq_name = self.ui_main.windows_pid.item(row_num, 1).text()
                task_name = self.ui_main.windows_pid.item(row_num, 2).text()
                # serialno = self.dev_obj_list[mnq_name]

                # if serialno is None:
                #     self.get_messagebox("错误", f"模拟器{mnq_name}未启动或模拟器名称异常")
                # else:
                if task_name == "":
                    self.get_messagebox("错误", f"模拟器序号[{mnq_index}]未设置执行任务")
                else:
                    if len(self.mnq_thread_tid[mnq_name]) == 0:
                        self.start_btn_dic[mnq_name].setEnabled(False)

                        # def run():
                        self._do_task_list([mnq_index])

                        # ThreadTools('', run).start()
                        self.stop_btn_dic[mnq_name].setEnabled(True)
                    else:
                        self.get_messagebox("错误", f"模拟器序号[{mnq_index}]之前的任务还在停止中,等待几秒后重试")
        except Exception as e:
            print(e)

    def stop_task_row(self):
        """列表停止按钮点击事件"""

        def _stop():
            ThreadTools.stop_thread_list(mnq_thread_list)  # 利用tid关闭线程
            mnq_thread_list.clear()

        button = self.ui_main.windows_pid.sender()
        if button:  # 确定位置
            row_num = self.ui_main.windows_pid.indexAt(button.parent().pos()).row()
            mnq_name = self.ui_main.windows_pid.item(row_num, 1).text()
            mnq_thread_list = self.mnq_thread_tid[mnq_name]
            # if :
            if not ThreadTools.is_threadname('停止任务', mnq_thread_list):
                if len(mnq_thread_list) > 0:
                    # dm_obj = self.dev_obj_list[mnq_name][0]
                    self.stop_btn_dic[mnq_name].setEnabled(False)
                    t1 = ThreadTools(f'{mnq_name}停止', _stop)
                    t1.start()
                    self.sn.table_value.emit(mnq_name, 7, "")
                    self.start_btn_dic[mnq_name].setEnabled(True)

    def console_output(self, text):
        """主进程日志输出"""
        cursor = self.ui_main.console_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.ui_main.console_text.setTextCursor(cursor)
        self.ui_main.console_text.ensureCursorVisible()

    def log_tab_output(self, tab_name, text):
        """单线程日志输出"""
        # print(tab_name)
        now_time = time.strftime("%m-%d %H:%M:%S", time.localtime())
        edit = self.log_tab_dic[tab_name]
        if text == 'clear':
            edit.clear()
        else:
            cursor = edit.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(f"[{now_time}]{text}\n")
            # edit.insertPlainText(text)
            edit.setTextCursor(cursor)
            edit.ensureCursorVisible()

    def _do_task_list(self, index_list, message=True):
        """启动任务"""
        for mnq_index in index_list:
            mnq_name = MnqTools().use_index_find_name(mnq_index)
            try:
                row_num = int(self.mnq_rownum_dic[mnq_name])
                self.ui_main.windows_pid.cellWidget(row_num, 0).setChecked(False)
            except BaseException as e:
                self.get_messagebox("错误", f"模拟器信息异常,启动失败{e}")
                return False
            task_name = self.ui_main.windows_pid.item(row_num, 2).text()
            # mnq_index = int(self.ui_main.windows_pid.cellWidget(row_num, 0).text())
            if task_name == "":
                if message:
                    self.get_messagebox("错误", f"模拟器序号[{mnq_index}]未设置执行任务")
                return False
            else:
                devname = self.dev_obj_list[mnq_name][0]
                res, dev = DevicesConnect(devname).connect_device()
                if not res:
                    self.get_messagebox("错误", f"模拟器序号[{mnq_index}]连接失败{dev}_检查adb")
                    return False
                devinfo=(dev,devname)
                mnq_name = self.ui_main.windows_pid.item(row_num, 1).text()
                mnq_thread_list = self.mnq_thread_tid[mnq_name]
                login_time = time.strftime('%m-%d %H:%M:%S')
                LoadConfig.writeconf(mnq_name, '最近登录时间', login_time, ini_name=mnq_name)
                LoadConfig.writeconf(mnq_name, '最近任务', task_name, ini_name=mnq_name)
                self.sn.table_value.emit(mnq_name, 9, login_time)
                self.sn.table_value.emit(mnq_name, 10, '0')
                self.sn.log_tab.emit(mnq_name, '--------启动任务--------')
                execute = StateExecute(devinfo,mnq_name,self.sn)
                select = StateSelect(devinfo,mnq_name,self.sn)
                StateMachine(execute, GlobalEnumG.ExecuteStates, execute_transition, "AutoTask")
                StateMachine(select, GlobalEnumG.SelectStates, select_transition, "Login")
                check_mnq_thread(f"{mnq_name}_{task_name}", mnq_thread_list,
                                 switch_case(execute, select,mnq_name, 1, 1, self.sn).do_case, thread_while=True)

    def _get_windows_pid(self):
        """获取设备信息"""

        def ldconsole_find_dev():
            mnq_index_list, mnq_name_list, mnq_devname_list = MnqTools().get_mnq_list()
            print(mnq_index_list, mnq_name_list, mnq_devname_list)
            self.sn.windows_pid.emit(self.ui_main.windows_pid, mnq_index_list, mnq_name_list, mnq_devname_list)

        def phone_devices():
            devindex_list, pinfo_list, dev_name_list = PhoneDevives().get_devices()
            self.sn.windows_pid.emit(self.ui_main.windows_pid, devindex_list, pinfo_list, dev_name_list)

        try:
            if self.ui_main.get_windows.isEnabled():
                self.get_timer.start()
                self.ui_main.get_windows.setEnabled(False)
            print()
            ld_thread = ThreadTools("获取模拟器窗口句柄", ldconsole_find_dev)
            ld_thread.start()
        except Exception as e:
            print(e)

    @catch_ex
    def set_windows_pid(self, table_object, index_list, pinfo_list, devname_list):
        """
        设置窗口标题，句柄，pid,设备名
        组件名：windows_pid
        """
        pop = []
        old = []
        new = []
        for i in range(1, len(index_list)):
            table_object.removeRow(i)
        table_object.setRowCount(len(index_list))  # 设置行数
        num = len(index_list)
        if len(self.mnq_name_old_list) > 0:
            for mnq_name in self.mnq_name_old_list:
                if mnq_name not in pinfo_list:
                    pop.append(mnq_name)
            for mnq_name in pinfo_list:
                if mnq_name in self.mnq_name_old_list:
                    old.append(mnq_name)
                else:
                    new.append(mnq_name)
                    self.mnq_name_old_list.append(mnq_name)
            if len(pop) > 0:
                for mnq_name in pop:
                    self.ui_main.log_tab_wid.removeTab(self.mnq_rownum_dic[mnq_name])
        if len(self.mnq_name_old_list) == 0:
            for i in range(num):
                self.mnq_name_old_list.append(pinfo_list[i])
        else:
            self.mnq_name_old_list.clear()
            self.mnq_name_old_list = new + old
        for i in range(num):
            # print(f"+++{i}")
            # self.mnq_name_old_list.append(title_list[i])
            self.mnq_rownum_dic[pinfo_list[i]] = i
        for i in range(num):  # 写入单元格
            btn_widget, start_btn, stop_btn = self.table_btn_row()
            self.start_btn_dic[pinfo_list[i]] = start_btn
            self.stop_btn_dic[pinfo_list[i]] = stop_btn
            self.btn_widget_dic[pinfo_list[i]] = btn_widget
            table_object.setCellWidget(i, 11, btn_widget)  # 在单元格中加入启动、停止按钮
            table_object.setCellWidget(i, 0, self.index_check_box(index_list[i]))  # 序号
            table_object.setItem(i, 1, self.set_tableitem_center(pinfo_list[i]))  # 窗口标题
            table_object.setItem(i, 2, self.set_tableitem_center(
                LoadConfig.getconf(pinfo_list[i], '最近任务', ini_name=pinfo_list[i])))  # 执行任务
            table_object.setItem(i, 3, self.set_tableitem_center(
                LoadConfig.getconf(pinfo_list[i], '等级', ini_name=pinfo_list[i])))  # 等级
            table_object.setItem(i, 4, self.set_tableitem_center(
                LoadConfig.getconf(pinfo_list[i], '星力', ini_name=pinfo_list[i])))  # 星力
            table_object.setItem(i, 5, self.set_tableitem_center(
                LoadConfig.getconf(pinfo_list[i], '战力', ini_name=pinfo_list[i])))  # 战力
            table_object.setItem(i, 6, self.set_tableitem_center(
                LoadConfig.getconf(pinfo_list[i], '金币', ini_name=pinfo_list[i])))  # 金币
            table_object.setItem(i, 7,
                                 self.set_tableitem_center(
                                     LoadConfig.getconf(pinfo_list[i], '产金量', ini_name=pinfo_list[i])))  # 产金量
            table_object.setItem(i, 8, self.set_tableitem_center(''))  # 状态
            table_object.setItem(i, 9,
                                 self.set_tableitem_center(
                                     LoadConfig.getconf(pinfo_list[i], '最近登录时间', ini_name=pinfo_list[i])))  # 最近登录时间
            table_object.setItem(i, 10, self.set_tableitem_center('0'))  # 闪退次数

            if pinfo_list[i] in self.mnq_thread_tid.keys():
                if len(self.mnq_thread_tid[pinfo_list[i]]) != 0:
                    start_btn.setEnabled(False)
                    stop_btn.setEnabled(True)
                else:
                    start_btn.setEnabled(True)
                    stop_btn.setEnabled(False)
                # stop_btn.setEnabled(True)
            else:
                start_btn.setEnabled(True)
                stop_btn.setEnabled(False)
                # print(start_btn.isEnabled())
            # 在单元格中加入启动、停止按钮

            self.mnq_rownum_dic[pinfo_list[i]] = i
            # print(self.log_tab_dic)
            if pinfo_list[i] in self.log_tab_dic.keys():
                pass
            else:
                try:
                    wd = QtWidgets.QWidget()
                    ed = QtWidgets.QTextEdit()
                    ed.setReadOnly(True)
                    layout = QVBoxLayout()
                    layout.addWidget(ed)
                    self.log_tab_dic[pinfo_list[i]] = ed
                    wd.setLayout(layout)
                    self.ui_main.log_tab_wid.insertTab(i, wd, f"窗口{index_list[i]}")
                except BaseException as e:
                    # DTools.error_log(e)
                    print(e)
        if len(self.dev_obj_list) > 0:
            for i in range(num):
                if not pinfo_list[i] in self.dev_obj_list.keys():
                    self.dev_obj_list[pinfo_list[i]] = [devname_list[i]]
        else:
            for i in range(num):
                self.dev_obj_list[pinfo_list[i]] = [devname_list[i]]  # 初始化多个链接对象,线程列表
        # if not self.mnq_thread_tid:
        if len(self.mnq_thread_tid) > 0:
            keys = self.mnq_thread_tid.keys()
            for i in range(num):
                if not pinfo_list[i] in keys:
                    self.mnq_thread_tid[pinfo_list[i]] = []
        else:
            for i in range(num):
                self.mnq_thread_tid[pinfo_list[i]] = []
        pop.clear()
        old.clear()
        new.clear()

    def timer_refresh(self):
        """获取窗口按钮设置刷新限制"""
        if self.get_time > 0:
            self.ui_main.get_windows.setText(f"{self.get_time}秒后可再次获取")
            self.get_time -= 1
        else:
            self.get_timer.stop()
            self.ui_main.get_windows.setEnabled(True)
            self.ui_main.get_windows.setText(f"获取窗口信息")
            self.get_time = 5


def main():
    app = QApplication(sys.argv)
    dz = DzUi()
    dz.ui_main.show()
    app.exec_()


if __name__ == '__main__':
    main()
