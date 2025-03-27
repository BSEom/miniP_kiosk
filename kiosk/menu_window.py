from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5 import uic
import requests
from exPrice_window import expriceWindow
import cx_Oracle as oci

menu_form = uic.loadUiType("ui/menu.ui")[0]

sid = 'XE'
host = 'localhost' 
port = 1521
username = 'kiosk' 
password = '12345'

# 메뉴창
class menuWindow(QMainWindow, menu_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.loadData()

    def initUI(self):
        uic.loadUi('ui/menu.ui', self)
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('img/coffee-cup.png'))

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
        버튼에 이미지와 텍스트를 삽입 (3*n 동적 레이아웃)
        """
        # 기존 버튼 제거 및 동적 레이아웃 생성
        grid_layout = QGridLayout(self.scrollAreaWidgetContents)  # 스크롤 영역에 레이아웃 추가
        self.scrollAreaWidgetContents.setLayout(grid_layout)

        # 열 간격 설정
        grid_layout.setHorizontalSpacing(10)

        # 버튼 생성 및 추가
        buttons = []
        for i, (image_url, text) in enumerate(zip(popular_images, popular_texts)):
            button = QPushButton(self)
            buttons.append(button)

            # 버튼 크기 설정
            button.setFixedSize(200, 150)

            # 이미지 설정
            # response = requests.get(image_url)
            # if response.status_code == 200:
            #     pixmap = QPixmap()
            #     pixmap.loadFromData(response.content)
            #     resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #     button.setIcon(QIcon(resized_pixmap))
            #     button.setIconSize(QSize(100, 100))

            # 텍스트 설정
            button.setText(text)

            # 버튼을 그리드 레이아웃에 추가 (3열 기준)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(button, row, col)

            # 버튼 클릭 이벤트 연결
            button.clicked.connect(self.showExpriceWindow)

    def showExpriceWindow(self):
        """
        exPriceWindow 창을 표시
        """
        self.window_4 = expriceWindow()
        self.window_4.show()