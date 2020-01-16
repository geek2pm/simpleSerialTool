#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,QTimer,QEventLoop
from PyQt5.QtWidgets import QApplication
import sys
import ui,message
import serial
import serial.tools.list_ports

class DataCaptureThread(QThread):
    def collectProcessData(self):
        print ("Collecting Process Data")

    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.dataCollectionTimer = QTimer()
        self.dataCollectionTimer.moveToThread(self)
        self.dataCollectionTimer.timeout.connect(self.collectProcessData)

    def run(self):
        self.dataCollectionTimer.start(1000)
        loop = QEventLoop()
        loop.exec_()

class Message(QtWidgets.QMainWindow, message.Ui_Dialog):
    def __init__(self, parent=None):
        super(Message, self).__init__(parent)
        self.setupUi(self)

class App(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.btn_open.clicked.connect(self.btn_open_Clicked)
        self.btn_send.clicked.connect(self.btn_send_Clicked)
        self.btn_clear.clicked.connect(self.btn_clear_Clicked)
        self.getCOMs();

    def btn_open_Clicked(self):

        if self.btn_open.text() == 'opened':
            self.btn_open.setText('closed')
            self.ser=None
        else:
            com = self.comboBox_COMs.currentData(self.comboBox_COMs.currentIndex())
            baud = self.comboBox_baud.currentData(self.comboBox_baud.currentIndex())
            try:
                #global ser
                self.ser=serial.Serial(com,baud,timeout=5000)
            except Exception as err:
                print(err)
                self.dialog = Message(self)
                self.dialog.textBrowser.setText("")
                self.dialog.textBrowser.append("<h2>error</h2>")
                self.dialog.textBrowser.append(str(err))
                self.dialog.show()
            else:
                print('ok')
                self.btn_open.setText('opened')
                self.dataCollectionThread = DataCaptureThread()
                self.dataCollectionThread.start()
                #self.ser.inWaiting()


    def btn_send_Clicked(self):
        print(self.lineEdit.text())
        self.textBrowser.append("{}\n".format(self.lineEdit.text()))
        self.lineEdit.setText("")

    def btn_clear_Clicked(self):
        self.textBrowser.setText("")

    def getCOMs(self):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            self.comboBox_COMs.addItem(port)

def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()