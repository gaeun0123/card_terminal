import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *

class ReceiverThread(QThread):
    # Recognize Tag Signal
    detected_signal = pyqtSignal(bytes)
    
    def __init__(self, conn, parent=None):
        super(ReceiverThread, self).__init__(parent)
        self.is_running = False
        self.conn = conn
        print("Reciver Thread init")
        
    
    def run(self):
        print("Reciver started")
        self.is_running = True
        while (self.is_running == True):
            if self.conn.readable():
                res = self.conn.read_until(b'\n')
                if len(res) > 0:
                    res = res[:-2]
                    cmd = res[:2].decode()
                    if cmd == "GS" and res[2] == 0:
                        print("Receiver detected")
                        self.detected_signal.emit(res[3:])
                    else:
                        print("Unknown error")
                        print(cmd)
          
                    
    def stop(self):
        print("Receiver stoped")
        self.is_running = False
        