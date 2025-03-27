import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
import cx_Oracle as oci

# DB 연결 함수
def get_db_connection():
    sid = 'XE'
    host = 'localhost'
    port = 1521
    username = 'kiosk'
    password = '12345'
    conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
    return conn

# 메뉴 데이터 로딩 함수
def load_menu_data(cursor, table_widget, category=None):
    if category:
        query = "SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU WHERE category = :1"
        cursor.execute(query, (category,))
    else:
        query = "SELECT menu_id, menu_name, menu_info, menu_price, category, image FROM MENU"
        cursor.execute(query)
    
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, item in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(item)))

# PyQt5 UI 설정 및 기능 구현
class ManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # UI 파일 로드
        uic.loadUi('manager_window.ui', self)

        # DB 연결
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # 메뉴 데이터 로딩
        load_menu_data(self.cursor, self.tblmenu)

        # 카테고리 선택 및 조회 버튼 기능 설정
        self.btn_check.clicked.connect(self.check_menu)

        # 버튼 기능 설정
        self.add_button.clicked.connect(self.add_menu)
        self.update_button.clicked.connect(self.update_menu)
        self.delete_button.clicked.connect(self.delete_menu)

        # 더블 클릭 시 상태 페이지로 이동
        self.tblmenu.doubleClicked.connect(self.double_click_event)

    def check_menu(self):
        category = self.category_combobox.currentText()
        if category == "All":
            load_menu_data(self.cursor, self.tblmenu)
        else:
            load_menu_data(self.cursor, self.tblmenu, category)

    def add_menu(self):
        menu_name = self.menu_name_input.text()
        menu_info = self.menu_info_input.text()
        menu_price = self.menu_price_input.text()
        category = self.menu_category_input.text()
        image_url = self.menu_image_input.text()

        if menu_name and menu_info and menu_price and category and image_url:
            insert_query = """
                INSERT INTO MENU (menu_name, menu_info, menu_price, category, image)
                VALUES (:1, :2, :3, :4, :5)
            """
            self.cursor.execute(insert_query, (menu_name, menu_info, menu_price, category, image_url))
            self.conn.commit()
            load_menu_data(self.cursor, self.tblmenu)

    def update_menu(self):
        selected_row = self.tblmenu.currentRow()
        if selected_row >= 0:
            menu_id = self.tblmenu.item(selected_row, 0).text()
            menu_name = self.menu_name_input.text()
            menu_info = self.menu_info_input.text()
            menu_price = self.menu_price_input.text()
            category = self.menu_category_input.text()
            image_url = self.menu_image_input.text()

            update_query = """
                UPDATE MENU
                SET menu_name = :1, menu_info = :2, menu_price = :3, category = :4, image = :5
                WHERE menu_id = :6
            """
            self.cursor.execute(update_query, (menu_name, menu_info, menu_price, category, image_url, menu_id))
            self.conn.commit()
            load_menu_data(self.cursor, self.tblmenu)

    def delete_menu(self):
        selected_row = self.tblmenu.currentRow()
        if selected_row >= 0:
            menu_id = self.tblmenu.item(selected_row, 0).text()
            delete_query = """
                DELETE FROM MENU WHERE menu_id = :1
            """
            self.cursor.execute(delete_query, (menu_id,))
            self.conn.commit()
            load_menu_data(self.cursor, self.tblmenu)

    def double_click_event(self):
        selected_row = self.tblmenu.currentRow()
        if selected_row >= 0:
            menu_id = self.tblmenu.item(selected_row, 0).text()
            menu_name = self.tblmenu.item(selected_row, 1).text()
            menu_info = self.tblmenu.item(selected_row, 2).text()
            menu_price = self.tblmenu.item(selected_row, 3).text()
            menu_category = self.tblmenu.item(selected_row, 4).text()
            menu_image = self.tblmenu.item(selected_row, 5).text()

            # 상태 페이지(tblmenu2)에 표시
            self.tblmenu2.setRowCount(1)
            self.tblmenu2.setItem(0, 0, QTableWidgetItem(menu_id))
            self.tblmenu2.setItem(0, 1, QTableWidgetItem(menu_name))
            self.tblmenu2.setItem(0, 2, QTableWidgetItem(menu_info))
            self.tblmenu2.setItem(0, 3, QTableWidgetItem(menu_price))
            self.tblmenu2.setItem(0, 4, QTableWidgetItem(menu_category))
            self.tblmenu2.setItem(0, 5, QTableWidgetItem(menu_image))

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManagerWindow()
    window.show()
    sys.exit(app.exec_())
