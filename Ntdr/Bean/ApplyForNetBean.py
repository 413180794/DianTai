import struct
import os
import sys
sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class ApplyForNetBean(object):
    __slots__ = ['_usage', '_device_category', '_width_band', '_interval',
                 '_routing_parameter', "_device_id"]
    usage = typed_property("usage", str)
    device_category_ = typed_property("device_category", str)
    width_band = typed_property("width_band", int)
    interval = typed_property("interval", int)
    routing_parameter = typed_property("routing_parameter", str)
    device_id = typed_property("device_id", int)
    ENCODE_TYPE = "utf-8"

    def __init__(self, *, device_category, width_band, interval, routing_parameter, device_id):
        self.usage = "apply_net"
        self.device_category_ = device_category
        self.device_id = device_id
        self.width_band = width_band
        self.interval = interval
        self.routing_parameter = routing_parameter

    @staticmethod
    def format_():
        return "!16s16sii16si"

    @property
    def all_data(self):
        return (
            self.usage,
            self.device_category_,
            self.width_band,
            self.interval,
            self.routing_parameter,
            self.device_id,
        )

    @property
    def pack_data(self):
        pack_data_ = tuple(
            map(lambda m: m.encode(ApplyForNetBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *pack_data_)

    @staticmethod
    def unpack_data(pack_data):
        unpack_data_ = tuple(
            map(lambda m: m.decode(ApplyForNetBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(ApplyForNetBean.format_(), pack_data))
        )

        bean = ApplyForNetBean(width_band=unpack_data_[2], interval=unpack_data_[3],
                               routing_parameter=unpack_data_[4], device_id=unpack_data_[5],
                               device_category=unpack_data_[1])

        return bean

    def send(self, send, addr):
        '''

        :param send: protocal
        :param addr: 地址
        :return:
        '''
        send.send_apply(self.pack_data, addr)

    def is_allow_in(self):
        '''

        :return: 看一下self.width_band == 1 2 4 8 self.interval 625 25
        '''
        if self.width_band in [1, 2, 4, 8] and self.interval in [25, 625] and self.routing_parameter in [
            "OSPF协议", ]:
            return True
        else:
            print(12)
            return False


if __name__ == '__main__':
    print(123)
