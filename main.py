# -*- coding:utf-8 -*-
import os
import sys
import time


import torch
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtGui import QTextCursor, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, \
    QTreeWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QTimer, QRegExp
from airtest.core.android.touch_methods.base_touch import DownEvent, SleepEvent, UpEvent
from cnocr import CnOcr
from cv2 import cv2

from DzTest.DzModeMachine import switch_case, StateExecute, StateMachine, StateSelect, execute_transition, \
    select_transition
from Utils.ExceptionTools import RestartTask
from Utils.LoadConfig import LoadConfig
from Utils.MnqTools import MnqTools
from Utils.OtherTools import OT, catch_ex
from Utils.QtSignals import QtSignals
from Utils.QueueManageTools import QueueManage
from Utils.ThreadTools import ThreadTools, check_mnq_thread
from Utils.AdbUtils import PhoneDevives
from Enum.ResEnum import GlobalEnumG
from Utils.Devicesconnect import DevicesConnect

import dzmainui
if __name__ == '__main__':
    dzmainui.main()
