# conding:utf-8
import json
import os
import socket
import sys

sys.path.append(os.path.abspath("../Bean"))
sys.path.append(os.path.abspath("../UDPChat"))
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QTimer,QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem, QAbstractItemView
from AcceptVoiceReplyBean import AcceptVoiceReplyBean
from ApplyForNetBean import ApplyForNetBean
from ApplyForVoiceBean import ApplyForVoiceBean
from NetSuccessBean import NetSuccessBean
from RejectVoiceReplyBean import RejectVoiceReplyBean
from TimedMBox import TimedMBox
from UDPProtocol import UDPProtocol
from VoiceDialog import VoiceDialog
from mainWindow import Ui_MainWindow
from mylogging import logger
from property import Property
from ChatDialog import ChatDialog


class MainForm(QMainWindow, Ui_MainWindow):
    connect_refused = pyqtSignal()
    reply_for_net_failure = pyqtSignal()
    reply_for_net_success = pyqtSignal(bytes)
    not_read_msg_count_signal = pyqtSignal()  # 未读消息计数信号
    apply_voice_signal = pyqtSignal(bytes, tuple)  # 其他人发送而来的请求通话命令

    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentWidget(self.MainWindow_tab)  # 先展示出主界面
        self.init_property()
        self.send_rate_dial.valueChanged.connect(self.send_rate_dial_valueChanged)  # 奇怪，使用装饰器绑定不到，是库的bug么
        self.send_rate_spinbox.valueChanged.connect(self.send_rate_spinbox_valueChanged)
        self.apply = UDPProtocol(host="127.0.0.1", port=10000, MainForm=self)
        self.connect_refused.connect(self.on_connect_refused)
        self.reply_for_net_success.connect(self.on_reply_for_net_success)
        self.reply_for_net_failure.connect(self.on_reply_for_net_failure)
        self.apply_voice_signal.connect(self.on_apply_voice_signal)
        self.not_read_msg_count_signal.connect(self.on_not_read_msg_count_signal)
        self.device_id = 0
        self.device_category = "mse_t_r"
        self.device_name = self.device_category + "_" + str(self.device_id)
        self.device_ip = self.get_host_ip()
        self.ip_id_table.setHorizontalHeaderLabels(["设备ID", "设备IP"])
        self.ip_id_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.god_node_addr = ('127.0.0.1', 10000)  # 上帝节点的地址
        self.text_dlg = ChatDialog(self)
        self.voice_dlg = VoiceDialog(self)
        self.not_read_msg_count = 0  # 未读消息计数
        reactor.listenUDP(10001, self.apply)
        self.property_save_button.clicked.emit()

    def on_apply_voice_signal(self, datagram, addr):
        '''
        一切的起始点都要从voicedialog的状态是等待拨号，只有在该状态下，才可以接收别人的请求通话命令
        如果其他请求通话时候，状态不是等待拨号，说明voicedialog正在通话中，返回拒绝通话命令（考虑正在通话命令）
        :return:
        '''
        self.other_addr = addr
        if self.voice_dlg.status_label.text() == "等待拨号":
            # 如果状态是等待拨号，收到请求通话命令后，状态切换为正在建立连接，并创建回调，10秒后判断状态是否
            # 仍然是正在建立连接，如果是，返回拒绝通话，并且挂断。
            apply_voice_bean = ApplyForVoiceBean.unpack_data(datagram)
            self.voice_dlg.status_label.setText('正在建立连接')
            self.voice_dlg.start_voice_button.setVisible(False)
            self.voice_dlg.device_name_label.setText(apply_voice_bean.device_name)
            self.voice_dlg.device_ip_label.setText(addr[0])
            self.voice_dlg.show()
            self.voice_dlg.raise_()
            self.voice_dlg.activateWindow()

            result = TimedMBox.question(title="请求通话", text=apply_voice_bean.device_category + "_" + str(
                apply_voice_bean.device_id) + "请求通话" + "\n" + "是否同意？")

            # 上述会定时10秒
            # result = QMessageBox.question(self.voice_dlg,
            #                               "请求通话",
            #                               apply_voice_bean.device_category + "_" + str(
            #                                   apply_voice_bean.device_id) + "请求通话" + "\n" + "是否同意？",
            #                               QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                # 如果同意对方的回答，那么就要开始向对象发送语音，弹出voiceDialog，发送语音的任务交给voiceDialog
                accept_voice_reply_bean = AcceptVoiceReplyBean()
                accept_voice_reply_bean.send(self.apply, addr)



            elif result == QMessageBox.No:
                # 　如果不同意通话，返回拒绝通话命令,并且挂断
                reject_voice_reply_bean = RejectVoiceReplyBean()
                reject_voice_reply_bean.send(self.apply, addr)
                self.voice_dlg.close()
        else:
            # 如果状态不是 等待拨号，说明该设备正在通话中或者正在建立通话中，直接返回拒绝通话
            reject_voice_reply_bean = RejectVoiceReplyBean()
            reject_voice_reply_bean.send(self.apply, addr)

    def closeEvent(self, QCloseEvent):
        QCoreApplication.instance().quit()

    def on_not_read_msg_count_signal(self):
        '''
        每次收到新的消息都会触发这个函数，此函数目的是对未读消息进行计数，默认如果用户
        打开了text_dlg，那么就认为用户读取了所有消息。如果用户没有打开text_dlg，就
        将未读消息加一
        :return:
        '''
        if self.text_dlg.isVisible():
            # 如果聊天框被打开，新的数据上来，什么都不用干
            pass
        else:
            # 如果聊天框没有被打开，新的数据上来，将未读数据加一
            self.not_read_msg_count += 1
            self.not_read_count_label.setText(str(self.not_read_msg_count))

    @pyqtSlot()
    def on_start_voice_button_clicked(self):
        if self.other_equip_ip.text() == "":
            QMessageBox.critical(self, "失败", "请选择对话的对象")
        else:
            self.voice_dlg.device_name_label.setText(self.other_equip_id.text())
            self.voice_dlg.device_ip_label.setText(self.other_equip_ip.text())
            self.voice_dlg.start_voice_button.setVisible(True)
            self.voice_dlg.close_button.setVisible(False)
            self.voice_dlg.show()
            self.voice_dlg.raise_()
            self.voice_dlg.activateWindow()

    @pyqtSlot(int, int)
    def on_ip_id_table_cellClicked(self, row, colmn):
        '''
        对点击ip_id_table做出响应，思路，点击某一行，将这一行的ip显示到右侧
        :param row:
        :param colmn:
        :return:
        '''
        device_ip = self.ip_id_table.item(row, 1).text()  # 获得该行中的ip地址
        device_id = self.ip_id_table.item(row, 0).text()  # 获得该行中的i
        self.other_equip_id.setText(device_id)
        self.other_equip_ip.setText(device_ip)

    def ip_id_list_to_many_one_line(self, ip_comma_interval):
        '''
        '127.0.0.0:sdd_MSE_t,123.2.1.2:sf_MSE_t' --- > yield [TableWidget(id),TableWidget(ip)]
        :param ip_comma_interval:
        :return:
        '''
        ip_id_list = str(ip_comma_interval).split(",")
        for ip_id in ip_id_list:
            ip = ip_id.split(":")[0]
            id = ip_id.split(":")[1]
            id_item = QTableWidgetItem(id)
            ip_item = QTableWidgetItem(ip)
            id_item.setTextAlignment(Qt.AlignCenter)
            ip_item.setTextAlignment(Qt.AlignCenter)
            yield [id_item, ip_item]

    def insert_data_to_ip_id_table(self, data):
        '''
        将data插入至表格，Data的形式为 [设备ID，设备IP]表示了一行
        :param result:
        :return:
        '''
        self.ip_id_table.insertRow(self.ip_id_table.rowCount())
        for y in range(self.ip_id_table.columnCount()):
            self.ip_id_table.setItem(self.ip_id_table.rowCount() - 1, y, data[y])
            self.ip_id_table.scrollToBottom()

    def clear_table_data(self):
        '''
            清空表格中的所有数据
        :return:　ｎｏｎｅ
        '''
        self.ip_id_table.setRowCount(0)  # 清空所有行
        self.ip_id_table.clearContents()  # 清空所有内容

    def on_reply_for_net_success(self, datagram):
        '''
        入网成功之后，将收到的"127.0.0.1:sdf_MSE_t,"123.1.2.3:sd_MSE_t"
        显示在表格中，清空原有的数据，填充新收到的数据
        :param ip_comma_interval:
        :return:
        '''
        reply_for_net_success_obj = NetSuccessBean.unpack_data(datagram)
        ip_comma_interval = reply_for_net_success_obj.ip_list
        self.clear_table_data()
        for data in self.ip_id_list_to_many_one_line(ip_comma_interval):
            self.insert_data_to_ip_id_table(data)
        self.if_connected_main.setText("成功入网")
        QMessageBox.about(self, "入网成功", "入网成功")

    def on_reply_for_net_failure(self):
        '''
        入网失败之后，提示入网失败
        :return: None
        '''
        self.if_connected_main.setText("未连接")
        QMessageBox.critical(self, "入网失败", "请正确设置设备属性，或联系网络管理员")
        self.clear_table_data()

    def send_rate_spinbox_valueChanged(self):
        '''
        dial与spinbox绑定
        :return:
        '''
        self.send_rate_dial.setValue(int(self.send_rate_spinbox.value()))

    def on_connect_refused(self):
        QMessageBox.critical(self, "入网申请错误", "请检查网络连接")

    # 绑定滚动dial
    def send_rate_dial_valueChanged(self):
        self.send_rate_spinbox.setValue(self.send_rate_dial.value())

    # 申请入网 属性配置 只需要 width_band interval routing_parameters
    def init_property(self):
        '''
        读取现有的property.json文件中的设备属性，并显示在界面中
        :return: None
        '''
        if os.path.exists("property.json"):
            with open("property.json", "r") as f:
                property_json = json.load(f)
                property_obj = Property(
                    width_band=property_json.get("width_band"),
                    interval=property_json.get("interval"),
                    routing_parameters=property_json.get("routing_parameters")
                )
            for name in property_obj.__slots__:
                # 一行代替以下所有的代码，getattr(self,name+"_combox") == self.xxx_combox
                # getattr(getattr(self,name+"_combox),"setCurrentText) == self.xxx_combox.setCurrent
                # getattr(self.property_obj,name) == property_obj.xxxx
                getattr(getattr(self, name + "_combox"), "setCurrentText")(getattr(property_obj, name))

    @pyqtSlot()
    def on_property_save_button_clicked(self):
        '''
        绑定保存按钮
        :return:
        '''
        # 如果需要添加属性，在property_json直接添加就可以了
        property_json = {
            "width_band": self.width_band_combox.currentText(),
            "interval": self.interval_combox.currentText(),
            "routing_parameters": self.routing_parameters_combox.currentText()
        }
        self.save_property_json(property_json)
        self.send_property(property_json)

        # self.tabWidget.setCurrentWidget(self.MainWindow_tab)
        # 数据的顺序以此是width_band,interval,schedule,routing_parameters,type,ip_id_list.入网申请的时候ip_id_list为空
        # 也就只给ip_id_list分配了一个字节

    def save_property_json(self, property_json):
        '''
        将property_json保存到文件中
        :param property_json:
        :return:
        '''
        with open("property.json", 'w', encoding='utf-8') as f:
            json.dump(property_json, f)

    def send_property(self, property_json):
        '''
        将property_json中的数据发送至上帝节点
        :param property_json:
        :return:
        '''
        # 该函数将property_json中的值进行打包，所有字节都是16个字节。json的长度可变
        width_band = {"30MHz~90MHz": 1, "610MHz~690MHz": 2, "225MHz~512MHz": 4, "1350MHz~1850MHz": 8}
        interval = {"625kHz": 625, "25kHz": 25}
        apply_for_net_obj = ApplyForNetBean(
            width_band=width_band.get(property_json.get("width_band")),
            interval=interval.get(property_json.get("interval")),
            routing_parameter=property_json.get("routing_parameters"),
            device_id=self.device_id,
            device_category=self.device_category
        )
        apply_for_net_obj.send(self.apply, self.god_node_addr)
        # self.apply.send_apply(apply_for_net_obj.pack_data, ("127.0.0.1", 10000))
        # 这里搞成applyforobj自己的属性。他可以实现自己发送 发送文本

    @pyqtSlot()
    def on_set_property_button_clicked(self):
        '''
        点击入网申请后，跳转至主页面
        :return:
        '''
        self.tabWidget.setCurrentWidget(self.Property_tab)
        # self.send_text_button

    @pyqtSlot()
    def on_send_file_button_clicked(self):
        '''
        点击发送文本后触发，生成一个聊天窗口，该窗口很简单，上面显示发送的和接收的文本
        下面为一个输入框，点击发送后将文本发送出去。
        :return:
        '''
        if self.other_equip_ip.text() == "":
            QMessageBox.critical(self, "失败", "请选择发送的对象")
        else:
            self.not_read_msg_count = 0
            self.not_read_count_label.setText(str(self.not_read_msg_count))
            self.text_dlg.my_device_id.setText(str(self.device_name))
            self.text_dlg.my_device_ip.setText(self.device_ip)
            self.text_dlg.other_device_id.setText(self.other_equip_id.text())
            self.text_dlg.other_device_ip.setText(self.other_equip_ip.text())
            self.text_dlg.show()
            self.text_dlg.raise_()
            self.text_dlg.activateWindow()

    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            logger.error(e)
        finally:
            s.close()
        return ip


if __name__ == '__main__':
    app = QApplication(sys.argv)
    import qt5reactor

    qt5reactor.install()
    from twisted.internet import reactor

    win = MainForm()
    win.show()
    reactor.run()
