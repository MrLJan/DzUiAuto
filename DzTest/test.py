# -*- coding: utf-8 -*-
import time

import uiautomator2 as u2
from cv2 import cv2
from matplotlib import pyplot as plt

from Enum.ResEnum import ImgEnumG
from Utils.OtherTools import OT

t1=time.time()
d=u2.connect('127.0.0.1:5555')
# print(d.toast.get_message())
# d.click()

d.screenshot(filename=r'D:\DzUiAuto\127.0.0.1:5555.png')
r=cv2.imread(r'D:\DzUiAuto\127.0.0.1:5555.png')
# d.__init__('127.0.0.1:5555')
print(type(d.serial))
# d.app_stop('com.nexon.maplem.global')
# d.screenshot(format='opencv')
# rr=d.screenshot(format='opencv')
res=OT.imgpath('22222')
tr=d.image.match(res)
# x,y=tr['point']
# d.healthcheck()
# d.click(x,y)
print(tr)

# d.click(286,187)
# _img = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
# print(type(r),time.time()-t1)
# plt.figure(figsize=(10, 9))
# cv2.imshow('dst', r)
# plt.show()