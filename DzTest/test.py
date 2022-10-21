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
    XT_MAP = {
        147: '崎岖的峡谷',
        144: '灰烬之风高原'
    }
    x = 145
    print(XT_MAP.keys())
    for i in XT_MAP.keys():
        if x > i:
            print(XT_MAP[i])
