# #
# #
# # 16s 16s 16s 16s 16s  kind width_band,interval,routing_parameters
# # 16s 16s 2048s kind type ip_list
# # 16s 16s 1s  kind type ip_list
# #
#
#
# # 用于检查属性是否符合要求的字典，测试自用，不用发送
# import struct
#
# check_request_dict = {
#     "width_band": ("30MHz~90MHz", "610MHz~690MHz", "225MHz~512MHz", "1350MHz~1850MHz"),
#     "interval": ("25kHz", "625kHz"),
#     "routing_parameters": ("OSPF协议",),
#     "type": ("request",),
#     "ip_id_list": ("",)
# }
# failure_net_reply_format = "!16s16s1s"
# failure_net_reply_dict = {
#     "kind": "reply_for_net".encode('utf-8'),
#     "type": "failure".encode('utf-8'),
#     "ip_list": "".encode('utf-8')
# }
# ip_list = "127.0.0.1,123.2.1.2,12.2.3.4,1.2.4.5,23.1.23.123"
# success_net_reply_format = "!16s16s2048s"
# success_net_reply_dict = {
#     "kind": "reply_for_net".encode('utf-8'),
#     "type": "success".encode('utf-8'),
#     "ip_list": ip_list.encode('utf-8')
# }
# success_net_reply = struct.pack(success_net_reply_format, *tuple(success_net_reply_dict.values()))
# failure_net_reply = struct.pack(failure_net_reply_format, *tuple(failure_net_reply_dict.values()))
# apply_for_net_format = "!16s16s16s16s"
# apply_for_net_key = ['kind', 'width_band', 'interval', 'routing_parameters']
# success_net_reply_key = ["kind", "type", "ip_list"]
# failure_net_reply_key = ["kind", "type", "ip_list"]
# # import struct
# #
# #
# # class Data(object):
# #     def __init__(self):
# #         self.__check_request_dict = {
# #             "width_band": ("30MHz~90MHz", "610MHz~690MHz", "225MHz~512MHz", "1350MHz~1850MHz"),
# #             "interval": ("25kHz", "625kHz"),
# #             "routing_parameters": ("OSPF协议",),
# #             "type": ("request",),
# #             "ip_id_list": ("",)
# #         }
# #         self.__failure_net_reply_dict = {
# #             "kind": "reply_for_net".encode('utf-8'),
# #             "type": "failure".encode('utf-8'),
# #             "ip_list": "".encode('utf-8')
# #         }
# #         self.__success_net_reply_dict = {
# #             "kind": "reply_for_net".encode('utf-8'),
# #             "type": "success".encode('utf-8'),
# #             "ip_list": self.ip_list.encode('utf-8')
# #         }
# #         self.__failure_net_reply_format = "!16s16s1s"
# #         self.__success_net_reply_format = "!16s16s2048s"
# #         self.__apply_for_net_format = "!16s16s16s16s"
# #         self.__success_net_reply = struct.pack(self.__success_net_reply_format,
# #                                                *tuple(self.__success_net_reply_dict.values()))
# #         self.__failure_net_reply = struct.pack(self.__failure_net_reply_format,
# #                                                *tuple(self.__failure_net_reply_dict.values()))
# #
# #         self.__apply_for_net_key = ['kind', 'width_band', 'interval', 'routing_parameters']
# #         self.__success_net_reply_key = ["kind", "type", "ip_list"]
# #         self.__failure_net_reply_key = ["kind", "type", "ip_list"]
# #         self.__ip_list = "127.0.0.1,123.2.1.2,12.2.3.4,1.2.4.5,23.1.23.123"
# #
# #     def get_dict(self, name):
# #         return getattr(self, "__" + name + "_dict", {})
# #
# #     def get_format(self, name):
# #         return getattr(self, "__" + name + "_format", "")
# #
# #     def get_key(self, name):
# #         return getattr(self, "__" + name + "_key", [])
# #
# #     def get_pack_data(self, name, *args):
# #         return struct.pack(self.get_format(name),*args)
# #
# #     def get_success_net_reply_pack_data(self):
# #         return self_
