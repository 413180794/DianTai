import struct
import os
import sys

from mylogging import logger

sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class MeasureDataBean:
    __slots__ = ['_usage', '_device_category', '_device_id', "_temperature"]
    usage = typed_property("usage", str)
    device_category = typed_property("device_category", str)
    device_id = typed_property("device_id", int)
    temperature = typed_property("temperature", float)

    ENCODE_TYPE = "utf-8"

    def __init__(self, *, device_category, device_id, temperature):
        self.usage = "position_data"
        self.device_category = device_category
        self.device_id = device_id
        self.temperature = temperature

    @staticmethod
    def format_():
        return "!16s16sid"

    @property
    def all_data(self):
        return (
            self.usage,
            self.device_category,
            self.device_id,
            self.temperature
        )

    @property
    def device_name(self):
        return self.device_category + "_" + str(self.device_id)

    @property
    def pack_data(self):
        __pack_data_ = tuple(
            map(lambda m: m.encode(MeasureDataBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *__pack_data_)

    @staticmethod
    def unpack_data(pack_data):
        unpack_data_ = tuple(
            map(lambda m: m.decode(MeasureDataBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(MeasureDataBean.format_(), pack_data))
        )
        bean = MeasureDataBean(device_category=unpack_data_[1], device_id=unpack_data_[2], temperature=unpack_data_[3])
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
            logger.error(e)

    def __str__(self):
        return str(self.all_data)


if __name__ == '__main__':
    x = MeasureDataBean(device_category="123",device_id=123,temperature=123.2)
    print(x)
