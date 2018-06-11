import struct
import os
import sys

from mylogging import logger

sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class PositionDataBean:
    __slots__ = ['_usage', '_device_category', '_device_id', '_position_x', '_position_y']
    usage = typed_property("usage", str)
    device_category = typed_property("device_category", str)
    device_id = typed_property("device_id", int)
    position_x = typed_property("position_x", int)
    position_y = typed_property("position_y", int)

    ENCODE_TYPE = "utf-8"

    def __init__(self, *, device_category, device_id, position_x, position_y):
        self.usage = "position_data"
        self.device_category = device_category
        self.device_id = device_id
        self.position_x = position_x
        self.position_y = position_y

    @staticmethod
    def format_():
        return "!16s16siii"

    @property
    def all_data(self):
        return (
            self.usage,
            self.device_category,
            self.device_id,
            self.position_x,
            self.position_y
        )

    @property
    def device_name(self):
        return self.device_category + "_" + str(self.device_id)

    @property
    def pack_data(self):
        __pack_data_ = tuple(
            map(lambda m: m.encode(PositionDataBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *__pack_data_)

    @staticmethod
    def unpack_data(pack_data):
        unpack_data_ = tuple(
            map(lambda m: m.decode(PositionDataBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(PositionDataBean.format_(), pack_data))
        )
        bean = PositionDataBean(device_category=unpack_data_[1], device_id=unpack_data_[2], position_x=unpack_data_[3],
                                position_y=unpack_data_[4])
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
        return "device_category:" + self.device_category + "_" + str(
            self.device_id) + " positoin:" + "(" + str(self.position_x) + "," + str(self.position_y) + ")"


if __name__ == '__main__':
    x = PositionDataBean(device_category="sdf", device_id=12, position_x=12, position_y=23)
    print(x)
