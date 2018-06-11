import hashlib
import os

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
import os
import sys
sys.path.append(os.path.abspath("../Bean"))
from PicDataBean import PicDataBean
from PicSuccessReceiveBean import PicSuccessReceiveBean
from TextDataBean import TextDataBean
from TextSuccessReceive import TextSuccessReceive
from chatWindows import Ui_Dialog


class ChatDialog(QDialog, Ui_Dialog):
    text_data_signal = pyqtSignal(bytes, tuple)  # 发送而来的文本数据信号
    pic_data_signal = pyqtSignal(bytes, tuple)  # 发送而来的图片数据信号
    text_data_receive_signal = pyqtSignal()  # 对方成功接收文本信号
    pic_data_receive_signal = pyqtSignal() # 对方成功接收图像信号
    change_other_ip_id_signal = pyqtSignal(str, str)
    IMAGE_PATH = '../saveImage'

    def __init__(self, MainForm=None):
        super(ChatDialog, self).__init__()
        self.setupUi(self)
        self.MainForm = MainForm
        self.text_data_signal.connect(self.on_text_data_signal) # 收到文本的信号
        self.pic_data_signal.connect(self.on_pic_data_signal) #收到图像的信号
        self.change_other_ip_id_signal.connect(self.on_change_other_ip_id)  # 为了实现双击聊天框，将对方的ip id放入到左侧
        self.text_data_receive_signal.connect(self.on_text_data_receive_signal)  # 得知对方已经收到发出的文本
        self.pic_data_receive_signal.connect(self.on_pic_data_receive_signal) # 得知对方已经收到发出的图像

        self.pic_data_dict = {}  # 存放每一个文件的数据，用于解决接收udp顺序错误问题

    def on_change_other_ip_id(self, ip, device_name):
        self.other_device_ip.setText(ip)
        self.other_device_id.setText(device_name)

    def on_text_data_receive_signal(self):
        self.if_receive_msg.setText("接收成功")

    def on_pic_data_receive_signal(self):
        self.if_receive_msg.setText("接收成功")

    @pyqtSlot()
    def on_close_button_clicked(self):
        '''
        绑定关闭按钮
        :return:
        '''
        self.close()

    @pyqtSlot()
    def on_send_msg_button_clicked(self):
        '''
        绑定发送消息按钮，需要做
        1.获取文本框的输入
        2.形成TextBean
        3.清空文本框
        4.展示 xxx：  输入内容
        5.发送出去

        :return:
        '''
        self.if_receive_msg.setText('未接收')
        msg = self.textEdit.document().toPlainText()  # 获取文本框的输入
        msg_bean = TextDataBean(device_category=self.MainForm.device_category,
                                device_id=self.MainForm.device_id,
                                data=msg
                                )  # 形成TextBean
        self.textEdit.document().clear()
        self.listWidget.addTextMsg(self.MainForm.device_name, msg, False, ip=self.MainForm.get_host_ip())
        print(self.other_device_ip.text())
        msg_bean.send(self.MainForm.apply, (self.other_device_ip.text(), 10001))

    def get_md5_of_file(self, fname):
        '''
        输入文件路径，返回该文件的md5值
        如果该文件不存在，则返回None,
        采用更新的方式，避免大文件内存溢出
        :param fname:
        :return:
        '''
        if not os.path.exists(fname):
            return None
        with open(fname, 'rb') as f:
            m = hashlib.md5()
            while True:
                d = f.read(10240)
                if not d:
                    break
                m.update(d)
        return m.hexdigest()

    def get_file_size(self, fname):
        '''
        传入文件路径，返回该文件的大小,
        如果文件不存在，则返回NOne
        :param fname:
        :return:
        '''
        if not os.path.exists(fname):
            return None
        return os.path.getsize(fname)

    def get_file_ext(self, fname):
        filepath, tempfilename = os.path.split(fname)
        shotname, extension = os.path.splitext(tempfilename)
        return extension

    @pyqtSlot()
    def on_send_pic_button_clicked(self):
        '''

        :return:
        '''
        self.if_receive_msg.setText("未接收")
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", '/', "Images (*.png *.jpg *.bmp)")
        print(file_name)

        file_ext = self.get_file_ext(file_name)
        print(file_ext)
        self.listWidget.addImageMsg(self.MainForm.device_name, file_name, False, ip=self.MainForm.get_host_ip())
        if file_name is "":
            return
        md_5 = self.get_md5_of_file(file_name)  # 获得该文件的md5值。
        if md_5 is None:  # 如果该文件不存在，给予提示，但基本不会不存在的。
            QMessageBox.critical(self, "文件不存在", "文件不存在")
        file_size_all = self.get_file_size(file_name)  # 取得文件整体大小

        data_nums = int(file_size_all / 2048) + 1  # 将file分成data_nums份
        print("data_nums:"+str(data_nums))
        with open(file_name, 'rb') as f:
            for data_num in range(0, data_nums ):
                data = f.read(2048)
                file_size = len(data)  # 当前读取出来的大小
                pic_bean = PicDataBean(file_ext=file_ext, md_5=md_5, device_category=self.MainForm.device_category,
                                       device_id=self.MainForm.device_id, size=file_size,
                                       data_nums=data_nums, data_num=data_num, data=data)
                pic_bean.send(self.MainForm.apply, (self.other_device_ip.text(), 10001))

    def on_text_data_signal(self, datagram, addr):
        '''
        收到对方发送而来的信息需要做，
        1.通过信号把datagram发送到showDialog
        2.将datagram形成bean
        3.将msg显示在界面中。
        4.
        5.给对面回复 我已经收到
        :param msg:
        :return:
        '''
        text_data_obj = TextDataBean.unpack_data(datagram)
        msg = text_data_obj.data
        self.listWidget.addTextMsg(text_data_obj.device_name, msg, True, ip=str(addr[0]))
        text_success_receive_bean = TextSuccessReceive()
        text_success_receive_bean.send(self.MainForm.apply, addr)

    def on_pic_data_signal(self, datagram, addr):
        # 通过bean自身保存到文件
        # 要解决数据不按顺序来的问题。
        bean = PicDataBean.unpack_date(datagram)
        print(bean.data_nums)
        print(bean.data_num)
        print(len(bean.data))
        # 先判断该图片有没有接收过。
        if not self.pic_data_dict.get(bean.md_5):
            # 如果事前没有,创建数组
            self.pic_data_dict[bean.md_5] = []
        # print(bean.data_num)
        self.pic_data_dict.get(bean.md_5).insert(bean.data_num,bean.data) # 按照序号添加
        #　判断是否已经接收完毕
        print(self.pic_data_dict)

        if len(self.pic_data_dict.get(bean.md_5)) == bean.data_nums:
            with open(os.path.join(self.IMAGE_PATH,bean.md_5+bean.file_ext),'ab') as f:
                for data in self.pic_data_dict.get(bean.md_5):
                    print("收完")
                    f.write(data)
            self.listWidget.addImageMsg(self.MainForm.device_name,
                                        os.path.join(self.IMAGE_PATH, bean.md_5 + bean.file_ext), True,
                                        ip=self.MainForm.get_host_ip())
            self.pic_data_dict.pop(bean.md_5)
            os.remove(os.path.join(self.IMAGE_PATH,bean.md_5+bean.file_ext))
        pic_success_receive_bean = PicSuccessReceiveBean()
        pic_success_receive_bean.send(self.MainForm.apply, addr)

