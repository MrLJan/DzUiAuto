# -*- coding:utf-8 -*-
# cython:language_level=3
import os
import sys
import time

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtGui import QTextCursor, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, \
    QTreeWidgetItem, QFileDialog, QListWidget
from PyQt5.QtCore import Qt, QTimer, QRegExp

from qt_material import apply_stylesheet
from DzTest.DzModeMachine import switch_case, StateExecute, StateMachine, StateSelect, execute_transition, \
    select_transition

from Utils.ExceptionTools import StopTaskErr
from Utils.LoadConfig import LoadConfig
from Utils.MnqTools import MnqTools
from Utils.OtherTools import OT, catch_ex
from Utils.QtSignals import QtSignals
from Utils.QueueManageTools import QueueManage
from Utils.ThreadTools import ThreadTools, check_mnq_thread

from Enum.ResEnum import GlobalEnumG
from Utils.Devicesconnect import DevicesConnect


@catch_ex
class DzUi:
    def __init__(self):
        self.ui_main = uic.loadUi(OT.abspath('/QtUI/dzmain.ui'))
        self.ui_main.setWindowTitle(f"岛主-当前版本{GlobalEnumG.Ver}")
        self.ui_main.setWindowIcon(QtGui.QIcon(OT.abspath("/Res/dz_icon.ico")))
        # 禁止窗口拉伸
        self.ui_main.setFixedSize(self.ui_main.width(), self.ui_main.height())
        # # 获取句柄窗口按钮
        self.ui_main.get_windows.clicked.connect(self._get_windows_pid)
        # # 开启/关闭模拟器按钮
        self.ui_main.filechoose_btn.clicked.connect(self.choose_mnq_file)  # 选中路径
        self.ui_main.start_mnq_all_btn.clicked.connect(lambda: self.mnq_start_quit(True))
        self.ui_main.quit_mnq_all_btn.clicked.connect(lambda: self.mnq_start_quit(False))
        self.ui_main.open_index_mnq_btn.clicked.connect(self.start_mnq_index)
        # self.ui_main.start_mnq_all_btn.setEnabled(False)
        # self.ui_main.quit_mnq_all_btn.setEnabled(False)
        # # 全选,取消选中,执行选中,停止选中
        self.ui_main.close_all_task_btn.clicked.connect(self.close_all_task)  # 全部停止
        self.ui_main.choose_stop_btn.clicked.connect(self.stop_choose)
        self.ui_main.choose_all_btn.clicked.connect(self.choose_all)
        self.ui_main.choose_cannel_btn.clicked.connect(self.cannel_choose)
        self.ui_main.choose_ot_btn.clicked.connect(self.choose_ot)
        self.ui_main.sort_btn.clicked.connect(self.sort_window)
        self.ui_main.mnq_set_btn.clicked.connect(self.set_mnq)
        # # 延时启动
        self.ui_main.yanshi_btn.clicked.connect(self.yanshi_todo_choose)
        # # 滚模拟器
        # self.ui_main.roll_mnq_btn.clicked.connect(self.roll_mnq_dotask)
        # 任务树
        self.set_link_label()
        self.set_tasktree(self.ui_main.task_tree_widget)
        self.ui_main.set_task_btn.clicked.connect(self._set_task_list)
        # self.ui_main.add_diy_task1_btn.clicked.connect(self.add_diy_task1_btn)
        # self.ui_main.add_diy_task2_btn.clicked.connect(self.add_diy_task2_btn)
        # 停止/打开配置

        self.ui_main.open_set_btn.clicked.connect(self.open_set)

        # ---------------设置界面-------------------
        # self.ui_main.hwnd_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,99}")))
        # self.ui_main.skip_mnqindex_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,99}")))
        self.ui_main.team_pwd_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,4}")))
        self.ui_main.hp_num_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,4}")))
        self.ui_main.mp_num_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,4}")))
        self.ui_main.auto_time_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        self.ui_main.task_level_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        self.ui_main.qh_level_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,2}")))
        self.ui_main.zhiye_edit.setValidator(QRegExpValidator(QRegExp("[0-9,]+$")))
        self.ui_main.d_use_mp_edit.setValidator(QRegExpValidator(QRegExp("[0-9,]+$")))
        self.ui_main.start_mnq_index_edit.setValidator(QRegExpValidator(QRegExp("[0-9,]+$")))
        self.ui_main.d1_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        self.ui_main.d2_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        self.ui_main.d3_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        self.ui_main.d4_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        self.ui_main.d5_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        self.ui_main.d6_duiyuan_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]+$")))
        self.ui_main.d1_pindao_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]{1,7}")))
        self.ui_main.d2_pindao_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]{1,7}")))
        self.ui_main.d3_pindao_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]{1,7}")))
        self.ui_main.d4_pindao_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]{1,7}")))
        self.ui_main.d5_pindao_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]{1,7}")))
        self.ui_main.d6_pindao_edit.setValidator(QRegExpValidator(QRegExp("[*0-9,]{1,7}")))
        self.ui_main.red_coin_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}")))
        self.ui_main.fps_edit.setValidator(QRegExpValidator(QRegExp("[0-9]{1,2}")))
        # 设置保存按钮
        self.ui_main.save_setting_btn.clicked.connect(self.save_setting)
        self.ui_main.save_setting_btn_2.clicked.connect(self.save_setting)
        self.set_setting_label(self.ui_main.line_mnqpath, "路径", "模拟器路径")
        self.set_bingmode(self.ui_main.mode_choose_box, "路径", "绑定模式")
        self.set_lineedit_text(self.ui_main.start_mnq_index_edit, "全局配置", "启动模拟器序号")
        self.set_lineedit_text(self.ui_main.auto_time_edit, "全局配置", "离线时长")
        self.set_lineedit_text(self.ui_main.autobat_time_edit, "全局配置", "挂机卡时长")
        self.set_lineedit_text(self.ui_main.qh_level_edit, "全局配置", "强化等级")
        self.set_lineedit_text(self.ui_main.task_level_edit, "全局配置", "任务停止等级")
        self.set_lineedit_text(self.ui_main.zhiye_edit, "野图配置", "短按窗口")
        self.set_lineedit_text(self.ui_main.d_use_mp_edit, "全局配置", "无蓝窗口")
        self.set_lineedit_text(self.ui_main.team_pwd_edit, "野图配置", "组队密码")
        self.set_lineedit_text(self.ui_main.d1_duiyuan_edit, "野图配置", "1队成员")
        self.set_lineedit_text(self.ui_main.d2_duiyuan_edit, "野图配置", "2队成员")
        self.set_lineedit_text(self.ui_main.d3_duiyuan_edit, "野图配置", "3队成员")
        self.set_lineedit_text(self.ui_main.d4_duiyuan_edit, "野图配置", "4队成员")
        self.set_lineedit_text(self.ui_main.d5_duiyuan_edit, "野图配置", "5队成员")
        self.set_lineedit_text(self.ui_main.d6_duiyuan_edit, "野图配置", "6队成员")
        self.set_lineedit_text(self.ui_main.d1_pindao_edit, "野图配置", "1队频道")
        self.set_lineedit_text(self.ui_main.d2_pindao_edit, "野图配置", "2队频道")
        self.set_lineedit_text(self.ui_main.d3_pindao_edit, "野图配置", "3队频道")
        self.set_lineedit_text(self.ui_main.d4_pindao_edit, "野图配置", "4队频道")
        self.set_lineedit_text(self.ui_main.d5_pindao_edit, "野图配置", "5队频道")
        self.set_lineedit_text(self.ui_main.d6_pindao_edit, "野图配置", "6队频道")
        self.set_lineedit_text(self.ui_main.red_coin_edit, '全局配置', '托管红币')
        self.set_zhiyebox_text(self.ui_main.zhiye_choose_box, "全局配置", "职业类型")
        self.set_check_box_text(self.ui_main.is_exitgame_box, "全局配置", "离线使用挂机卡")
        self.set_check_box_text(self.ui_main.is_exit_team_box, "全局配置", "人少退组")
        self.set_check_box_text(self.ui_main.is_change_role_box, "全局配置", "自动切换角色")
        self.set_check_box_text(self.ui_main.close_game_box, "全局配置", "任务结束关闭游戏")
        self.set_check_box_text(self.ui_main.gonghui_box, "全局配置", "公会内容")
        self.set_check_box_text(self.ui_main.boss_check_box, "全局配置", "混王图")
        self.set_check_box_text(self.ui_main.meiti_check_box, "全局配置", "定时任务")
        self.set_check_box_text(self.ui_main.open_auto_box, "全局配置", "混合自动按键")
        self.set_check_box_text(self.ui_main.wulin_box, "全局配置", "武陵")
        self.set_check_box_text(self.ui_main.jinzita_box, "全局配置", "金字塔")
        self.set_check_box_text(self.ui_main.jinghua_box, "全局配置", "进化系统")
        self.set_check_box_text(self.ui_main.jingying_box, "全局配置", "菁英地城")
        self.set_check_box_text(self.ui_main.startower_box, "全局配置", "星光塔")
        self.set_check_box_text(self.ui_main.gw_park_box, "全局配置", "怪物公园")
        self.set_check_box_text(self.ui_main.meiri_box, "全局配置", "每日地城")
        self.set_check_box_text(self.ui_main.ciyuan_box, "全局配置", "次元入侵")
        self.set_check_box_text(self.ui_main.tangbaobao_box, "全局配置", "汤宝宝")
        self.set_check_box_text(self.ui_main.mini_dc_box, "全局配置", "迷你地城")
        self.set_check_box_text(self.ui_main.qh_youhui_box, "全局配置", "强化优惠卷")
        self.set_check_box_text(self.ui_main.xinyun_box, "全局配置", "幸运卷轴")
        self.set_check_box_text(self.ui_main.dunpai_box, "全局配置", "盾牌卷轴")
        self.set_check_box_text(self.ui_main.baohu_box, "全局配置", "保护卷轴")
        self.set_check_box_text(self.ui_main.auto_wait_box, "全局配置", "随机休息")
        self.set_check_box_text(self.ui_main.saodi_box, "全局配置", "扫地模式")
        self.set_check_box_text(self.ui_main.jump_mode_box, "全局配置", "跳跃模式")
        self.set_check_box_text(self.ui_main.use_stone_box, "全局配置", "随机使用石头")
        self.set_combobox_text(self.ui_main.hp_box, "全局配置", "HP等级")
        self.set_combobox_text(self.ui_main.mp_box, "全局配置", "MP等级")
        self.set_lineedit_text(self.ui_main.hp_num_edit, "全局配置", "hp数量")
        self.set_lineedit_text(self.ui_main.mp_num_edit, "全局配置", "mp数量")
        self.set_check_box_text(self.ui_main.ym_box, "全局配置", "炎魔")
        self.set_check_box_text(self.ui_main.pkj_box, "全局配置", "皮卡啾")
        self.set_check_box_text(self.ui_main.nh_box, "全局配置", "女皇")
        self.set_check_box_text(self.ui_main.hd_boss_box, "全局配置", "混沌炎魔")
        self.set_nd(self.ui_main.ym_pt_rbtn, self.ui_main.ym_kn_rbtn, '全局配置', '炎魔难度')
        self.set_nd(self.ui_main.pkj_pt_rbtn, self.ui_main.pkj_kn_rbtn, '全局配置', '皮卡啾难度')
        self.set_nd(self.ui_main.nh_pt_rbtn, self.ui_main.nh_kn_rbtn, '全局配置', '女皇难度')
        self.set_radio_btn(self.ui_main.radioButton, '全局配置', '离线休息')
        self.set_radio_btn(self.ui_main.radioButton2, '全局配置', '在线休息')
        #
        # # 设置定时
        self.set_meiri_time_box(self.ui_main.meiri_time_box, "全局配置", "固定每日时间", True)
        self.set_meiri_time_box(self.ui_main.fenz_box, "全局配置", "固定每日时间", False)
        # dm 设置tablewidget

        self.ui_main.windows_pid.doubleClicked.connect(self.windows_click)
        self.ui_main.windows_pid.itemClicked.connect(self.item_choose)
        self.ui_main.windows_pid.setColumnCount(14)  # 设置列数
        self.ui_main.windows_pid.setColumnWidth(0, 80)
        self.ui_main.windows_pid.setColumnWidth(1, 100)
        self.ui_main.windows_pid.setColumnWidth(2, 100)
        self.ui_main.windows_pid.setColumnWidth(3, 80)
        self.ui_main.windows_pid.setColumnWidth(4, 80)
        self.ui_main.windows_pid.setColumnWidth(5, 100)
        self.ui_main.windows_pid.setColumnWidth(6, 75)
        self.ui_main.windows_pid.setColumnWidth(7, 90)
        self.ui_main.windows_pid.setColumnWidth(8, 90)
        self.ui_main.windows_pid.setColumnWidth(9, 160)
        self.ui_main.windows_pid.setColumnWidth(10, 160)
        self.ui_main.windows_pid.setColumnWidth(11, 100)
        self.ui_main.windows_pid.setColumnWidth(12, 50)
        self.ui_main.windows_pid.setColumnWidth(13, 50)
        self.ui_main.windows_pid.setShowGrid(False)

        self.set_list_widget()  # 清理道具list_widget
        self.ui_main.add_list_btn.clicked.connect(self.add_list_item)
        self.ui_main.remove_list_btn.clicked.connect(self.remove_list_item)
        # 重定向print输出信号
        self.sn = QtSignals()  # 初始化信号类
        sys.stdout = QtSignals(text_signal=self.console_output)
        sys.stderr = QtSignals(text_signal=self.console_output)

        self.sn.message_box.connect(self.get_messagebox)  # 弹窗消息信号
        self.sn.label_text.connect(self.set_label_text)  # 版本号label信号
        self.sn.windows_pid.connect(self.set_windows_pid)  # 窗口句柄信号
        self.sn.table_value.connect(self.set_table_value)  # 更改单元格状态栏文本
        self.sn.restart.connect(self.restart_task)  # 重启模拟器
        self.sn.stoptask.connect(self._stop_task)
        # self.sn.task_over_signal.connect(self.roll_mnq_dotask)
        # self.sn.close_mnq_index.connect(self.close_taskover_mnq)  # 关闭无任务模拟器
        # self.sn.btn_enable.connect(self.set_btn_enable)
        self.sn.log_tab.connect(self.log_tab_output)  # 输出窗口日志
        self.log_tab_dic = {}  # 存储窗口日志edit组件
        self.start_btn_dic = {}  # 存储窗口开始按钮
        self.stop_btn_dic = {}  # 存储窗口关闭按钮
        self.btn_widget_dic = {}  # 存储窗口按钮布局
        self.mnq_rownum_dic = {}  # 存储窗口行号
        self.mnq_adb_tcp_dic = {}  # 存储tcp端口
        self.mnq_name_old_list = []  # 存储旧窗口名
        self.mnq_name_pop_list = []  # 存储需要删除的窗口
        self.mnq_name_flag = None
        self.dev_obj_list = {}  # 初始化每个模拟器的连接对象名
        self.dev_list = {}  # 存储连接成功后的dev
        self.mnq_thread_tid = {}  # 存储每个模拟器的线程tid

        self.get_time = 5
        self.get_timer = QTimer()
        self.get_timer.setInterval(1000)
        self.get_timer.timeout.connect(self.timer_refresh)
        self.stop_time = 15
        self.stop_timer = QTimer()
        self.stop_timer.setInterval(1000)
        self.stop_timer.timeout.connect(self.close_btnrefresh)
        self.mnq_timer_time = 10
        self.mnq_timer = QTimer()
        self.index_queue = QueueManage()
        self.mnq_timer.setInterval(1000)
        self.mnq_timer.timeout.connect(self.open_mnq_dotask)
        self.roll_mnq_time = 10
        self.roll_mnq_timer = QTimer()
        self.roll_mnq_queue = QueueManage()
        self.roll_mnq_timer.setInterval(1000)

        self.team_event_dic = self.get_team_event()
        self.team_queue_dic = self.get_team_queue()

    def sort_window(self):
        row = self.ui_main.windows_pid.rowCount()
        if not row == 0:
            for i in range(row):
                if i > 19:
                    move_y = 410
                    move_x = 10 + ((i - 20) * 150)
                elif i > 14:
                    move_y = 310
                    move_x = 10 + ((i - 15) * 150)
                elif i > 9:
                    move_y = 210
                    move_x = 10 + ((i - 10) * 150)
                elif i > 4:
                    move_y = 110
                    move_x = 10 + ((i - 5) * 150)
                else:
                    move_y = 10
                    move_x = 10 + (i * 150)
                mnq_name = self.ui_main.windows_pid.item(i, 1).text()
                hwnd = int(self.ui_main.windows_pid.item(i, 13).text())
                dev = self.dev_obj_list[mnq_name]
                dev.MoveWindow(hwnd, move_x, move_y)
                dev.SetWindowState(hwnd, 1)  # 置顶窗口

    def windows_click(self, Item):
        row = Item.row()  # 获取行数
        mnq_name = self.ui_main.windows_pid.item(row, 1).text()
        dev = self.dev_obj_list[mnq_name]
        hwnd = int(self.ui_main.windows_pid.item(row, 13).text())
        self.ui_main.windows_pid.cellWidget(row, 0).setChecked(True)
        dev.SetWindowState(hwnd, 1)

    def item_choose(self, Item):
        row = Item.row()  # 获取行数
        self.ui_main.windows_pid.cellWidget(row, 0).setChecked(True)

    def set_mnq(self):
        _fps = self.ui_main.fps_edit.text()
        MnqTools().global_setting(_fps)

    def open_mnq_dotask(self):
        if self.mnq_timer_time > 0:
            self.ui_main.yanshi_btn.setText(f"{self.mnq_timer_time}秒后启动下一个")
            self.mnq_timer_time -= 1
        else:
            mnq_name = self.index_queue.get_task()
            if not mnq_name:
                self.mnq_timer.stop()
                self.ui_main.yanshi_btn.setText(r"延时启动")
                self.ui_main.yanshi_btn.setEnabled(True)
            else:
                # mnq_name = MnqTools().use_index_find_name(mnq_index)
                if not MnqTools().running_mnq_list([mnq_name]):
                    MnqTools().start_mnq_name_list([mnq_name])
                if len(self.mnq_thread_tid[mnq_name]) == 0:
                    self._do_task_list([mnq_name], message=False)
                    self.start_btn_dic[mnq_name].setEnabled(False)
                    self.stop_btn_dic[mnq_name].setEnabled(True)
                self.index_queue.task_over(mnq_name)
                if not self.index_queue.queue.empty():
                    try:
                        self.mnq_timer_time = int(self.ui_main.yanshi_start_edit.text()) * 60
                    except BaseException:
                        self.mnq_timer_time = 10
                else:
                    print(f"延时启动任务完成")

    def start_mnq_index(self):
        mnq_index_list = self.ui_main.start_mnq_index_edit.text()
        mnq_index = mnq_index_list.split(',')
        if mnq_index_list == '':
            self.get_messagebox('错误', '未设置需要开启的模拟器序号')
        else:
            LoadConfig.writeconf("全局配置", "启动模拟器序号", mnq_index_list)
            MnqTools().start_mnq_index_list(mnq_index)

    def mnq_start_quit(self, is_start):
        if is_start:
            MnqTools().start_mnq_all()
        else:
            self.close_all_task()
            MnqTools().quit_mnq_all()

    def yanshi_todo_choose(self):
        try:
            rows = self.ui_main.windows_pid.rowCount()
            if rows == 0:
                self.get_messagebox('错误', '先启动模拟器并获取窗口信息')
            else:
                for row in range(rows):
                    # mnq_index = str(self.ui_main.windows_pid.cellWidget(row, 0).text())
                    mnq_name = self.ui_main.windows_pid.item(row, 1).text()
                    self.index_queue.put_queue(mnq_name)
                self.mnq_timer.start()
                self.ui_main.yanshi_btn.setEnabled(False)
        except Exception:
            self.mnq_timer_time = 1

    def choose_ot(self):
        rows = self.ui_main.windows_pid.rowCount()
        if rows == 0:
            pass
        else:
            for i in range(rows):
                if self.ui_main.windows_pid.cellWidget(i, 0).isChecked():
                    self.ui_main.windows_pid.cellWidget(i, 0).setChecked(False)
                else:
                    self.ui_main.windows_pid.cellWidget(i, 0).setChecked(True)

    def choose_all(self):
        rows = self.ui_main.windows_pid.rowCount()
        if rows == 0:
            pass
        else:
            for i in range(rows):
                self.ui_main.windows_pid.cellWidget(i, 0).setChecked(True)

    def cannel_choose(self):
        rows = self.ui_main.windows_pid.rowCount()
        if rows == 0:
            pass
        else:
            for i in range(rows):
                self.ui_main.windows_pid.cellWidget(i, 0).setChecked(False)

    def stop_choose(self):
        rows = self.ui_main.windows_pid.rowCount()
        name_list = []
        if rows == 0:
            print("没有获取设备信息")
        else:
            for i in range(rows):
                if self.ui_main.windows_pid.cellWidget(i, 0).isChecked():
                    _name = self.ui_main.windows_pid.item(i, 1).text()
                    name_list.append(_name)
            # print(index_list)
            if len(name_list) > 0:
                self._stop_task(name_list)
            else:
                print('没有选中任何模拟器')

    def close_all_task(self):
        """关闭所有任务"""
        close_list = []
        if self.ui_main.close_all_task_btn.isEnabled():
            self.stop_timer.start()
            self.ui_main.close_all_task_btn.setEnabled(False)
        row = self.ui_main.windows_pid.rowCount()
        for i in range(row):
            # _index = str(self.ui_main.windows_pid.cellWidget(i, 0).text())
            _name = self.ui_main.windows_pid.item(i, 1).text()
            close_list.append(_name)
        if len(close_list) > 0:
            self._stop_task(close_list)

    @staticmethod
    def open_set():
        set_path = OT.abspath('/res')
        os.startfile(set_path)

    def set_setting_label(self, label_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        self.set_label_text(label_obj, data_text)

    def set_link_label(self):
        self.ui_main.label_21.setText(
            "<a style='color: red; text-decoration: none' href = http://www.huoniu.buzz>岛主24小时自助提卡网址,点击跳转")
        self.ui_main.label_21.setAlignment(Qt.AlignCenter)
        self.ui_main.label_21.setOpenExternalLinks(True)

    @staticmethod
    def set_bingmode(label_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        if data_text == '模式一':
            label_obj.setCurrentIndex(0)
        elif data_text == '模式二':
            label_obj.setCurrentIndex(1)
        elif data_text == '模式三':
            label_obj.setCurrentIndex(2)
        elif data_text == '模式四':
            label_obj.setCurrentIndex(3)
        else:
            label_obj.setCurrentIndex(0)

    @staticmethod
    def set_combobox_text(label_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        if data_text == '4阶药水':
            label_obj.setCurrentIndex(0)
        elif data_text == '5阶药水':
            label_obj.setCurrentIndex(1)
        elif data_text == '6阶药水':
            label_obj.setCurrentIndex(2)
        elif data_text == '7阶药水':
            label_obj.setCurrentIndex(3)
        elif data_text == '8阶药水':
            label_obj.setCurrentIndex(4)
        elif data_text == '9阶药水':
            label_obj.setCurrentIndex(5)
        else:
            label_obj.setCurrentIndex(0)

    @staticmethod
    def set_lineedit_text(label_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        label_obj.setText(data_text)

    @staticmethod
    def set_check_box_text(check_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        if data_text == '0':
            check_obj.setChecked(False)
        else:
            check_obj.setChecked(True)

    @staticmethod
    def set_radio_btn(radio_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        if data_text == '0':
            radio_obj.setChecked(False)
        else:
            radio_obj.setChecked(True)

    @staticmethod
    def set_nd(pt_obj, kn_obj, data_section, data_name):
        """难度按钮设置"""
        data_text = LoadConfig.getconf(data_section, data_name)
        if data_text == '0':
            pt_obj.setChecked(True)
            kn_obj.setChecked(False)
        else:
            kn_obj.setChecked(True)
            pt_obj.setChecked(False)

    @staticmethod
    def set_meiri_time_box(box_obk, data_section, data_name, is_hour):
        data_text = LoadConfig.getconf(data_section, data_name)
        data_list = data_text.split(":")
        data_h = data_list[0]
        data_m = data_list[-1]
        if is_hour:
            box_obk.setValue(int(data_h))
        else:
            box_obk.setValue(int(data_m))

    @staticmethod
    def set_zhiyebox_text(label_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        index_num = int(data_text)
        label_obj.setCurrentIndex(index_num)

    @staticmethod
    def set_pindaobox_text(label_obj, data_section, data_name):
        data_text = LoadConfig.getconf(data_section, data_name)
        index_num = int(data_text) - 1
        label_obj.setCurrentIndex(index_num)

    def get_list_widget_textlist(self):
        """获取道具清理列表"""
        rows = self.ui_main.dq_list_w2.count()
        d_value = list(GlobalEnumG.Discard_ID.values())
        dv_list = []
        dv_str = ''
        for dr in range(rows):
            dr_text = self.ui_main.dq_list_w2.item(dr).text()
            dv_list.append(str(d_value.index(dr_text)))
        for ds in dv_list:
            if dv_str != '':
                dv_str = dv_str + ',' + ds
            else:
                dv_str = ds
        return dv_str

    def save_setting(self):
        """保存设置界面设置，写入配置文件"""
        dv_list = str(self.get_list_widget_textlist())  # 道具丢弃列表
        bind_mode = self.ui_main.mode_choose_box.currentText()
        ld_mnq_path = self.ui_main.line_mnqpath.text()
        hp_levle = self.ui_main.hp_box.currentText()
        mp_levle = self.ui_main.mp_box.currentText()
        hp_num = self.ui_main.hp_num_edit.text()
        mp_num = self.ui_main.mp_num_edit.text()
        zhiye_id = self.ui_main.zhiye_choose_box.currentText()
        d_use_mp = self.ui_main.d_use_mp_edit.text()
        zhiye_windows = self.ui_main.zhiye_edit.text()
        qh_level = self.ui_main.qh_level_edit.text()
        exit_game_time = self.ui_main.auto_time_edit.text()
        auto_time = self.ui_main.autobat_time_edit.text()
        task_level_end = self.ui_main.task_level_edit.text()
        d1_duiyuan = self.ui_main.d1_duiyuan_edit.text()
        d2_duiyuan = self.ui_main.d2_duiyuan_edit.text()
        d3_duiyuan = self.ui_main.d3_duiyuan_edit.text()
        d4_duiyuan = self.ui_main.d4_duiyuan_edit.text()
        d5_duiyuan = self.ui_main.d5_duiyuan_edit.text()
        d6_duiyuan = self.ui_main.d6_duiyuan_edit.text()
        d1_pindao = self.ui_main.d1_pindao_edit.text()
        d2_pindao = self.ui_main.d2_pindao_edit.text()
        d3_pindao = self.ui_main.d3_pindao_edit.text()
        d4_pindao = self.ui_main.d4_pindao_edit.text()
        d5_pindao = self.ui_main.d5_pindao_edit.text()
        d6_pindao = self.ui_main.d6_pindao_edit.text()
        red_coin = self.ui_main.red_coin_edit.text()
        mnq_index = self.ui_main.start_mnq_index_edit.text()
        zhiye = GlobalEnumG.ZhiYe
        team_pwd = self.ui_main.team_pwd_edit.text()
        meiri_time = self.ui_main.meiri_time_box.value()
        fenz_time = self.ui_main.fenz_box.value()
        do_meiri_time = str(meiri_time) + ":" + str(fenz_time)
        boss_task = '1' if self.ui_main.boss_check_box.isChecked() else '0'
        dingshi_task = '1' if self.ui_main.meiti_check_box.isChecked() else '0'
        result = '1' if self.ui_main.open_auto_box.isChecked() else '0'
        wulin_task = '1' if self.ui_main.wulin_box.isChecked() else '0'
        jinzita_task = '1' if self.ui_main.jinzita_box.isChecked() else '0'
        jingying_task = '1' if self.ui_main.jingying_box.isChecked() else '0'
        meiri_task = '1' if self.ui_main.meiri_box.isChecked() else '0'
        jinghua_task = '1' if self.ui_main.jinghua_box.isChecked() else '0'
        ciyuan_task = '1' if self.ui_main.ciyuan_box.isChecked() else '0'
        startower_task = '1' if self.ui_main.startower_box.isChecked() else '0'
        tangbaobao_task = '1' if self.ui_main.tangbaobao_box.isChecked() else '0'
        mini_dc_task = '1' if self.ui_main.mini_dc_box.isChecked() else '0'
        gw_park_task = '1' if self.ui_main.gw_park_box.isChecked() else '0'
        use_stone = '1' if self.ui_main.use_stone_box.isChecked() else '0'

        qh_youhui = '1' if self.ui_main.qh_youhui_box.isChecked() else '0'
        xingyun_jz = '1' if self.ui_main.xinyun_box.isChecked() else '0'
        dunpai_jz = '1' if self.ui_main.dunpai_box.isChecked() else '0'
        baohu_jz = '1' if self.ui_main.baohu_box.isChecked() else '0'
        ym = '1' if self.ui_main.ym_box.isChecked() else '0'
        ym_nd = '1' if self.ui_main.ym_kn_rbtn.isChecked() else '0'
        pjk = '1' if self.ui_main.pkj_box.isChecked() else '0'
        pjk_nd = '1' if self.ui_main.pkj_kn_rbtn.isChecked() else '0'
        nh = '1' if self.ui_main.nh_box.isChecked() else '0'
        nh_nd = '1' if self.ui_main.nh_kn_rbtn.isChecked() else '0'
        hd_ym = '1' if self.ui_main.hd_boss_box.isChecked() else '0'
        auto_wait = '1' if self.ui_main.auto_wait_box.isChecked() else '0'
        on_wait_sleep = '1' if self.ui_main.radioButton2.isChecked() else '0'
        off_wait_sleep = '1' if self.ui_main.radioButton.isChecked() else '0'
        is_exit_team = '1' if self.ui_main.is_exit_team_box.isChecked() else '0'
        gonghui = '1' if self.ui_main.gonghui_box.isChecked() else '0'
        close_game = '1' if self.ui_main.close_game_box.isChecked() else '0'
        is_exitgame = '1' if self.ui_main.is_exitgame_box.isChecked() else '0'
        is_change_role = '1' if self.ui_main.is_change_role_box.isChecked() else '0'
        saodi_mode = '1' if self.ui_main.saodi_box.isChecked() else '0'
        jump_mode = '1' if self.ui_main.jump_mode_box.isChecked() else '0'

        LoadConfig.writeconf("路径", "模拟器路径", ld_mnq_path)
        LoadConfig.writeconf("路径", "绑定模式", bind_mode)
        LoadConfig.writeconf("全局配置", "清理道具", dv_list)
        LoadConfig.writeconf("全局配置", "扫地模式", saodi_mode)
        LoadConfig.writeconf("全局配置", "跳跃模式", jump_mode)
        LoadConfig.writeconf("全局配置", "HP等级", hp_levle)
        LoadConfig.writeconf("全局配置", "MP等级", mp_levle)
        LoadConfig.writeconf("全局配置", "hp数量", hp_num)
        LoadConfig.writeconf("全局配置", "mp数量", mp_num)
        LoadConfig.writeconf("全局配置", "启动模拟器序号", mnq_index)
        LoadConfig.writeconf("野图配置", "短按窗口", zhiye_windows)
        LoadConfig.writeconf("野图配置", "组队密码", team_pwd)
        LoadConfig.writeconf("全局配置", "无蓝窗口", d_use_mp)
        LoadConfig.writeconf("全局配置", "人少退组", is_exit_team)
        LoadConfig.writeconf("全局配置", "随机使用石头", use_stone)
        LoadConfig.writeconf("全局配置", "自动切换角色", is_change_role)
        LoadConfig.writeconf("全局配置", "任务停止等级", task_level_end)
        LoadConfig.writeconf("全局配置", "离线时长", exit_game_time)
        LoadConfig.writeconf("全局配置", "随机休息", auto_wait)
        LoadConfig.writeconf("全局配置", "在线休息", on_wait_sleep)
        LoadConfig.writeconf("全局配置", "离线休息", off_wait_sleep)
        LoadConfig.writeconf("全局配置", "挂机卡时长", auto_time)
        LoadConfig.writeconf("全局配置", "炎魔", ym)
        LoadConfig.writeconf("全局配置", "炎魔难度", ym_nd)
        LoadConfig.writeconf("全局配置", "皮卡啾", pjk)
        LoadConfig.writeconf("全局配置", "皮卡啾难度", pjk_nd)
        LoadConfig.writeconf("全局配置", "女皇", nh)
        LoadConfig.writeconf("全局配置", "女皇难度", nh_nd)
        LoadConfig.writeconf("全局配置", "混沌炎魔", hd_ym)
        LoadConfig.writeconf("全局配置", "任务结束关闭游戏", close_game)
        LoadConfig.writeconf("全局配置", "公会内容", gonghui)
        LoadConfig.writeconf("全局配置", "混王图", boss_task)
        LoadConfig.writeconf("全局配置", "定时任务", dingshi_task)
        LoadConfig.writeconf("全局配置", "固定每日时间", str(do_meiri_time))
        LoadConfig.writeconf("全局配置", "职业类型", zhiye[zhiye_id])
        LoadConfig.writeconf("全局配置", "混合自动按键", result)
        LoadConfig.writeconf("全局配置", "武陵", wulin_task)
        LoadConfig.writeconf("全局配置", "金字塔", jinzita_task)
        LoadConfig.writeconf("全局配置", "每日地城", meiri_task)
        LoadConfig.writeconf("全局配置", "菁英地城", jingying_task)
        LoadConfig.writeconf("全局配置", "进化系统", jinghua_task)
        LoadConfig.writeconf("全局配置", "次元入侵", ciyuan_task)
        LoadConfig.writeconf("全局配置", "汤宝宝", tangbaobao_task)
        LoadConfig.writeconf("全局配置", "星光塔", startower_task)
        LoadConfig.writeconf("全局配置", "怪物公园", gw_park_task)
        LoadConfig.writeconf("全局配置", "迷你地城", mini_dc_task)
        LoadConfig.writeconf("全局配置", "强化等级", qh_level)
        LoadConfig.writeconf("全局配置", "强化优惠卷", qh_youhui)
        LoadConfig.writeconf("全局配置", "幸运卷轴", xingyun_jz)
        LoadConfig.writeconf("全局配置", "盾牌卷轴", dunpai_jz)
        LoadConfig.writeconf("全局配置", "保护卷轴", baohu_jz)
        LoadConfig.writeconf("全局配置", "离线使用挂机卡", is_exitgame)
        LoadConfig.writeconf("野图配置", "1队成员", d1_duiyuan)
        LoadConfig.writeconf("野图配置", "2队成员", d2_duiyuan)
        LoadConfig.writeconf("野图配置", "3队成员", d3_duiyuan)
        LoadConfig.writeconf("野图配置", "4队成员", d4_duiyuan)
        LoadConfig.writeconf("野图配置", "5队成员", d5_duiyuan)
        LoadConfig.writeconf("野图配置", "6队成员", d6_duiyuan)
        LoadConfig.writeconf("野图配置", "1队频道", d1_pindao)
        LoadConfig.writeconf("野图配置", "2队频道", d2_pindao)
        LoadConfig.writeconf("野图配置", "3队频道", d3_pindao)
        LoadConfig.writeconf("野图配置", "4队频道", d4_pindao)
        LoadConfig.writeconf("野图配置", "5队频道", d5_pindao)
        LoadConfig.writeconf("野图配置", "6队频道", d6_pindao)
        LoadConfig.writeconf("全局配置", "托管红币", red_coin)
        self.get_messagebox("设置", "配置已更新")

    @staticmethod
    def get_team_queue():
        queue_dic = {'team1': QueueManage(), 'team2': QueueManage(), 'team3': QueueManage(),
                     'team4': QueueManage(), 'team5': QueueManage(), 'team6': QueueManage(), 'team7': QueueManage()}
        return queue_dic

    @staticmethod
    def get_team_event():
        event_dic = {'team1': ThreadTools.new_event(), 'team2': ThreadTools.new_event(),
                     'team3': ThreadTools.new_event(),
                     'team4': ThreadTools.new_event(), 'team5': ThreadTools.new_event(),
                     'team6': ThreadTools.new_event(),
                     'team7': ThreadTools.new_event()}
        return event_dic

    def set_tasktree(self, tree_obj):
        tree_obj.setColumnCount(2)
        tree_obj.setColumnWidth(0, 130)
        tree_obj.setColumnWidth(1, 90)
        tree_obj.setHeaderLabels(['任务', '备注'])
        root_item = QTreeWidgetItem(tree_obj)
        root_item.setText(0, '一键托管')
        root_item.setText(1, '自动选择任务')
        # child31 = QTreeWidgetItem(tree_obj)
        # child31.setText(0, '自定义一')
        # child31.setText(1, '自定义任务顺序')
        # child32 = QTreeWidgetItem(tree_obj)
        # child32.setText(0, '自定义二')
        # child32.setText(1, '自定义任务顺序')
        child1 = QTreeWidgetItem(tree_obj)
        child1.setText(0, '自动任务')
        child1.setText(1, '做任务直到无任务')
        child2 = QTreeWidgetItem(tree_obj)
        child2.setText(0, '自动每日')
        child2.setText(1, '根据设置做每日')
        child3 = QTreeWidgetItem(tree_obj)
        child3.setText(0, '混Boss图')
        child3.setText(1, '混困难炎魔,皮卡啾,女皇')
        child4 = QTreeWidgetItem(tree_obj)
        child4.setText(0, '自动星图')
        child40 = QTreeWidgetItem(child4)
        child40.setText(0, '研究所102')
        child40.setText(1, '40星')
        child19 = QTreeWidgetItem(child4)
        child19.setText(0, '西边森林')
        child19.setText(1, '45星')
        child17 = QTreeWidgetItem(child4)
        child17.setText(0, '冰冷死亡战场')
        child17.setText(1, '65星')
        child37 = QTreeWidgetItem(child4)
        child37.setText(0, '龙蛋')
        child37.setText(1, '80星')
        child5 = QTreeWidgetItem(child4)
        child5.setText(0, '爱奥斯塔入口')
        child5.setText(1, '90星')
        child105 = QTreeWidgetItem(child4)
        child105.setText(0, '奥斯塔入口')
        child105.setText(1, '105星')
        child18 = QTreeWidgetItem(child4)
        child18.setText(0, '天空露台2')
        child18.setText(1, '110星')
        child113 = QTreeWidgetItem(child4)
        child113.setText(0, '机械室')
        child113.setText(1, '113星')
        child115 = QTreeWidgetItem(child4)
        child115.setText(0, '时间漩涡')
        child115.setText(1, '115星')
        child36 = QTreeWidgetItem(child4)
        child36.setText(0, '忘却之路4')
        child36.setText(1, '120星')
        child35 = QTreeWidgetItem(child4)
        child35.setText(0, '偏僻泥沼')
        child35.setText(1, '130星')
        child351 = QTreeWidgetItem(child4)
        child351.setText(0, '变形的森林')
        child351.setText(1, '136星')
        child34 = QTreeWidgetItem(child4)
        child34.setText(0, '武器库星图')
        child34.setText(1, '142星')
        child144 = QTreeWidgetItem(child4)
        child144.setText(0, '灰烬之风高原')
        child144.setText(1, '144星')
        child147 = QTreeWidgetItem(child4)
        child147.setText(0, '崎岖的峡谷')
        child147.setText(1, '147星')
        child6 = QTreeWidgetItem(tree_obj)
        child6.setText(0, '自动野图')
        child7 = QTreeWidgetItem(child6)
        child7.setText(0, '神秘森林')
        child7.setText(1, '6.65w战力')
        child8 = QTreeWidgetItem(child6)
        child8.setText(0, '露台2')
        child8.setText(1, '13w战力')
        child9 = QTreeWidgetItem(child6)
        child9.setText(0, '忘却之路3')
        child9.setText(1, '20.5w战力')
        child11 = QTreeWidgetItem(child6)
        child11.setText(0, '武器库')
        child11.setText(1, '44w战力')
        child33 = QTreeWidgetItem(child6)
        child33.setText(0, '崎岖峡谷')
        child33.setText(1, '56w战力')
        child10 = QTreeWidgetItem(child6)
        child10.setText(0, '木菇菇林')
        child10.setText(1, '68.5w战力')
        child12 = QTreeWidgetItem(tree_obj)
        child12.setText(0, '其他功能')
        # child13 = QTreeWidgetItem(child12)
        # child13.setText(0, '默认设置')
        # child13.setText(1, '设置游戏及副本入口')
        child20 = QTreeWidgetItem(child12)
        child20.setText(0, '强化装备')
        child20.setText(1, '默认12,可设置强化等级')
        child21 = QTreeWidgetItem(child12)
        child21.setText(0, '升级装备')
        child21.setText(1, '默认使用罕见研磨材料')
        child14 = QTreeWidgetItem(child12)
        child14.setText(0, '装备技能')
        child14.setText(1, '摆放技能')
        child15 = QTreeWidgetItem(child12)
        child15.setText(0, '穿戴新手宠物')
        child15.setText(1, '仅限3种新手宠物摆放')
        child161 = QTreeWidgetItem(child12)
        child161.setText(0, '背包出售')
        child161.setText(1, '出售+分解')
        child16 = QTreeWidgetItem(child12)
        child16.setText(0, '背包清理')
        child16.setText(1, '丢弃部分垃圾')
        child17 = QTreeWidgetItem(child12)
        child17.setText(0, '奖励领取')
        child17.setText(1, '领取奖励,邮件')

        # child13 = QTreeWidgetItem(child12)
        # child13.setText(0, '装备技能')
        tree_obj.addTopLevelItem(root_item)
        tree_obj.clicked.connect(self.task_tree_clicked)
        # self.ui_main.setCentralWidget(tree_obj)

    def _set_task_list(self):
        rows = self.ui_main.windows_pid.rowCount()
        task_name = self.ui_main.task_name_label.text()

        if rows == 0 or task_name == "":
            pass
        else:
            for i in range(rows):
                if self.ui_main.windows_pid.cellWidget(i, 0).isChecked():
                    mnq_name = self.ui_main.windows_pid.item(i, 1).text()
                    if len(self.mnq_thread_tid[mnq_name]) == 0:
                        self.set_table_value(mnq_name, 2, task_name)  # 设置任务

    def task_tree_clicked(self):
        res = self.ui_main.task_tree_widget.currentItem()
        if res.text(0) in ['自动星图', '自动野图', '其他功能']:
            self.set_label_text(self.ui_main.task_name_label, "")
        else:
            self.set_label_text(self.ui_main.task_name_label, res.text(0))
            self.ui_main.task_name_label.setStyleSheet("color:red")

    def add_list_item(self):
        try:
            res = self.ui_main.dq_list_w.currentItem().text()
            self.ui_main.dq_list_w2.addItem(res)
            self.ui_main.dq_list_w.removeItemWidget(self.ui_main.dq_list_w.currentItem())
            self.ui_main.dq_list_w.takeItem(self.ui_main.dq_list_w.currentRow())
        except Exception as e:
            print('没有选中任何道具')

    def remove_list_item(self):
        try:
            res = self.ui_main.dq_list_w2.currentItem().text()
            self.ui_main.dq_list_w.addItem(res)
            self.ui_main.dq_list_w2.removeItemWidget(self.ui_main.dq_list_w2.currentItem())
            self.ui_main.dq_list_w2.takeItem(self.ui_main.dq_list_w2.currentRow())
        except Exception as e:
            print('没有选中任何道具')

    def set_list_widget(self):
        try:
            d_list = LoadConfig.getconf('全局配置', '清理道具')
            if d_list != '':
                d_list = d_list.split(',')
            else:
                d_list = []
            d_k_list = list(GlobalEnumG.Discard_ID.keys())
            d_name_list = []
            d2_name_list = []
            for d2_id in d_list:
                dis_name = GlobalEnumG.Discard_ID[d2_id]
                d2_name_list.append(dis_name)
                d_k_list.pop(d_k_list.index(d2_id))
            for d_id in d_k_list:
                dis_name = GlobalEnumG.Discard_ID[d_id]
                d_name_list.append(dis_name)
            if len(d2_name_list) != 0:
                self.ui_main.dq_list_w2.addItems(d2_name_list)
            self.ui_main.dq_list_w.addItems(d_name_list)
        except Exception as e:
            print(e, '配置清理道具id错误')

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
            row_num = self.mnq_rownum_dic[mnq_name]['rownum']
            self.ui_main.windows_pid.setItem(row_num, col_num, self.set_tableitem_center(value))
        except Exception as e:
            print(e)

    def get_messagebox(self, title, text):
        """消息弹窗"""
        QMessageBox.information(self.ui_main, title, text)

    def choose_mnq_file(self):
        """设置界面，选择模拟器路径"""
        file_choose_dialog = QFileDialog(self.ui_main, "选择一个文件", "../", "exe(*.exe)")
        file_choose_dialog.setLabelText(QFileDialog.FileName, "模拟器路径")
        file_choose_dialog.setLabelText(QFileDialog.Accept, "确认")
        file_choose_dialog.setLabelText(QFileDialog.Reject, "取消")
        file_choose_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_choose_dialog.fileSelected.connect(lambda f_path: self.set_label_text(self.ui_main.line_mnqpath, f_path))
        file_choose_dialog.open()

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

    @staticmethod
    def index_check_box(index):
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
                sub_hwnd = self.ui_main.windows_pid.item(row_num, 12).text()
                pid_now, hwnd_now, subhwnd_now = MnqTools().check_ld_hwnd_subhwnd(str(mnq_index))
                if pid_now == 0 or hwnd_now == 0 or subhwnd_now == 0:
                    self.get_messagebox("错误", f"模拟器{mnq_name}未启动或模拟器名称异常")
                else:
                    if sub_hwnd != subhwnd_now:
                        if hwnd_now == 0:
                            self.get_messagebox("错误", f"等待模拟器{mnq_name}启动完成")
                        else:
                            self.sn.table_value.emit(mnq_name, 12, str(subhwnd_now))
                            self.sn.table_value.emit(mnq_name, 13, str(hwnd_now))
                    if task_name == "":
                        self.get_messagebox("错误", f"模拟器:[{mnq_name}]未设置执行任务")
                    else:
                        if len(self.mnq_thread_tid[mnq_name]) == 0:
                            self.start_btn_dic[mnq_name].setEnabled(False)

                            def run():
                                self._do_task_list([mnq_name])

                            ThreadTools('', run).start()
                            self.stop_btn_dic[mnq_name].setEnabled(True)
                        else:
                            self.get_messagebox("错误", f"模拟器:[{mnq_name}]之前的任务还在停止中,等待几秒后重试")
        except Exception as e:
            print(e)

    def stop_task_row(self):
        """列表停止按钮点击事件"""

        def _stop():
            dev_close.KeyDownChar('up')
            dev_close.KeyDownChar('down')
            dev_close.KeyDownChar('left')
            dev_close.KeyDownChar('right')
            dev_close.KeyDownChar('x')
            dev_close.KeyDownChar('z')
            dev_close.KeyDownChar('c')
            time.sleep(0.05)
            dev_close.KeyUpChar('up')
            dev_close.KeyUpChar('down')
            dev_close.KeyUpChar('left')
            dev_close.KeyUpChar('right')
            dev_close.KeyUpChar('x')
            dev_close.KeyUpChar('z')
            dev_close.KeyUpChar('c')
            ThreadTools.stop_thread_list(mnq_thread_list)  # 利用tid关闭线程
            mnq_thread_list.clear()
            dev_close.UnBindWindow()  # 解除绑定

        button = self.ui_main.windows_pid.sender()
        if button:  # 确定位置
            row_num = self.ui_main.windows_pid.indexAt(button.parent().pos()).row()
            mnq_name = self.ui_main.windows_pid.item(row_num, 1).text()
            dev_close = self.dev_list[mnq_name]
            mnq_thread_list = self.mnq_thread_tid[mnq_name]
            if not ThreadTools.is_threadname('停止任务', mnq_thread_list):
                if len(mnq_thread_list) > 0:
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

    def log_tab_output(self, mnq_name, text):
        """单线程日志输出"""
        # print(tab_name)
        now_time = time.strftime("%m-%d %H:%M:%S", time.localtime())
        edit = self.log_tab_dic[mnq_name]
        if text == 'clear':
            edit.clear()
        else:
            cursor = edit.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(f"[{now_time}]{text}\n")
            # edit.insertPlainText(text)
            edit.setTextCursor(cursor)
            edit.ensureCursorVisible()

    def _stop_task(self, name_list, err_stop=False):

        def stop_thread():
            for mnq_name in name_list:
                # mnq_name = MnqTools().use_index_find_name(mnq_index)
                mnq_thread_list = self.mnq_thread_tid[mnq_name]
                if len(mnq_thread_list) != 0:
                    ThreadTools.stop_thread_list(mnq_thread_list)  # 利用tid关闭线程
                    mnq_thread_list.clear()
                    dev_close = self.dev_list[mnq_name]
                    dev_close.KeyDownChar('up')
                    dev_close.KeyDownChar('down')
                    dev_close.KeyDownChar('left')
                    dev_close.KeyDownChar('right')
                    dev_close.KeyDownChar('x')
                    dev_close.KeyDownChar('z')
                    dev_close.KeyDownChar('c')
                    time.sleep(0.05)
                    dev_close.KeyUpChar('up')
                    dev_close.KeyUpChar('down')
                    dev_close.KeyUpChar('left')
                    dev_close.KeyUpChar('right')
                    dev_close.KeyUpChar('x')
                    dev_close.KeyUpChar('z')
                    dev_close.KeyUpChar('c')
                    if not err_stop:
                        dev_close.UnBindWindow()
                    self.sn.table_value.emit(mnq_name, 7, "")
                    self.stop_btn_dic[mnq_name].setEnabled(False)
                    self.start_btn_dic[mnq_name].setEnabled(True)
            return True

        if err_stop:
            mnq_thread_list = self.mnq_thread_tid[name_list[-1]]
            if not ThreadTools.is_threadname('停止任务', mnq_thread_list):
                stop = ThreadTools("停止任务", stop_thread)
                stop.start()
        else:
            stop = ThreadTools("停止任务", stop_thread)
            stop.start()

    @staticmethod
    def init_dm(dm_obj, sub_hwnd):
        DevicesConnect.bind_windows(dm_obj, sub_hwnd)

    def _do_task_list(self, name_list, message=True):
        """启动任务"""
        for mnq_name in name_list:
            # mnq_name = MnqTools().use_index_find_name(mnq_index)
            mnq_thread_list = self.mnq_thread_tid[mnq_name]
            try:
                row_num = int(self.mnq_rownum_dic[mnq_name]['rownum'])
                self.ui_main.windows_pid.cellWidget(row_num, 0).setChecked(False)
            except BaseException as e:
                self.get_messagebox("错误", f"模拟器信息异常,启动失败{e}")
                return False
            task_name = self.ui_main.windows_pid.item(row_num, 2).text()
            dm_obj = self.dev_obj_list[mnq_name]
            sub_hwnd = int(self.ui_main.windows_pid.item(row_num, 12).text())
            if task_name == "":
                if message:
                    self.get_messagebox("错误", f"模拟器:[{mnq_name}]未设置执行任务")
                return False
            else:
                # devname = self.dev_obj_list[mnq_name][0]  # devname 设备名,mnq_name是标题名
                # try:
                ThreadTools("初始化", self.init_dm, args=(dm_obj, sub_hwnd)).start()
                self.dev_list[mnq_name] = dm_obj  # dev是连接成功后的设备对象
                devinfo = (dm_obj, mnq_name)
                # except:
                # res = False
                # devinfo = []
                # if not res:
                #     self.get_messagebox("错误", f"模拟器:[{mnq_name}]连接失败_检查adb")
                #     self.start_btn_dic[mnq_name].setEnabled(True)
                #     self.stop_btn_dic[mnq_name].setEnabled(False)
                #     mnq_thread_list.clear()
                #     return False
                # self.dev_list[mnq_name] = dev  # dev是连接成功后的设备对象
                mnq_name = self.ui_main.windows_pid.item(row_num, 1).text()
                _time = time.time()
                login_time = time.strftime('%m-%d %H:%M:%S', time.localtime(_time))
                LoadConfig.writeconf(mnq_name, '最近登录时间', str(_time), ini_name=mnq_name)
                LoadConfig.writeconf(mnq_name, '最近任务', task_name, ini_name=mnq_name)
                self.sn.table_value.emit(mnq_name, 10, login_time)  # 最近登录时间
                self.sn.table_value.emit(mnq_name, 11, '0')  # 闪退次数
                self.sn.log_tab.emit(mnq_name, '------启动任务------')
                taskdic = self.task_dic(devinfo, task_name, mnq_thread_list)
                StateMachine(taskdic['执行器'], GlobalEnumG.ExecuteStates, execute_transition, "Wait")
                StateMachine(taskdic['选择器'], GlobalEnumG.SelectStates, select_transition, "Check")
                try:
                    check_mnq_thread(f"{mnq_name}_{task_name}", mnq_thread_list,
                                     switch_case(self.sn, **taskdic).do_case, thread_while=True)
                except StopTaskErr:
                    self.sn.log_tab.emit(self.mnq_name, f"模拟器adb连接异常断开,停止任务")
                    self.sn.stoptask.emit([self.mnq_name], True)
                except (Exception, TypeError):
                    dev_close = self.dev_list[mnq_name]
                    dev_close.KeyDownChar('up')
                    dev_close.KeyDownChar('down')
                    dev_close.KeyDownChar('left')
                    dev_close.KeyDownChar('right')
                    time.sleep(0.05)
                    dev_close.KeyUpChar('up')
                    dev_close.KeyUpChar('down')
                    dev_close.KeyUpChar('left')
                    dev_close.KeyUpChar('right')
                    dev_close.KeyUpChar('x')
                    dev_close.KeyUpChar('z')
                    dev_close.KeyUpChar('c')
                    dev_close.UnBindWindow()  # 解除绑定
                    ThreadTools.stop_thread_list(mnq_thread_list)
                    mnq_thread_list.clear()
                    self._do_task_list([mnq_name])

    def restart_task(self, mnq_name, mnq_thread_list):
        """重启任务"""

        def stop():
            dev_close = self.dev_list[mnq_name]
            dev_close.KeyDownChar('up')
            dev_close.KeyDownChar('down')
            dev_close.KeyDownChar('left')
            dev_close.KeyDownChar('right')
            dev_close.KeyDownChar('x')
            dev_close.KeyDownChar('z')
            dev_close.KeyDownChar('c')
            time.sleep(0.05)
            dev_close.KeyUpChar('up')
            dev_close.KeyUpChar('down')
            dev_close.KeyUpChar('left')
            dev_close.KeyUpChar('right')
            dev_close.KeyUpChar('x')
            dev_close.KeyUpChar('z')
            dev_close.KeyUpChar('c')
            ThreadTools.stop_thread_list(mnq_thread_list)
            mnq_thread_list.clear()

        dev_colse = self.dev_list[mnq_name]
        dev_colse.UnBindWindow()  # 解除绑定
        ThreadTools('Restart', stop).start()
        self._do_task_list([mnq_name])

    def task_dic(self, devinfo, task_name, mnq_thread_list):
        execute = StateExecute(devinfo, self.sn)
        select = StateSelect(devinfo, self.sn)
        taskdic = {
            '执行器': execute,
            '选择器': select,
            '机器名': devinfo[-1],
            '线程列表': mnq_thread_list,
            '任务名': task_name,
            '位置信息': self.mnq_rownum_dic[devinfo[-1]],
            '队列': {
                '执行器任务队列': QueueManage(1),
                '选择器任务队列': QueueManage(10, lifo=True),
                '楼梯队列': QueueManage(1),
                '方向队列': QueueManage(1),
                '每日任务队列': QueueManage(),
                '休息队列': QueueManage(),
                '队伍队列': self.team_queue_dic,
                '队伍锁': self.team_event_dic,
            }
        }
        return taskdic

    def _get_windows_pid(self):
        """获取设备信息"""

        def ldconsole_find_dev():
            mnq_index_list, mnq_name_list, mnq_subhwnd_list, mnq_hwnd_list = MnqTools().get_mnq_list()
            # print(mnq_index_list, mnq_name_list, mnq_devname_list)
            self.sn.windows_pid.emit(self.ui_main.windows_pid, mnq_index_list,
                                     mnq_name_list, mnq_subhwnd_list, mnq_hwnd_list)

        # def phone_devices():
        #     devindex_list, pinfo_list, dev_name_list = PhoneDevives().get_devices()
        #     self.sn.windows_pid.emit(self.ui_main.windows_pid, devindex_list, pinfo_list, dev_name_list)

        try:
            if self.ui_main.get_windows.isEnabled():
                self.get_timer.start()
                self.ui_main.get_windows.setEnabled(False)
            ld_thread = ThreadTools("获取模拟器窗口句柄", ldconsole_find_dev)
            ld_thread.start()
        except Exception as e:
            print(e)

    @catch_ex
    def set_windows_pid(self, table_object, index_list, pinfo_list, subhwnd_list, hwnd_list):
        """
        设置窗口标题，句柄，pid,设备名
        组件名：windows_pid
        """
        pop = []
        old = []
        new = []
        for _i in range(1, len(index_list) + 1):
            table_object.removeRow(_i)
        table_object.setRowCount(len(index_list))  # 设置行数
        num = len(index_list)
        table_object.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭水平进度条
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
                    self.ui_main.log_tab_wid.removeTab(self.mnq_rownum_dic[mnq_name]['rownum'])
        if len(self.mnq_name_old_list) == 0:
            for _ in range(num):
                self.mnq_name_old_list.append(pinfo_list[_])
        else:
            self.mnq_name_old_list.clear()
            self.mnq_name_old_list = new + old
        for i in range(num):  # 写入单元格
            btn_widget, start_btn, stop_btn = self.table_btn_row()
            self.start_btn_dic[pinfo_list[i]] = start_btn
            self.stop_btn_dic[pinfo_list[i]] = stop_btn
            self.btn_widget_dic[pinfo_list[i]] = btn_widget
            # 存储模拟器行号,序号
            self.mnq_rownum_dic[pinfo_list[i]] = {'rownum': i,
                                                  'index': index_list[i]}
            table_object.setCellWidget(i, 9, btn_widget)  # 在单元格中加入启动、停止按钮
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
            _time = LoadConfig.getconf(pinfo_list[i], '最近登录时间', ini_name=pinfo_list[i])
            table_object.setItem(i, 10, self.set_tableitem_center(
                time.strftime('%m-%d %H:%M:%S', time.localtime(float(_time)))))  # 最近登录时间
            table_object.setItem(i, 11, self.set_tableitem_center('0'))  # 闪退次数
            table_object.setItem(i, 12, self.set_tableitem_center(subhwnd_list[i]))  # 子句柄
            table_object.setItem(i, 13, self.set_tableitem_center(hwnd_list[i]))  # 窗口句柄
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

            # print(self.log_tab_dic)
            if pinfo_list[i] in self.log_tab_dic.keys():
                pass
            else:
                wd = QtWidgets.QWidget()
                ed = QtWidgets.QTextEdit()
                ed.setReadOnly(True)
                ed.document().setMaximumBlockCount(100)
                layout = QVBoxLayout()
                layout.addWidget(ed)
                self.log_tab_dic[pinfo_list[i]] = ed
                wd.setLayout(layout)
                self.ui_main.log_tab_wid.insertTab(i, wd, f"窗口{index_list[i]}")
        if len(self.dev_obj_list) > 0:
            for i in range(num):
                if not pinfo_list[i] in self.dev_obj_list.keys():
                    self.dev_obj_list[pinfo_list[i]] = DevicesConnect.dm_init()
        else:
            for i in range(num):
                self.dev_obj_list[pinfo_list[i]] = DevicesConnect.dm_init()  # 初始化多个链接对象,线程列表
        # if not self.mnq_thread_tid:
        if len(self.mnq_thread_tid) > 0:
            keys = self.mnq_thread_tid.keys()
            for i in range(num):
                if not pinfo_list[i] in keys:
                    self.mnq_thread_tid[pinfo_list[i]] = []
        else:
            for i in range(num):
                self.mnq_thread_tid[pinfo_list[i]] = []
        table_object.setColumnHidden(10, True)  # 隐藏10-13列
        table_object.setColumnHidden(11, True)
        table_object.setColumnHidden(12, True)
        table_object.setColumnHidden(13, True)
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

    def close_btnrefresh(self):
        if self.stop_time > 0:
            self.ui_main.close_all_task_btn.setText(f"{self.stop_time}秒后可点击")
            self.stop_time -= 1
        else:
            self.stop_timer.stop()
            self.ui_main.close_all_task_btn.setEnabled(True)
            self.ui_main.close_all_task_btn.setText(f"全部停止")
            self.stop_time = 3


def main():
    app = QApplication(sys.argv)
    dz = DzUi()
    extra = {
        # Density Scale
        'density_scale': '-1',
        # Font
        'font_family': 'monoespace',
        'font_size': '13px',
        'line_height': '13px',
    }
    # apply_stylesheet(app, 'default', invert_secondary=False, extra=extra)
    color_mode = LoadConfig.getconf('全局配置', '中控颜色')
    if color_mode == '红色':
        apply_stylesheet(app, theme='dark_red.xml', extra=extra)
    elif color_mode == '蓝色':
        apply_stylesheet(app, theme='dark_cyan.xml', extra=extra)
    elif color_mode == '绿色':
        apply_stylesheet(app, theme='dark_teal.xml', extra=extra)
    elif color_mode == '原色':
        pass
    dz.ui_main.show()
    app.exec_()

# if __name__ == '__main__':
#     main()
