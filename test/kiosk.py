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

# 시작화면
class mainWindow(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 팝업창 이름, 아이콘 설정
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon('D:\YEJ\code\miniP_Kiosk\coffee-cup.png'))

        # DB 연결 설정
        #sid = 'XE'
        ##host = '210.119.14.76'
        ##port = 1521
        #username = 'kiosk'
        #password = '12345'

        # DB 연결
        #conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        #cursor = conn.cursor()

        # 메뉴 데이터 가져오기
        #query = 'SELECT menu_id, menu_name, menu_price, category, image FROM MENU'
        #cursor.execute(query)

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

        # 인기기탭 메뉴 이미지 삽입=======================================
        popular_buttons = [
            self.popular1, self.popular2, self.popular3,
            self.popular4, self.popular5, self.popular6,
            self.popular7, self.popular8, self.popular9,
        ]

        popular_image = [
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg"
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        for button, image_path in zip(popular_buttons, popular_image):
            button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(100, 100))

        # 시즌탭 메뉴 이미지 삽입=======================================
        season_buttons = [
            self.season1, self.season2, self.season3,
            self.season4, self.season5, self.season6,
            self.season7, self.season8, self.season9
        ]

        season_image = [
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg"
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        for button, image_path in zip(season_buttons, season_image):
            button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(100, 100))
        

        # 커피탭 메뉴 이미지 삽입=======================================
        coffee_buttons = [
            self.coffee1, self.coffee2, self.coffee3,
            self.coffee4, self.coffee5, self.coffee6,
            self.coffee7, self.coffee8, self.coffee9
        ]

        coffee_image = [
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg"
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        for button, image_path in zip(coffee_buttons, coffee_image):
            button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(100, 100))

        # 논커피 메뉴 이미지 삽입=======================================
        n_coffee_buttons = [
            self.n_coffee1, self.n_coffee2, self.n_coffee3,
            self.n_coffee4, self.n_coffee5, self.n_coffee6,
            self.n_coffee7, self.n_coffee8, self.n_coffee9
        ]

        n_coffee_image = [
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg"
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        for button, image_path in zip(n_coffee_buttons, n_coffee_image):
            button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(100, 100))

        # 스무디 메뉴 이미지 삽입=======================================
        smoothie_buttons = [
            self.smoothie1, self.smoothie2, self.smoothie3,
            self.smoothie4, self.smoothie5, self.smoothie6,
            self.smoothie7, self.smoothie8, self.smoothie9
        ]

        smoothie_image = [
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg"
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        for button, image_path in zip(smoothie_buttons, smoothie_image):
            button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(100, 100))

        # 에이드 메뉴 이미지 삽입=======================================
        ade_buttons = [
            self.ade1, self.ade2, self.ade3,
            self.ade4, self.ade5, self.ade6,
            self.ade7, self.ade8, self.ade9
        ]

        ade_image = [
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg",
            "D:/YEJ/code/miniP_Kiosk/mainImage.jpg"
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        for button, image_path in zip(ade_buttons, ade_image):
            button.setIcon(QIcon(image_path))
            button.setIconSize(QSize(100, 100))
    

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
