# -*- coding: utf-8 -*-
from airtest.core.android import Android
from airtest.core.error import DeviceConnectionError, AdbError

from Utils.AdbUtils import PD


class DevicesConnect:
    def __init__(self, devname):
        self.devname = devname

    def connect_device(self):
        try:
            dev = Android(serialno=self.devname,)#)
            print(f"{self.devname}_连接成功")
            return True, dev
        except DeviceConnectionError as e:
            return False, e
        except (UnicodeDecodeError, ConnectionResetError, Exception,ConnectionAbortedError,AdbError):
            print(f"Adb重连")
            PD.kill_adb()
            self.connect_device()

