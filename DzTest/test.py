# -*- encoding=utf8 -*-

class test:

    def __init__(self):
        self.func_list = {
            't1': [self.t1('t'), self.t2]
        }

    def t1(self, x):
        print(x)
        return 5

    def t2(self, y):
        print(y)

    def t3(self):
        r=self.func_list['t1'][0]
        print(r)



if __name__ == '__main__':
    list=[(1,2),4]
    list.pop(0)
    print(list)

