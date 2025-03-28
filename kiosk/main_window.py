from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from menu_window import menuWindow
from check_window import checkWindow


main_form = uic.loadUiType("ui\kiosk.ui")[0]

class mainWindow(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img\coffee-cup.png"))

        self.start_btn.clicked.connect(self.menuWindow)
        self.manager_btn.clicked.connect(self.checkWindow)
        self.show()

    def menuWindow(self):
        self.window_2 = menuWindow()
        self.window_2.show()

    def checkWindow(self):
        self.window_4 = checkWindow()
        self.window_4.show()

