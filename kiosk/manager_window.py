from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import uic

manager_form = uic.loadUiType("D:/project/miniP_kiosk/ui/manager.ui")[0]

# 관리자창
class managerWindow(QMainWindow, manager_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("D:/project/miniP_kiosk/img/coffee-cup.png"))
