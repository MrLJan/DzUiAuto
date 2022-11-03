# # -*- coding: utf-8 -*-
# import numpy
# from airtest.core.android import Android
# from cv2 import cv2
# from matplotlib import pyplot as plt
#
# dev = Android(serialno='127.0.0.1:5555')
# e1 = cv2.getTickCount()
# img = dev.snapshot()
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# crop_img = img[150:609, 1091:1156]
# sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
#
# ret1, img1 = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 转换为二值图像, thresh=63
# contours, hierarchy = cv2.findContours(img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# print(len(contours))
# M = cv2.moments(contours[0])
# cX = int(M["m10"] / M["m00"])
# cY = int(M["m01"] / M["m00"])
# print(cX, cY)
# pos_list = []
#
# # pos_list2 = copy.deepcopy(pos_list)
# all_list = []
# pos_y = None
# s_index = 0
# e_index = 0
# for _i in range(len(contours)):
#     x, y, w1, h1 = cv2.boundingRect(contours[_i])
#     if pos_y is None:
#         pos_y = y
#     ar = w1 / float(h1)
#     print(ar, x, y, w1, h1)
#     if 0.8 > ar > 0.5 and 20>h1>10:
#         pos_list.append((x, y, w1, h1))
#
# print(f"p{pos_list}")
# pos_list.reverse()
# for _ in range(len(pos_list)):
#     if abs(pos_y - pos_list[_][1]) <= 1:
#         if _ == len(pos_list) - 1:
#             all_list.append(pos_list[s_index:])
#         else:
#             pass
#     else:
#         e_index = _
#         all_list.append(pos_list[s_index:e_index])
#         s_index = _
#         pos_y = pos_list[_][1]
#
# print(f"a{all_list}")
#
# temp = {
#     r'D:\xd\M\DZ\p0.npy': '0',
#     r'D:\xd\M\DZ\p1.npy': '1',
#     r'D:\xd\M\DZ\p2.npy': '2',
#     r'D:\xd\M\DZ\p3.npy': '3',
#     r'D:\xd\M\DZ\p4.npy': '4',
#     r'D:\xd\M\DZ\p5.npy': '5',
#     r'D:\xd\M\DZ\p6.npy': '6',
#     r'D:\xd\M\DZ\p7.npy': '7',
#     r'D:\xd\M\DZ\p8.npy': '8',
#     r'D:\xd\M\DZ\p9.npy': '9',
# }
# _res_pos = []
# _str = ''
# _x = 0
# _y = 0
# for _ in range(len(all_list)):
#     if len(all_list[_]) > 0:
#         for _t in all_list[_]:
#             _con = 0.8
#             for _p in temp.keys():
#                 res = cv2.matchTemplate(
#                     cv2.resize(crop_img[_t[1]:_t[1] + _t[-1], _t[0]:_t[0] + _t[2]], (72, 128)),
#                     numpy.load(_p), method=cv2.TM_CCOEFF_NORMED)
#                 if numpy.any(res > _con):
#                     _str = _str + temp[_p]
#                     _x = _t[0]
#                     _y = _t[1]
#                     _con = 100
#         _res_pos.append((_str, (_x + 1091, _y + 150)))
#         _str = ''
# print(_res_pos)
# e2 = cv2.getTickCount()
# plt.figure(figsize=(10, 9))
# time1 = (e2 - e1) / cv2.getTickFrequency()
# print(time1)
# plt.subplot(3, 10, 17), plt.title('img_closed'), plt.axis('off')
# plt.imshow(crop_img)
# plt.show()
