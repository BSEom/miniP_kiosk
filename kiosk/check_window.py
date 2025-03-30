from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from manager_window import managerWindow

pwd_data = 'root1234'

check_form = uic.loadUiType("ui\check.ui")[0]

class checkWindow(QDialog, check_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img\coffee-cup.png"))

        self.check_btn.clicked.connect(self.check_btnClick)


    def check_btnClick(self):
        m_pwd = self.input_pwd.text()

        if m_pwd == pwd_data:
            self.managerWindow()
            self.close()
        else:
            QMessageBox.warning(self, '경고', '비밀번호가 다릅니다!')
            return
        
        
    def managerWindow(self):
            self.window_3 = managerWindow()
            self.window_3.show()