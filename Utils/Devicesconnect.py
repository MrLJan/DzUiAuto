# -*- coding: utf-8 -*-
import ctypes
import win32com.client
import win32com

from Utils.LoadConfig import LoadConfig
from frozen import path


class DevicesConnect:
    def __init__(self, mnq_name=None, sn=None):
        self.mnq_name = mnq_name
        self.sn = sn
    @staticmethod
    def dm_init():
        """
        创建大漠对象
        :return: 大漠对象
        """
        dm = ctypes.windll.LoadLibrary(path + r'\dmdll\DmReg.dll')
        dm.SetDllPathW(path + r'\dmdll\dm.dll', 0)
        dm_obj = win32com.client.DispatchEx('dm.dmsoft')
        return dm_obj

    @staticmethod
    def bind_windows(dm_obj, sub_hwnd):
        """
        注册并绑定窗口
        """
        reg = dm_obj.Reg("xf30557fc317f617eead33dfc8de3bdd4ab9043", "xfqz4ys944wo700")
        bind_mode = LoadConfig.getconf("路径", "绑定模式")
        # bind_mode='模式三'
        # dm_obj.SetWindowState(sub_hwnd, 1)
        if bind_mode == '模式一':
            bing_res = dm_obj.BindWindowEx(sub_hwnd, "dx2", "windows3",
                                           "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                                           "", 101)
        elif bind_mode == '模式二':
            bing_res = dm_obj.BindWindowEx(sub_hwnd, "dx.graphic.opengl",
                                           "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input."
                                           "lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                                           "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api", "", 101)


        else:
            bing_res = dm_obj.BindWindowEx(sub_hwnd, "dx.graphic.opengl", "windows3",
                                           "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                                           "dx.public.down.cpu", 101)
        # dm_obj.SetWindowSize(sub_hwnd, 1280, 720)
        dm_obj.SetMouseDelay('windows', 100)
        dm_obj.SetKeypadDelay('dx', 50)
        # dm_obj.SetShowErrorMsg(0)
        # dm_obj.DownCpu(1, 30)
        if reg != 1:
            print(f"注册失败，错误码{reg}")
        if bing_res != 1:
            dm_obj.UnBindWindow()
            """雷电、夜神绑定"""
            if bind_mode == '模式一':
                bing_res = dm_obj.BindWindowEx(sub_hwnd, "dx2", "windows3",
                                               "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                                               "dx.public.active.api2", 101)
            elif bind_mode == '模式二':
                bing_res = dm_obj.BindWindowEx(sub_hwnd, "dx.graphic.opengl",
                                               "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input."
                                               "lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                                               "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api", "", 101)
            elif bind_mode == '模式三':
                bing_res = dm_obj.BindWindowEx(sub_hwnd, "dx.graphic.opengl", "windows3",
                                               "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                                               "dx.public.down.cpu", 101)

            # dm_obj.SetWindowSize(sub_hwnd, 1280, 720)
            dm_obj.SetMouseDelay('windows', 100)
            dm_obj.SetKeypadDelay('dx', 50)
            # dm_obj.SetShowErrorMsg(0)
            if bing_res == 1:
                print("之前有绑定,解绑后绑定成功")
        res = dm_obj.GetClientSize(sub_hwnd)
        # if res[0] == 1:
        #     if res[1] != 1280 or res[-1] != 720:
        #         dm_obj.SetWindowSize(sub_hwnd, 1280, 720)
        dm_obj.SetPath(path + r"\Res\img")
        dm_obj.SetDict(0, r"\dict\word.txt")
        dm_obj.SetDict(1, r"\dict\mr.txt")
        dm_obj.SetDict(2, r"\dict\ui.txt")
        dm_obj.SetDict(3, r"\dict\gold_num.txt")
        dm_obj.SetDict(4, r"\dict\lv_num.txt")
        dm_obj.SetDict(5, r"\dict\xl_num.txt")
        dm_obj.SetDict(6, r"\dict\bat_num.txt")
        dm_obj.SetDict(7, r"\dict\xt_map.txt")
        dm_obj.SetDict(8, r"\dict\pd_num.txt")
        dm_obj.SetDict(9,r"\dict\put_num.txt")
        dm_obj.SetDict(10, r"\dict\qh_num.txt")
        dm_obj.SetDict(11, r"\dict\yt_map.txt")
        return dm_obj
        # dm_id = dm_obj.GetID()
        # print(f"大漠ID：{dm_id}")

