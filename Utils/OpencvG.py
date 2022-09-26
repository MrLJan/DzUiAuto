# -*- coding: utf-8 -*-
import re
import time

import numpy as np
from airtest.aircv import aircv
from airtest.core.android.touch_methods.base_touch import DownEvent, SleepEvent, UpEvent
from airtest.core.error import TargetNotFoundError
from cnocr import CnOcr

from Enum.ResEnum import GlobalEnumG, ImgEnumG, BatEnumG
from UiPage import DailyTaskG
# from UiPage import UpRoleG
# from UiPage import RewardG
# from UiPage import AutoBatG
# from UiPage import TeamStateG
# from UiPage import StateCheckG
from Utils.Devicesconnect import DevicesConnect
from Utils.ExceptionTools import NotFindImgErr
from Utils.QueueManageTools import QueueManage


class OpenCvTools:
    def __init__(self):
        self.dev = None

    def get_rgb(self, get_x, get_y, find_color=None, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime):
        """获取某一像素点RBG数据"""
        img = self.dev.snapshot()
        color = img[get_y, get_x]  # 横屏1280x720
        np.array(color)
        r = color.tolist()
        r.reverse()  # 反序
        expoint = ''
        for point in r:
            expoint += str(hex(point))[-2:].replace('x', '0').upper()
        print(expoint)
        if expoint == find_color:
            if clicked:
                self.dev.touch((get_x, get_y))
                if touch_wait > 0:
                    time.sleep(touch_wait)
            return True
        return False

    def mulcolor_check(self, find_list, clicked=True, touch_wait=GlobalEnumG.TouchWaitTime):
        """对比多个点的颜色，只要有一个错误就返回"""
        for _p in find_list:
            print(_p)
            if self.get_rgb(_p[0], _p[1]) != _p[-1]:
                return False
        if clicked:
            self.dev.touch((find_list[0][0], find_list[0][1]))
            if touch_wait > 0:
                time.sleep(touch_wait)
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

    turn_pos = {
        'up': (146, 471),
        'down': (144, 629),
        'left': (79, 543),
        'right': (239, 544),
        'jump': (1207, 624),
        'attack': (1074, 619),
        'c': (948, 659),
        'v': (958, 559),
        'd': (1054, 501),
        'f': (1148, 505)
    }

    # @staticmethod
    def crop_image_find(self, area_temp, clicked=True, timeout=0.1, touch_wait=GlobalEnumG.TouchWaitTime,
                        get_pos=False):
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
                        self.dev.touch(pos)
                        if touch_wait > 0:
                            time.sleep(touch_wait)
                    if get_pos:
                        return True, pos[0], pos[-1]
                    return True
            if get_pos:
                return False, 0, 0
            return False
            # print(time.time()-start_time)
            # raise NotFindImgErr(f"范围{area}中未找到{temp}_超时时长{timeout}")
        except (NotFindImgErr, AttributeError) as e:
            print(e)
            return False

    def find_all_pos(self, temp, timeout=GlobalEnumG.FindImgTimeOut):
        try:
            img = temp[-1]
            s_time = time.time()
            pos_list = []
            while time.time() - s_time < timeout:  # 超时
                screen = self.dev.snapshot()
                if screen is None:
                    raise TargetNotFoundError
                else:
                    match_pos = img.match_all_in(screen)
                    if not match_pos:
                        return False, (0, 0)
                    for pos in match_pos:
                        res = pos['result']
                        pos_list.append(res)
                    return True, pos_list
        except TargetNotFoundError as e:
            print(e.value)
            return False, (0, 0)

    def air_loop_find(self, temp, clicked=True, timeout=GlobalEnumG.FindImgTimeOut,
                      touch_wait=GlobalEnumG.TouchWaitTime):
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
                    if not match_pos:
                        return False
                    if match_pos:
                        if clicked:
                            self.dev.touch(match_pos)
                            if touch_wait > 0:
                                time.sleep(touch_wait)
                    return True
        except TargetNotFoundError as e:
            print(e.value)
            return False

    def air_touch(self, touch_xy, duration=0.2, touch_wait=0):
        self.dev.touch(touch_xy, duration=duration)
        if touch_wait > 0:
            time.sleep(touch_wait)

    def air_swipe(self, start_xy, end_xy, swipe_wait=0):
        self.dev.swipe(start_xy, end_xy)
        if swipe_wait > 0:
            time.sleep(swipe_wait)

    def move_turn(self, turn, k_time):
        _pos = self.turn_pos[turn]
        self.air_touch(_pos, duration=k_time)

    def mul_point_touch(self, turn, action, k_time=1, long_click=False):
        """多点长按，控制移动"""

        t_pos = self.turn_pos[turn]
        a_pos = self.turn_pos[action]
        if long_click:
            multitouch_event = [
                DownEvent(t_pos, 0),  # 手指1按下(100, 100)
                DownEvent(a_pos, 1),  # 手指2按下(200, 200)
                SleepEvent(k_time),
                UpEvent(0), UpEvent(1)
            ]
        else:
            multitouch_event = [
                DownEvent(t_pos, 0),  # 手指1按下(100, 100)
                DownEvent(a_pos, 1),  # 手指2按下(200, 200)
                UpEvent(1),
                SleepEvent(0.1),
                DownEvent(a_pos, 1),
                SleepEvent(0.1),
                UpEvent(1),
                SleepEvent(k_time),
                UpEvent(0)
            ]
            # UpEvent(0), UpEvent(1)]  # 2个手指分别抬起
        self.dev.touch_proxy.perform(multitouch_event)


class ImageCreat:
    def __init__(self, img):
        self.img = img

    def crop_image(self, area):
        """"区域裁剪"""
        return aircv.crop_image(self.img, area)


class CnOcrTool:
    def __init__(self):
        self.dev = None

    def ocr_find(self, ocr_list, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime):
        """
        范围查找文字，返回坐标
        :param ocr_list:查找文字范围和文字
        :param clicked: 是否点击
        :param touch_wait: 点击后等待时长
        :return: 查找结果
        """
        x1, y1, x2, y2 = ocr_list[0]
        screen = self.dev.snapshot()
        img_fp = aircv.crop_image(screen, (x1, y1, x2, y2))
        ocr = CnOcr(rec_model_name='densenet_lite_136-fc',
                    det_model_name='ch_PP-OCRv3_det')  # 'ch_PP-OCRv3_det')  # ch_PP-OCRv3繁体中文匹配模型
        out = ocr.ocr(img_fp)
        if len(out) == 0:
            return False
        for i in range(len(out)):
            ntext = out[i]['text']
            if ocr_list[-1] in ntext:
                npar = out[i]['position']
                ls = npar.tolist()
                lx = int((ls[-2][0] + ls[0][0]) / 2)
                ly = int((ls[-2][-1] + ls[0][-1]) / 2)
                if clicked:
                    self.dev.touch((lx + x1, ly + y1))
                    if touch_wait > 0:
                        time.sleep(touch_wait)
                print(ocr_list[-1])
                return True
        return False

    def get_all_text(self, ocr_list):
        find_pos_list = []
        x1, y1, x2, y2 = ocr_list[0]
        screen = self.dev.snapshot()
        img_fp = aircv.crop_image(screen, (x1, y1, x2, y2))
        ocr = CnOcr(rec_model_name='densenet_lite_136-fc',
                    det_model_name='ch_PP-OCRv3_det')  # 'ch_PP-OCRv3_det')  # ch_PP-OCRv3繁体中文匹配模型
        out = ocr.ocr(img_fp)
        if len(out) == 0:
            return False
        for i in range(len(out)):
            ntext = out[i]['text']
            if ocr_list[-1] in ntext:
                npar = out[i]['position']
                ls = npar.tolist()
                lx = int((ls[-2][0] + ls[0][0]) / 2)
                ly = int((ls[-2][-1] + ls[0][-1]) / 2)
                find_pos_list.append((lx + x1, ly + y1))
        return find_pos_list

    def get_ocrres(self, area):
        """
        范围查找文字，返回坐标
        :param ocr_list:查找文字范围和文字
        :return: 查找结果
        """
        screen = self.dev.snapshot()
        img_fp = aircv.crop_image(screen, area)
        ocr = CnOcr(rec_model_name='densenet_lite_136-fc',
                    det_model_name='ch_PP-OCRv3_det')  # 'ch_PP-OCRv3_det')  # ch_PP-OCRv3繁体中文匹配模型
        out = ocr.ocr(img_fp)
        if len(out) == 0:
            return False
        for i in range(len(out)):
            ntext = out[i]['text']
            return ntext

    def get_all_ocr(self, area):
        screen = self.dev.snapshot()
        x1, y1, x2, y2 = area
        img_fp = aircv.crop_image(screen, area)
        res_list = []
        ocr = CnOcr(rec_model_name='densenet_lite_136-fc',
                    det_model_name='ch_PP-OCRv3_det')  # 'ch_PP-OCRv3_det')  # ch_PP-OCRv3繁体中文匹配模型
        out = ocr.ocr(img_fp)
        if len(out) == 0:
            return False
        for i in range(len(out)):
            ntext = out[i]['text']
            npar = out[i]['position']
            ls = npar.tolist()
            lx = int((ls[-2][0] + ls[0][0]) / 2)
            ly = int((ls[-2][-1] + ls[0][-1]) / 2)
            if ntext != '':
                res_list.append((ntext, (lx + x1, ly + y1)))
        return res_list


if __name__ == '__main__':
    # img_fp = r'D:\DzAutoUi\Res\img\21.bmp'
    # res, dev = DevicesConnect('emulator-5554').connect_device()
    res2, dev2 = DevicesConnect('127.0.0.1:5557').connect_device()
    print(res2, dev2)
    # img=G.DEVICE.snapshot()
    # aircv.imwrite(r'D:\DzAutoUi\Res\img\21.png',img)
    # loop_find(img_fp)
    try:
        # start_time = time.time()
        # print(start_time)
        c = CnOcrTool()
        a = AirImgTools()
        o = OpenCvTools()
        c.dev = dev2
        a.dev = dev2
        o.dev = dev2
        # while True:
        #     r=c.crop_image_find(ImgEnumG.PERSON_POS,clicked=False,get_pos=True)
        #     print(r)
        # r = c.mul_point_touch('down', 'jdown', k_time=1)
        # r=UpRoleG.UpRoleG((dev2,'emulator-5556'),'ld1',1).upequip()
        # while True:
        #     r=c.crop_image_find(ImgEnumG.PERSON_POS,clicked=False,get_pos=True)
        #     print(r)
        #     time.sleep(1)
        # r=c.mul_point_touch('down', 'jump',long_click=True)
        # louti_queue = QueueManage(1)
        # turn_queue = QueueManage(1)
        # auto_wait = QueueManage(1)
        # map_data=BatEnumG.MAP_DATA['爱奥斯塔入口']
        # while True:
        #     AutoBatG.AutoBatG((dev2,'emulator-5554'),1,1).keyboard_bat(map_data, 1,auto_wait,1,louti_queue,turn_queue)
        # r=StateCheckG.StateCheckG((dev2,'emulator-5554'),1,1).get_num((685,189,721,218))
        # r=TeamStateG.TeamStateG((dev2,'emulator-5554'),1,1).choose_pindao()
        # r=DailyTaskG.DailyTaskAutoG((dev2,'emulator-5556'),1,1).hdboss_task()
        # r=UpRoleG.UpRoleG((dev2,'emulator-5554'),'ld1',1).strongequip()
        # r=a.crop_image_find(ImgEnumG.YM_READY)
        # r=a.air_loop_find(ImgEnumG.UI_QR,False)
        r=c.ocr_find(ImgEnumG.MNDC_JSQR,True)
        # a.air_swipe((925, 432), (400, 432))
        # r = c.get_ocrres((464,324,804,362))#((568,313,708,346))#自勤速腺中
        # 稻路状熊不佳，伺服器回鹰延避中 招路状熊不佳，伺服器回鹰处涯中
        #游咸罪元结束!275秒俊自勤退出

        # r=o.get_rgb(1180, 653)
        print(r)
        # r = c.get_ocrres((157,516,188,543))
        # for i in r:
        #     a.air_touch(i,touch_wait=1)
        # for i in range(3):
        #     r=o.get_rgb(1238,284+i)
        #     print(r)
        # r=a.air_loop_find(ImgEnumG.EQ_UP_QR)

        # print(r3)
        #     for pos in r[-1]:
        #         a.air_touch(pos)
        # print(r)
        # r=c.air_swipe((912,507),(912,343))
        # r = c.get_all_text([(740,234,1254,266),'装'])
        # r=c.get_rgb(1122,648)
        # r = c.ocr_find([(577,157,704,196),'装'])
        # r = c.get_all_text([(779,664,864,689),'装'])
        # try:
        #     r=c.get_ocrres((1116,368,1184,387))
        #     print(int(r))
        # except ValueError:
        #     print(0)
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
