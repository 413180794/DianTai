import ctypes
import struct
# def trans(string):
#     return str(string).encode('utf-8')
# dct_ = {"ad":"12","223":"sad"}
# print(tuple(dict_.values()))
# x = map(trans,tuple(dict_.values()))
# print(tuple(list(x)))
# values = (  *tuple(dict_.values())   ,1,'abc',2.3)
# print(values)
import time

from twisted.internet import reactor
from twisted.internet.threads import deferToThread


class tttt(object):
    def mysleep(self):
        time.sleep(3)
        return 4

    def say(self,result):
        print(result)

d = deferToThread(tttt().mysleep)
d.addCallback(tttt().say)

print('afasdfsaf')
reactor.run()



