# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'property.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!


# ----------------设备属性配置对话框----------------------




from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_dialog(QDialog):
    def __init__(self,parent = None):
        super(Ui_dialog, self).__init__(parent)
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(589, 355)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(400, 310, 171, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 381, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.__width_band_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.__width_band_label.setAutoFillBackground(False)
        self.__width_band_label.setObjectName("__width_band_label")
        self.horizontalLayout.addWidget(self.__width_band_label, 0, QtCore.Qt.AlignHCenter)
        self.width_band_combox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.width_band_combox.setObjectName("width_band_combox")
        self.width_band_combox.addItem("")
        self.width_band_combox.addItem("")
        self.width_band_combox.addItem("")
        self.width_band_combox.addItem("")
        self.horizontalLayout.addWidget(self.width_band_combox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.__send_rate_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.__send_rate_label.setAutoFillBackground(False)
        self.__send_rate_label.setObjectName("__send_rate_label")
        self.horizontalLayout_2.addWidget(self.__send_rate_label, 0, QtCore.Qt.AlignHCenter)
        self.send_rate_combox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.send_rate_combox.setObjectName("send_rate_combox")
        self.send_rate_combox.addItem("")
        self.send_rate_combox.addItem("")
        self.send_rate_combox.addItem("")
        self.send_rate_combox.addItem("")
        self.horizontalLayout_2.addWidget(self.send_rate_combox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.__interval_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.__interval_label.setAutoFillBackground(False)
        self.__interval_label.setObjectName("__interval_label")
        self.horizontalLayout_3.addWidget(self.__interval_label, 0, QtCore.Qt.AlignHCenter)
        self.interval_combox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.interval_combox.setObjectName("interval_combox")
        self.interval_combox.addItem("")
        self.interval_combox.addItem("")
        self.horizontalLayout_3.addWidget(self.interval_combox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.__network_ste_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.__network_ste_label.setAutoFillBackground(False)
        self.__network_ste_label.setObjectName("__network_ste_label")
        self.horizontalLayout_4.addWidget(self.__network_ste_label, 0, QtCore.Qt.AlignHCenter)
        self.network_ste_combox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.network_ste_combox.setObjectName("network_ste_combox")
        self.horizontalLayout_4.addWidget(self.network_ste_combox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.__routing_parameters_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.__routing_parameters_label.setAutoFillBackground(False)
        self.__routing_parameters_label.setObjectName("__routing_parameters_label")
        self.horizontalLayout_6.addWidget(self.__routing_parameters_label, 0, QtCore.Qt.AlignHCenter)
        self.routing_parameters_combox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.routing_parameters_combox.setObjectName("routing_parameters_combox")
        self.routing_parameters_combox.addItem("")
        self.horizontalLayout_6.addWidget(self.routing_parameters_combox)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.__interface_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.__interface_label.setAutoFillBackground(False)
        self.__interface_label.setObjectName("__interface_label")
        self.horizontalLayout_7.addWidget(self.__interface_label, 0, QtCore.Qt.AlignHCenter)
        self.interface_combox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.interface_combox.setObjectName("interface_combox")
        self.interface_combox.addItem("")
        self.interface_combox.addItem("")
        self.horizontalLayout_7.addWidget(self.interface_combox)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.__schedule_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.__schedule_label.setAutoFillBackground(False)
        self.__schedule_label.setObjectName("__schedule_label")
        self.horizontalLayout_8.addWidget(self.__schedule_label, 0, QtCore.Qt.AlignHCenter)
        self.schedule_combox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.schedule_combox.setObjectName("schedule_combox")
        self.horizontalLayout_8.addWidget(self.schedule_combox)
        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Dialog"))
        self.__width_band_label.setText(_translate("dialog", "频率间隔"))
        self.width_band_combox.setItemText(0, _translate("dialog", "30MHz~90MHz"))
        self.width_band_combox.setItemText(1, _translate("dialog", "610MHz~690MHz"))
        self.width_band_combox.setItemText(2, _translate("dialog", "225MHz~512MHz"))
        self.width_band_combox.setItemText(3, _translate("dialog", "1350MHz~1850MHz"))
        self.__send_rate_label.setText(_translate("dialog", "发送速率"))
        self.send_rate_combox.setItemText(0, _translate("dialog", "1.2b/s~100kb/s"))
        self.send_rate_combox.setItemText(1, _translate("dialog", "100kb/s~200kb/s"))
        self.send_rate_combox.setItemText(2, _translate("dialog", "200kb/s~300kb/s"))
        self.send_rate_combox.setItemText(3, _translate("dialog", "300kb/s~375kb/s"))
        self.__interval_label.setText(_translate("dialog", "信道间隔"))
        self.interval_combox.setItemText(0, _translate("dialog", "25kHz"))
        self.interval_combox.setItemText(1, _translate("dialog", "625kHz"))
        self.__network_ste_label.setText(_translate("dialog", "组网策略"))
        self.__routing_parameters_label.setText(_translate("dialog", "路由协议"))
        self.routing_parameters_combox.setItemText(0, _translate("dialog", "OSPF协议"))
        self.__interface_label.setText(_translate("dialog", "网口串口"))
        self.interface_combox.setItemText(0, _translate("dialog", "网口"))
        self.interface_combox.setItemText(1, _translate("dialog", "串口"))
        self.__schedule_label.setText(_translate("dialog", "调度策略"))

