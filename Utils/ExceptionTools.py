# -*- coding: utf-8 -*-
class BaseError(Exception):
    pass


class NotFindImgErr(BaseError):
    """查找图片失败"""

    def __init__(self, img):
        super(NotFindImgErr, self).__init__()
        self.img = img


class ConnectDevErr(BaseError):
    """
    连接失败
    """
    pass


class MrTaskErr(BaseError):
    """每日任务异常"""
    pass


class ControlTimeOut(BaseError):
    """操作超时"""

    def __init__(self, task):
        super(ControlTimeOut, self).__init__()
        self.task = task


class NotInGameErr(BaseError):
    """掉线"""
    pass


class FuHuoRoleErr(BaseError):
    """复活"""
    pass


class BuyYErr(BaseError):
    """没药"""
    pass


class RestartTask(BaseError):
    """重启任务"""
    pass
