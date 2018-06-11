
import struct
import os
import sys

from mylogging import logger

sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property
class RejectVoiceApplyBean(object):
    __slots__ = ['_usage']
    usage = typed_property('usage', str)
    ENCODE_TYPE = 'utf-8'

    def __init__(self):
        self.usage = 'reject_voice_a'

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
            map(lambda m: m.encode(RejectVoiceApplyBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *pack_data_)

    @staticmethod
    def unpack_data():
        bean = RejectVoiceApplyBean()
        return bean

    def send(self, __send, addr):
        try:
            __send.send_apply(self.pack_data, addr)
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    x = RejectVoiceApplyBean()
    print(x.pack_data)
