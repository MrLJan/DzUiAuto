# coding=gbk
import os
import sys


def exe_path():
    if hasattr(sys, 'frozen'):
        path_sys = os.path.dirname(sys.executable)
        return path_sys  # ʹ��pyinstaller������exeĿ¼
    path_py = os.path.dirname(__file__)
    return path_py  # û���ǰ��pyĿ¼


path = exe_path()

