import struct
import os
import sys

sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class NetFailedBean(object):
    __slots__ = ['_usage']
    usage = typed_property("usage", str)
    ENCODE_TYPE = "utf-8"

    def __init__(self):
        self.usage = "net_failed"

    @staticmethod
    def format_():
        return "!16s"

    @property
    def all_data(self):
        return (
            self.usage,
        )

    @property
    def pack_data(self):
        __pack_data = tuple(
            map(lambda m: m.encode(NetFailedBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        print(__pack_data)
        return struct.pack(self.format_(), *__pack_data)

    @staticmethod
    def unpack_data(pack_data):
        # unpack_data_ = tuple(
        #     map(lambda m: m.decode(ReplyForNetFailureBean.ENCODE_TYPE).strip("\x00"),
        #         struct.unpack(ReplyForNetFailureBean.format_(), pack_data))
        # )
        bean = NetFailedBean()
        return bean
