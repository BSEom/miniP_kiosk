from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton
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

    def menuTable(self, popular_images, popular_texts):
        # 이미지가 저장된 폴더 경로 설정 (현재 실행 파일 기준)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(base_dir, "../images/")  # 이미지 폴더 상대 경로
        
        # 기존 버튼 제거 및 동적 레이아웃 생성
        grid_layout = QGridLayout(self.scrollAreaWidgetContents)  # 스크롤 영역에 레이아웃 추가
        self.scrollAreaWidgetContents.setLayout(grid_layout)

        # 열 간격 설정
        grid_layout.setHorizontalSpacing(10)

        # 버튼 생성 및 추가
        buttons = []
        for i, (image_filename, text) in enumerate(zip(popular_images, popular_texts)):
            button = QPushButton(self)
            # buttons.append(button)

            # 버튼 크기 설정
            button.setFixedSize(200, 150)
            
            # 이미지 경로 조합 (파일명이 저장된 경우)
            image_path = os.path.join(image_folder, image_filename)
            image_path = os.path.normpath(image_path)  # OS에 맞게 경로 변환
            image_path = image_path.replace('\\', '/')
            
            # 이미지 설정 (로컬 이미지 파일 사용)
            pixmap = QPixmap(image_path)

            if not pixmap.isNull():  # 이미지가 정상적으로 로드되었을 경우
                resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                button.setIcon(QIcon(resized_pixmap))
                button.setIconSize(QSize(100, 100))
            else:
                print(f"이미지 로드 실패: {image_path}")  # 경로 오류 시 로그 출력

            # 텍스트 설정
            button.setText(text)

            # 버튼을 그리드 레이아웃에 추가 (3열 기준)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(button, row, col)

            # 메뉴 버튼 클릭 > 설명창 띄움
            button.clicked.connect(self.showExpriceWindow)

    def showExpriceWindow(self):
        self.window_4 = expriceWindow()
        self.window_4.show()