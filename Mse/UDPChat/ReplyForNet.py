import os
import sys
sys.path.append(os.path.abspath("../Bean"))
sys.path.append(os.path.abspath("../UIPy"))
print(sys.path)
import functools
import struct
import time

from twisted.internet import reactor,  threads
from twisted.internet.protocol import DatagramProtocol


from ApplyForNetBean import ApplyForNetBean
from NetSuccessBean import NetSuccessBean
from NetFailedBean import NetFailedBean
from mylogging import logger


# 测试入网申请，此代码相当于虚拟节点，检测入网是否正确
# 分析得知datagramReveived只会收到入网申请传来的数据，
# 数据包含了 “width_band,interval,interface,routing-parameters,send_rate"
# 对以上参数的数值进行校验，之后返回success_ip地址 或者fail_


class replyForNet(DatagramProtocol):
    def __init__(self):
        self.ip_lists = "192.168.31.180:mse_t_v_12,192.168.31.41:mse_t_v_11,12.32.32.12:mse_t_v_23"

    def startProtocol(self):
        print("startProtocol")

    def datagramReceived(self, datagram, addr):

        # datagram 是以utf-8编码格式的bytes类型
        usage = struct.unpack("!16s", datagram[0:16])[0].decode('utf-8').strip('\x00')
        print(usage)
        # type_name = struct.unpack("!16s", datagram[16:32])[0].decode('utf-8').strip('\x00')
        try:
            function_ = functools.partial(getattr(self, usage + "_handle"), datagram, addr)
            d = threads.deferToThread(function_)
            d.addCallback(self.success_or_failure)
            d.addErrback(lambda m:print(m))
        except AttributeError as e:
            logger.error(e)

    def success_or_failure(self, status_addr):
        if status_addr[0] == "success_net_reply":
            reply_for_net_success_obj = NetSuccessBean(ip_list=self.ip_lists)

            self.transport.write(reply_for_net_success_obj.pack_data, status_addr[1])
        elif status_addr[0] == "failure_net_reply":

            reply_for_net_failure_obj = NetFailedBean()
            self.transport.write(reply_for_net_failure_obj.pack_data, status_addr[1])

    # 对内容校验函数
    def apply_net_handle(self, datagram, addr):
        # 此处的data还没有解码
        apply_for_net_obj = ApplyForNetBean.unpack_data(datagram)
        if apply_for_net_obj.is_allow_in():
            return "success_net_reply", addr
        else:
            return "failure_net_reply", addr

    def connectionRefused(self):
        logger.info("connectionResused")


if __name__ == '__main__':
    reactor.listenUDP(10000, replyForNet())
    reactor.run()
