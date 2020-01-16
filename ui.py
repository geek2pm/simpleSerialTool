# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serial.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(698, 354)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(340, 10, 89, 31))
        self.btn_open.setObjectName("btn_open")
        self.comboBox_COMs = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_COMs.setGeometry(QtCore.QRect(10, 10, 221, 31))
        self.comboBox_COMs.setObjectName("comboBox_COMs")
        self.comboBox_baud = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_baud.setGeometry(QtCore.QRect(240, 10, 86, 31))
        self.comboBox_baud.setObjectName("comboBox_baud")
        self.comboBox_baud.addItem("")
        self.comboBox_baud.addItem("")
        self.comboBox_baud.addItem("")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 50, 680, 230))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 678, 228))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setGeometry(QtCore.QRect(-1, -1, 680, 230))
        self.textBrowser.setObjectName("textBrowser")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btn_send = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QtCore.QRect(610, 290, 80, 31))
        self.btn_send.setObjectName("btn_send")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 290, 591, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(600, 10, 89, 31))
        self.btn_clear.setObjectName("btn_clear")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "simple Serial Tool"))
        self.btn_open.setText(_translate("MainWindow", "open"))
        self.comboBox_baud.setItemText(0, _translate("MainWindow", "9600"))
        self.comboBox_baud.setItemText(1, _translate("MainWindow", "115200"))
        self.comboBox_baud.setItemText(2, _translate("MainWindow", "512000"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.btn_send.setText(_translate("MainWindow", "send"))
        self.btn_clear.setText(_translate("MainWindow", "clear"))
