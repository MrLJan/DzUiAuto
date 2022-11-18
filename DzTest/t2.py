# -*- coding: utf-8 -*-
import numpy
from airtest.core.android import Android
from cv2 import cv2
from matplotlib import pyplot as plt
from Utils.OtherTools import OT

dev = Android(serialno='127.0.0.1:5555',cap_method='JAVACAP')

# img = cv2.imread(r"D:\xd\M\DZ\15.png", flags=0)  # 读取彩色图像(BGR)
img = dev.snapshot()
x, y, x1, y1 = 88, 198, 210, 382  # 92,11,241,66
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# _crop_img = img[158:580, 38:1268]
_crop_img = img[y:y1, x:x1]
pos_list = []
# _crop_img=cv2.resize(_crop_img,(128,72))
# sqKernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
_img1 = cv2.threshold(_crop_img.copy(), 240, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 转换为二值图像, thresh=63
_img2 = cv2.morphologyEx(_img1, cv2.MORPH_CLOSE, sqKernel)
res_cont = cv2.findContours(_img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
print(len(res_cont))
ori_list = []
for cnt in res_cont:
    x, y, w1, h1 = cv2.boundingRect(cnt)
    ar = w1 / float(h1)
    print(ar, x, y, w1, h1)
    if 100 > ar > 5 and w1 > 50:
        print(ar, x, y, w1, h1)
        ori_list.append([_crop_img[y:y + h1, x:x + w1], (x, y)])
ori_list = sorted(ori_list, key=lambda x: x[-1][0])

plt.figure(figsize=(10, 9))
_bat_num = ''
_res_pos = []
_x = 0  # 存储计算每行数字的坐标
_y = 0
# _cmp_img=OT.npypath()
for _row in range(len(ori_list)):
    # for _p in OpenCvEnumG.XT_MAP.keys():
    plt.subplot(3, 10, _row + 1), plt.title(f'{_row}'), plt.axis('off')
    plt.imshow(ori_list[_row][0])

    _re = cv2.matchTemplate(
        cv2.resize(ori_list[_row][0], (72, 128)),
        numpy.load(OT.npypath('team_zdjr')), method=cv2.TM_CCOEFF_NORMED)
    print(_re)
    if numpy.any(_re > 0.9):
        _bat_num = _bat_num + 'bat_auto'
        # print(f"{row}_{_t}_{ori_list[row][-1][0]+38}_y{ori_list[row][-1][-1]+158}")
        _res_pos.append((_bat_num, ori_list[_row][1]))
        _bat_num = ''
    _f = '999'
    _on = 11
    if _row == 0:
        _f = 'team_zdjr'
    # elif _row==1:
    #     _f='team_cldw'
    # elif _row==2:
    #     _f='team_zdjr'
    # elif _row==6:
    #     _f='mr_gh'
    # elif _row==7:
    #     _f='mr_xl'
    # elif _row==8:
    #     _f='mr_wl'
    # elif row==6:
    #     _f='tjp'
    # elif row==9:
    #     _f='jy'
    # elif row==10:
    #     _f='mr'
    if _on == 1:
        file_name = f"D:\\xd\\M\\DZ\\{_f}"
        numpy.save(file_name, cv2.resize(ori_list[_row][0], (72, 128)))
    # out_num(ori_list[row],row+1)
# plt.subplot(3, 1, 1), plt.title('img_closed'), plt.axis('off')
# plt.imshow(img_closed)
# plt.subplot(3, 7, 15), plt.title('img1'), plt.axis('off')
# plt.imshow(img1)
print(_res_pos)
dst = cv2.drawContours(_crop_img.copy(), res_cont, -1, (0, 0, 125), 1)
# cv2.imwrite(r'D:\xd\M\DZ\jy.png',xl)
# plt.subplot(3, 7, 16), plt.title('dst'), plt.axis('off')
# plt.imshow(dst)
cv2.imshow('img1', _img1)
cv2.imshow('dst', dst)
plt.show()
