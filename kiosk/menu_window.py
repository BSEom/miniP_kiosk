from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5 import uic
import requests
from exPrice_window import expriceWindow
import cx_Oracle as oci

menu_form = uic.loadUiType("ui\menu.ui")[0]

sid = 'XE'
host = '127.0.0.1' 
port = 1521
username = 'kiosk' 
password = '12345'

class menuWindow(QMainWindow, menu_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.loadData()

    def initUI(self):
        uic.loadUi('ui\menu.ui', self)
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('./coffee-cup.png'))

    def loadData(self):
        """
        데이터베이스에서 메뉴 데이터를 불러와 menuTable에 전달
        """
        # DB 연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = 'SELECT menu_name, menu_info, menu_price, image FROM menu'
        cursor.execute(query)

        # popular_images와 popular_texts 리스트 생성
        popular_images = []
        popular_texts = []
        for row in cursor:
            popular_texts.append(row[0])  # 메뉴 이름 추가
            popular_images.append(row[3])  # 이미지 URL 또는 경로 추가

        cursor.close()
        conn.close()

        # menuTable 함수 호출
        self.menuTable(popular_images, popular_texts)

    def menuTable(self, popular_images, popular_texts):
        """
        버튼에 이미지와 텍스트를 삽입
        """
        # 3x3 버튼 목록
        popular_buttons = [
            self.popular1, self.popular2, self.popular3,
            self.popular4, self.popular5, self.popular6,
            self.popular7, self.popular8, self.popular9
        ]

        # 버튼에 이미지 및 텍스트 삽입
        for button, image_url, text in zip(popular_buttons, popular_images, popular_texts):
            response = requests.get(image_url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                button.setIcon(QIcon(resized_pixmap))
                button.setIconSize(QSize(100, 100))
            button.setText(text)  # 버튼에 텍스트 설정

        # 버튼 클릭 이벤트 연결
        for button in popular_buttons:
            button.clicked.connect(self.showExpriceWindow)

    def showExpriceWindow(self):
        """
        exPriceWindow 창을 표시
        """
        self.window_4 = expriceWindow()
        self.window_4.show()