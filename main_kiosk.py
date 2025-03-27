import cx_Oracle as oci
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

sid = 'XE'
host = '210.119.14.76'
port = 1521 
username = 'kiosk'
password = '12345'

# main_form = uic.loadUiType("./kiosk.ui")[0]
# menu_form = uic.loadUiType("./menu.ui")[0]
# manager_form = uic.loadUiType("./manager.ui")[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./kiosk.ui', self)
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('./coffee-cup.png'))

        # 시작버튼 클릭시 menuWindow 호출
        self.start_btn.clicked.connect(self.menuWindow)
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

# 사용자 메뉴창
class menuWindow(QMainWindow):
    def __init__(self):
        super(menuWindow, self).__init__()
        self.lst_menu = []  # DB에서 불러온 데이터를 저장할 리스트
        # self.page_size = 9  # 한 페이지에 표시할 개수 (3x3)
        # self.current_page = 0  # 현재 페이지 번호
        self.popular_image = []
        self.initUI()
        self.loadData()  # DB에서 데이터 로드

    def initUI(self):
        uic.loadUi('./menu.ui', self)
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('./coffee-cup.png'))

    def menuTable(self, popular_image):
        popular_buttons = [
            self.popular1, self.popular2, self.popular3,
            self.popular4, self.popular5, self.popular6,
            self.popular7, self.popular8, self.popular9,
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        # print(popular_image)
        for button, image_path in zip(popular_buttons, popular_image):
            print(image_path)
            button.setIcon(QIcon("https://ediya.com/files/menu/IMG_1647320805422.png"))
            # button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(100, 100))


    def loadData(self):
        # DB연결
        print("data로드완료")
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = 'SELECT menu_name, menu_info, menu_price, image FROM menu'
        cursor.execute(query)

        for v in cursor:
            self.popular_image.append(v[3])
        # print(self.popular_image)

        self.menuTable(self.popular_image) 

        cursor.close()
        conn.close()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()
