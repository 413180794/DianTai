import json
import struct

from UDPChat.request_dict import success_net_reply_key, success_net_reply_format


class Tools(object):

    # 将string转成utf-8并把空格去除
    @staticmethod
    def __string_decode_strip(string):
        return string.decode('utf-8').strip('\x00')
    @staticmethod
    def __string_encode(string):
        return string.encode('utf-8')
    # 　收到成功入网的命令,将其解码转成字典
    def for_net_data_to_dict(self, *, key, format, datagram):
        return dict(
            zip(
                key,
                list(
                    map(
                        self.__string_decode_strip, struct.unpack(format, datagram)
                    )
                )
            )
        )

    # 将property_json保存到property文件中


    # def data_to_pack(self,*,data,type="",kind):


