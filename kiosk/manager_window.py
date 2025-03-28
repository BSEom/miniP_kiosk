import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QStackedWidget
from PyQt5.uic import loadUi
import cx_Oracle as oci
from PyQt5.QtCore import Qt


# DB 연결 함수
def get_db_connection():
    sid = 'XE'
    host = 'localhost'
    port = 1521
    username = 'kiosk'
    password = '12345'
    return oci.connect(f'{username}/{password}@{host}:{port}/{sid}')


class ManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/manager.ui", self)  # Qt Designer UI 로드

        # DB 연결
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # 버튼 이벤트 연결
        self.mbtn_check.clicked.connect(self.check_menu)
        self.mbtn_add.clicked.connect(self.add_menu)
        self.mbtn_mod.clicked.connect(self.update_menu)
        self.mbtn_del.clicked.connect(self.delete_menu)

        # 더블 클릭 시 상태 페이지(tblMenu2)로 이동하기 위한 코드
        self.tblMenu.doubleClicked.connect(self.double_click_event)

        # 초기 메뉴 데이터 로드
        self.load_menu_data()

        # QStackedWidget 설정
        self.stackedWidget.setCurrentIndex(0)  # 기본 페이지를 조회 페이지로 설정

        # 상태 페이지의 수정, 추가, 삭제 버튼 비활성화 (초기 설정)
        self.disable_edit_buttons()

    # 메뉴 데이터 로딩
    def load_menu_data(self, category=None):
        query = "SELECT menu_id, menu_name, menu_info, menu_price, category FROM MENU"  # 카테고리 포함
        if category:  # 카테고리 선택했을 때
            query += " WHERE category = :1"
            self.cursor.execute(query, (category,))
        else:  # 선택하지 않은 경우 모든 메뉴 조회
            self.cursor.execute(query)

        rows = self.cursor.fetchall()

        if not rows:
            print("No data found in database.")
        else:
            print(f"Fetched {len(rows)} rows from the database.")  # 데이터 확인

        self.tblMenu.setRowCount(len(rows))  # 행 수 설정
        self.tblMenu.setColumnCount(5)  # 열 수 설정 (5개 컬럼: menu_id, menu_name, menu_info, menu_price, category)
        self.tblMenu.setHorizontalHeaderLabels(["ID", "Name", "Info", "Price", "Category"])  # 열 헤더 설정

        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)  # 편집 방지
                self.tblMenu.setItem(i, j, table_item)  # 각 셀에 데이터 넣기

    # 메뉴 조회
    def check_menu(self):
        category = self.category_combobox.currentText()  # 카테고리 선택
        self.load_menu_data(category)  # 선택된 카테고리에 맞는 메뉴 로드

    # 메뉴 추가
    def add_menu(self):
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.text()
        menu_price = self.menu_price_input.text()
        category = self.menu_category_input.text()
        image_url = self.menu_image_input.text()

        if menu_name and menu_info and menu_price and category and image_url:
            self.add_menu_item(menu_name, menu_info, menu_price, category, image_url)
            self.conn.commit()
            self.load_menu_data()

    # 메뉴 추가 - 내부 함수
    def add_menu_item(self, menu_name, menu_info, menu_price, category, image_url):
        self.cursor.execute(
            """
            INSERT INTO MENU (menu_name, menu_info, menu_price, category, image)
            VALUES (:1, :2, :3, :4, :5)
            """, (menu_name, menu_info, menu_price, category, image_url))

    # 메뉴 수정
    def update_menu(self):
        selected_row = self.tblMenu2.currentRow()  # 수정은 tblMenu2에서만
        if selected_row >= 0:
            menu_id = self.tblMenu2.item(selected_row, 0).text()  # tblMenu2에서 선택된 값
            menu_name = self.menu_name_input.text()
            menu_info = self.menu_info_input.text()
            menu_price = self.menu_price_input.text()
            category = self.menu_category_input.text()
            image_url = self.menu_image_input.text()

            self.update_menu_item(menu_id, menu_name, menu_info, menu_price, category, image_url)
            self.conn.commit()
            self.load_menu_data()

    # 메뉴 수정 - 내부 함수
    def update_menu_item(self, menu_id, menu_name, menu_info, menu_price, category, image_url):
        self.cursor.execute(""" 
            UPDATE MENU
            SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
            WHERE menu_id = :6
        """, (menu_name, menu_info, menu_price, category, image_url, menu_id))

    # 메뉴 삭제
    def delete_menu(self):
        selected_row = self.tblMenu2.currentRow()  # 삭제는 tblMenu2에서만
        if selected_row >= 0:
            menu_id = self.tblMenu2.item(selected_row, 0).text()  # tblMenu2에서 선택된 값
            self.delete_menu_item(menu_id)
            self.conn.commit()
            self.load_menu_data()

    # 메뉴 삭제 - 내부 함수
    def delete_menu_item(self, menu_id):
        self.cursor.execute("DELETE FROM MENU WHERE menu_id = :1", (menu_id,))

    # 조회 페이지에서 더블 클릭했을 때 상태 페이지로 이동
    def double_click_event(self):
        print("더블 클릭 이벤트 발생")  # 디버깅용 로그 추가
        selected_row = self.tblMenu.currentRow()
        if selected_row >= 0:
            # 상태 페이지로 이동 (여기서만 수정, 삭제 가능)
            print("상태 페이지로 이동")  # 디버깅용 로그 추가
            self.stackedWidget.setCurrentIndex(1)  # 1은 상태 페이지가 위치한 인덱스 번호로 설정 (필요한 인덱스로 수정)

            # 상태 페이지(tblMenu2)로 데이터 전달
            self.tblMenu2.setRowCount(1)  # 상태 페이지에 한 행만 설정 (필요시 수정 가능)
            for col in range(self.tblMenu.columnCount()):
                item = self.tblMenu.item(selected_row, col)
                print(f"Setting tblMenu2[{0}, {col}] with {item.text() if item else ''}")  # 디버깅용 로그 추가
                self.tblMenu2.setItem(0, col, QTableWidgetItem(item.text() if item else ""))

            # 상태 페이지에서만 수정, 삭제 가능하도록 설정
            self.enable_edit_buttons()

    # 상태 페이지에서만 수정, 삭제, 추가 버튼 활성화
    def enable_edit_buttons(self):
        self.mbtn_add.setEnabled(True)
        self.mbtn_mod.setEnabled(True)
        self.mbtn_del.setEnabled(True)

    # 상태 페이지에서만 수정, 삭제, 추가 버튼 비활성화
    def disable_edit_buttons(self):
        self.mbtn_add.setEnabled(False)
        self.mbtn_mod.setEnabled(False)
        self.mbtn_del.setEnabled(False)

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManagerWindow()
    window.show()
    sys.exit(app.exec_())
