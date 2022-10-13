# -*- coding: utf-8 -*-
import inspect
import threading
import time
import ctypes


lock = threading.Lock()


def _async_raise(thread_tid, thread_name, exctype):
    """根据线程tid抛出异常，中断线程"""
    _thread_tid = ctypes.c_long(thread_tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(_thread_tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError(f"tid:{thread_tid}有误")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(_thread_tid, None)
        raise SystemError(f"中断{thread_name}_{thread_tid}失败,检查线程是否已经结束")
    elif res == 1:
        print(f"{thread_name}_{thread_tid}已强制中断")


def stop_thread(thread_tid, thread_name):
    try:
        _async_raise(thread_tid, thread_name, SystemExit)
    except ValueError as e:
        print(e)


class ThreadTools(threading.Thread):

    def __init__(self, thread_name, target=None, args=(), kwargs=None, thread_while=False):
        super().__init__()
        self.thread_name = thread_name
        if kwargs is None:
            kwargs = {}
        self._args = args
        self._kwargs = kwargs
        self.thread_func = target
        self.thread_while = thread_while
        self.stop_flag = threading.Event()  # 停止标识
        self.stop_flag.set()
        self.running_flag = threading.Event()  # 暂停标识
        self.running_flag.set()
        self.setDaemon(True)  # 设置守护线程,保证主进程结束子进程全部退出

    @staticmethod
    def new_event():
        return threading.Event()

    @staticmethod
    def new_lock():
        return threading.Lock()

    def run(self):
        # with lock:
        lock.acquire()
        self.setName(self.thread_name)
        print(f"任务：{self.name}_{self.ident}" + " 开始\n")
        if self.thread_while:
            lock.release()
            while self.stop_flag.is_set():  # 判断线程是否停止
                if self.running_flag.is_set():
                    self.thread_func(*self._args, **self._kwargs)
                else:
                    print(f"任务：{self.name}_{self.ident}" + " 暂停\n")
                    while not self.running_flag.is_set():  # 判断线程是否暂停
                        time.sleep(1)
            print(f"任务：{self.name}_{self.ident}" + " 停止\n")
            self.stop_flag.set()
        else:
            self.thread_func(*self._args, **self._kwargs)
            lock.release()
            print(f"任务：{self.name}_{self.ident}" + " 结束\n")


    def stop(self):
        """停止线程"""
        self.stop_flag.clear()

    def pause(self):
        """暂停线程"""
        if self.running_flag.is_set():
            self.running_flag.clear()
        else:
            self.running_flag.set()

    @staticmethod
    def stop_thread_list(thread_list):
        if len(thread_list) == 0:
            print("无任务可停止")
        elif len(thread_list) == 1:
            stop_thread(thread_list[-1].ident, thread_list[-1].getName())
        else:
            for i in range(len(thread_list)):
                stop_thread(thread_list[i].ident, thread_list[i].getName())

    @staticmethod
    def pause_thread_list(thread_list):
        if len(thread_list) > 1:
            for i in range(len(thread_list)):
                thread_list[i].pause()
        else:
            thread_list[0].pause()

    @staticmethod
    def is_threadname(check_name, thread_list):
        try:
            for i in thread_list:
                name = i.getName()
                if name == check_name:
                    print(f"已存在_{check_name}\n")
                    return True
            return False
        except Exception as e:
            print(e)

    @staticmethod
    def check_threadname(check_name, thread_list):
        """检查线程是否重复创建"""
        try:
            stop_list = []
            for i in thread_list:
                name = i.getName()
                if name in check_name:
                    print("任务已创建过")
                    stop_list.append(i)
            for i in stop_list:
                stop_thread(i.ident, i.getName())
                thread_list.remove(i)
        except Exception as e:
            print(e)


def check_mnq_thread(thread_name, mnq_thread_list, func, thread_while=False):
    """创建线程前删除之前线程列表存在的同名线程"""
    try:
        ThreadTools.check_threadname(thread_name, mnq_thread_list)
        new_thread = ThreadTools(thread_name, func, thread_while=thread_while)
        new_thread.start()
        mnq_thread_list.append(new_thread)

    except BaseException as e:
        print(e)


def stop_thread_with_name(name_list, mnq_thread_list):
    """停止除name_list以外的其他线程"""
    remove_list = []
    for i in mnq_thread_list:
        name = i.getName()
        if name in name_list:
            pass
        else:
            remove_list.append(i)
    for i in remove_list:
        stop_thread(i.ident, i.getName())
        mnq_thread_list.remove(i)
