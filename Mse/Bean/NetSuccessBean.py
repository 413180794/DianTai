import struct
import os
import sys
sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class NetSuccessBean(object):
    __slots__ = ['_usage', '_ip_list']
    usage = typed_property("usage", str)
    ip_list = typed_property("ip_list", str)
    ENCODE_TYPE = "utf-8"

    def __init__(self, *, ip_list):
        self.usage = "net_success"
        self.ip_list = ip_list

    @staticmethod
    def format_():
        return "!16s2048s"

    @property
    def all_data(self):
        return (
            self.usage,
            self.ip_list
        )

    @property
    def pack_data(self):
        __pack_data = tuple(
            map(lambda m: m.encode(NetSuccessBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        print(__pack_data)
        # dprint(struct.pack(ReplyForNetSuccessBean.format_(),pack_data_))
        return struct.pack(NetSuccessBean.format_(), *__pack_data)

    @staticmethod
    def unpack_data(pack_data):
        unpack_data_ = tuple(
            map(lambda m: m.decode(NetSuccessBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(NetSuccessBean.format_(), pack_data))
        )
        bean = NetSuccessBean(ip_list=unpack_data_[1])
        return bean
