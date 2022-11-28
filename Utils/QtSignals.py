# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtWidgets import QTextBrowser, QLabel, QTableWidget, QPushButton


class QtSignals(QtCore.QObject):
    """
    处理信号定义
    signal(组件类型,传递参数类型）
    使用：
    实例化 self.sn=QtSignals()
        self.sn.edit_text.connect(self.处理函数）
    处理函数
        self.sn.edit_text.emit(组件名,"文本")
    """
    edit_text = QtCore.pyqtSignal(QTextBrowser, int)  # 更改进度条控件文本
    message_box = QtCore.pyqtSignal(str, str)  # 弹窗消息
    label_text = QtCore.pyqtSignal(QLabel, str)  # 更改标签文本
    mnq_index = QtCore.pyqtSignal(QLabel, int)  # 模拟器indexID
    device_list = QtCore.pyqtSignal(QTableWidget, list)  # 设备列表
    windows_pid = QtCore.pyqtSignal(QTableWidget, list, list, list,list)  # 窗口句柄列表
    table_value = QtCore.pyqtSignal(str, int, str)  # 表格更新
    thread_name = QtCore.pyqtSignal(list, str)
    start_thread = QtCore.pyqtSignal(int, str)
    error_label = QtCore.pyqtSignal(str, str)  # 桌面弹窗提示
    log_tab = QtCore.pyqtSignal(str, str)  # 输出各窗口日志
    btn_enable = QtCore.pyqtSignal(QPushButton, bool)
    task_over_signal = QtCore.pyqtSignal(str, str)
    close_mnq_index = QtCore.pyqtSignal(str)
    restart = QtCore.pyqtSignal(str, list)
    stoptask=QtCore.pyqtSignal(list,bool)
    # task_thread=QtCore.pyqtSignal(int, str,int)
    # 重定向信号
    text_signal = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.text_signal.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(10, loop.quit)
        loop.exec_()

    def flush(self):
        pass


sn = QtSignals()
