# -*- coding: utf-8 -*-
class BaseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NotFindImgErr(BaseError):
    """查找图片失败"""
    pass


class ConnectDevErr(BaseError):
    """
    连接失败
    """
    pass
