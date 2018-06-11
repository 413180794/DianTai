# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'voiceWindows.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(401, 302)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 7, 401, 291))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.__status_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.__status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.__status_label.setObjectName("__status_label")
        self.horizontalLayout.addWidget(self.__status_label)
        self.status_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.horizontalLayout.addWidget(self.status_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.__device_ip_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.__device_ip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.__device_ip_label.setObjectName("__device_ip_label")
        self.horizontalLayout_2.addWidget(self.__device_ip_label)
        self.device_ip_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.device_ip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.device_ip_label.setObjectName("device_ip_label")
        self.horizontalLayout_2.addWidget(self.device_ip_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.__device_name_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.__device_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.__device_name_label.setObjectName("__device_name_label")
        self.horizontalLayout_3.addWidget(self.__device_name_label)
        self.device_name_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.device_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.device_name_label.setObjectName("device_name_label")
        self.horizontalLayout_3.addWidget(self.device_name_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.start_voice_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.start_voice_button.setObjectName("start_voice_button")
        self.verticalLayout.addWidget(self.start_voice_button)
        self.close_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.close_button.setObjectName("close_button")
        self.verticalLayout.addWidget(self.close_button)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.__status_label.setText(_translate("Dialog", "通话状态"))
        self.status_label.setText(_translate("Dialog", "等待拨号"))
        self.__device_ip_label.setText(_translate("Dialog", "设备IP"))
        self.device_ip_label.setText(_translate("Dialog", "正在拨号"))
        self.__device_name_label.setText(_translate("Dialog", "设备名称"))
        self.device_name_label.setText(_translate("Dialog", "正在拨号"))
        self.start_voice_button.setText(_translate("Dialog", "拨号"))
        self.close_button.setText(_translate("Dialog", "挂断"))

