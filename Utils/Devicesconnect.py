# -*- coding: utf-8 -*-
from airtest.core.android import Android
from airtest.core.error import DeviceConnectionError


class DevicesConnect:
    def __init__(self, devname):
        self.devname = devname

    def connect_device(self):
        try:
            dev = Android(serialno=self.devname)
            # dev1 = connect_device(f"Android://127.0.0.1:5037/{self.devname}?cap_method=MINICAP")  #
            # ?cap_method=JAVACAP&&ori_method=ADBORI")
            print(f"{self.devname}_连接成功")
            return True, dev
        except DeviceConnectionError as e:
            return False, e
        except (UnicodeDecodeError, ConnectionResetError, Exception,ConnectionAbortedError):
            print(f"Adb重连")
            self.connect_device()


if __name__ == '__main__':
    r = DevicesConnect('127.0.0.1:5585')
    res = r.connect_device()
    print(res[1], res[-1])
