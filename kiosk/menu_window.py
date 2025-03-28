from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5 import uic
import os
import cx_Oracle as oci
from exPrice_window import expriceWindow

menu_form = uic.loadUiType("miniP_kiosk/ui/menu.ui")[0]

# DB 연결 정보
sid = 'XE'
host = '210.119.14.76'
port = 1521
username = 'kiosk'
password = '12345'

class menuWindow(QMainWindow, menu_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.loadMenuData()

    def initUI(self):
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('img/coffee-cup.png'))

    def loadMenuData(self):
        """
        데이터베이스에서 메뉴 데이터를 가져와 동적으로 버튼 생성
        """
        # DB 연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        # 메뉴 데이터 가져오기
        query = 'SELECT menu_id, menu_name, menu_info, menu_price, image FROM menu'
        cursor.execute(query)

        # 메뉴 데이터를 저장할 리스트
        menu_data = cursor.fetchall()

        # DB 연결 닫기
        cursor.close()
        conn.close()

        # menuTable 함수 호출
        self.menuTable(menu_data)

    def menuTable(self, menu_data):
        """
        동적으로 버튼 생성 및 클릭 이벤트 연결
        """
        # 이미지가 저장된 폴더 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(base_dir, "../images/")  # 이미지 폴더 상대 경로

        # 기존 버튼 제거 및 동적 레이아웃 생성
        grid_layout = QGridLayout(self.scrollAreaWidgetContents)  # 스크롤 영역에 레이아웃 추가
        self.scrollAreaWidgetContents.setLayout(grid_layout)

        # 열 간격 설정
        grid_layout.setHorizontalSpacing(10)

        # 버튼 생성 및 추가
        for i, (menu_id, menu_name, menu_info, menu_price, image_filename) in enumerate(menu_data):
            button = QPushButton(self)

            # 버튼 크기 설정
            button.setFixedSize(200, 150)

            # 이미지 경로 조합
            image_path = os.path.join(image_folder, image_filename)
            image_path = os.path.normpath(image_path)  # OS에 맞게 경로 변환

            # 이미지 설정
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                resized_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                button.setIcon(QIcon(resized_pixmap))
                button.setIconSize(QSize(100, 100))
            else:
                print(f"이미지 로드 실패: {image_path}")

            # 텍스트 설정
            button.setText(menu_name)

            # 버튼을 그리드 레이아웃에 추가 (3열 기준)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(button, row, col)

            # 메뉴 버튼 클릭 > 설명창 띄움
            button.clicked.connect(lambda _, mid=menu_id: self.showExpriceWindow(mid))

    def showExpriceWindow(self, menu_id):
        """
        exPriceWindow 창을 열고 menu_id를 전달
        """
        self.window_4 = expriceWindow(menu_id=menu_id)
        self.window_4.show()