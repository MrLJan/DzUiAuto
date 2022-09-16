# -*- coding: utf-8 -*-
import shutil
from time import sleep

import re

from airtest.core.android.adb import ADB
from airtest.core.api import keyevent
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# from tidevice._ipautil import IPAReader

from Utils.OtherTools import OT

install_success = False


class PhoneDevives:
    def __init__(self, serialno=None):
        self.adb = self.adb_init(serialno)

    def adb_init(self, serialno=None):
        return ADB(serialno=serialno, adb_path=OT.abspath('/Adb/adb.exe'))

    def get_devices(self):
        devices = self.adb.devices()
        devindex_list = []
        devname_list = []
        pinfo_list = []
        for ls in devices:
            # if 'emulator' in ls[0]:
            # pass
            # else:
            if ls[-1] != 'device':
                print(f"设备{ls[0]} 未开启adb调试")
            else:
                devindex_list.append(devices.index(ls))
                devname_list.append(ls[0])
                pinfo_list.append(self.get_phoneinfo(ls[0]))
        return devindex_list, devname_list, pinfo_list

    def get_phoneinfo(self, serialno=None):
        adb = self.adb_init(serialno)
        manufacturer = adb.get_manufacturer()
        model = adb.get_model()
        return manufacturer + '-' + model

    def get_display(self):
        """返回分辨率大小x,y"""
        return self.adb.get_display_info()['width'], self.adb.get_display_info()['height']

    def get_activity_app(self):
        """返回当前界面应用名"""
        return self.adb.get_top_activity()[0]


PD = PhoneDevives()
if __name__ == '__main__':
    print(PD.get_devices())
    r1 = PhoneDevives('emulator-5554').get_display()
    # res = PhoneDevives().get_devices()
    print(r1)
