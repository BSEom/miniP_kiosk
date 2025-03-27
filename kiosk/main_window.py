from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from menu_window import menuWindow
from manager_window import managerWindow

main_form = uic.loadUiType("D:/project/miniP_kiosk/ui/kiosk.ui")[0]

# 시작, 관리자 선택창
class mainWindow(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img/coffee-cup.png"))

        self.start_btn.clicked.connect(self.menuWindow)         # 시작버튼 클릭
        self.manager_btn.clicked.connect(self.managerWindow)    # 관리자버튼 클릭
        self.show()

    # 메뉴창으로 이동
    def menuWindow(self):
        self.window_2 = menuWindow()
        self.window_2.show()
    
    # 관리자창으로 이동
    def managerWindow(self):
        self.window_3 = managerWindow()
        self.window_3.show()

