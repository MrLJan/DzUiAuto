# -*- coding: utf-8 -*-
import random
import time

import numpy
from cv2 import cv2

from Utils.AdbUtils import PhoneDevives
from Utils.OtherTools import OT


class test:

    def __init__(self, bat):
        self.task = 1
        self.bat = bat
        self.func_list = {
            't1': [self.t1(self.task), self.t2]
        }

    def t1(self, x):
        print(x)
        return 5

    def t2(self, **kwargs):
        # print(args)
        print(kwargs['mapdata']['mapid'], self.task, self.bat)
        time.sleep(4)
        if self.task == 1:
            self.t3()

    def t3(self, **kwargs):
        time.sleep(3)
        print(kwargs)


if __name__ == '__main__':
    serialno='127.0.0.1:5555'
    r=serialno.split(':')[-1]
    adb=PhoneDevives(serialno=serialno,display_id=r'D:\DzUiAuto\Res\ddd.png').adb
    # byteImage = adb.cmd(cmds='shell screencap -p > /sdcard/screen.png', device=serialno, ensure_unicode=False)
    # print(byteImage)
    r1=adb.snapshot()
    print(r1)
    adb.shell('screencap -p > /sdcard/screen.png')
    adb.pull(local=OT.abspath(f'/Res/{r}.png'),remote='/sdcard/screen.png')
    color=cv2.imread(OT.abspath(f'/Res/{r}.png'))

    # byteImage = adb.cmd(cmds='shell screencap -p',device=serialno,ensure_unicode=False).replace(b'\r\n', b'\n').replace(b'\r\n', b'\n')
    # cv2.imwrite(OT.abspath('Res/fff.png'),byteImage)
    # # opencv读取内存图片
    # print(byteImage)
    # r1=cv2.imdecode(numpy.asarray(bytearray(byteImage), dtype=numpy.uint8), cv2.IMREAD_GRAYSCALE)
    # r=snapshot()
    # print(byteImage,r1)
    # print(type(r1),r1)
