#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import sys,time
import serial
import serial.tools.list_ports

qtCreatorFile = "ui/main.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = "ui/message.ui" # Enter file here.
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class DataCaptureThread(QtCore.QThread):
    data_ok = QtCore.pyqtSignal(object)
    def __init__(self,ser):
        self.ser = ser
        QtCore.QThread.__init__(self)
    def run(self):
        try:
            num = self.ser.inWaiting()
        except:
            print('none data')
        else:
            if num>0:
                data = self.ser.read(num)
                text = str(data, encoding = "utf8")
                self.data_ok.emit(text)
        # QtCore.QThread.sleep(1)
        time.sleep(0.1)
        self.run()

class Message(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(Message, self).__init__(parent)
        self.setupUi(self)

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.btn_open.clicked.connect(self.btn_open_Clicked)
        self.btn_send.clicked.connect(self.btn_send_Clicked)
        self.btn_clear.clicked.connect(self.btn_clear_Clicked)
        self.getCOMs()

    def btn_open_Clicked(self):

        if self.btn_open.text() == 'opened':
            self.btn_open.setText('closed')
            self.ser=None
        else:
            com = self.comboBox_COMs.currentData(self.comboBox_COMs.currentIndex())
            baud = self.comboBox_baud.currentData(self.comboBox_baud.currentIndex())
            try:
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
                self.dataCollectionThread = DataCaptureThread(self.ser)
                self.dataCollectionThread.data_ok.connect(self.on_data_ready)
                self.dataCollectionThread.start()
    def on_data_ready(self, data):
        # self.textBrowser.append("{}\n".format(data))
        self.textBrowser.append(data)

    def btn_send_Clicked(self):
        try:
            self.ser.write(("{}\r\n".format(self.lineEdit.text())).encode('utf8'))
        except Exception as err:
            self.dialog = Message(self)
            self.dialog.textBrowser.setText("")
            self.dialog.textBrowser.append("<h2>error</h2>")
            self.dialog.textBrowser.append(str(err))
            self.dialog.show()
        else:
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
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()