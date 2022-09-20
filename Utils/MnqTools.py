# -*- encoding=utf8 -*-
import os

from Utils.LoadConfig import LoadConfig


class MnqTools:
    def __init__(self):
        self.ld_path = LoadConfig.getconf("路径", "模拟器路径")

    def get_mnq_list(self):
        """
         0, k0, 5312230, 9504916, 1, 2032184, 31536
         1, k1, 6427566, 2233538, 1, 1907096, 250544
        """
        mnq_name_list = []
        mnq_index_list = []
        mnq_devname_list = []
        cmd = os.popen(self.ld_path + " list2")
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(dnplayer)
        for mnq_name in result:
            if mnq_name[4] == "0" or mnq_name[0] == '99999':  # 剔除未启动的模拟器信息
                pass
            else:
                if mnq_name[7] != '1280' or mnq_name[8] != '720':
                    # self.reboot_mnq_index(mnq_name[0])
                    self.reset_resolution(mnq_name[0])
                    print(f'模拟器:{mnq_name[1]}大小异常,已重设')
                # self.lockwindow(mnq_name[0])
                devname = 'emulator-'+str(int(mnq_name[0]) * 2 + 5554)  # 雷电模拟器默认5554开始
                mnq_index_list.append(mnq_name[0])
                mnq_name_list.append(mnq_name[1])
                mnq_devname_list.append(devname)
                # self.lockwindow(mnq_name[0])#锁定窗口大小
        return mnq_index_list, mnq_name_list, mnq_devname_list

    def use_index_find_name(self, mnq_index):
        cmd = os.popen(self.ld_path + " list2")
        mnq_list = cmd.read().split('\n')
        cmd.close()
        mnq_dic = {}
        for _mnq in mnq_list:
            mnq_info = _mnq.split(',')
            if mnq_info[0] == '':
                pass
            else:
                mnq_dic[mnq_info[0]] = mnq_info[1]
        if str(mnq_index) in mnq_dic.keys():
            return mnq_dic[mnq_index]
        return '99999'

    def start_mnq_index_list(self, index_list):
        for i in index_list:
            cmd = os.popen(self.ld_path + f" launch --index {i}")
            cmd.close()
            print(f"模拟器 {i} 启动")

    def start_mnq_name(self, name):
        cmd = os.popen(self.ld_path + f" launch --name {str(name)}")
        cmd.close()

    def quit_mnq_index(self, index):
        """根据序列id关闭模拟器"""
        cmd = os.popen(self.ld_path + r" quit --index " + str(index))
        cmd.close()

    def quit_mnq_name(self, name):
        """根据模拟器名关闭模拟器"""
        cmd = os.popen(self.ld_path + r" quit --name " + str(name))
        cmd.close()

    def quit_mnq_all(self):
        """退出所有模拟器"""
        cmd = os.popen(self.ld_path + r" quitall")
        cmd.close()
        print("模拟器全部关闭")

    def lockwindow(self, index):
        cmd = os.popen(self.ld_path + f"  modify --index {index} --lockwindow 1")
        res = cmd.read()
        cmd.close()
        return res

    def reset_resolution(self, index):
        cmd = os.popen(self.ld_path + f" modify --index {index} --resolution 1280,720,240")
        cmd.close()

    def reboot_mnq_index(self, index):
        cmd = os.popen(self.ld_path + f" reboot --index {index}")
        cmd.close()

    def install_app(self, mnq_index, apk_file):
        cmd = os.popen(self.ld_path + f" installapp --index {mnq_index} --filename {apk_file}")
        cmd.close()

    def reboot_and_runapp(self, index):
        cmd = os.popen(self.ld_path + f" action --index {index} --key call.reboot --value com.nexon.maplem.global")
        cmd.close()
