from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import cx_Oracle as oci

expPrice_form = uic.loadUiType("ui/exp_price.ui")[0]

# DB 연결 정보
sid = 'XE'
host = '210.119.14.76'
port = 1521
username = 'kiosk'
password = '12345'

class expriceWindow(QMainWindow, expPrice_form):
    def __init__(self, menu_id):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cafe Kiosk")
        self.setWindowIcon(QIcon("img/coffee-cup.png"))

        self.loadData(menu_id)

    def loadData(self, menu_id):
        """
        데이터베이스에서 menu_id에 해당하는 메뉴 데이터를 가져와 UI에 표시
        """
        # DB 연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        # menu_id에 해당하는 메뉴 데이터 가져오기
        query = '''
            SELECT menu_name, menu_info, menu_price, category, image
            FROM MENU
            WHERE menu_id = :menu_id
        '''
        cursor.execute(query, {'menu_id': menu_id})

        # 데이터 가져오기
        row = cursor.fetchone()
        if row:
            menu_name, menu_info, menu_price, category, image = row

            # QLabel에 데이터 설정
            self.menu_name.setText(menu_name)  # 메뉴 이름 설정
            self.exp_label.setText(menu_info)  # 메뉴 설명 설정
            self.price_label.setText(f"가격: {menu_price}원")  # 가격 설정
            self.exp_label.setWordWrap(True)  # 텍스트 줄바꿈 활성화

        else:
            print(f"menu_id {menu_id}에 해당하는 데이터를 찾을 수 없습니다.")

        # DB 연결 닫기
        cursor.close()
        conn.close()