# -*- encoding=utf8 -*-
import re
import time

from Enum.ResEnum import ImgEnumG, BatEnumG
from Utils.ThreadTools import ThreadTools


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
    a = '塔'
    b = '^金.塔'
    p=re.match(b,a)
    print(p)