# -*- coding: utf-8 -*-
import cmd
import shutil
import subprocess
from time import sleep

import re

from airtest.core.android.adb import ADB
from airtest.core.api import keyevent
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# from tidevice._ipautil import IPAReader

from Utils.OtherTools import OT

install_success = False


class PhoneDevives(ADB):
    def __init__(self, serialno=None,display_id=None):
        super(PhoneDevives,self).__init__()
        self.adb = self.adb_init(serialno)
        self.display_id=display_id

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

    def get_state(self):
        if not self.adb.get_status():
            self.adb.remove_forward()

    def shell_cmd(self, command):
        """adb shell命令"""
        result = None
        try:
            result = self.adb.shell(command)
        except Exception as e:
            print("shell exception:{},{}".format(command, e))

        if result is not None:
            result = str.strip(result)
        return result

    def disconnect(self):
        return self.adb.remove_forward()

PD = PhoneDevives()
if __name__ == '__main__':
    print(PD.get_devices())
    r1 = PhoneDevives('emulator-5554').get_display()
    # res = PhoneDevives().get_devices()
    print(r1)
