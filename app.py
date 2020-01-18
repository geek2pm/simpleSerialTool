#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication
import sys,time
import serial
import serial.tools.list_ports

TITLE = 'simple Serial Tool'

qtCreatorFile = "ui/main.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile = "ui/message.ui" # Enter file here.
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

def center_on_screen(self,QtWidgets):
    resolution = QtWidgets.QDesktopWidget().screenGeometry()
    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),(resolution.height() / 2) - (self.frameSize().height() / 2))

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

class GetCOMsThread(QtCore.QThread):
    data = QtCore.pyqtSignal(object)
    last = None
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        ports = serial.tools.list_ports.comports()
        if ports != self.last:
            self.data.emit(ports)
            self.last = ports
        # QtCore.QThread.sleep(1)
        time.sleep(1)
        self.run()

class Message(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(Message, self).__init__(parent)
        self.setupUi(self)
        center_on_screen(self,QtWidgets)

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        center_on_screen(self,QtWidgets)
        self.btn_open.clicked.connect(self.btn_open_Clicked)
        self.btn_send.clicked.connect(self.btn_send_Clicked)
        self.btn_clear.clicked.connect(self.btn_clear_Clicked)
        self.btn_about.clicked.connect(self.btn_about_Clicked)
        self.getCOMs()

    def btn_open_Clicked(self):

        if self.btn_open.text() == 'close':
            self.btn_open.setText('open')
            self.setWindowTitle("{} ({})".format(TITLE,"closed"))
            self.ser=None
            self.btn_send.setEnabled(False)
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
                self.btn_open.setText('close')
                self.setWindowTitle("{} ({})".format(TITLE,"opened"))
                self.dataCollectionThread = DataCaptureThread(self.ser)
                self.dataCollectionThread.data_ok.connect(self.on_data_ready)
                self.dataCollectionThread.start()
                self.btn_send.setEnabled(True)
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
            self.dialog.textBrowser.setOpenLinks(True)
            self.dialog.textBrowser.setOpenExternalLinks(True)
            self.dialog.textBrowser.append(str(err))
            self.dialog.show()
        else:
            self.lineEdit.setText("")

    def btn_clear_Clicked(self):
        self.textBrowser.setText("")
    
    def btn_about_Clicked(self):
        self.dialog = Message(self)
        self.dialog.textBrowser.setText("")
        self.dialog.textBrowser.append("<h2>about</h2>")
        link = "<a target='_blank' href='https://github.com/geek2pm/simpleSerialTool'>https://github.com/geek2pm/simpleSerialTool</a>"
        self.dialog.textBrowser.append(link)
        self.dialog.textBrowser.setOpenExternalLinks(True)
        self.dialog.show()

    def getCOMs(self):
        self.getCOMsThread = GetCOMsThread()
        self.getCOMsThread.data.connect(self.on_data_coms)
        self.getCOMsThread.start()
    
    def on_data_coms(self, ports):
        if len(ports)>0:
            self.btn_open.setEnabled(True)
            self.btn_clear.setEnabled(True)
            self.comboBox_COMs.clear()
            for port, desc, hwid in sorted(ports):
                print("{}: {} [{}]".format(port, desc, hwid))
                self.comboBox_COMs.addItem(port)
            self.btn_open.setText('open')
            self.setWindowTitle("{} ({})".format(TITLE,"ready to open"))
        else:
            self.btn_open.setEnabled(False)
            self.btn_send.setEnabled(False)
            self.btn_clear.setEnabled(False)
            self.btn_open.setText('open')
            self.setWindowTitle("{} ({})".format(TITLE,"no device found"))
def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()