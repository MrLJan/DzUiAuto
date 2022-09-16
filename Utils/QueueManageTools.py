# -*- encoding=utf8 -*-
from queue import Queue

from Utils.OtherTools import OT


class QueueManage:
    """状态队列，后续用来检查游戏状态"""

    def __init__(self, num=50):
        self.queue = Queue(num)

    def put_queue(self, key):
        """存数据"""
        try:
            if not self.check_queue(key):
                self.queue.put(key)

        except Exception as e:
            print(f"{key}队列异常{e}")

    def check_queue(self, key):
        """取数据,t=任务"""
        for i in range(self.queue.qsize()):
            task_key = self.queue.get()
            if task_key == key:
                self.queue.put(task_key)
                return True
            else:
                self.queue.put(task_key)
        return False

    def task_over(self, over_key):
        for i in range(self.queue.qsize()):
            task_key = self.queue.get()
            if task_key == over_key:
                return True
            else:
                self.queue.put(task_key)
        return False

    def get_task(self):
        if self.queue.empty():
            return False
        else:
            task = self.queue.get()
            self.queue.put(task)
            return task

    def clear(self):
        for i in range(self.queue.qsize()):
            self.queue.get()


if __name__ == '__main__':
    obj = QueueManage()

    # for i in range(5):
    #     obj.put_queue(i)
    obj.put_queue(1)
    obj.put_queue(2)
    obj.put_queue(3)
    # print(obj.queue.empty())
    print(obj.get_task())
    print(obj.task_over(2))
    print(obj.get_task())
    print(obj.task_over(3))
    print(obj.task_over(1))
    print(obj.get_task())
    print(obj.get_task())
    print(obj.get_task())
    print(obj.get_task())
    # print(obj.get_task())
    # print(obj.queue.qsize())
    # obj.get_queue('q')
    if obj.queue.qsize() > 1:
        print(11)
    else:
        print(21)
