from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QWidget, QVBoxLayout, QLabel, QTabWidget
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

# 메뉴 목록을 보여주는 창
class menuWindow(QMainWindow, menu_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.loadCategories()
        # self.loadMenuData()   # 카테고리 로드한 후에 카테고리별로 실행해야돼서 뺐음

    def initUI(self):
        self.setWindowTitle('Cafe Kiosk')
        self.setWindowIcon(QIcon('img/coffee-cup.png'))
    
    # 카테고리 목록을 DB에서 가져와서 탭 동적 생성
    def loadCategories(self):
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = 'SELECT DISTINCT category FROM menu'    # 카테고리 중복 제거
        cursor.execute(query)
        categories = [row[0] for row in cursor]  # 카테고리 목록

        cursor.close()
        conn.close()

        # 각 카테고리에 대한 탭 추가
        for category in categories:
            self.addCategoryTab(category)

    # 카테고리 탭 추가하고 카테고리별로 메뉴를 DB에서 가져와서 버튼 동적 생성
    # 이 부분에 뭘 잘 수정하면 ui틀 유지하면서 스크롤 기능 들어갈 것 같은데... ㅠ -정민
    def addCategoryTab(self, category):
        tab = QWidget()
        layout = QGridLayout(tab)
        tab.setLayout(layout)

        # 탭을 tabWidget에 추가
        self.tabWidget.addTab(tab, category)

        # 카테고리별로 메뉴 불러오기
        self.loadMenuData(category, layout)

    # 카테고리별 메뉴를 DB에서 가져와서 버튼 동적 생성
    def loadMenuData(self, category, layout):
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = 'SELECT menu_id, menu_name, image FROM menu WHERE category = :category'
        cursor.execute(query, {'category': category})

        # 메뉴 데이터를 저장할 리스트
        menu_data = cursor.fetchall()

        cursor.close()
        conn.close()

        # 메뉴 테이블 생성
        self.menuTable(menu_data, layout)
        
        # 이 아래 코드는 일단 지우지말아주세요... -정민
        # for i, (menu_id, menu_name, image_filename) in enumerate(menu_data):
        #     menu_item = self.createMenuWidget(menu_id, image_filename, menu_name)
        #     row, col = divmod(i, 3)  # 3열 기준 배치
        #     layout.addWidget(menu_item, row, col)

    # 메뉴 테이블 생성
    def menuTable(self, menu_data, layout):
        # 기존 버튼 제거 및 동적 레이아웃 생성
        grid_layout = QGridLayout(self.scrollAreaWidgetContents)  # 스크롤 영역에 레이아웃 추가
        self.scrollAreaWidgetContents.setLayout(grid_layout)
        grid_layout.setHorizontalSpacing(1)
        grid_layout.setContentsMargins(0, 0, 0, 0)  

        # 버튼 생성 및 추가
        for i, (menu_id, menu_name, image_filename) in enumerate(menu_data):
            menu_item = self.createMenuWidget(menu_id, image_filename, menu_name)
            layout.addWidget(menu_item, i // 3, i % 3)

    def createMenuWidget(self, menu_id, image_filename, text):
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
        label.setFixedSize(95, 40)

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