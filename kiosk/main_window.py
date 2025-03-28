from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from menu_window import menuWindow
from manager_window import managerWindow


main_form = uic.loadUiType("miniP_kiosk/ui/kiosk.ui")[0]

class mainWindow(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("miniP_kiosk/img/coffee-cup.png"))

        self.start_btn.clicked.connect(self.menuWindow)
        self.manager_btn.clicked.connect(self.managerWindow)
        self.show()

    def menuWindow(self):
        self.window_2 = menuWindow()
        self.window_2.show()

    def managerWindow(self):
        self.window_3 = managerWindow()
        self.window_3.show()

