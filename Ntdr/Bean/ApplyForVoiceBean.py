'''
请求通话命令
'''
import struct
import struct
import os
import sys
sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property

class ApplyForVoiceBean(object):
    __slots__ = ['_usage', '_device_category', '_device_id']
    usage = typed_property('usage', str)
    device_category = typed_property('device_category', str)
    device_id = typed_property('device_id', int)

    ENCODE_TYPE = 'utf-8'

    def __init__(self, *, device_category, device_id):
        self.usage = 'apply_voice'
        self.device_category = device_category
        self.device_id = device_id

    @staticmethod
    def format_():
        return "!16s16si"

    @property
    def all_data(self):
        return (
            self.usage,
            self.device_category,
            self.device_id,
        )

    @property
    def device_name(self):
        return self.device_category + "_" + str(self.device_id)

    @property
    def pack_data(self):
        __pack_data = tuple(
            map(lambda m: m.encode(ApplyForVoiceBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *__pack_data)

    @staticmethod
    def unpack_data(pack_data):
        unpack_data = tuple(
            map(lambda m: m.decode(ApplyForVoiceBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(ApplyForVoiceBean.format_(), pack_data))
        )
        bean = ApplyForVoiceBean(device_category=unpack_data[1], device_id=unpack_data[2])
        return bean

    def send(self, __send, addr):
        try:
            __send.send_apply(self.pack_data, addr)
        except Exception as e:
            print(e)

    def __str__(self):
        return self.usage + "---" + self.device_category + "---" + str(self.device_id)
