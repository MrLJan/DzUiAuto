# -*- coding: utf-8 -*-
import time

from airtest.aircv import aircv
from airtest.core.android.touch_methods.base_touch import DownEvent, SleepEvent, UpEvent
from cnocr import CnOcr
from Enum.ResEnum import GlobalEnumG, ImgEnumG
from Utils.Devicesconnect import DevicesConnect
from Utils.ThreadTools import ThreadTools


class OpenCvTools:
    def __init__(self):
        self.dev = None
        self._img = None

    def get_rgb(self, rgb_info, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime,
                t_log=GlobalEnumG.TestLog):
        """获取某一像素点RBG数据"""
        get_x, get_y, find_color = rgb_info
        self._img = self.dev.snapshot()
        if self._img is not None:
            _color = self.nd_to_hex(self._img[get_y, get_x])
            if t_log:
                print(f'expoint:{_color}_find:{find_color}_x,y:{get_x},{get_y}')
            if find_color in _color:
                if clicked:
                    self.dev.touch((get_x, get_y))
                    if touch_wait > 0:
                        time.sleep(touch_wait)
                return True
        return False

    def rgb(self, get_x, get_y):
        self._img = self.dev.snapshot()
        _color = self._img[get_y, get_x]  # 横屏1280x720
        return self.nd_to_hex(_color)

    @staticmethod
    def nd_to_hex(ndarry):
        _point = ''
        for _p in ndarry:
            _point = str(hex(_p))[-2:].replace('x', '0').upper() + _point
        return _point

    def mulcolor_check(self, find_list, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog,
                       get_grb=False):
        """对比多个点的颜色，只要有一个错误就返回"""
        self._img = self.dev.snapshot()
        if self._img is not None:
            c_list = []
            if get_grb:
                _list = find_list
            else:
                _list = find_list[0]
            for _p in _list:
                if get_grb:
                    _color = self.nd_to_hex(self._img[_p[1], _p[0]])
                    c_list.append((_p[0], _p[1], _color))
                else:
                    if _p[-1] not in self.nd_to_hex(self._img[_p[1], _p[0]]):
                        if t_log:
                            print(f"{_p},{self.nd_to_hex(self._img[_p[1], _p[0]])} {find_list[-1]}")
                        return False
            if t_log:
                print(c_list)
            if clicked:
                self.dev.touch((find_list[0][0][0], find_list[0][0][1]))
                if touch_wait > 0:
                    time.sleep(touch_wait)
            if t_log:
                print(f'T_{find_list[-1]}')
                time.sleep(GlobalEnumG.WaitTime)
            return True
        return False

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
        self._img = None

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
                        get_pos=False, t_log=GlobalEnumG.TestLog):
        """区域找图"""
        self._img = self.dev.snapshot()
        if self._img is not None:
            area = area_temp[0]
            temp = area_temp[-1]
            crop_img = aircv.crop_image(self._img, area)
            res = temp.match_in(crop_img)
            if res:
                pos = (res[0] + area[0], res[1] + area[1])
                if clicked:
                    self.dev.touch(pos)
                    if touch_wait > 0:
                        time.sleep(touch_wait)
                if get_pos:
                    if t_log:
                        print(f"crop_image_find:{temp}")
                    return True, pos[0], pos[-1]
                if t_log:
                    print(f"crop_image_find:{temp}")
                return True
            if get_pos:
                return False, 0, 0
            if t_log:
                print(f"f_crop_image_find:{temp}")
            return False
        return False

    def find_all_pos(self, temp, timeout=GlobalEnumG.FindImgTimeOut):
        img = temp[-1]
        pos_list = []
        self._img = self.dev.snapshot()
        if self._img is not None:
            match_pos = img.match_all_in(self._img)
            if not match_pos:
                return False, (0, 0)
            for pos in match_pos:
                res = pos['result']
                pos_list.append(res)
            return True, pos_list
        return False, (0, 0)

    def air_loop_find(self, temp, clicked=True, timeout=GlobalEnumG.FindImgTimeOut,
                      touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog):
        """
        循环查找图片并点击，超时返回
        """
        img = temp[-1]
        self._img = self.dev.snapshot()
        if self._img is not None:
            match_pos = img.match_in(self._img)
            if not match_pos:
                if t_log:
                    print(f"f_air_loop_find:{temp}")
                return False
            if match_pos:
                if clicked:
                    self.dev.touch(match_pos)
                    if touch_wait > 0:
                        time.sleep(touch_wait)
            if t_log:
                print(f"air_loop_find:{temp}")
            return True
        if t_log:
            print(f"f_air_loop_find:{temp}")
        return False

    def air_touch(self, touch_xy, duration=0.2, touch_wait=1):
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
                UpEvent(1), UpEvent(0)
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
        self._img = None

    def ocr_find(self, ocr_list, clicked=False, touch_wait=GlobalEnumG.TouchWaitTime, t_log=GlobalEnumG.TestLog,
                 get_pos=False):
        """
        范围查找文字，返回坐标
        :param ocr_list:查找文字范围和文字
        :param clicked: 是否点击
        :param touch_wait: 点击后等待时长
        :return: 查找结果
        """
        x1, y1, x2, y2 = ocr_list[0]
        self._img = self.dev.snapshot()
        if self._img is not None:
            img_fp = aircv.crop_image(self._img, (x1, y1, x2, y2))
            t1 = time.time()
            self.cn_ocr[-1].acquire()
            out = self.cn_ocr[0].ocr(img_fp, resized_shape=(720, 1280), batch_size=1)
            self.cn_ocr[-1].release()
            if t_log:
                print(time.time() - t1)
            if len(out) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                if t_log:
                    print(f"f_{ocr_list}")
                return False
            for i in range(len(out)):
                ntext = out[i]['text']
                if t_log:
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
                    if t_log:
                        print(f"T_{ocr_list}")
                    time.sleep(touch_wait)
                    if get_pos:
                        return lx + x1, ly + y1
                    return True
        time.sleep(touch_wait / 2)
        return False

    def get_all_text(self, ocr_list):
        find_pos_list = []
        x1, y1, x2, y2 = ocr_list[0]
        self._img = self.dev.snapshot()
        if self._img is not None:
            self.cn_ocr[-1].acquire()
            img_fp = aircv.crop_image(self._img, (x1, y1, x2, y2))
            out = self.cn_ocr[0].ocr(img_fp)
            self.cn_ocr[-1].release()
            if len(out) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                return find_pos_list
            for i in range(len(out)):
                ntext = out[i]['text']
                if ocr_list[-1] in ntext:
                    npar = out[i]['position']
                    ls = npar.tolist()
                    lx = int((ls[-2][0] + ls[0][0]) / 2)
                    ly = int((ls[-2][-1] + ls[0][-1]) / 2)
                    find_pos_list.append((lx + x1, ly + y1))
        time.sleep(GlobalEnumG.WaitTime)
        return find_pos_list

    def get_ocrres(self, area, t_log=GlobalEnumG.TestLog):
        """
        范围查找文字，返回坐标
        :param ocr_list:查找文字范围和文字
        :return: 查找结果
        """
        self._img = self.dev.snapshot()
        if self._img is not None:
            img_fp = aircv.crop_image(self._img, area)
            self.cn_ocr[-1].acquire()
            out = self.cn_ocr[0].ocr_for_single_line(img_fp)
            self.cn_ocr[-1].release()
            if len(out) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                return ''
            if t_log:
                print(f"get_ocrres:{area}_ntext:{out['text']}")
            time.sleep(GlobalEnumG.WaitTime)
            return out['text']
        return ''

    def get_roleinfo(self, area_list, t_log=GlobalEnumG.TestLog):
        self._img = self.dev.snapshot()
        img_area = []
        out_list = []
        ntext_list = []
        if self._img is not None:
            for _a in area_list:
                img_fp = aircv.crop_image(self._img, _a)
                img_area.append(img_fp)
            self.cn_ocr[-1].acquire()
            for _img in img_area:
                out = self.cn_ocr[0].ocr_for_single_line(_img)
                if len(out) > 0:
                    out_list.append(out)
            self.cn_ocr[-1].release()
            if t_log:
                print(f"get_roleinfo:out_{out_list}")
            if len(out_list) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                return False
            for _o in out_list:
                ntext = ''.join(filter(lambda x: x.isdigit(), _o['text']))
                try:
                    ntext_list.append(int(ntext))
                except ValueError:
                    ntext_list.append(0)
            time.sleep(GlobalEnumG.WaitTime)
            if t_log:
                print(f"get_roleinfo:ntext_list_{ntext_list}")
            return ntext_list
        return ntext_list

    def get_all_ocr(self, area, t_log=False):
        self._img = self.dev.snapshot()
        res_list = []
        if self._img is not None:
            x1, y1, x2, y2 = area
            img_fp = aircv.crop_image(self._img, area)
            self.cn_ocr[-1].acquire()
            out = self.cn_ocr[0].ocr(img_fp)
            self.cn_ocr[-1].release()
            if len(out) == 0:
                time.sleep(GlobalEnumG.WaitTime / 2)
                if t_log:
                    print(f"F_get_all_ocr:{area}")
                return False
            for i in range(len(out)):
                ntext = out[i]['text']
                npar = out[i]['position']
                ls = npar.tolist()
                lx = int((ls[-2][0] + ls[0][0]) / 2)
                ly = int((ls[-2][-1] + ls[0][-1]) / 2)
                if ntext != '':
                    res_list.append((ntext, (lx + x1, ly + y1)))
        time.sleep(GlobalEnumG.WaitTime)
        return res_list


if __name__ == '__main__':
    # img_fp = r'D:\DzAutoUi\Res\img\21.bmp'
    # res, dev = DevicesConnect('emulator-5554').connect_device()
    res2, dev2 = DevicesConnect('127.0.0.1:5581').connect_device()
    # print(res2, dev2)
    # cv2.setNumThreads(1)
    # cv2.ocl.setUseOpenCL(False)
    # torch.set_num_threads(1)
    # torch.no_grad()
    # torch.set_grad_enabled(False)
    cnocr = CnOcr(rec_model_name='densenet_lite_136-fc',
                  det_model_name='db_shufflenet_v2_small')  # 'ch_PP-OCRv3_det')  # ch_PP-OCRv3繁体中文匹配模型
    ocr_lock = ThreadTools.new_lock()
    cn_ocr = [cnocr, ocr_lock]
    # img=G.DEVICE.snapshot()
    # aircv.imwrite(r'D:\DzAutoUi\Res\img\21.png',img)
    # loop_find(img_fp)
    c = CnOcrTool()
    a = AirImgTools()
    o = OpenCvTools()
    c.dev = dev2
    a.dev = dev2
    o.dev = dev2
    c.cn_ocr = cn_ocr
    # r=o.mulcolor_check(ColorEnumG.LOGIN_MAIN)
    # while True:

    #     t1=time.time()
    #     r=a.crop_image_find(ImgEnumG.INGAME_FLAG2,False)
    #     print(r,time.time()-t1)
    r=o.rgb(922, 160)
    #
    # r=c.get_ocrres([33,1,86,29],t_log=True)
    print(r)
    # for x in range(833,867):
    #     for y in range(377,411):
    #         print(f"{x},{y},{o.rgb(x,y)}")
    # r = a.crop_image_find(ImgEnumG.UI_SET, False)

    # while True:
    #     r=c.crop_image_find(ImgEnumG.PERSON_POS,clicked=False,get_pos=True)
    #     print(r)
    # r = c.mul_point_touch('down', 'jdown', k_time=1)


    # r=c.mul_point_touch('down', 'jump',long_click=True)
    # louti_queue = QueueManage(1)
    # turn_queue = QueueManage(1)
    # auto_wait = QueueManage(1)
    # map_data=BatEnumG.MAP_DATA['爱奥斯塔入口']
    # while True:
    #     AutoBatG.AutoBatG((dev2,'emulator-5554'),1,1).keyboard_bat(map_data, 1,auto_wait,1,louti_queue,turn_queue)
    # r=StateCheckG.StateCheckG((dev2,'emulator-5554'),1,1).get_num((685,189,721,218))
    # r=TeamStateG.TeamStateG((dev2,'emulator-5554'),1,1).choose_pindao()

    # r=UpRoleG.UpRoleG((dev2,'emulator-5554'),'ld1',1).strongequip()
    # r=RewardG.RewardG((dev2,'emulator'),'ld1',1).get_equip()
    # r=a.crop_image_find(ImgEnumG.L_BS)
    # r=a.air_loop_find(ImgEnumG.FJ_HE2)
    # r=a.find_all_pos(ImgEnumG.ZB_TS)

    # r = c.ocr_find([(0, 0, 1280, 720), 'LV'])
    # a.air_swipe((925, 432), (400, 432))x
    # r = c.get_ocrres((41, 66, 165, 87))  # ((568,313,708,346))#自勤速腺中

    # c_l = [
    #     ColorEnumG.LOGIN_CLOSE, ColorEnumG.LOGIN_MAIN, ColorEnumG.LOGIN_START,
    #     ColorEnumG.MAIN_UI, ColorEnumG.PET_TIME_END, ColorEnumG.QD_HD_BJBS, ColorEnumG.QD_HD_BJBS_CLOSE,
    #     ColorEnumG.QD_MY, ColorEnumG.HD_LB, ColorEnumG.BAG_MAIN, ColorEnumG.BAG_SELL, ColorEnumG.BAG_GOLD,
    #     ColorEnumG.BAG_SX, ColorEnumG.TASK_CLOSE, ColorEnumG.MR_KSDY, ColorEnumG.WL_MAIN, ColorEnumG.WL_JR,
    #     ColorEnumG.JZT_MAIN, ColorEnumG.JZT_JR, ColorEnumG.MRDC_MAIN, ColorEnumG.MRDC_JR, ColorEnumG.JHXT_MAIN,
    #     ColorEnumG.JHXT_JR, ColorEnumG.YZD_MAIN, ColorEnumG.GWSLT_MAIN, ColorEnumG.TBB_MAIN, ColorEnumG.TBB_JR,
    #     ColorEnumG.TBB_ZCJR, ColorEnumG.XLZC_MAIN, ColorEnumG.CYRQ_MAIN, ColorEnumG.MNDC_MAIN, ColorEnumG.MNDC_JR,
    #     ColorEnumG.XGT_MAIN, ColorEnumG.EXIT_TEAM, ColorEnumG.HDYZD_MAIN, ColorEnumG.GH_MAIN, ColorEnumG.GH_WXDC,
    #     ColorEnumG.MAIL_MAIN, ColorEnumG.KT_MAIN, ColorEnumG.PET_MAIN, ColorEnumG.JN_MAIN, ColorEnumG.YS_LOGIN,
    #     ColorEnumG.YS_SHOP, ColorEnumG.YS_XQ, ColorEnumG.YS_GM_QR
    # ]
    # screen=dev2.snapshot()
    # cv2.cv2.setNumThreads(1)
    # cv2.cv2.ocl.setUseOpenCL(False)
    # while True:
    #     t1 = time.time()
    #     # o.screen = dev2.snapshot()
    #     # r = DailyTaskG.DailyTaskAutoG((dev2, 'emulator-5556'), 1, 1,cn_ocr).wulin_task()
    #     # r=o.mulcolor_check(ColorEnumG.LOGIN_START, clicked=True,test=False)
    #     r = o.mulcolor_check(ColorEnumG.MR_KSDY, test=False)
    #     #     for _f in c_l:
    #     #         r = o.mulcolor_check(_f,test=False)
    #     #         print(r, time.time() - t1)
    #     #     r=a.crop_image_find(ImgEnumG.TEAM_FIND)
    #     #     r = c.ocr_find([(0, 0, 1280, 720), 'LV'])
    #     print(r, time.time() - t1)
    # while True:
    #     r=a.crop_image_find(ImgEnumG.PERSON_POS,clicked=False,get_pos=True)
    #     print(r)
    #     time.sleep(1)
#
