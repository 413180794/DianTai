
import struct
import os
import sys

from mylogging import logger

sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property

class TextDataBean(object):
    __slots__ = ['_usage', '_device_category', '_device_id', '_data']
    usage = typed_property("usage", str)
    device_category = typed_property("device_category", str)
    device_id = typed_property("device_id", int)
    data = typed_property("data", str)

    ENCODE_TYPE = "utf-8"

    def __init__(self, *, device_category, device_id, data):
        self.usage = "text_data"
        self.device_category = device_category
        self.device_id = device_id
        self.data = data

    @staticmethod
    def format_():
        return "!16s16si1024s"

    @property
    def all_data(self):
        return (
            self.usage,
            self.device_category,
            self.device_id,
            self.data
        )

    @property
    def device_name(self):
        return self.device_category + "_" + str(self.device_id)

    @property
    def pack_data(self):
        __pack_data_ = tuple(
            map(lambda m: m.encode(TextDataBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *__pack_data_)

    @staticmethod
    def unpack_data(pack_data):
        unpack_data_ = tuple(
            map(lambda m: m.decode(TextDataBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(TextDataBean.format_(), pack_data))
        )
        bean = TextDataBean(device_category=unpack_data_[1], device_id=unpack_data_[2], data=unpack_data_[3])
        return bean

    def send(self, __send, addr):
        '''
        使用send 向 addr发送数据
        :param send: protocal
        :param addr: 地址
        :return:
        '''
        try:
            __send.send_apply(self.pack_data, addr)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    print(123)
