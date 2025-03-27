# Kiosk ui
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, uic
import cx_Oracle as oci
from PyQt5.QtCore import Qt, QSize
import requests
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from io import BytesIO

main_form = uic.loadUiType("D:\YEJ\code\miniP_Kiosk\kiosk.ui")[0]
menu_form = uic.loadUiType("D:\YEJ\code\miniP_Kiosk\menu.ui")[0]
manager_form = uic.loadUiType("D:\YEJ\code\miniP_Kiosk\manager.ui")[0]
expPrice_form = uic.loadUiType("D:\YEJ\code\miniP_Kiosk\exp_price.ui")[0]

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
    def expriceWindow(self):
        self.window_4 = expriceWindow()
        self.window_4.show()

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon('D:\YEJ\code\miniP_Kiosk\coffee-cup.png'))

        # 인기탭 메뉴 이미지 삽입
        popular_buttons = [
            self.popular1, self.popular2, self.popular3,
            self.popular4, self.popular5, self.popular6,
            self.popular7, self.popular8, self.popular9,
        ]

        popular_image = [
            "https://ediya.com/files/menu/IMG_1660608743501.png",
            "https://ediya.com/files/menu/IMG_1647324593188.png",
            "https://ediya.com/files/menu/IMG_1647321941152.png",
            "https://ediya.com/files/menu/IMG_1730080275823.png",
            "https://ediya.com/files/menu/IMG_1709599391117.png",
            "https://ediya.com/files/menu/IMG_1737089595532.png",
            "https://ediya.com/files/menu/IMG_1721112356312.png",
            "https://ediya.com/files/menu/IMG_1721117534865.png",
            "https://ediya.com/files/menu/IMG_1742279746779.png"
        ]

        # 반복문으로 버튼에 아이콘과 크기 설정
        for button, image_url in zip(popular_buttons, popular_image):
            try:
                # URL에서 이미지 다운로드
                response = requests.get(image_url)
                if response.status_code == 200:
                    # 이미지를 QPixmap으로 로드
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    
                    # 이미지 크기 조정
                    resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    # 버튼에 아이콘 설정
                    button.setIcon(QIcon(resized_pixmap))
                    button.setIconSize(QSize(100, 100))
                else:
                    print(f"이미지를 다운로드할 수 없습니다: {image_url}")
            except Exception as e:
                print(f"이미지 로드 중 오류 발생: {e}")
        
        # popular1 버튼 클릭 시 설명 창 띄우기
        self.popular1.clicked.connect(self.expriceWindow)
        self.show()
        

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


# 메뉴 설명 화면
class expriceWindow(QMainWindow, expPrice_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon('D:\YEJ\code\miniP_Kiosk\coffee-cup.png'))

    # 메뉴 설명 창 내용 
    def updateContent(self, name,description,price):
        self.menu_name_label.setText(name)  # 메뉴 이름 표시
        self.menu_description_label.setText(description)  # 메뉴 설명 표시
        self.menu_price_label.setText(f"가격: {price}원")  # 메뉴 가격 표시

   
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
