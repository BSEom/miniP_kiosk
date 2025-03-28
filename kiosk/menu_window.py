from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5 import uic
import cx_Oracle as oci
import os
from exPrice_window import expriceWindow

menu_form = uic.loadUiType("ui/menu.ui")[0]

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
            menu_item = self.createMenuWidget(menu_id, image_filename, menu_name)

            # 버튼을 그리드 레이아웃에 추가 (3열 기준)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(menu_item, row, col)

    def createMenuWidget(self, menu_id, image_filename, text):
        """
        메뉴 위젯 생성 (이미지 버튼, 텍스트)
        """
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
        pixmap = QPixmap(image_path)

        # 이미지 로드
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
        button.clicked.connect(lambda _, mid=menu_id: self.showExpriceWindow(mid))

        return menu_item

    def showExpriceWindow(self, menu_id):
        """
        exPriceWindow 창을 열고 menu_id를 전달
        """
        self.window_4 = expriceWindow(menu_id=menu_id)
        self.window_4.show()