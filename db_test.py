# Kiosk ui
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, uic
import cx_Oracle as oci
from PyQt5.QtCore import Qt, QSize


main_form = uic.loadUiType("D:\YEJ\code\miniP_Kiosk\kiosk.ui")[0]
menu_form = uic.loadUiType("D:\YEJ\code\miniP_Kiosk\menu.ui")[0]
manager_form = uic.loadUiType("D:\YEJ\code\miniP_Kiosk\manager.ui")[0]

# DB 연결 설정
sid = 'XE'
host = '210.119.14.76'
port = 1521
username = 'kiosk'
password = '12345'

# 시작화면
class mainWindow(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 팝업창 이름, 아이콘 설정
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon('D:\YEJ\code\miniP_Kiosk\coffee-cup.png'))

        # 버튼 클릭 시 menuWindow 호출
        self.start_btn.clicked.connect(self.menuWindow)
        self.show()

        # 버튼 클릭 시 managerWindow 호출
        self.manager_btn.clicked.connect(self.managerWindow)
        self.show()

    def initUI(self):
        self.setWindowTitle("Cafe Kiosk")
        self.resize(800, 600)
        self.center()
        self.show()

    
    # 창 화면 가운데 정렬
    def center(self):
        qr = self.frameGeometry()   
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def menuWindow(self):
        self.window_2 = menuWindow() 
        self.window_2.show()

    def managerWindow(self):
        self.window_3 = managerWindow()
        self.window_3.show()
       
# 메뉴 화면
class menuWindow(QMainWindow, menu_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon('D:\YEJ\code\miniP_Kiosk\coffee-cup.png'))

        # 데이터베이스 연결
        db = DatabaseManager()
        db.connect()

        # 메뉴 데이터 가져오기
        menu_data = db.fetch_menu_data()

        # 카테고리별 버튼 리스트
        buttons = {
            "popular": [
                self.popular1, self.popular2, self.popular3,
                self.popular4, self.popular5, self.popular6,
                self.popular7, self.popular8, self.popular9
            ],
            "season": [
                self.season1, self.season2, self.season3,
                self.season4, self.season5, self.season6,
                self.season7, self.season8, self.season9
            ],
            # 다른 카테고리도 추가 가능
        }

        # 버튼에 데이터 설정
        for menu_id, menu_name, menu_price, category, image in menu_data:
            if category in buttons:
                button_list = buttons[category]
                if menu_id <= len(button_list):  # 버튼이 존재하는 경우
                    button = button_list[menu_id - 1]
                    button.setText(menu_name)  # 버튼 텍스트 설정
                    button.setIcon(QIcon(image))  # 버튼 아이콘 설정
                    button.setIconSize(QSize(100, 100))  # 아이콘 크기 설정

        # 데이터베이스 연결 종료
        db.disconnect()


        

    

# 관리자 화면
class managerWindow(QMainWindow, manager_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon('D:\YEJ\code\miniP_Kiosk\coffee-cup.png'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = mainWindow()
    app.exec_()
