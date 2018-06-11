# conding:utf-8
import json
import os
import struct
import sys
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem

from Bean.ApplyForNetBean import ApplyForNetBean
from UDPChat.UDPProtocol import UDPProtocol
# from UDPChat.Tools import Tools
# from UDPChat.request_dict import apply_for_net_format
from mylogging import logger
from mainWindow import Ui_MainWindow

from property import Property


class MainForm(QMainWindow, Ui_MainWindow):
    connect_refused = pyqtSignal()
    reply_for_net_failure = pyqtSignal()
    reply_for_net_success = pyqtSignal(str)

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
        self.device_id = 0
        self.device_kind = "mse_t_r"
        self.ip_id_table.setHorizontalHeaderLabels(["设备ID", "设备IP"])
        self.ip_id_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.god_node_addr = ('127.0.0.1',10000) # 上帝节点的地址
        # 将收到的IP显示出来
        # self.tools = Tools()
        reactor.listenUDP(10002, self.apply)

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
            yield [QTableWidgetItem(id), QTableWidgetItem(ip)]

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

    def on_reply_for_net_success(self, ip_comma_interval):
        '''
        入网成功之后，将收到的"127.0.0.1:sdf_MSE_t,"123.1.2.3:sd_MSE_t"
        显示在表格中，清空原有的数据，填充新收到的数据
        :param ip_comma_interval:
        :return:
        '''
        self.clear_table_data()
        for data in self.ip_id_list_to_many_one_line(ip_comma_interval):
            self.insert_data_to_ip_id_table(data)

    def on_reply_for_net_failure(self):
        '''
        入网失败之后，提示入网失败
        :return: None
        '''
        QMessageBox.critical(self, "入网失败", "请正确设置设备属性，或联系网络管理员")

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
        QMessageBox.about(self, "保存成功", "属性保存成功")

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
            type_= self.device_kind
        )
        apply_for_net_obj.send(self.apply, self.god_node_addr)
        # self.apply.send_apply(apply_for_net_obj.pack_data, ("127.0.0.1", 10000))
        # 这里搞成applyforobj自己的属性。他可以实现自己发送
        # 这里需要使用struct库进行打包，方便莫偲拆包

    @pyqtSlot()
    def on_set_property_button_clicked(self):
        '''
        点击入网申请后，跳转至主页面
        :return:
        '''
        self.tabWidget.setCurrentWidget(self.Property_tab)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    import qt5reactor

    qt5reactor.install()
    from twisted.internet import reactor

    win = MainForm()
    win.show()
    reactor.run()
