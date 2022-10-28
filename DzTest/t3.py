# -*- coding: utf-8 -*-
import numpy
from airtest.core.android import Android
from cv2 import cv2
from matplotlib import pyplot as plt

dev = Android(serialno='127.0.0.1:5555')
e1 = cv2.getTickCount()
# img = cv2.imread(r"D:\xd\M\DZ\15.png", flags=0)  # 读取彩色图像(BGR)
img=dev.snapshot(filename=r'D:\xd\M\DZ\15.png')
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
crop_img = img[364:878, 584:1824]
# sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# gaussian = cv2.GaussianBlur(crop_img, (1, 1), 1)
ret1, img1 = cv2.threshold(crop_img, 0, 255, cv2.THRESH_OTSU)  # 转换为二值图像, thresh=63
contours, hierarchy = cv2.findContours(img1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
pos_list = []
plt.figure(figsize=(10, 9))
# pos_list2 = copy.deepcopy(pos_list)
all_list = []
pos_y = None
s_index = 0
e_index = 0
for _i in range(len(contours)):
    x, y, w1, h1 = cv2.boundingRect(contours[_i])
    if pos_y is None:
        pos_y = y
    ar = w1 / float(h1)
    print(ar, x, y, w1, h1)
    if 0.8 >= ar > 0.5:
        pos_list.append((x, y, w1, h1))

print(f"p{pos_list}")
pos_list.reverse()
temp = {
    r'D:\xd\M\DZ\p0.npy': '0',
    r'D:\xd\M\DZ\p1.npy': '1',
    r'D:\xd\M\DZ\p2.npy': '2',
    r'D:\xd\M\DZ\p3.npy': '3',
    r'D:\xd\M\DZ\p4.npy': '4',
    r'D:\xd\M\DZ\p5.npy': '5',
    r'D:\xd\M\DZ\p6.npy': '6',
    r'D:\xd\M\DZ\p7.npy': '7',
    r'D:\xd\M\DZ\p8.npy': '8',
    r'D:\xd\M\DZ\p9.npy': '9',
}
_re=[]
for _row in range(len(pos_list)):
    _con=0.8
    for _p in temp.keys():
        # res = cv2.matchTemplate(
        #     cv2.resize(crop_img[pos_list[_row][1]:pos_list[_row][1] + pos_list[_row][-1],
        #     pos_list[_row][0]:pos_list[_row][0] + pos_list[_row][2]],(72,128)),
        #     numpy.load(_p), method=cv2.TM_CCOEFF_NORMED)
        plt.subplot(3, 30, _row + 1), plt.title(f'{_row}'), plt.axis('off')
        plt.imshow(crop_img[pos_list[_row][1]:pos_list[_row][1] + pos_list[_row][-1],
                              pos_list[_row][0]:pos_list[_row][0] + pos_list[_row][2]])
        # if _row == 17:
        #     _f = 'p4'
        #     file_name = f"D:\\xd\\M\\DZ\\{_f}"
        #     numpy.save(file_name, cv2.resize(crop_img[pos_list[_row][1]:pos_list[_row][1] + pos_list[_row][-1],
        #                                      pos_list[_row][0]:pos_list[_row][0] + pos_list[_row][2]], (72, 128)))
        # if numpy.any(res[0]>_con):
        #     print(res, type(res))
        #     _re.append(temp[_p])
        #     _con=100
print(_re)
        # _f =r'999'

        # elif _row == 0:
        #     _f = 'p4'
        # elif _row == 4:
        #     _f = 'p5'
        # elif _row == 6:
        #     _f = 'p7'
        # elif _row == 11:
        #     _f = 'p8'
        # elif _row == 8:
        #     _f = 'p6'
        # elif _row == 14:
        #     _f = 'p9'
        # elif _row == 16:
        #     _f = 'p4'
        # file_name = f"D:\\xd\\M\\DZ\\{_f}"
        # numpy.save(file_name, cv2.resize(crop_img[pos_list[_row][1]:pos_list[_row][1] + pos_list[_row][-1],
        #                                  pos_list[_row][0]:pos_list[_row][0] + pos_list[_row][2]], (72, 128)))
        # if numpy.any(res > 0.9):
        #     plt.subplot(3, 10, _row+1), plt.title(f'_row'), plt.axis('off')
        #     plt.imshow(crop_img[pos_list[_row][1]:pos_list[_row][1] + pos_list[_row][-1], pos_list[_row][0]:pos_list[_row][0] + pos_list[_row][2]])
e2 = cv2.getTickCount()

time1 = (e2 - e1) / cv2.getTickFrequency()
print(time1)
plt.subplot(3, 10, 19), plt.title('img_closed'), plt.axis('off')
plt.imshow(img1)
plt.show()
