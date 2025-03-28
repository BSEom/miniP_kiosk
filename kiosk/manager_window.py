from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import uic

manager_form = uic.loadUiType("miniP_kiosk/ui/manager.ui")[0]

class managerWindow(QMainWindow, manager_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("miniP_kiosk/img/coffee-cup.png"))
