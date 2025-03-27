from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import uic

expPrice_form = uic.loadUiType("ui/exp_price.ui")[0]

import cx_Oracle as oci

# DB연결
sid = 'XE'
# host = '210.119.14.76' 
host = 'localhost'
port = 1521
username = 'kiosk' 
password = '12345'

class expriceWindow(QMainWindow, expPrice_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img/coffee-cup.png"))

    def loadData(self):
        # db연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = 'SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU' 
        cursor.execute(query)

        label_text = ""

        for i, row in enumerate(cursor, start=1):
            menu_id, menu_name, menu_info, menu_price, category, image = row
    
            # 각 컬럼을 따로 변수로 사용
            label_text += f"메뉴ID: {menu_id}/n"
            label_text += f"메뉴명: {menu_name}/n"
            label_text += f"메뉴설명: {menu_info}/n"
            label_text += f"가격: {menu_price}/n"
            label_text += f"카테고리: {category}/n"
            label_text += f"이미지경로(또는 URL): {image}/n"
            label_text += "-" * 40 + "/n"  # 구분선 추가

        self.explain_label.setText(label_text)
        self.explain_label.setWordWrap(True)  # 텍스트 줄바꿈 설정


        cursor.close()
        conn.close()
    