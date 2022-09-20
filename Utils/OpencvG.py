# -*- coding: utf-8 -*-
import time

import numpy as np
from airtest.aircv import aircv
from airtest.core.api import touch
from airtest.core.error import TargetNotFoundError
from cnocr import CnOcr

from Enum.ResEnum import GlobalEnumG, ImgEnumG, UiEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.ExceptionTools import NotFindImgErr


class OpenCvTools:
    def __init__(self, dev):
        self.dev = dev

    def get_rgb(self, get_x, get_y):
        """获取某一像素点RBG数据"""
        img = self.dev.snapshot()
        color = img[get_y, get_x]  # 横屏1280x720
        np.array(color)
        r = color.tolist()
        r.reverse()  # 反序
        expoint = ''
        print(r)
        for point in r:
            expoint += str(hex(point))[-2:].replace('x', '0').upper()
        print(expoint)
        return expoint

    def mulcolor_check(self, find_list, clicked=True, duration=GlobalEnumG.TouchDurationTime):
        """对比多个点的颜色，只要有一个错误就返回"""
        for _p in find_list:
            print(_p)
            if self.get_rgb(_p[0], _p[1]) != _p[-1]:
                return False
        if clicked:
            touch(find_list[0][0], find_list[0][1], duration=duration)
        return True

    def find_color(self, get_x, get_y, get_x1, get_y1, f_color):
        """
        指定范围查找颜色
        :param get_x:
        :param get_y:
        :param get_x1:
        :param get_y1:
        :param f_color: 需要查找的颜色
        :return: 返回找到的坐标
        """
        for x in range(get_x, get_x1):
            for y in range(get_y, get_y1):
                color = self.get_rgb(x, y)
                if color == f_color:
                    return x, y
        return False


class AirImgTools:
    def __init__(self):
        self.dev = None

    # @staticmethod
    def crop_image_find(self, area_temp, clicked=True, timeout=0.1, touch_wait=0):
        """区域找图"""
        try:
            screen = self.dev.snapshot()
            area = area_temp[0]
            temp = area_temp[-1]
            crop_img = aircv.crop_image(screen, area)
            s_time = time.time()
            while time.time() - s_time < timeout:
                res = temp.match_in(crop_img)
                if res:
                    pos = (res[0] + area[0], res[1] + area[1])
                    if clicked:
                        if touch_wait > 0:
                            time.sleep(touch_wait)
                        self.dev.touch(pos)
                    return True
            return False
            # print(time.time()-start_time)
            # raise NotFindImgErr(f"范围{area}中未找到{temp}_超时时长{timeout}")
        except (NotFindImgErr, AttributeError) as e:
            print(e)
            return False

    # @staticmethod
    def air_loop_find(self, temp, clicked=True, timeout=GlobalEnumG.FindImgTimeOut):
        """
        循环查找图片并点击，超时返回
        """
        try:
            img = temp[-1]
            s_time = time.time()
            while time.time() - s_time < timeout:  # 超时
                screen = self.dev.snapshot()
                if screen is None:
                    raise TargetNotFoundError
                else:
                    match_pos = img.match_in(screen)
                    if match_pos:
                        if clicked:
                            self.dev.touch(match_pos)
                    return True
        except TargetNotFoundError as e:
            print(e.value)
            return False

    def air_touch(self, touch_x, touch_y, duration=0):
        return self.dev.touch((touch_x, touch_y), duration=duration)


class ImageCreat:
    def __init__(self, img):
        self.img = img

    def crop_image(self, area):
        """"区域裁剪"""
        return aircv.crop_image(self.img, area)


class CnOcrTool:
    def __init__(self):
        self.dev = None

    def ocr_find(self, ocr_list, clicked=False):
        """
        范围查找文字，返回坐标
        :param ocr_list:查找文字范围和文字
        :param clicked: 是否点击
        :return: 查找结果
        """
        x1,y1,x2,y2=ocr_list[0]
        screen = self.dev.snapshot()
        img_fp = aircv.crop_image(screen, ocr_list[0])
        ocr = CnOcr(rec_model_name='densenet_lite_136-fc',
                    det_model_name='ch_PP-OCRv3_det')  # 'ch_PP-OCRv3_det')  # ch_PP-OCRv3繁体中文匹配模型
        out = ocr.ocr(img_fp)
        if len(out) == 0:
            return False
        for i in range(len(out)):
            ntext = out[i]['text']
            print(ntext)
            if ocr_list[-1] in ntext:
                npar = out[i]['position']
                ls = npar.tolist()
                lx = int((ls[-2][0] + ls[0][0]) / 2)
                ly = int((ls[-2][-1] + ls[0][-1]) / 2)
                if clicked:
                    self.dev.touch((lx + x1, ly + y1))
                return True
        return False

    @staticmethod
    def get_ocrres():
        pass


if __name__ == '__main__':
    # img_fp = r'D:\DzAutoUi\Res\img\21.bmp'
    # res, dev = DevicesConnect('emulator-5554').connect_device()
    res2, dev2 = DevicesConnect('emulator-5556').connect_device()
    # img=G.DEVICE.snapshot()
    # aircv.imwrite(r'D:\DzAutoUi\Res\img\21.png',img)
    # loop_find(img_fp)
    try:
        # start_time = time.time()
        # print(start_time)
        # c = CnOcrTool()
        c=AirImgTools()
        c.dev = dev2
        # while True:
        r= c.air_loop_find(ImgEnumG.UI_LB)
        # r = c.ocr_find(40, 88, 152, 104, '佃人', True)
        # r=OpenCvTools(dev2).get_rgb(431, 654)
        print(r)
        # r=touch(ImgEnumG.GAME_ICON,times=1)
        # AirImgTools.air_loop_find(ImgEnumG.TEST, 0.1)
        # r=CnOcrTool.ocr_find(0,0,1280,720,'rr')
        # r = ImgEnumG.LOGIN_FLAG1[0]
        # x = ImgEnumG.LOGIN_FLAG1[-1]
        # print(r, x)
        # r1 = AirImgTools.crop_image_find(dev, ImgEnumG.GAME_ICON)
        # r = AirImgTools.crop_image_find(dev2, ImgEnumG.GAME_ICON, True)
        # r=OpenCvTools().mulcolor_check(UiEnumG.BAG_UI)
        # print(r, r1)
        # print(time.time() - start_time)
    except TargetNotFoundError:
        print('err')
    # r=AirImgTools.air_loop_find(ResEnumG.GAME_ICON,1)

    # ocr = CnOcr(rec_model_name='densenet_lite_136-fc',det_model_name='ch_PP-OCRv3_det')
    # out = ocr.ocr(img_fp)
    # print(out)
    # img = cv2.imread(r"C:\Users\igg\Pictures\08_18_21_04_39.bmp")
    # print(aircv.get_resolution(img))
    # resize = cv2.resize(img, (), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # OpenCvTools(img).find_color()
    # t = time.time()
    # r = OpenCvTools(img).find_color(1250, 160, 1255, 172, 'DCDEE1')
    # t2 = time.time() - t
    # print(t2, r)
    # print(len(img))
    # img2 = aircv.crop_image(img, (100, 200, 151, 252))
    # print(len(img2))
    # print(aircv.get_resolution(img2))
    # OpenCvTools(img2).get_rgb(10, 10)
    # print(type(img2))
    # cv2.imshow('t', img2)
    # while True:
    #     if cv2.waitKey(0):
    #         break
