# -*- coding: utf-8 -*-
from airtest.core.android import Android
from airtest.core.error import DeviceConnectionError, AdbError, AdbShellError

from Utils.AdbUtils import PD


class DevicesConnect:
    def __init__(self, devname):
        self.devname = devname

    def connect_device(self):
        try:
            dev = Android(serialno=self.devname,cap_method='MINICAP',touch_method='ADBTOUCH',ori_method='ADBORI')
            print(f"{dev.serialno}_连接成功")
            return True, dev
        except (UnicodeDecodeError, ConnectionResetError, Exception,ConnectionAbortedError,AdbError,TypeError,AdbShellError):
            print(f"Adb重连")
            PD.kill_adb()
            self.connect_device()
        except DeviceConnectionError as e:
            return False, e

