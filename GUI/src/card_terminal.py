import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import serial
import struct

from Receiver import ReceiverThread

from_class = uic.loadUiType("GUI/ui/card_terminal.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("카드 단말기")

        # Ardino connect
        self.uid = bytes(4)
        self.conn = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)

        # Receiver init
        self.recv = ReceiverThread(self.conn)
        self.recv.start()
        # Recognize Tag
        self.recv.detected_signal.connect(self.detected)
        
        # Button connect
        self.button_init()
        self.disable()
        
        # Request Tag
        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.getStatus)
        self.timer.start()


    def button_init(self):
        self.resetButton.clicked.connect(self.reset)
        self.chargeButton.clicked.connect(self.charge)
        self.paymentButton.clicked.connect(self.payment)


    def send(self, command, data=0):
        print("send")
        req_data = struct.pack("<2s4sic", command, self.uid, data, b"\n")
        self.conn.write(req_data)
        return
    
    
    def getStatus(self):
        print("getStatus")
        self.send(b"GS")
        return
    
    def detected(self, uid):
        print("detected")
        self.uid = uid
        self.timer.stop()
        self.enable(0)
        return
    
    def getTotal(self):
        print("getTotal")
        self.send(b"GT")
        return
    
    
    def setTotal(self, total):
        print("setTotal")
        self.send(b"ST", total)
        return
    
    
    def reset(self):
        print("reset")
        return


    def charge(self):
        print("charge")
        return


    def payment(self):
        print("payment")
        return


    def enable(self, total):
        self.totalLabel.setText(str(total))
        self.chargeEdit.setDisabled(False)
        self.chargeButton.setDisabled(False)
        self.paymentEdit.setDisabled(False)
        self.paymentButton.setDisabled(False)


    def disable(self):
        self.totalLabel.setText("-")
        self.resetButton.setDisabled(True)
        self.chargeEdit.setDisabled(True)
        self.chargeButton.setDisabled(True)
        self.paymentEdit.setDisabled(True)
        self.paymentButton.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWindows = WindowClass()

    myWindows.show()

    sys.exit(app.exec_())
