# -*- coding: utf-8 -*-

from airtest.core.api import connect_device
from airtest.core.error import DeviceConnectionError
from Utils.ThreadTools import ThreadTools
from Utils.OtherTools import catch_ex


@catch_ex
class DevicesConnect:
    def __init__(self, devname):
        self.devname = devname

    def connect_device(self):
        try:
            # dev = connect_device(f"Android://127.0.0.1:5037/{self.devname}?cap_method=ADBCAP")
            dev = connect_device(f"Android://127.0.0.1:5037/{self.devname}?cap_method=MINICAP"")  # ?cap_method=JAVACAP&&ori_method=ADBORI")
            print(f"{self.devname}_连接成功")
            return True, dev
        except (DeviceConnectionError, ConnectionResetError) as e:
            return False, e


def run(devid):
    d = DevicesConnect(devid).connect_device()
    if d:
        print(1)
        # t1 = time.time()
        # res1 = loop_find(ResEnumG.GAME_ICON, timeout=3)
        # t2 = time.time() - t1
        # print(t2)
        # print(res1)
    else:
        print('err')


if __name__ == '__main__':
    t1 = ThreadTools('t1', run, args=['emulator-5554'])  # emulator-5554
    # t2 = ThreadTools('t2', run, args=['emulator-5556'])
    t1.start()
    # t2.start()
    t1.join()
    # t2.join()
    # d_list = dev.list_app(third_only=True)
    # res = dev.check_app('com.nexon.maplem.global')
    # res1 = loop_find(ResEnumG.GAME_ICON, timeout=3)
    # touch(res1)
    # # res1=ResEnumG.GAME_ICON
    # screen = G.DEVICE.snapshot()
    # img = aircv.crop_image(screen, (0, 100, 200, 300))
    # aircv.imwrite(OT.abspath('/res/img/t.png'), img)
    # height = G.DEVICE.display_info['height']
    # width = G.DEVICE.display_info['width']
    # print(res1)
