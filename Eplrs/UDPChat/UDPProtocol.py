import functools
import struct

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import threads
from mylogging import logger


class UDPProtocol(DatagramProtocol):

    def __init__(self, *, host, port, MainForm):
        super(UDPProtocol, self).__init__()
        self.host = host
        self.port = port
        # self.tools = Tools()
        self.MainForm = MainForm

    def startProtocol(self):
        # self.transport.connect(self.host, self.port)
        logger.info("now we can only send to host %s port %d" % (self.host, self.port))

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
        # reply_for_net_success_obj = ReplyForNetSuccessBean.unpack_data(datagram)
        self.MainForm.reply_for_net_success.emit(datagram)

    def net_failed_handle(self, datagram, addr):
        # 入网失败
        # reply_for_net_failure_obj = ReplyForNetFailureBean.unpack_data(datagram)
        self.MainForm.reply_for_net_failure.emit()

    def text_received_handle(self, datagram, addr):
        '''
        收到消息发送成功的提示
        :param datagram:
        :param addr:
        :return:
        '''
        self.MainForm.text_dlg.text_data_receive_signal.emit()

    def image_received_handle(self, datagram, addr):
        '''
        告知对方成功接收图像
        :param datagram:
        :param addr:
        :return:
        '''
        self.MainForm.text_dlg.text_data_receive_signal.emit()

    def text_data_handle(self, datagram, addr):
        # 处理发送过来的文字
        self.MainForm.not_read_msg_count_signal.emit()
        self.MainForm.text_dlg.text_data_signal.emit(datagram, addr)

    def image_data_handle(self, datagram, addr):
        '''
        收到图像数据
        :param datagram:
        :param addr:
        :return:
        '''
        self.MainForm.not_read_msg_count_signal.emit()
        self.MainForm.text_dlg.pic_data_signal.emit(datagram, addr)

    def apply_voice_handle(self,datagram,addr):
        '''
        收到请求通话命令,其他人发来的命令，我方在主界面进行提示，让其选择是否同意。
        :param datagram:
        :param addr:
        :return:
        '''
        self.MainForm.apply_voice_signal.emit(datagram,addr)

    def accept_voice_r_handle(self,datagram,addr):
        '''
        对方允许通话
        :return:
        '''
        self.MainForm.voice_dlg.accept_voice_r_signal.emit(addr)

    def reject_voice_r_handle(self,datagram,addr):
        '''
        对方拒绝通话，
        :return:
        '''
        self.MainForm.voice_dlg.reject_voice_r_signal.emit()


    def reject_voice_a_handle(self,datagram,addr):
        self.MainForm.voice_dlg.reject_voice_a_signal.emit()

    def voice_data_handle(self,datagram,addr):
        '''
        发送而来的语音信号，交给VoiceDialog播放
        :param datagram:
        :param addr:
        :return:
        '''
        self.MainForm.voice_dlg.voice_data_signal.emit(datagram,addr)



    def connectionRefused(self):
        self.MainForm.connect_refused.emit()

    def send_apply(self, order, addr):
        logger.info(order)

        self.transport.write(order, addr)


if __name__ == '__main__':
    from twisted.internet import reactor
