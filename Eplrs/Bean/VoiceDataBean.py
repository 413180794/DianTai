import struct
import os
import sys


sys.path.append(os.path.abspath("../tool"))
from typeProperty import typed_property


class VoiceDataBean(object):
    __slots__ = ['_usage', '_device_category', '_device_id', '_voice_data']

    usage = typed_property('usage', str)
    device_category = typed_property('device_category', str)
    device_id = typed_property('device_id', int)
    voice_data = typed_property('voice_data', bytes)
    ENCODE_TYPE = 'utf-8'

    def __init__(self, *, device_category, device_id, voice_data):
        self.usage = 'voice_data'
        self.device_category = device_category
        self.device_id = device_id
        # 待解决问题。如果获得voice_data,
        # 不在bean中解决，bean中数据不具有特殊型
        self.voice_data = voice_data

    @staticmethod
    def format_():
        return "!16s16si2048s"

    @staticmethod
    def format_without_voice():
        return "!16s16si"

    @property
    def all_data(self):
        return (
            self.usage,
            self.device_category,
            self.device_id,
            self.voice_data,

        )

    @property
    def pack_data(self):
        '''
        将Bean打包，返回已经按照format格式打包的数据包
        :return:
        '''
        __pack_data_ = tuple(
            map(lambda m: m.encode(VoiceDataBean.ENCODE_TYPE) if type(m) == str else m, self.all_data)
        )
        return struct.pack(self.format_(), *__pack_data_)

    @staticmethod
    def unpack_data(pack_data):
        voice_data = pack_data[36:]
        str_data = pack_data[:36]

        unpack_data_ = tuple(
            map(lambda m: m.decode(VoiceDataBean.ENCODE_TYPE).strip("\x00") if type(m) == bytes else m,
                struct.unpack(VoiceDataBean.format_without_voice(), str_data))
        )
        bean = VoiceDataBean(device_category=unpack_data_[1], device_id=unpack_data_[2], voice_data=voice_data)
        return bean

    def send(self, __send, addr):
        __send.send_apply(self.pack_data, addr)
