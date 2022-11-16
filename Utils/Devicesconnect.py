# -*- coding: utf-8 -*-
from airtest.core.android import Android
from airtest.core.error import DeviceConnectionError, AdbError, AdbShellError

from Utils.AdbUtils import PD, PhoneDevives


class DevicesConnect:
    def __init__(self, devname,mnq_name=None,sn=None):
        self.devname = devname
        self.mnq_name=mnq_name
        self.sn=sn

    def connect_device(self):
        dev = None
        try:
            PhoneDevives(self.devname).disconnect()
            dev = Android(serialno=self.devname, cap_method='JAVACAP', touch_method='ADBTOUCH', ori_method='ADBORI')
            if self.sn:
                self.sn.log_tab.emit(self.mnq_name, f"{dev.serialno}_连接成功")
            else:
                print(f"{dev.serialno}_连接成功")
            return True, dev
        except (UnicodeDecodeError, ConnectionResetError, Exception, ConnectionAbortedError, AdbError, TypeError,
                AdbShellError):
            print(f"Adb重连")
            dev.adb.disconnect()
            PD.kill_adb()
            self.connect_device()
        except DeviceConnectionError as e:
            return False, e


if __name__ == '__main__':
    s, r,t = DevicesConnect('127.0.0.1:5555').connect_device()
    print(r.adb)
