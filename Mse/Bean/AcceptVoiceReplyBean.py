'''
请求通话的回应，允许通话应答
ss
'''
import struct
import os
import sys
sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class AcceptVoiceReplyBean(object):
    __slots__ = ['_usage']
    usage = typed_property('usage', str)
    ENCODE_TYPE = 'utf-8'

    def __init__(self):
        self.usage = 'accept_voice_r'

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
        pack_data_ = tuple(
            map(lambda m: m.encode(AcceptVoiceReplyBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *pack_data_)

    @staticmethod
    def unpack_data():
        bean = AcceptVoiceReplyBean()
        return bean

    def send(self, __send, addr):
        __send.send_apply(self.pack_data, addr)


if __name__ == '__main__':
    x = AcceptVoiceReplyBean()
    print(x.pack_data)
