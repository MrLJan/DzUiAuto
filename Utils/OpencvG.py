# -*- coding: utf-8 -*-
import time

import numpy as np
from airtest.aircv import aircv
from airtest.core.android.touch_methods.base_touch import DownEvent, SleepEvent, UpEvent
from airtest.core.error import TargetNotFoundError
from cnocr import CnOcr

from Enum.ResEnum import GlobalEnumG
# from UiPage import DailyTaskG
# from UiPage import UpRoleG
# from UiPage import RewardG
# from UiPage import AutoBatG
# from UiPage import TeamStateG
# from UiPage import StateCheckG
from Utils.Devicesconnect import DevicesConnect
from Utils.ExceptionTools import NotFindImgErr
from Utils.OtherTools import OT


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
        # print(expoint)
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
        except TargetNotFoundError:
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
        except TargetNotFoundError:
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
            if action == 'jump' and turn != 'down':
                multitouch_event = [
                    DownEvent(self.turn_pos['up'], 2),
                    DownEvent(t_pos, 0),  # 手指1按下(100, 100)
                    DownEvent(a_pos, 1),  # 手指2按下(200, 200)
                    UpEvent(1),
                    SleepEvent(0.1),
                    DownEvent(a_pos, 1),
                    SleepEvent(0.1),
                    UpEvent(1),
                    SleepEvent(k_time),
                    UpEvent(2),
                    UpEvent(0)
                ]
                # UpEvent(0), UpEvent(1)]  # 2个手指分别抬起
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
        self.cn_ocr = None

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
        t1 = time.time()
        out = self.cn_ocr.ocr(img_fp, resized_shape=(720, 1280), batch_size=1)
        print(time.time() - t1)
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
                    if touch_wait > 0:
                        time.sleep(touch_wait)
                return True
        return False

    def get_all_text(self, ocr_list):
        find_pos_list = []
        x1, y1, x2, y2 = ocr_list[0]
        screen = self.dev.snapshot()
        img_fp = aircv.crop_image(screen, (x1, y1, x2, y2))
        out = self.cn_ocr.ocr(img_fp)
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
        out = self.cn_ocr.ocr_for_single_line(img_fp)
        # print(out)
        if len(out) == 0:
            return False
        for i in range(len(out)):
            ntext = out['text']
            return ntext

    def get_all_ocr(self, area):
        screen = self.dev.snapshot()
        x1, y1, x2, y2 = area
        img_fp = aircv.crop_image(screen, area)
        res_list = []
        out = self.cn_ocr.ocr(img_fp)
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
    res2, dev2 = DevicesConnect('127.0.0.1:5555').connect_device()
    print(res2, dev2)
    # img=G.DEVICE.snapshot()
    # aircv.imwrite(r'D:\DzAutoUi\Res\img\21.png',img)
    # loop_find(img_fp)
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

    # r=c.mul_point_touch('down', 'jump',long_click=True)
    # louti_queue = QueueManage(1)
    # turn_queue = QueueManage(1)
    # auto_wait = QueueManage(1)
    # map_data=BatEnumG.MAP_DATA['爱奥斯塔入口']
    # while True:
    #     AutoBatG.AutoBatG((dev2,'emulator-5554'),1,1).keyboard_bat(map_data, 1,auto_wait,1,louti_queue,turn_queue)
    # r=StateCheckG.StateCheckG((dev2,'emulator-5554'),1,1).get_num((685,189,721,218))
    # r=TeamStateG.TeamStateG((dev2,'emulator-5554'),1,1).choose_pindao()
    # r=DailyTaskG.DailyTaskAutoG((dev2,'emulator-5556'),1,1).boss_task()
    # r=UpRoleG.UpRoleG((dev2,'emulator-5554'),'ld1',1).strongequip()
    # r=RewardG.RewardG((dev2,'emulator'),'ld1',1).get_equip()
    # r=a.crop_image_find(ImgEnumG.L_BS)
    # r=a.air_loop_find(ImgEnumG.FJ_HE2)
    # r=a.find_all_pos(ImgEnumG.ZB_TS)

    r = c.ocr_find([(0, 0, 1280, 720), 'LV'])
    # a.air_swipe((925, 432), (400, 432))x
    # r = c.get_ocrres((41, 66, 165, 87))  # ((568,313,708,346))#自勤速腺中
    # r=o.get_rgb(1167, 642)
    print(r)
    # while True:
    #     r=a.crop_image_find(ImgEnumG.PERSON_POS,clicked=False,get_pos=True)
    #     print(r)
    #     time.sleep(1)
#
