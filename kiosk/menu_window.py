from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5 import uic
import requests
from exPrice_window import expriceWindow
import cx_Oracle as oci
import os

menu_form = uic.loadUiType("ui/menu.ui")[0]

sid = 'XE'
host = '210.119.14.76' 
# host = 'localhost'
port = 1521
username = 'kiosk' 
password = '12345'

# 메뉴창
class menuWindow(QMainWindow, menu_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        # self.loadCategoryData() # 카테고리 데이터 로드    -- 카테고리탭 추가중!!! 
        self.loadMenuData()     # 메뉴 데이터 로드

    def initUI(self):
        # uic.loadUi('ui/menu.ui', self)
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('img/coffee-cup.png'))

    # 메뉴 데이터 로드
    def loadMenuData(self):     # loadData() -> loadMenuData() 변경     -- 이거 이름 바꿈!!!! 확인 부탁!!!
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

    # 메뉴 테이블 생성
    def menuTable(self, popular_images, popular_texts):
        grid_layout = QGridLayout(self.scrollAreaWidgetContents)  
        self.scrollAreaWidgetContents.setLayout(grid_layout)
        grid_layout.setHorizontalSpacing(1)
        grid_layout.setVerticalSpacing(1)
        grid_layout.setContentsMargins(0, 0, 0, 0)  

        for i, (image_filename, text) in enumerate(zip(popular_images, popular_texts)):
            menu_item = self.createMenuWidget(image_filename, text)

            row = i // 3
            col = i % 3
            grid_layout.addWidget(menu_item, row, col)

    # 메뉴 위젯 생성(이미지 버튼, 텍스트)
    def createMenuWidget(self, image_filename, text):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(base_dir, "../images/")  
        image_path = os.path.join(image_folder, image_filename)
        image_path = os.path.normpath(image_path)

        # 위젯 생성
        menu_item = QWidget()
        layout = QVBoxLayout(menu_item)
        layout.setAlignment(Qt.AlignCenter)  # 중앙 정렬 추가

        # 버튼 생성
        button = QPushButton()
        button.setFixedSize(95, 95)
        pixmap = QPixmap(os.path.join(image_folder, image_filename))

        # 이미지 로드
        # pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            button.setIcon(QIcon(resized_pixmap))
            button.setIconSize(QSize(80, 80))
        else:
            print(f"이미지 로드 실패: {image_path}")

        # 메뉴명 추가
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setFixedWidth(95)
        label.setFixedHeight(40)

        # 레이아웃 추가
        layout.addWidget(button)
        layout.addWidget(label)

        # 클릭 이벤트 연결
        button.clicked.connect(self.showExpriceWindow)

        return menu_item

    # 메뉴설명창으로 이동
    def showExpriceWindow(self):
        self.window_4 = expriceWindow()
        self.window_4.show()