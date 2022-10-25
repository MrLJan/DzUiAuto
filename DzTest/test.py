# -*- coding: utf-8 -*-
import random
import time

import numpy
from airtest.core.android import Android
from cv2 import cv2
from matplotlib import pyplot as plt

from Utils.AdbUtils import PhoneDevives
from Utils.Devicesconnect import DevicesConnect
from Utils.OtherTools import OT


# dev = Android(serialno='127.0.0.1:5579',cap_method='ADBCAP')
# dev2 = Android(serialno='127.0.0.1:5579')
# img1=dev.snapshot(filename=r'D:\xd\M\DZ\11.png')
# img2=dev2.snapshot()
# e1 = cv2.getTickCount()
# img.item(10,10,0)
# img.item(10,10,1)
# img.item(10,10,2)
# e2 = cv2.getTickCount()
# time1 = (e2 - e1)/ cv2.getTickFrequency()
# print(time1)
# hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# lower=numpy.array([0,0,0])
# hight=numpy.array([0,0,255])
# mask=cv2.inRange(hsv,lower,hight)
# img_end=cv2.bitwise_and(img,img,mask=mask)
# cv2.rectangle(img,(384,555),(510,128),(0,255,0),3)#话画矩形
# cv2.imshow('image',hsv)
# cv2.imshow('mask',mask)
# cv2.imshow('img_end',img_end)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.destroyAllWindows()
# 1.29 图像的位操作
img = cv2.imread(r"D:\xd\M\DZ\11.png",flags=0)  # 读取彩色图像(BGR)
ret1, img1 = cv2.threshold(img, 63, 255, cv2.THRESH_BINARY)  # 转换为二值图像, thresh=63
ret2, img2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # 转换为二值图像, thresh=127
ret3, img3 = cv2.threshold(img, 11, 255, cv2.THRESH_BINARY)  # 转换为二值图像, thresh=191
ret4, img4 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)  # 逆二值图像，BINARY_INV
ret5, img5 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)  # TRUNC 阈值处理，THRESH_TRUNC
ret6, img6 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)  # TOZERO 阈值处理，THRESH_TOZERO
# img2 = cv2.imread("../images/imgB2.jpg")  # 读取彩色图像(BGR)
plt.figure(figsize=(9, 6))
titleList = [f"1. BINARY(thresh={ret1})", f"2. BINARY(thresh={ret2})", f"3. BINARY(thresh={ret3})", f"4. THRESH_BINARY_INV{ret4}", f"5. THRESH_TRUNC{ret5}", f"6. THRESH_TOZERO{ret6}"]
imageList = [img1, img2, img3, img4, img5, img6]
for i in range(6):
    plt.subplot(2, 3, i+1), plt.title(titleList[i]), plt.axis('off')
    plt.imshow(imageList[i], 'gray')  # 灰度图像 ndim=2
# plt.subplot(1,1,1),plt.title('img2'),plt.axis('off')
# plt.imshow(cv2.cvtColor(img1,cv2.COLOR_BGR2RGB),'gray')
plt.show()

