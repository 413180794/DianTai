import functools
import struct

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import threads
from mylogging import logger


class UDPProtocol(DatagramProtocol):

    def __init__(self, *, MainForm):
        super(UDPProtocol, self).__init__()
        self.MainForm = MainForm
    
    def startProtocol(self):
        logger.info("启动udp")

    def datagramReceived(self, datagram, addr):
        # print(datagram)
        # 取出前16个字节，拿到元祖第一个内容，解码utf-8,去除空格

        usage = struct.unpack("!16s", datagram[0:16])[0].decode('utf-8').strip('\x00')
        try:
            function_ = functools.partial(getattr(self, usage + "_handle"), datagram, addr)
            d = threads.deferToThread(function_)
            d.addErrback(lambda m: print(m))

        except AttributeError as e:
            logger.error(e)

    def net_success_handle(self, datagram, addr):
        # 入网成功
        self.MainForm.reply_for_net_success.emit(datagram)

    def net_failed_handle(self, datagram, addr):
        # 入网失败
        # reply_for_net_failure_obj = ReplyForNetFailureBean.unpack_data(datagram)
        self.MainForm.reply_for_net_failure.emit()

    def connectionRefused(self):
        self.MainForm.connect_refused.emit()

    def send_apply(self, order, addr):
        logger.info(order)
        self.transport.write(order, addr)


if __name__ == '__main__':
    from twisted.internet import reactor
