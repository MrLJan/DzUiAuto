import logging
import os
import sys
from functools import wraps
from frozen import path

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
handlerTotxt = logging.FileHandler(os.path.join(path, 'res/log.txt'))  # 记录log到txt中
handlerTotxt.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerTotxt.setFormatter(formatter)

console = logging.FileHandler(os.path.join(path, 'res/log.txt'))
console.setLevel(level=logging.DEBUG)

edittext_out = logging.StreamHandler(stream=sys.stdout)
edittext_out.setLevel(logging.DEBUG)

edittext_der = logging.StreamHandler(stream=sys.stderr)
edittext_der.setLevel(logging.DEBUG)

logger.addHandler(handlerTotxt)
logger.addHandler(console)
#
#
logger1 = logging.getLogger("airtest")  # 捕获airtest输出的log
logger1.setLevel(logging.ERROR)
logger1.addHandler(handlerTotxt)

def catch_ex(func):
    @wraps(func)
    def try_catch(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
        return result

    return try_catch


class OtherTools:
    def abspath(self, addpath):
        return path + addpath

    def imgpath(self, imgname):
        return path + r'/res/img/' + imgname+'.bmp'


OT = OtherTools()
if __name__ == '__main__':
    print(OT.abspath(r'\rq'))
