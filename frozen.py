# coding=gbk
import os
import sys


def exe_path():
    if hasattr(sys, 'frozen'):
        path_sys = os.path.dirname(sys.executable)
        return path_sys  # 使用pyinstaller打包后的exe目录
    path_py = os.path.dirname(__file__)
    return path_py  # 没打包前的py目录


path = exe_path()

